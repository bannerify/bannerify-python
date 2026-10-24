"""Bannerify Client for Python"""

import hashlib
import hmac
import json
import time
from typing import Any, ContextManager, Dict, Iterator, List, Optional, Union
from urllib.parse import quote, quote_plus

import httpx
from pydantic import TypeAdapter

from .models import Modification

SUPPORTED_FORMATS = {"png", "jpeg", "webp"}

# The waits in seconds before each new read of a video whose stream dropped.
RECONNECT_DELAYS = (1.0, 2.0, 4.0, 8.0)


def _encode_form(value: str) -> str:
    """Encode a string like JavaScript's URLSearchParams.

    The server rebuilds the signed text with URLSearchParams. quote_plus differs
    for "*", which URLSearchParams keeps, and "~", which URLSearchParams encodes.
    """
    return quote_plus(value, safe="*").replace("~", "%7E")


def _encode_query(params: Dict[str, str]) -> str:
    """Join the parameters sorted by name, each key and value encoded like URLSearchParams."""
    return "&".join(
        f"{_encode_form(key)}={_encode_form(value)}" for key, value in sorted(params.items())
    )


def _read_events(response: httpx.Response) -> Iterator[Dict[str, Any]]:
    """The JSON of each 'data' field of a server-sent event stream"""
    data: List[str] = []
    for line in response.iter_lines():
        if line.startswith("data:"):
            data.append(line[5:].strip())
        elif line == "" and data:
            yield json.loads("\n".join(data))
            data = []


