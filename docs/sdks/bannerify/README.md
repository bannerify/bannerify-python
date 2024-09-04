# Bannerify SDK

## Overview

### Available Operations

* [post_v1_templates_create_image](#post_v1_templates_create_image) - Create an image from a template
* [post_v1_templates_create_pdf](#post_v1_templates_create_pdf)
* [get_v1_templates_signedurl](#get_v1_templates_signedurl) - Generate a signed URL for a template
* [get_v1_info](#get_v1_info) - Get project info
* [get_v1_templates_id](#get_v1_templates_id) - Template details

## post_v1_templates_create_image

Create an image from a template

### Example Usage

```python
from bannerify import Bannerify

s = Bannerify(
    token="BANNERIFY_API_KEY",
)


res = s.post_v1_templates_create_image(request={
    "api_key": "<value>",
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

### Parameters

| Parameter                                                                                             | Type                                                                                                  | Required                                                                                              | Description                                                                                           |
| ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `request`                                                                                             | [models.PostV1TemplatesCreateImageRequestBody](../../models/postv1templatescreateimagerequestbody.md) | :heavy_check_mark:                                                                                    | The request object to use for the request.                                                            |
| `retries`                                                                                             | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                      | :heavy_minus_sign:                                                                                    | Configuration to override the default retry behavior of the client.                                   |

### Response

**[models.PostV1TemplatesCreateImageResponse](../../models/postv1templatescreateimageresponse.md)**

### Errors

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


## post_v1_templates_create_pdf

### Example Usage

```python
from bannerify import Bannerify

s = Bannerify(
    token="BANNERIFY_API_KEY",
)


res = s.post_v1_templates_create_pdf(request={
    "api_key": "<value>",
    "template_id": "tpl_xxx",
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

### Parameters

| Parameter                                                                                         | Type                                                                                              | Required                                                                                          | Description                                                                                       |
| ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `request`                                                                                         | [models.PostV1TemplatesCreatePdfRequestBody](../../models/postv1templatescreatepdfrequestbody.md) | :heavy_check_mark:                                                                                | The request object to use for the request.                                                        |
| `retries`                                                                                         | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                  | :heavy_minus_sign:                                                                                | Configuration to override the default retry behavior of the client.                               |

### Response

**[httpx.Response](../../models/.md)**

### Errors

| Error Object                                | Status Code                                 | Content Type                                |
| ------------------------------------------- | ------------------------------------------- | ------------------------------------------- |
| models.PostV1TemplatesCreatePdfResponseBody | 400                                         | application/json                            |
| models.ErrUnauthorized                      | 401                                         | application/json                            |
| models.ErrForbidden                         | 403                                         | application/json                            |
| models.ErrNotFound                          | 404                                         | application/json                            |
| models.ErrConflict                          | 409                                         | application/json                            |
| models.ErrTooManyRequests                   | 429                                         | application/json                            |
| models.ErrInternalServerError               | 500                                         | application/json                            |
| models.SDKError                             | 4xx-5xx                                     | */*                                         |


## get_v1_templates_signedurl

Generate a signed URL for a template

### Example Usage

```python
from bannerify import Bannerify

s = Bannerify(
    token="BANNERIFY_API_KEY",
)


res = s.get_v1_templates_signedurl(request={
    "template_id": "tpl_xxxxxxxxx",
    "sign": "<value>",
    "nocache": "true",
})

if res is not None:
    # handle response
    pass

```

### Parameters

| Parameter                                                                               | Type                                                                                    | Required                                                                                | Description                                                                             |
| --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `request`                                                                               | [models.GetV1TemplatesSignedurlRequest](../../models/getv1templatessignedurlrequest.md) | :heavy_check_mark:                                                                      | The request object to use for the request.                                              |
| `retries`                                                                               | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                        | :heavy_minus_sign:                                                                      | Configuration to override the default retry behavior of the client.                     |

### Response

**[bytes](../../models/.md)**

### Errors

| Error Object                               | Status Code                                | Content Type                               |
| ------------------------------------------ | ------------------------------------------ | ------------------------------------------ |
| models.GetV1TemplatesSignedurlResponseBody | 400                                        | application/json                           |
| models.ErrUnauthorized                     | 401                                        | application/json                           |
| models.ErrForbidden                        | 403                                        | application/json                           |
| models.ErrNotFound                         | 404                                        | application/json                           |
| models.ErrConflict                         | 409                                        | application/json                           |
| models.ErrTooManyRequests                  | 429                                        | application/json                           |
| models.ErrInternalServerError              | 500                                        | application/json                           |
| models.SDKError                            | 4xx-5xx                                    | */*                                        |


## get_v1_info

Get project info

### Example Usage

```python
from bannerify import Bannerify

s = Bannerify(
    token="BANNERIFY_API_KEY",
)


res = s.get_v1_info(api_key="key_xxxxxxxxx")

if res is not None:
    # handle response
    pass

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `api_key`                                                           | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 | key_xxxxxxxxx                                                       |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.GetV1InfoResponseBody](../../models/getv1inforesponsebody.md)**

### Errors

| Error Object                         | Status Code                          | Content Type                         |
| ------------------------------------ | ------------------------------------ | ------------------------------------ |
| models.GetV1InfoResponseResponseBody | 400                                  | application/json                     |
| models.ErrUnauthorized               | 401                                  | application/json                     |
| models.ErrForbidden                  | 403                                  | application/json                     |
| models.ErrNotFound                   | 404                                  | application/json                     |
| models.ErrConflict                   | 409                                  | application/json                     |
| models.ErrTooManyRequests            | 429                                  | application/json                     |
| models.ErrInternalServerError        | 500                                  | application/json                     |
| models.SDKError                      | 4xx-5xx                              | */*                                  |


## get_v1_templates_id

Template details

### Example Usage

```python
from bannerify import Bannerify

s = Bannerify(
    token="BANNERIFY_API_KEY",
)


res = s.get_v1_templates_id(api_key="key_xxxxxxxxx")

if res is not None:
    # handle response
    pass

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `api_key`                                                           | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 | key_xxxxxxxxx                                                       |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.GetV1TemplatesIDResponseBody](../../models/getv1templatesidresponsebody.md)**

### Errors

| Error Object                                | Status Code                                 | Content Type                                |
| ------------------------------------------- | ------------------------------------------- | ------------------------------------------- |
| models.GetV1TemplatesIDResponseResponseBody | 400                                         | application/json                            |
| models.ErrUnauthorized                      | 401                                         | application/json                            |
| models.ErrForbidden                         | 403                                         | application/json                            |
| models.ErrNotFound                          | 404                                         | application/json                            |
| models.ErrConflict                          | 409                                         | application/json                            |
| models.ErrTooManyRequests                   | 429                                         | application/json                            |
| models.ErrInternalServerError               | 500                                         | application/json                            |
| models.SDKError                             | 4xx-5xx                                     | */*                                         |
