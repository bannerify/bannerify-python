"""Bannerify Client for Python"""

import hashlib
import hmac
import json
from typing import Any, Dict, Iterator, List, Optional, Union
from urllib.parse import quote_plus

import httpx
from pydantic import TypeAdapter

from .models import Modification

SUPPORTED_FORMATS = {"png", "jpeg", "webp"}


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

        Each second of the video counts as one generation, and as two at 60 fps.

        Args:
            template_id: Template ID
            modifications: List of modifications to apply

        Yields:
            Event dicts: {'type': 'queued', 'ahead'} while the video waits for a renderer,
            {'type': 'progress', 'frame', 'totalFrames', 'progress'} while its frames render,
            then {'type': 'done', 'url'} or {'type': 'error', 'error'}
        """
        mods_list = [
            mod.model_dump(exclude_none=True) if isinstance(mod, Modification) else mod
            for mod in modifications or []
        ]
        payload = {
            "apiKey": self.api_key,
            "templateId": template_id,
            "modifications": mods_list,
        }

        try:
            # A render can wait in line for minutes, so only the connection has a timeout.
            with self._client.stream(
                "POST",
                f"{self.base_url}/templates/renderVideo",
                params={"stream": "true"},
                json=payload,
                timeout=httpx.Timeout(self.timeout, read=None),
            ) as response:
                if response.status_code != 200:
                    response.read()
                    yield {"type": "error", **self._response_error(response)}
                    return

                data: List[str] = []
                for line in response.iter_lines():
                    if line.startswith("data:"):
                        data.append(line[5:].strip())
                    elif line == "" and data:
                        yield json.loads("\n".join(data))
                        data = []

        except httpx.TimeoutException:
            yield {"type": "error", **self._build_error("TIMEOUT", "Request timed out")}
        except httpx.RequestError as e:
            yield {"type": "error", **self._build_error("REQUEST_ERROR", str(e))}

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
