# bannerify

<!-- Start SDK Installation [installation] -->
## SDK Installation

PIP
```bash
pip install git+https://github.com/bannerify/bannerify-python.git
```

Poetry
```bash
poetry add git+https://github.com/bannerify/bannerify-python.git
```
<!-- End SDK Installation [installation] -->

<!-- Start SDK Example Usage [usage] -->
## SDK Example Usage

### Example

```python
# Synchronous Example
from bannerify import Bannerify

s = Bannerify(
    bearer_auth="BANNERIFY_API_KEY",
)


res = s.post_v1_templates_create_image(request={
    "api_key": "key_xxxxxxxxx",
    "template_id": "tpl_xxxxxxxxx",
    "modifications": [
        {
            "name": "Text 1",
            "color": "#FF0000",
            "src": "https://example.com/image.jpg",
            "text": "Hello World",
            "barcode": "1234567890",
            "qrcode": "Some text",
            "visible": True,
            "star": 5,
        },
    ],
})

if res is not None:
    # handle response
    pass
```

</br>

The same SDK client can also be used to make asychronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
from bannerify import Bannerify

async def main():
    s = Bannerify(
        bearer_auth="BANNERIFY_API_KEY",
    )
    res = await s.post_v1_templates_create_image_async(request={
        "api_key": "key_xxxxxxxxx",
        "template_id": "tpl_xxxxxxxxx",
        "modifications": [
            {
                "name": "Text 1",
                "color": "#FF0000",
                "src": "https://example.com/image.jpg",
                "text": "Hello World",
                "barcode": "1234567890",
                "qrcode": "Some text",
                "visible": True,
                "star": 5,
            },
        ],
    })
    if res is not None:
        # handle response
        pass

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->

<!-- Start Available Resources and Operations [operations] -->
## Available Resources and Operations

### [Bannerify SDK](docs/sdks/bannerify/README.md)

