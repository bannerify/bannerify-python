# Bannerify SDK


## Overview

### Available Operations

* [post_v1_templates_create_image](#post_v1_templates_create_image)
* [get_v1_templates_signedurl](#get_v1_templates_signedurl)
* [get_v1_info](#get_v1_info) - Get project info

## post_v1_templates_create_image

### Example Usage

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

## get_v1_templates_signedurl

### Example Usage

```python
from bannerify import Bannerify

s = Bannerify(
    bearer_auth="BANNERIFY_API_KEY",
)


res = s.get_v1_templates_signedurl(request={
    "template_id": "tpl_xxxxxxxxx",
    "api_key_md5": "<value>",
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
    bearer_auth="BANNERIFY_API_KEY",
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

| Error Object    | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| models.SDKError | 4xx-5xx         | */*             |