class BannerifyClient:
    """Bannerify API Client
    
    A simple, developer-friendly client for the Bannerify API.
    Generate images and PDFs from templates at scale.
    
    Example:
        >>> client = BannerifyClient("your-api-key")
        >>> result = client.create_image("tpl_xxx", modifications=[
        ...     {"name": "title", "text": "Hello World"}
        ... ])
        >>> if "result" in result:
        ...     with open("output.png", "wb") as f:
        ...         f.write(result["result"])
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.bannerify.co/v1",
        timeout: float = 60.0,
    ):
        """Initialize the Bannerify client
        
        Args:
            api_key: Your Bannerify API key
            base_url: API base URL (default: https://api.bannerify.co/v1)
            timeout: Request timeout in seconds (default: 60.0)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client = httpx.Client(
            timeout=timeout,
            headers={
                "Authorization": f"Bearer {api_key}",
                "User-Agent": "bannerify-python/0.1.0",
            },
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Close the HTTP client"""
        self._client.close()

    def create_image(
        self,
        template_id: str,
        modifications: Optional[List[Union[Modification, Dict[str, Any]]]] = None,
        format: str = "png",
    ) -> Dict[str, Any]:
        """Generate an image from a template
        
        Args:
            template_id: Template ID (e.g., 'tpl_xxxxxxxxx')
            modifications: List of modifications to apply
            format: Output format - 'png', 'jpeg', or 'webp' (default: 'png')
            
        Returns:
            Dict with either 'result' (bytes) or 'error' (dict)
            
        Example:
            >>> result = client.create_image(
            ...     "tpl_xxx",
            ...     modifications=[{"name": "title", "text": "Hello"}],
            ...     format="png"
            ... )
        """
        try:
            # Convert modifications to dicts if they're Pydantic models
            mods_list = []
            if modifications:
                for mod in modifications:
                    if isinstance(mod, Modification):
                        mods_list.append(mod.model_dump(exclude_none=True))
                    else:
                        mods_list.append(mod)
            format = (format or "png").lower()
            if format not in SUPPORTED_FORMATS:
                return self._build_error(
                    "INVALID_FORMAT",
                    f"Unsupported format '{format}'. Valid formats: png, jpeg, webp.",
                )

            payload = {
                "apiKey": self.api_key,
                "templateId": template_id,
                "modifications": mods_list,
                "format": format,
            }

            response = self._client.post(
                f"{self.base_url}/templates/createImage",
                json=payload,
            )

            if response.status_code == 200:
                return {"result": response.content}

            # Handle error responses
            if response.headers.get("content-type", "").startswith("application/json"):
                error_data = response.json()
                if "error" in error_data:
                    return {"error": error_data["error"]}
            
            return self._build_error(
                "HTTP_ERROR",
                f"HTTP {response.status_code}: {response.text[:100]}"
            )

        except httpx.TimeoutException:
            return self._build_error("TIMEOUT", "Request timed out")
        except httpx.RequestError as e:
            return self._build_error("REQUEST_ERROR", str(e))
        except Exception as e:
            return self._build_error("EXCEPTION", str(e))

    def create_pdf(
        self,
        template_id: str,
        modifications: Optional[List[Union[Modification, Dict[str, Any]]]] = None,
    ) -> Dict[str, Any]:
        """Generate a PDF from a template
        
        Args:
            template_id: Template ID
            modifications: List of modifications to apply
            
        Returns:
            Dict with either 'result' (bytes) or 'error' (dict)
        """
        try:
            # Convert modifications to dicts if they're Pydantic models
            mods_list = []
            if modifications:
                for mod in modifications:
                    if isinstance(mod, Modification):
                        mods_list.append(mod.model_dump(exclude_none=True))
                    else:
                        mods_list.append(mod)
            
            payload = {
                "apiKey": self.api_key,
                "templateId": template_id,
                "modifications": mods_list,
            }

            response = self._client.post(
                f"{self.base_url}/templates/createPdf",
                json=payload,
            )

            if response.status_code == 200:
                return {"result": response.content}

            # Handle error responses
            if response.headers.get("content-type", "").startswith("application/json"):
                error_data = response.json()
                if "error" in error_data:
                    return {"error": error_data["error"]}
            
            return self._build_error(
                "HTTP_ERROR",
                f"HTTP {response.status_code}: {response.text[:100]}"
            )

        except httpx.TimeoutException:
            return self._build_error("TIMEOUT", "Request timed out")
        except httpx.RequestError as e:
            return self._build_error("REQUEST_ERROR", str(e))
        except Exception as e:
            return self._build_error("EXCEPTION", str(e))

    def create_stored_image(
        self,
        template_id: str,
        modifications: Optional[List[Union[Modification, Dict[str, Any]]]] = None,
        format: str = "png",
    ) -> Dict[str, Any]:
        """Create an image and store it on Bannerify's CDN
        
        Args:
            template_id: Template ID
            modifications: List of modifications to apply
            format: Output format - 'png', 'jpeg', or 'webp'
            
        Returns:
            Dict with either 'result' (URL string) or 'error' (dict)
        """
        try:
            # Convert modifications to dicts if they're Pydantic models
            mods_list = []
            if modifications:
                for mod in modifications:
                    if isinstance(mod, Modification):
                        mods_list.append(mod.model_dump(exclude_none=True))
                    else:
                        mods_list.append(mod)
            format = (format or "png").lower()
            if format not in SUPPORTED_FORMATS:
                return self._build_error(
                    "INVALID_FORMAT",
                    f"Unsupported format '{format}'. Valid formats: png, jpeg, webp.",
                )

            payload = {
                "apiKey": self.api_key,
                "templateId": template_id,
                "modifications": mods_list,
                "format": format,
            }

            response = self._client.post(
                f"{self.base_url}/templates/createStoredImage",
                json=payload,
            )

            if response.status_code == 200:
                data = response.json()
                return {"result": data.get("url")}

            # Handle error responses
            if response.headers.get("content-type", "").startswith("application/json"):
                error_data = response.json()
                if "error" in error_data:
                    return {"error": error_data["error"]}
            
            return self._build_error(
                "HTTP_ERROR",
                f"HTTP {response.status_code}: {response.text[:100]}"
            )

        except httpx.TimeoutException:
            return self._build_error("TIMEOUT", "Request timed out")
        except httpx.RequestError as e:
            return self._build_error("REQUEST_ERROR", str(e))
        except Exception as e:
            return self._build_error("EXCEPTION", str(e))

    def render_video(
        self,
        template_id: str,
        modifications: Optional[List[Union[Modification, Dict[str, Any]]]] = None,
    ) -> Iterator[Dict[str, Any]]:
        """Render a video template as an MP4 and stream the events of the render

        Each second of the video counts as one generation, and as two at 60 fps. When the stream drops, the
        client reads the same video again by its id, so the video does not render twice.

        Args:
            template_id: Template ID
            modifications: List of modifications to apply

        Yields:
            Event dicts: {'type': 'created', 'id'} with the id of the video,
            {'type': 'queued', 'ahead'} while the video waits for a renderer,
            {'type': 'progress', 'frame', 'totalFrames', 'progress'} while its frames render,
            then {'type': 'done', 'url'} or {'type': 'error', 'error'}
        """
        mods_list = [
            mod.model_dump(exclude_none=True) if isinstance(mod, Modification) else mod
            for mod in modifications or []
        ]
        yield from self._follow_video(
            render={
                "apiKey": self.api_key,
                "templateId": template_id,
                "modifications": mods_list,
            }
        )

    def create_video(
        self,
        template_id: str,
        modifications: Optional[List[Union[Modification, Dict[str, Any]]]] = None,
    ) -> Dict[str, Any]:
        """Start the render of a video template and answer its id at once

        The client does not send this request again, because a second request
        renders a second video. Read the video later with get_video or watch_video.

        Args:
            template_id: Template ID
            modifications: List of modifications to apply

        Returns:
            Dict with either 'result' (dict with 'id' and 'status': 'queued') or 'error' (dict)
        """
        mods_list = [
            mod.model_dump(exclude_none=True) if isinstance(mod, Modification) else mod
            for mod in modifications or []
        ]
        try:
            response = self._client.post(
                f"{self.base_url}/templates/renderVideo",
                params={"wait": "false"},
                json={
                    "apiKey": self.api_key,
                    "templateId": template_id,
                    "modifications": mods_list,
                },
            )

            if response.status_code == 202:
                return {"result": response.json()}

            return self._response_error(response)

        except httpx.TimeoutException:
            return self._build_error("TIMEOUT", "Request timed out")
        except httpx.RequestError as e:
            return self._build_error("REQUEST_ERROR", str(e))
        except Exception as e:
            return self._build_error("EXCEPTION", str(e))

    def watch_video(self, video_id: str) -> Iterator[Dict[str, Any]]:
        """Stream the events of a video again, from its latest one, as render_video does

        Args:
            video_id: Video ID (e.g., 'vid_xxx'), from the 'created' event of render_video

        Yields:
            The event dicts of render_video, without 'created'
        """
        yield from self._follow_video(video_id=video_id)

    def get_video(self, video_id: str) -> Dict[str, Any]:
        """Read the status of a video, and its URL once it is done

        Args:
            video_id: Video ID (e.g., 'vid_xxx'), from the 'created' event of render_video

        Returns:
            Dict with either 'result' (dict with 'id', 'status' and, when the video is
            done or failed, 'url' or 'error') or 'error' (dict)
        """
        try:
            response = self._client.get(
                f"{self.base_url}/videos/{quote(video_id, safe='')}",
                params={"apiKey": self.api_key},
            )

            if response.status_code == 200:
                return {"result": response.json()}

            return self._response_error(response)

        except httpx.TimeoutException:
            return self._build_error("TIMEOUT", "Request timed out")
        except httpx.RequestError as e:
            return self._build_error("REQUEST_ERROR", str(e))
        except Exception as e:
            return self._build_error("EXCEPTION", str(e))

    def _follow_video(
        self,
        video_id: Optional[str] = None,
        render: Optional[Dict[str, Any]] = None,
    ) -> Iterator[Dict[str, Any]]:
        """The events of a video until 'done' or 'error'

        The first request sends the render payload when there is one, else it reads the
        video by its id. When the stream drops, the client waits and reads the video
        again by its id (from 'created'). It never sends the render again, because that
        renders and bills a second video. A refused render is the last event, and so is
        a refused read, except a server error, which is tried again.
        """
        for delay in (*RECONNECT_DELAYS, None):
            try:
                with self._open_video_events(video_id, render) as response:
                    if response.status_code == 200:
                        for event in _read_events(response):
                            if event["type"] == "created":
                                video_id = event["id"]
                            yield event
                            if event["type"] in ("done", "error"):
                                return
                    elif response.status_code < 500 or render is not None:
                        response.read()
                        yield {"type": "error", **self._response_error(response)}
                        return
            except httpx.RequestError:
                pass  # The connection dropped: read the video again below.

            if video_id is None or delay is None:
                message = (
                    f"Lost the connection to the video {video_id}. Read it again with get_video."
                    if video_id
                    else "Lost the connection before the video got an id."
                )
                yield {"type": "error", **self._build_error("TIMEOUT_ERROR", message)}
                return
            time.sleep(delay)
            render = None

    def _open_video_events(
        self, video_id: Optional[str], render: Optional[Dict[str, Any]]
    ) -> ContextManager[httpx.Response]:
        """Open the event stream of a new render, or of the video video_id"""
        # A render can wait in line for minutes, so only the connection has a timeout.
        timeout = httpx.Timeout(self.timeout, read=None)
        headers = {"Accept": "text/event-stream"}
        if render is not None:
            return self._client.stream(
                "POST",
                f"{self.base_url}/templates/renderVideo",
                params={"stream": "true"},
                json=render,
                headers=headers,
                timeout=timeout,
            )
        return self._client.stream(
            "GET",
            f"{self.base_url}/videos/{quote(str(video_id), safe='')}",
            params={"apiKey": self.api_key, "stream": "true"},
            headers=headers,
            timeout=timeout,
        )

    def render_and_wait_video(
        self,
        template_id: str,
        modifications: Optional[List[Union[Modification, Dict[str, Any]]]] = None,
    ) -> Dict[str, Any]:
        """Render a video template as an MP4 and wait until it is stored

        Args:
            template_id: Template ID
            modifications: List of modifications to apply

        Returns:
            Dict with either 'result' (URL string of the MP4) or 'error' (dict)
        """
        for event in self.render_video(template_id, modifications):
            if event["type"] == "done":
                return {"result": event["url"]}
            if event["type"] == "error":
                return {"error": event["error"]}
        return self._build_error("STREAM_ENDED", "The render ended before the video was done")

    def generate_image_signed_url(
        self,
        template_id: str,
        modifications: Optional[List[Union[Modification, Dict[str, Any]]]] = None,
        format: str = "png",
        nocache: bool = False,
    ) -> str:
        """Generate a signed URL for on-demand image generation
        
        Args:
            template_id: Template ID
            modifications: List of modifications to apply
            format: Output format - 'png', 'jpeg', or 'webp'
            nocache: Bypass cache
            
        Returns:
            The signed URL string
            
        Example:
            >>> url = client.generate_image_signed_url(
            ...     "tpl_xxx",
            ...     modifications=[{"name": "title", "text": "Dynamic"}]
            ... )
            >>> print(f"<img src='{url}' />")
        """
        # Hash the API key
        api_key_hashed = hashlib.sha256(self.api_key.encode()).hexdigest()

        params = {
            "apiKeyHashed": api_key_hashed,
            "templateId": template_id,
        }

        if format:
            normalized_format = format.lower()
            if normalized_format not in SUPPORTED_FORMATS:
                raise ValueError("format must be one of: png, jpeg, webp")
            params["format"] = normalized_format

        if modifications:
            # Convert modifications to dicts if they're Pydantic models
            mods_list = []
            for mod in modifications:
                if isinstance(mod, Modification):
                    mods_list.append(mod.model_dump(exclude_none=True))
                else:
                    mods_list.append(mod)
            params["modifications"] = json.dumps(mods_list, separators=(",", ":"))

        if nocache:
            params["nocache"] = "true"

        # Generate signature: HMAC keyed with the API key, so the URL can be
        # shared without exposing anything that can sign a different one.
        query_string = _encode_query(params)
        sign = hmac.new(
            self.api_key.encode(), query_string.encode(), hashlib.sha256
        ).hexdigest()

        return f"{self.base_url}/templates/signedurl?{query_string}&sign={sign}"

    def _response_error(self, response: httpx.Response) -> Dict[str, Any]:
        """The error of a refused request: the API error object, or an HTTP_ERROR"""
        if response.headers.get("content-type", "").startswith("application/json"):
            error_data = response.json()
            if "error" in error_data:
                return {"error": error_data["error"]}
        return self._build_error(
            "HTTP_ERROR", f"HTTP {response.status_code}: {response.text[:100]}"
        )

    def _build_error(self, code: str, message: str) -> Dict[str, Any]:
        """Build an error response
        
        Args:
            code: Error code
            message: Error message
            
        Returns:
            Error dict
        """
        return {
            "error": {
                "code": code,
                "message": message,
                "docs": "https://bannerify.co/docs",
            }
        }
