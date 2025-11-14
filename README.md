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

# Generate SVG
result = client.create_image(
    "tpl_xxxxxxxxx",
    format="svg",
    modifications=[{"name": "title", "text": "My Title"}]
)

# Generate thumbnail
result = client.create_image("tpl_xxxxxxxxx", thumbnail=True)
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
    format: str = "png",
    thumbnail: bool = False
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
    format: str = "png",
    thumbnail: bool = False
) -> Dict[str, Any]
```

### generate_image_signed_url

```python
client.generate_image_signed_url(
    template_id: str,
    modifications: Optional[List[Dict[str, Any]]] = None,
    format: str = "png",
    thumbnail: bool = False,
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