* [post_v1_templates_create_image](docs/sdks/bannerify/README.md#post_v1_templates_create_image)
* [get_v1_templates_signedurl](docs/sdks/bannerify/README.md#get_v1_templates_signedurl)
* [get_v1_info](docs/sdks/bannerify/README.md#get_v1_info) - Get project info
<!-- End Available Resources and Operations [operations] -->

<!-- Start Retries [retries] -->
## Retries

Some of the endpoints in this SDK support retries. If you use the SDK without any configuration, it will fall back to the default retry strategy provided by the API. However, the default retry strategy can be overridden on a per-operation basis, or across the entire SDK.

To change the default retry strategy for a single API call, simply provide a `RetryConfig` object to the call:
```python
from bannerify import Bannerify
from bannerify.utils import BackoffStrategy, RetryConfig

s = Bannerify(
    bearer_auth="BANNERIFY_API_KEY",
)


res = s.post_v1_templates_create_image(request={
    "api_key": "key_xxxxxxxxx",
    "template_id": "tpl_xxxxxxxxx",
    "modifications": [
        {
            "name": "Text 1",
            "color": "#FF0000",
            "src": "https://example.com/image.jpg",
            "text": "Hello World",
            "barcode": "1234567890",
            "qrcode": "Some text",
            "visible": True,
            "star": 5,
        },
    ],
},
    RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False))

if res is not None:
    # handle response
    pass

```

If you'd like to override the default retry strategy for all operations that support retries, you can use the `retry_config` optional parameter when initializing the SDK:
```python
from bannerify import Bannerify
from bannerify.utils import BackoffStrategy, RetryConfig

s = Bannerify(
    retry_config=RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False),
    bearer_auth="BANNERIFY_API_KEY",
)


res = s.post_v1_templates_create_image(request={
    "api_key": "key_xxxxxxxxx",
    "template_id": "tpl_xxxxxxxxx",
    "modifications": [
        {
            "name": "Text 1",
            "color": "#FF0000",
            "src": "https://example.com/image.jpg",
            "text": "Hello World",
            "barcode": "1234567890",
            "qrcode": "Some text",
            "visible": True,
            "star": 5,
        },
    ],
})

if res is not None:
    # handle response
    pass

```
<!-- End Retries [retries] -->

<!-- Start Error Handling [errors] -->
## Error Handling

Handling errors in this SDK should largely match your expectations.  All operations return a response object or raise an error.  If Error objects are specified in your OpenAPI Spec, the SDK will raise the appropriate Error type.

| Error Object                                  | Status Code                                   | Content Type                                  |
| --------------------------------------------- | --------------------------------------------- | --------------------------------------------- |
| models.PostV1TemplatesCreateImageResponseBody | 400                                           | application/json                              |
| models.ErrUnauthorized                        | 401                                           | application/json                              |
| models.ErrForbidden                           | 403                                           | application/json                              |
| models.ErrNotFound                            | 404                                           | application/json                              |
| models.ErrConflict                            | 409                                           | application/json                              |
| models.ErrTooManyRequests                     | 429                                           | application/json                              |
| models.ErrInternalServerError                 | 500                                           | application/json                              |
| models.SDKError                               | 4xx-5xx                                       | */*                                           |

### Example

```python
from bannerify import Bannerify, models

s = Bannerify(
    bearer_auth="BANNERIFY_API_KEY",
)

res = None
try:
    res = s.post_v1_templates_create_image(request={
    "api_key": "key_xxxxxxxxx",
    "template_id": "tpl_xxxxxxxxx",
    "modifications": [
        {
            "name": "Text 1",
            "color": "#FF0000",
            "src": "https://example.com/image.jpg",
            "text": "Hello World",
            "barcode": "1234567890",
            "qrcode": "Some text",
            "visible": True,
            "star": 5,
        },
    ],
})

except models.PostV1TemplatesCreateImageResponseBody as e:
    # handle exception
    raise(e)
except models.ErrUnauthorized as e:
    # handle exception
    raise(e)
except models.ErrForbidden as e:
    # handle exception
    raise(e)
except models.ErrNotFound as e:
    # handle exception
    raise(e)
except models.ErrConflict as e:
    # handle exception
    raise(e)
except models.ErrTooManyRequests as e:
    # handle exception
    raise(e)
except models.ErrInternalServerError as e:
    # handle exception
    raise(e)
except models.SDKError as e:
    # handle exception
    raise(e)

if res is not None:
    # handle response
    pass

```
<!-- End Error Handling [errors] -->

<!-- Start Server Selection [server] -->
## Server Selection

### Select Server by Index

You can override the default server globally by passing a server index to the `server_idx: int` optional parameter when initializing the SDK client instance. The selected server will then be used as the default on the operations that use it. This table lists the indexes associated with the available servers:

| # | Server | Variables |
| - | ------ | --------- |
| 0 | `https://api.bannerify.co` | None |

#### Example

```python
from bannerify import Bannerify

s = Bannerify(
    server_idx=0,
    bearer_auth="BANNERIFY_API_KEY",
)


res = s.post_v1_templates_create_image(request={
    "api_key": "key_xxxxxxxxx",
    "template_id": "tpl_xxxxxxxxx",
    "modifications": [
        {
            "name": "Text 1",
            "color": "#FF0000",
            "src": "https://example.com/image.jpg",
            "text": "Hello World",
            "barcode": "1234567890",
            "qrcode": "Some text",
            "visible": True,
            "star": 5,
        },
    ],
})

if res is not None:
    # handle response
    pass

```


### Override Server URL Per-Client

The default server can also be overridden globally by passing a URL to the `server_url: str` optional parameter when initializing the SDK client instance. For example:
```python
from bannerify import Bannerify

s = Bannerify(
    server_url="https://api.bannerify.co",
    bearer_auth="BANNERIFY_API_KEY",
)


res = s.post_v1_templates_create_image(request={
    "api_key": "key_xxxxxxxxx",
    "template_id": "tpl_xxxxxxxxx",
    "modifications": [
        {
            "name": "Text 1",
            "color": "#FF0000",
            "src": "https://example.com/image.jpg",
            "text": "Hello World",
            "barcode": "1234567890",
            "qrcode": "Some text",
            "visible": True,
            "star": 5,
        },
    ],
})

if res is not None:
    # handle response
    pass

```
<!-- End Server Selection [server] -->

<!-- Start Custom HTTP Client [http-client] -->
## Custom HTTP Client

The Python SDK makes API calls using the [httpx](https://www.python-httpx.org/) HTTP library.  In order to provide a convenient way to configure timeouts, cookies, proxies, custom headers, and other low-level configuration, you can initialize the SDK client with your own HTTP client instance.
Depending on whether you are using the sync or async version of the SDK, you can pass an instance of `HttpClient` or `AsyncHttpClient` respectively, which are Protocol's ensuring that the client has the necessary methods to make API calls.
This allows you to wrap the client with your own custom logic, such as adding custom headers, logging, or error handling, or you can just pass an instance of `httpx.Client` or `httpx.AsyncClient` directly.

For example, you could specify a header for every request that this sdk makes as follows:
```python
from bannerify import Bannerify
import httpx

http_client = httpx.Client(headers={"x-custom-header": "someValue"})
s = Bannerify(client=http_client)
```

or you could wrap the client with your own custom logic:
```python
from bannerify import Bannerify
from bannerify.httpclient import AsyncHttpClient
import httpx

class CustomClient(AsyncHttpClient):
    client: AsyncHttpClient

    def __init__(self, client: AsyncHttpClient):
        self.client = client

    async def send(
        self,
        request: httpx.Request,
        *,
        stream: bool = False,
        auth: Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault, None
        ] = httpx.USE_CLIENT_DEFAULT,
        follow_redirects: Union[
            bool, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
    ) -> httpx.Response:
        request.headers["Client-Level-Header"] = "added by client"

        return await self.client.send(
            request, stream=stream, auth=auth, follow_redirects=follow_redirects
        )

    def build_request(
        self,
        method: str,
        url: httpx._types.URLTypes,
        *,
        content: Optional[httpx._types.RequestContent] = None,
        data: Optional[httpx._types.RequestData] = None,
        files: Optional[httpx._types.RequestFiles] = None,
        json: Optional[Any] = None,
        params: Optional[httpx._types.QueryParamTypes] = None,
        headers: Optional[httpx._types.HeaderTypes] = None,
        cookies: Optional[httpx._types.CookieTypes] = None,
        timeout: Union[
            httpx._types.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
        extensions: Optional[httpx._types.RequestExtensions] = None,
    ) -> httpx.Request:
        return self.client.build_request(
            method,
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            extensions=extensions,
        )

s = Bannerify(async_client=CustomClient(httpx.AsyncClient()))
```
<!-- End Custom HTTP Client [http-client] -->

<!-- Start Authentication [security] -->
## Authentication

### Per-Client Security Schemes

This SDK supports the following security scheme globally:

| Name          | Type          | Scheme        |
| ------------- | ------------- | ------------- |
| `bearer_auth` | apiKey        | API key       |

To authenticate with the API the `bearer_auth` parameter must be set when initializing the SDK client instance. For example:
```python
from bannerify import Bannerify

s = Bannerify(
    bearer_auth="BANNERIFY_API_KEY",
)


res = s.post_v1_templates_create_image(request={
    "api_key": "key_xxxxxxxxx",
    "template_id": "tpl_xxxxxxxxx",
    "modifications": [
        {
            "name": "Text 1",
            "color": "#FF0000",
            "src": "https://example.com/image.jpg",
            "text": "Hello World",
            "barcode": "1234567890",
            "qrcode": "Some text",
            "visible": True,
            "star": 5,
        },
    ],
})

if res is not None:
    # handle response
    pass

```
<!-- End Authentication [security] -->

<!-- Placeholder for Future Speakeasy SDK Sections -->

# Development

## Maturity

This SDK is in beta, and there may be breaking changes between versions without a major version update. Therefore, we recommend pinning usage
to a specific package version. This way, you can install the same version each time without breaking changes unless you are intentionally
looking for the latest version.

## Contributions

While we value open-source contributions to this SDK, this library is generated programmatically. Any manual changes added to internal files will be overwritten on the next generation. 
We look forward to hearing your feedback. Feel free to open a PR or an issue with a proof of concept and we'll do our best to include it in a future release. 

### SDK Created by [Speakeasy](https://www.speakeasy.com/?utm_source=<no value>&utm_campaign=python)
