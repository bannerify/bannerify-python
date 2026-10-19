"""Tests for the Bannerify Python SDK.

Run with: python -m unittest discover -s tests -v
"""

import hashlib
import hmac
import json
import os
import sys
import unittest
from urllib.parse import parse_qs

import httpx

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from bannerify import BannerifyClient, Modification  # noqa: E402

# The vectors come from the JavaScript URLSearchParams, which the server uses to
# verify a signed URL.
with open(os.path.join(os.path.dirname(__file__), "..", "testdata", "signed-url-vectors.json")) as f:
    VECTORS = json.load(f)


def query_pair(url, key):
    for pair in url.split("?", 1)[1].split("&"):
        if pair.startswith(f"{key}="):
            return pair
    return None


def client_with(handler):
    client = BannerifyClient(VECTORS["apiKey"], base_url=VECTORS["baseUrl"])
    client._client = httpx.Client(transport=httpx.MockTransport(handler))
    return client


class SignedUrlTest(unittest.TestCase):
    def setUp(self):
        self.client = BannerifyClient(VECTORS["apiKey"], base_url=VECTORS["baseUrl"])

    def test_encodes_values_like_url_search_params(self):
        for vector in VECTORS["encoded"]:
            with self.subTest(input=vector["input"]):
                url = self.client.generate_image_signed_url(vector["input"])

                self.assertEqual(f"templateId={vector['encoded']}", query_pair(url, "templateId"))

    def test_builds_the_golden_urls(self):
        for golden in VECTORS["golden"]:
            with self.subTest(name=golden["name"]):
                url = self.client.generate_image_signed_url(
                    golden["templateId"],
                    modifications=golden["modifications"],
                    format=golden["format"],
                )

                self.assertEqual(golden["url"], url)

    def test_signs_the_sorted_query(self):
        url = self.client.generate_image_signed_url(
            "tpl_x",
            modifications=[{"name": "title", "text": "A*B~C"}],
            format="jpeg",
        )

        *params, sign = url.split("?", 1)[1].split("&")

        self.assertEqual(sorted(params), params)
        expected = hmac.new(
            VECTORS["apiKey"].encode(), "&".join(params).encode(), hashlib.sha256
        ).hexdigest()
        self.assertEqual(f"sign={expected}", sign)

    def test_serializes_modification_models_without_none_fields(self):
        url = self.client.generate_image_signed_url(
            "tpl_x", modifications=[Modification(name="title", text="Hello")]
        )

        query = parse_qs(url.split("?", 1)[1])
        self.assertEqual('[{"name":"title","text":"Hello"}]', query["modifications"][0])

    def test_rejects_an_unsupported_format(self):
        with self.assertRaises(ValueError):
            self.client.generate_image_signed_url("tpl_x", format="gif")

    def test_has_no_thumbnail_option(self):
        with self.assertRaises(TypeError):
            self.client.generate_image_signed_url("tpl_x", thumbnail=True)


class RequestTest(unittest.TestCase):
    def test_create_image_sends_no_thumbnail_field(self):
        bodies = []

        def handler(request):
            bodies.append(json.loads(request.content))
            return httpx.Response(200, content=b"image")

        client = client_with(handler)

        self.assertEqual({"result": b"image"}, client.create_image("tpl_x"))
        self.assertEqual(["apiKey", "format", "modifications", "templateId"], sorted(bodies[0]))
        with self.assertRaises(TypeError):
            client.create_image("tpl_x", thumbnail=True)

    def test_create_stored_image_sends_no_thumbnail_field(self):
        bodies = []

        def handler(request):
            bodies.append(json.loads(request.content))
            return httpx.Response(200, json={"url": "https://images.bannerify.co/files/a.png"})

        client = client_with(handler)

        self.assertEqual(
            {"result": "https://images.bannerify.co/files/a.png"}, client.create_stored_image("tpl_x")
        )
        self.assertEqual(["apiKey", "format", "modifications", "templateId"], sorted(bodies[0]))
        with self.assertRaises(TypeError):
            client.create_stored_image("tpl_x", thumbnail=True)

    def test_returns_the_api_error_object(self):
        error = {
            "code": "BAD_REQUEST",
            "message": "Invalid api key",
            "docs": "https://bannerify.co/docs/api-reference/errors/code/BAD_REQUEST",
            "requestId": "req:abc123",
        }
        client = client_with(lambda request: httpx.Response(400, json={"error": error}))

        self.assertEqual({"error": error}, client.create_image("tpl_x"))


def sse(events):
    body = "".join(f"event: {event['type']}\ndata: {json.dumps(event)}\n\n" for event in events)
    return httpx.Response(200, headers={"content-type": "text/event-stream"}, content=body.encode())


DONE = {"type": "done", "url": "https://images.bannerify.co/files/a.mp4"}


class RenderVideoTest(unittest.TestCase):
    def test_streams_the_events_of_the_render(self):
        requests = []

        def handler(request):
            requests.append(request)
            return sse(
                [
                    {"type": "queued", "ahead": 1},
                    {"type": "progress", "frame": 30, "totalFrames": 60, "progress": 0.5},
                    DONE,
                ]
            )

        client = client_with(handler)

        events = list(client.render_video("tpl_x", [Modification(name="Title", text="Hi")]))

        self.assertEqual(["queued", "progress", "done"], [event["type"] for event in events])
        self.assertEqual("/v1/templates/renderVideo", requests[0].url.path)
        self.assertEqual("true", requests[0].url.params["stream"])
        self.assertEqual(
            {
                "apiKey": VECTORS["apiKey"],
                "templateId": "tpl_x",
                "modifications": [{"name": "Title", "text": "Hi"}],
            },
            json.loads(requests[0].content),
        )

    def test_turns_a_refused_request_into_one_error_event(self):
        error = {
            "code": "PRECONDITION_FAILED",
            "message": "Video rendering is not available yet.",
            "docs": "",
            "requestId": "req_1",
        }
        client = client_with(lambda request: httpx.Response(412, json={"error": error}))

        self.assertEqual([{"type": "error", "error": error}], list(client.render_video("tpl_x")))

    def test_render_and_wait_video_answers_the_url_or_the_error(self):
        waited = client_with(lambda request: sse([{"type": "queued", "ahead": 0}, DONE]))
        self.assertEqual({"result": DONE["url"]}, waited.render_and_wait_video("tpl_x"))

        error = {"code": "INTERNAL_SERVER_ERROR", "message": "Could not download a clip.", "requestId": "req_2"}
        failed = client_with(lambda request: sse([{"type": "error", "error": error}]))
        self.assertEqual({"error": error}, failed.render_and_wait_video("tpl_x"))


if __name__ == "__main__":
    unittest.main()
