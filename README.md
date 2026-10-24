# Bannerify Python SDK

Official Python SDK for [Bannerify](https://bannerify.co) - Generate images and PDFs at scale via API.

[![PyPI version](https://badge.fury.io/py/bannerify.svg)](https://badge.fury.io/py/bannerify)
[![Python versions](https://img.shields.io/pypi/pyversions/bannerify.svg)](https://pypi.org/project/bannerify/)

## Installation

```bash
pip install bannerify
```

Or with uv:

```bash
uv add bannerify
```

## Quick Start

```python
from bannerify import BannerifyClient

# Create client with your API key
client = BannerifyClient("your-api-key")

# Generate an image
result = client.create_image(
    "tpl_xxxxxxxxx",
    modifications=[
        {"name": "title", "text": "Hello World"},
        {"name": "subtitle", "text": "From Python SDK"}
    ]
)

if "result" in result:
    with open("output.png", "wb") as f:
        f.write(result["result"])
    print("Image created successfully!")
else:
    print(f"Error: {result['error']['message']}")
```

## Features

- 🚀 Simple, intuitive API
- 🔒 Type-safe with full type hints
- ⚡ Built on httpx for performance
- 🎯 Result/Error pattern for explicit error handling
- 📝 Comprehensive documentation
- ✅ Well-tested

## Usage

### Creating Images

```python
# Generate PNG
result = client.create_image(
    "tpl_xxxxxxxxx",
    modifications=[
        {"name": "title", "text": "My Title"},
        {"name": "image", "src": "https://example.com/image.jpg"}
    ]
)

# Generate WebP
result = client.create_image(
    "tpl_xxxxxxxxx",
    format="webp",
    modifications=[{"name": "title", "text": "My Title"}]
)
```

### Creating PDFs

```python
result = client.create_pdf(
    "tpl_xxxxxxxxx",
    modifications=[{"name": "title", "text": "Invoice #123"}]
)

if "result" in result:
    with open("invoice.pdf", "wb") as f:
        f.write(result["result"])
```

### Generating Signed URLs

```python
signed_url = client.generate_image_signed_url(
    "tpl_xxxxxxxxx",
    modifications=[{"name": "title", "text": "Dynamic Title"}],
    format="png"
)

# Use in HTML
print(f"<img src='{signed_url}' alt='Generated Image' />")
```

### Rendering Videos

A video template renders as an MP4. Each second of the video counts as one generation, and as two at 60 fps.

```python
# Follow the render: created, queued, progress, then done or error
for event in client.render_video("tpl_xxxxxxxxx", modifications=[{"name": "title", "text": "Hi"}]):
    if event["type"] == "progress":
        print(f"{event['progress']:.0%}")
    elif event["type"] == "done":
        print(event["url"])
    elif event["type"] == "error":
        print(event["error"]["message"])

# Or wait for the URL of the MP4
result = client.render_and_wait_video("tpl_xxxxxxxxx")
```

The `created` event gives the id of the video. The video renders to its end even when the connection drops. Then `render_video` reads the same video again by its id: it waits 1, 2, 4 and 8 seconds before each of 4 attempts, and it never sends the render again. When the attempts run out, the last event is an `error` with the code `TIMEOUT_ERROR`.

```python
# Start the video and get its id at once, without waiting
created = client.create_video("tpl_xxxxxxxxx")  # {"result": {"id", "status": "queued"}} or {"error": {...}}
```

`create_video` sends the render once and never again, because a second request renders a second video.

```python
# Read the video later by its id
video = client.get_video("vid_xxx")  # {"result": {"id", "status", "url"}} or {"error": {...}}

# Follow its events again, from the latest one
for event in client.watch_video("vid_xxx"):
    print(event["type"])
```

### Error Handling

```python
result = client.create_image("tpl_xxxxxxxxx")

if "error" in result:
    error = result["error"]
    print(f"Error Code: {error['code']}")
    print(f"Message: {error['message']}")
    print(f"Docs: {error['docs']}")
else:
    # Process result
    image_data = result["result"]
```

### Context Manager

```python
with BannerifyClient("your-api-key") as client:
    result = client.create_image("tpl_xxxxxxxxx")
    # Client is automatically closed
```

## API Reference

### BannerifyClient

```python
BannerifyClient(
    api_key: str,
    base_url: str = "https://api.bannerify.co/v1",
    timeout: float = 60.0
)
```

### create_image

```python
client.create_image(
    template_id: str,
    modifications: Optional[List[Dict[str, Any]]] = None,
    format: str = "png"
) -> Dict[str, Any]
```

### create_pdf

```python
client.create_pdf(
    template_id: str,
    modifications: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]
```

### create_stored_image

```python
client.create_stored_image(
    template_id: str,
    modifications: Optional[List[Dict[str, Any]]] = None,
    format: str = "png"
) -> Dict[str, Any]
```

### render_video

```python
client.render_video(
    template_id: str,
    modifications: Optional[List[Dict[str, Any]]] = None
) -> Iterator[Dict[str, Any]]
```

Yields `{"type": "created", "id"}`, `{"type": "queued", "ahead"}`, `{"type": "progress", "frame", "totalFrames", "progress"}`, then `{"type": "done", "url"}` or `{"type": "error", "error"}`.

### render_and_wait_video

```python
client.render_and_wait_video(
    template_id: str,
    modifications: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]
```

### watch_video

```python
client.watch_video(video_id: str) -> Iterator[Dict[str, Any]]
```

Yields the events of `render_video` again, from the latest one, without `created`.

### create_video

```python
client.create_video(
    template_id: str,
    modifications: Optional[List[Union[Modification, Dict]]] = None
) -> Dict[str, Any]
```

Starts the video and returns `{"result": {"id", "status": "queued"}}` or `{"error": {...}}` at once.

### get_video

```python
client.get_video(video_id: str) -> Dict[str, Any]
```

Returns `{"result": {"id", "status", "url"?, "error"?}}` or `{"error": {...}}`. `status` is `queued`, `rendering`, `done` or `failed`.

### generate_image_signed_url

```python
client.generate_image_signed_url(
    template_id: str,
    modifications: Optional[List[Dict[str, Any]]] = None,
    format: str = "png",
    nocache: bool = False
) -> str
```

## Examples

### Generate Multiple Images

```python
products = [
    {"name": "Product A", "price": "$29.99"},
    {"name": "Product B", "price": "$39.99"},
]

for i, product in enumerate(products):
    result = client.create_image(
        "tpl_product_banner",
        modifications=[
            {"name": "product_name", "text": product["name"]},
            {"name": "price", "text": product["price"]}
        ]
    )
    
    if "result" in result:
        with open(f"banner_{i}.png", "wb") as f:
            f.write(result["result"])
```

### Email Campaigns

```python
for recipient in recipients:
    signed_url = client.generate_image_signed_url(
        "tpl_email_header",
        modifications=[{"name": "name", "text": f"Hi, {recipient['name']}!"}]
    )
    # Use signed_url in email HTML
```

## Development

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Type checking
uv run mypy src/

# Format code
uv run ruff format src/
```

## Documentation

Full documentation available at [https://bannerify.co/docs/sdk/python/overview](https://bannerify.co/docs/sdk/python/overview)

## Support

- Documentation: https://bannerify.co/docs
- Issues: https://github.com/bannerify/bannerify-python/issues
- Email: support@bannerify.co

## License

MIT License - see LICENSE file for details
