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


if __name__ == "__main__":
    unittest.main()
