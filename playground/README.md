# Python SDK Playground

Test the Bannerify Python SDK locally before publishing.

## Setup

1. Make sure you have the API key in `.env`:
   ```bash
   API_KEY=your_api_key_here
   ```

2. Run the test:
   ```bash
   uv run python playground/test.py
   ```

## What it tests

- ✅ Create image with dict modifications
- ✅ Create image with typed Modification objects (type-safe!)
- ✅ Create SVG image
- ✅ Generate signed URL
- ✅ Error handling

Results will be saved in `playground/output/`.

