"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from .basesdk import BaseSDK
from .httpclient import AsyncHttpClient, HttpClient
from .sdkconfiguration import SDKConfiguration
from .utils.retries import RetryConfig
from bannerify import models
from bannerify._hooks import HookContext, SDKHooks
from bannerify.types import BaseModel, OptionalNullable, UNSET
import bannerify.utils as utils
from enum import Enum
import httpx
from typing import Any, Callable, Dict, Optional, Union, cast
class PostV1TemplatesCreateImageAcceptEnum(str, Enum):
    IMAGE_PNG = "image/png"
    IMAGE_SVG_PLUS_XML = "image/svg+xml"

class Bannerify(BaseSDK):
    def __init__(
        self,
        bearer_auth: Union[str, Callable[[], str]],
        server_idx: Optional[int] = None,
        server_url: Optional[str] = None,
        url_params: Optional[Dict[str, str]] = None,
        client: Optional[HttpClient] = None,
        async_client: Optional[AsyncHttpClient] = None,
        retry_config: OptionalNullable[RetryConfig] = UNSET,
        timeout_ms: Optional[int] = None
    ) -> None:
        r"""Instantiates the SDK configuring it with the provided parameters.

        :param bearer_auth: The bearer_auth required for authentication
        :param server_idx: The index of the server to use for all methods
        :param server_url: The server URL to use for all methods
        :param url_params: Parameters to optionally template the server URL with
        :param client: The HTTP client to use for all synchronous methods
        :param async_client: The Async HTTP client to use for all asynchronous methods
        :param retry_config: The retry configuration to use for all supported methods
        :param timeout_ms: Optional request timeout applied to each operation in milliseconds
        """
        if client is None:
            client = httpx.Client()

        assert issubclass(
            type(client), HttpClient
        ), "The provided client must implement the HttpClient protocol."

        if async_client is None:
            async_client = httpx.AsyncClient()

        assert issubclass(
            type(async_client), AsyncHttpClient
        ), "The provided async_client must implement the AsyncHttpClient protocol."
        
        security: Any = None
        if callable(bearer_auth):
            security = lambda: models.Security(bearer_auth = bearer_auth()) # pylint: disable=unnecessary-lambda-assignment
        else:
            security = models.Security(bearer_auth = bearer_auth)

        if server_url is not None:
            if url_params is not None:
                server_url = utils.template_url(server_url, url_params)
    

        BaseSDK.__init__(self, SDKConfiguration(
            client=client,
            async_client=async_client,
            security=security,
            server_url=server_url,
            server_idx=server_idx,
            retry_config=retry_config,
            timeout_ms=timeout_ms
        ))

        hooks = SDKHooks()

        current_server_url, *_ = self.sdk_configuration.get_server_details()
        server_url, self.sdk_configuration.client = hooks.sdk_init(current_server_url, self.sdk_configuration.client)
        if current_server_url != server_url:
            self.sdk_configuration.server_url = server_url

        # pylint: disable=protected-access
        self.sdk_configuration.__dict__["_hooks"] = hooks
    
    
    def post_v1_templates_create_image(
        self, *,
        request: Union[models.PostV1TemplatesCreateImageRequestBody, models.PostV1TemplatesCreateImageRequestBodyTypedDict],
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        accept_header_override: Optional[PostV1TemplatesCreateImageAcceptEnum] = None
    ) -> Optional[models.PostV1TemplatesCreateImageResponse]:
        r"""
        :param request: The request object to send.
        :param retries: Override the default retry configuration for this method
        :param server_url: Override the default server URL for this method
        :param timeout_ms: Override the default request timeout configuration for this method in milliseconds
        :param accept_header_override: Override the default accept header for this method
        """
        base_url = None
        url_variables = None
        if timeout_ms is None:
            timeout_ms = self.sdk_configuration.timeout_ms
        
        if server_url is not None:
            base_url = server_url
        
        if not isinstance(request, BaseModel):
            request = utils.unmarshal(request, models.PostV1TemplatesCreateImageRequestBody)
        request = cast(models.PostV1TemplatesCreateImageRequestBody, request)
        
        req = self.build_request(
            method="POST",
            path="/v1/templates/createImage",
            base_url=base_url,
            url_variables=url_variables,
            request=request,
            request_body_required=True,
            request_has_path_params=False,
            request_has_query_params=True,
            user_agent_header="user-agent",
            accept_header_value=accept_header_override.value if accept_header_override is not None else "image/png;q=1, image/svg+xml;q=0",
            security=self.sdk_configuration.security,
            get_serialized_body=lambda: utils.serialize_request_body(request, False, False, "json", models.PostV1TemplatesCreateImageRequestBody),
            timeout_ms=timeout_ms,
        )
        
        if retries == UNSET:
            if self.sdk_configuration.retry_config is not UNSET:
                retries = self.sdk_configuration.retry_config

        retry_config = None
        if isinstance(retries, utils.RetryConfig):
            retry_config = (retries, [
                "429",
                "500",
                "502",
                "503",
                "504"
            ])                
        
        http_res = self.do_request(
            hook_ctx=HookContext(operation_id="post_/v1/templates/createImage", oauth2_scopes=[], security_source=self.sdk_configuration.security),
            request=req,
            error_status_codes=["400","401","403","404","409","429","4XX","500","5XX"],
            stream=True,
            retry_config=retry_config
        )
        
        data: Any = None
        if utils.match_response(http_res, "200", "image/png"):
            return http_res
        if utils.match_response(http_res, "200", "image/svg+xml"):
            return http_res.text
        if utils.match_response(http_res, "400", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.PostV1TemplatesCreateImageResponseBodyUnion)
            raise models.PostV1TemplatesCreateImageResponseBody(data=data)
        if utils.match_response(http_res, "401", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.ErrUnauthorizedData)
            raise models.ErrUnauthorized(data=data)
        if utils.match_response(http_res, "403", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.ErrForbiddenData)
            raise models.ErrForbidden(data=data)
        if utils.match_response(http_res, "404", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.ErrNotFoundData)
            raise models.ErrNotFound(data=data)
        if utils.match_response(http_res, "409", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.ErrConflictData)
            raise models.ErrConflict(data=data)
        if utils.match_response(http_res, "429", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.ErrTooManyRequestsData)
            raise models.ErrTooManyRequests(data=data)
        if utils.match_response(http_res, "500", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.ErrInternalServerErrorData)
            raise models.ErrInternalServerError(data=data)
        if utils.match_response(http_res, ["4XX","5XX"], "*"):
            raise models.SDKError("API error occurred", http_res.status_code, http_res.text, http_res)
        
        content_type = http_res.headers.get("Content-Type")
        raise models.SDKError(f"Unexpected response received (code: {http_res.status_code}, type: {content_type})", http_res.status_code, http_res.text, http_res)

    
    
    async def post_v1_templates_create_image_async(
        self, *,
        request: Union[models.PostV1TemplatesCreateImageRequestBody, models.PostV1TemplatesCreateImageRequestBodyTypedDict],
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        accept_header_override: Optional[PostV1TemplatesCreateImageAcceptEnum] = None
    ) -> Optional[models.PostV1TemplatesCreateImageResponse]:
        r"""
        :param request: The request object to send.
        :param retries: Override the default retry configuration for this method
        :param server_url: Override the default server URL for this method
        :param timeout_ms: Override the default request timeout configuration for this method in milliseconds
        :param accept_header_override: Override the default accept header for this method
        """
        base_url = None
        url_variables = None
        if timeout_ms is None:
            timeout_ms = self.sdk_configuration.timeout_ms
        
        if server_url is not None:
            base_url = server_url
        
        if not isinstance(request, BaseModel):
            request = utils.unmarshal(request, models.PostV1TemplatesCreateImageRequestBody)
        request = cast(models.PostV1TemplatesCreateImageRequestBody, request)
        
        req = self.build_request(
            method="POST",
            path="/v1/templates/createImage",
            base_url=base_url,
            url_variables=url_variables,
            request=request,
            request_body_required=True,
            request_has_path_params=False,
            request_has_query_params=True,
            user_agent_header="user-agent",
            accept_header_value=accept_header_override.value if accept_header_override is not None else "image/png;q=1, image/svg+xml;q=0",
            security=self.sdk_configuration.security,
            get_serialized_body=lambda: utils.serialize_request_body(request, False, False, "json", models.PostV1TemplatesCreateImageRequestBody),
            timeout_ms=timeout_ms,
        )
        
        if retries == UNSET:
            if self.sdk_configuration.retry_config is not UNSET:
                retries = self.sdk_configuration.retry_config

        retry_config = None
        if isinstance(retries, utils.RetryConfig):
            retry_config = (retries, [
                "429",
                "500",
                "502",
                "503",
                "504"
            ])                
        
        http_res = await self.do_request_async(
            hook_ctx=HookContext(operation_id="post_/v1/templates/createImage", oauth2_scopes=[], security_source=self.sdk_configuration.security),
            request=req,
            error_status_codes=["400","401","403","404","409","429","4XX","500","5XX"],
            stream=True,
            retry_config=retry_config
        )
        
        data: Any = None
        if utils.match_response(http_res, "200", "image/png"):
            return http_res
        if utils.match_response(http_res, "200", "image/svg+xml"):
            return http_res.text
        if utils.match_response(http_res, "400", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.PostV1TemplatesCreateImageResponseBodyUnion)
            raise models.PostV1TemplatesCreateImageResponseBody(data=data)
        if utils.match_response(http_res, "401", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.ErrUnauthorizedData)
            raise models.ErrUnauthorized(data=data)
        if utils.match_response(http_res, "403", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.ErrForbiddenData)
            raise models.ErrForbidden(data=data)
        if utils.match_response(http_res, "404", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.ErrNotFoundData)
            raise models.ErrNotFound(data=data)
        if utils.match_response(http_res, "409", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.ErrConflictData)
            raise models.ErrConflict(data=data)
        if utils.match_response(http_res, "429", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.ErrTooManyRequestsData)
            raise models.ErrTooManyRequests(data=data)
        if utils.match_response(http_res, "500", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.ErrInternalServerErrorData)
            raise models.ErrInternalServerError(data=data)
        if utils.match_response(http_res, ["4XX","5XX"], "*"):
            raise models.SDKError("API error occurred", http_res.status_code, http_res.text, http_res)
        
        content_type = http_res.headers.get("Content-Type")
        raise models.SDKError(f"Unexpected response received (code: {http_res.status_code}, type: {content_type})", http_res.status_code, http_res.text, http_res)

    
    
    def get_v1_templates_signedurl(
        self, *,
        request: Union[models.GetV1TemplatesSignedurlRequest, models.GetV1TemplatesSignedurlRequestTypedDict],
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
    ) -> Optional[bytes]:
        r"""
        :param request: The request object to send.
        :param retries: Override the default retry configuration for this method
        :param server_url: Override the default server URL for this method
        :param timeout_ms: Override the default request timeout configuration for this method in milliseconds
        """
        base_url = None
        url_variables = None
        if timeout_ms is None:
            timeout_ms = self.sdk_configuration.timeout_ms
        
        if server_url is not None:
            base_url = server_url
        
        if not isinstance(request, BaseModel):
            request = utils.unmarshal(request, models.GetV1TemplatesSignedurlRequest)
        request = cast(models.GetV1TemplatesSignedurlRequest, request)
        
        req = self.build_request(
            method="GET",
            path="/v1/templates/signedurl",
            base_url=base_url,
            url_variables=url_variables,
            request=request,
            request_body_required=False,
            request_has_path_params=False,
            request_has_query_params=True,
            user_agent_header="user-agent",
            accept_header_value="image/png",
            security=self.sdk_configuration.security,
            timeout_ms=timeout_ms,
        )
        
        if retries == UNSET:
            if self.sdk_configuration.retry_config is not UNSET:
                retries = self.sdk_configuration.retry_config

        retry_config = None
        if isinstance(retries, utils.RetryConfig):
            retry_config = (retries, [
                "429",
                "500",
                "502",
                "503",
                "504"
            ])                
        
        http_res = self.do_request(
            hook_ctx=HookContext(operation_id="get_/v1/templates/signedurl", oauth2_scopes=[], security_source=self.sdk_configuration.security),
            request=req,
            error_status_codes=["400","401","403","404","409","429","4XX","500","5XX"],
            retry_config=retry_config
        )
        
        data: Any = None
        if utils.match_response(http_res, "200", "image/png"):
            return http_res.content
        if utils.match_response(http_res, "400", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.GetV1TemplatesSignedurlResponseBodyUnion)
            raise models.GetV1TemplatesSignedurlResponseBody(data=data)
        if utils.match_response(http_res, "401", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.ErrUnauthorizedData)
            raise models.ErrUnauthorized(data=data)
        if utils.match_response(http_res, "403", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.ErrForbiddenData)
            raise models.ErrForbidden(data=data)
        if utils.match_response(http_res, "404", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.ErrNotFoundData)
            raise models.ErrNotFound(data=data)
        if utils.match_response(http_res, "409", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.ErrConflictData)
            raise models.ErrConflict(data=data)
        if utils.match_response(http_res, "429", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.ErrTooManyRequestsData)
            raise models.ErrTooManyRequests(data=data)
        if utils.match_response(http_res, "500", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.ErrInternalServerErrorData)
            raise models.ErrInternalServerError(data=data)
        if utils.match_response(http_res, ["4XX","5XX"], "*"):
            raise models.SDKError("API error occurred", http_res.status_code, http_res.text, http_res)
        
        content_type = http_res.headers.get("Content-Type")
        raise models.SDKError(f"Unexpected response received (code: {http_res.status_code}, type: {content_type})", http_res.status_code, http_res.text, http_res)

    
    
    async def get_v1_templates_signedurl_async(
        self, *,
        request: Union[models.GetV1TemplatesSignedurlRequest, models.GetV1TemplatesSignedurlRequestTypedDict],
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
    ) -> Optional[bytes]:
        r"""
        :param request: The request object to send.
        :param retries: Override the default retry configuration for this method
        :param server_url: Override the default server URL for this method
        :param timeout_ms: Override the default request timeout configuration for this method in milliseconds
        """
        base_url = None
        url_variables = None
        if timeout_ms is None:
            timeout_ms = self.sdk_configuration.timeout_ms
        
        if server_url is not None:
            base_url = server_url
        
        if not isinstance(request, BaseModel):
            request = utils.unmarshal(request, models.GetV1TemplatesSignedurlRequest)
        request = cast(models.GetV1TemplatesSignedurlRequest, request)
        
        req = self.build_request(
            method="GET",
            path="/v1/templates/signedurl",
            base_url=base_url,
            url_variables=url_variables,
            request=request,
            request_body_required=False,
            request_has_path_params=False,
            request_has_query_params=True,
            user_agent_header="user-agent",
            accept_header_value="image/png",
            security=self.sdk_configuration.security,
            timeout_ms=timeout_ms,
        )
        
        if retries == UNSET:
            if self.sdk_configuration.retry_config is not UNSET:
                retries = self.sdk_configuration.retry_config

        retry_config = None
        if isinstance(retries, utils.RetryConfig):
            retry_config = (retries, [
                "429",
                "500",
                "502",
                "503",
                "504"
            ])                
        
        http_res = await self.do_request_async(
            hook_ctx=HookContext(operation_id="get_/v1/templates/signedurl", oauth2_scopes=[], security_source=self.sdk_configuration.security),
            request=req,
            error_status_codes=["400","401","403","404","409","429","4XX","500","5XX"],
            retry_config=retry_config
        )
        
        data: Any = None
        if utils.match_response(http_res, "200", "image/png"):
            return http_res.content
        if utils.match_response(http_res, "400", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.GetV1TemplatesSignedurlResponseBodyUnion)
            raise models.GetV1TemplatesSignedurlResponseBody(data=data)
        if utils.match_response(http_res, "401", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.ErrUnauthorizedData)
            raise models.ErrUnauthorized(data=data)
        if utils.match_response(http_res, "403", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.ErrForbiddenData)
            raise models.ErrForbidden(data=data)
        if utils.match_response(http_res, "404", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.ErrNotFoundData)
            raise models.ErrNotFound(data=data)
        if utils.match_response(http_res, "409", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.ErrConflictData)
            raise models.ErrConflict(data=data)
        if utils.match_response(http_res, "429", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.ErrTooManyRequestsData)
            raise models.ErrTooManyRequests(data=data)
        if utils.match_response(http_res, "500", "application/json"):
            data = utils.unmarshal_json(http_res.text, models.ErrInternalServerErrorData)
            raise models.ErrInternalServerError(data=data)
        if utils.match_response(http_res, ["4XX","5XX"], "*"):
            raise models.SDKError("API error occurred", http_res.status_code, http_res.text, http_res)
        
        content_type = http_res.headers.get("Content-Type")
        raise models.SDKError(f"Unexpected response received (code: {http_res.status_code}, type: {content_type})", http_res.status_code, http_res.text, http_res)

    
    
    def get_v1_info(
        self, *,
        api_key: str,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
    ) -> Optional[models.GetV1InfoResponseBody]:
        r"""Get project info

        :param api_key: 
        :param retries: Override the default retry configuration for this method
        :param server_url: Override the default server URL for this method
        :param timeout_ms: Override the default request timeout configuration for this method in milliseconds
        """
        base_url = None
        url_variables = None
        if timeout_ms is None:
            timeout_ms = self.sdk_configuration.timeout_ms
        
        if server_url is not None:
            base_url = server_url
        
        request = models.GetV1InfoRequest(
            api_key=api_key,
        )
        
        req = self.build_request(
            method="GET",
            path="/v1/info",
            base_url=base_url,
            url_variables=url_variables,
            request=request,
            request_body_required=False,
            request_has_path_params=False,
            request_has_query_params=True,
            user_agent_header="user-agent",
            accept_header_value="application/json",
            security=self.sdk_configuration.security,
            timeout_ms=timeout_ms,
        )
        
        if retries == UNSET:
            if self.sdk_configuration.retry_config is not UNSET:
                retries = self.sdk_configuration.retry_config

        retry_config = None
        if isinstance(retries, utils.RetryConfig):
            retry_config = (retries, [
                "429",
                "500",
                "502",
                "503",
                "504"
            ])                
        
        http_res = self.do_request(
            hook_ctx=HookContext(operation_id="get_/v1/info", oauth2_scopes=[], security_source=self.sdk_configuration.security),
            request=req,
            error_status_codes=["4XX","5XX"],
            retry_config=retry_config
        )
        
        if utils.match_response(http_res, "200", "application/json"):
            return utils.unmarshal_json(http_res.text, Optional[models.GetV1InfoResponseBody])
        if utils.match_response(http_res, ["4XX","5XX"], "*"):
            raise models.SDKError("API error occurred", http_res.status_code, http_res.text, http_res)
        
        content_type = http_res.headers.get("Content-Type")
        raise models.SDKError(f"Unexpected response received (code: {http_res.status_code}, type: {content_type})", http_res.status_code, http_res.text, http_res)

    
    
    async def get_v1_info_async(
        self, *,
        api_key: str,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
    ) -> Optional[models.GetV1InfoResponseBody]:
        r"""Get project info

        :param api_key: 
        :param retries: Override the default retry configuration for this method
        :param server_url: Override the default server URL for this method
        :param timeout_ms: Override the default request timeout configuration for this method in milliseconds
        """
        base_url = None
        url_variables = None
        if timeout_ms is None:
            timeout_ms = self.sdk_configuration.timeout_ms
        
        if server_url is not None:
            base_url = server_url
        
        request = models.GetV1InfoRequest(
            api_key=api_key,
        )
        
        req = self.build_request(
            method="GET",
            path="/v1/info",
            base_url=base_url,
            url_variables=url_variables,
            request=request,
            request_body_required=False,
            request_has_path_params=False,
            request_has_query_params=True,
            user_agent_header="user-agent",
            accept_header_value="application/json",
            security=self.sdk_configuration.security,
            timeout_ms=timeout_ms,
        )
        
        if retries == UNSET:
            if self.sdk_configuration.retry_config is not UNSET:
                retries = self.sdk_configuration.retry_config

        retry_config = None
        if isinstance(retries, utils.RetryConfig):
            retry_config = (retries, [
                "429",
                "500",
                "502",
                "503",
                "504"
            ])                
        
        http_res = await self.do_request_async(
            hook_ctx=HookContext(operation_id="get_/v1/info", oauth2_scopes=[], security_source=self.sdk_configuration.security),
            request=req,
            error_status_codes=["4XX","5XX"],
            retry_config=retry_config
        )
        
        if utils.match_response(http_res, "200", "application/json"):
            return utils.unmarshal_json(http_res.text, Optional[models.GetV1InfoResponseBody])
        if utils.match_response(http_res, ["4XX","5XX"], "*"):
            raise models.SDKError("API error occurred", http_res.status_code, http_res.text, http_res)
        
        content_type = http_res.headers.get("Content-Type")
        raise models.SDKError(f"Unexpected response received (code: {http_res.status_code}, type: {content_type})", http_res.status_code, http_res.text, http_res)

    
