<!-- Start SDK Example Usage [usage] -->
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