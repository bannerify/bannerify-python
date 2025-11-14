"""Bannerify Client for Python"""

import hashlib
import json
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

import httpx
from pydantic import TypeAdapter

from .models import Modification


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
        thumbnail: bool = False,
    ) -> Dict[str, Any]:
        """Generate an image from a template
        
        Args:
            template_id: Template ID (e.g., 'tpl_xxxxxxxxx')
            modifications: List of modifications to apply
            format: Output format - 'png' or 'svg' (default: 'png')
            thumbnail: Generate thumbnail version (default: False)
            
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
            
            payload = {
                "apiKey": self.api_key,
                "templateId": template_id,
                "modifications": mods_list,
                "format": format,
                "thumbnail": thumbnail,
            }

            response = self._client.post(
                f"{self.base_url}/templates/createImage",
                json=payload,
            )

            if response.status_code == 200:
                content_type = response.headers.get("content-type", "")
                
                if "image/svg" in content_type:
                    return {"result": response.text}
                else:
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
        thumbnail: bool = False,
    ) -> Dict[str, Any]:
        """Create an image and store it on Bannerify's CDN
        
        Args:
            template_id: Template ID
            modifications: List of modifications to apply
            format: Output format - 'png' or 'svg'
            thumbnail: Generate thumbnail version
            
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
            
            payload = {
                "apiKey": self.api_key,
                "templateId": template_id,
                "modifications": mods_list,
                "format": format,
                "thumbnail": thumbnail,
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

    def generate_image_signed_url(
        self,
        template_id: str,
        modifications: Optional[List[Union[Modification, Dict[str, Any]]]] = None,
        format: str = "png",
        thumbnail: bool = False,
        nocache: bool = False,
    ) -> str:
        """Generate a signed URL for on-demand image generation
        
        Args:
            template_id: Template ID
            modifications: List of modifications to apply
            format: Output format - 'png' or 'svg'
            thumbnail: Generate thumbnail version
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

        if format == "svg":
            params["format"] = "svg"

        if modifications:
            # Convert modifications to dicts if they're Pydantic models
            mods_list = []
            for mod in modifications:
                if isinstance(mod, Modification):
                    mods_list.append(mod.model_dump(exclude_none=True))
                else:
                    mods_list.append(mod)
            params["modifications"] = json.dumps(mods_list)

        if nocache:
            params["nocache"] = "true"

        if thumbnail:
            params["thumbnail"] = "true"

        # Sort parameters
        sorted_params = dict(sorted(params.items()))

        # Generate signature
        query_string = urlencode(sorted_params)
        sign_input = query_string + api_key_hashed
        sign = hashlib.sha256(sign_input.encode()).hexdigest()
        sorted_params["sign"] = sign

        return f"{self.base_url}/templates/signedurl?{urlencode(sorted_params)}"

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
