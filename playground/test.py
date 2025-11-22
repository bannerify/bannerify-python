#!/usr/bin/env python3
"""
Playground test for Bannerify Python SDK

Run with: uv run python playground/test.py
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for local development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from bannerify import BannerifyClient, Modification
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("API_KEY")
TEMPLATE_ID = os.getenv("TEMPLATE_ID", "tpl_xxxxxxxxx")

if not API_KEY:
    print("❌ API_KEY not found in .env file")
    sys.exit(1)

print("🎨 Bannerify Python SDK Playground\n")

# Create output directory
output_dir = Path(__file__).parent / "output"
output_dir.mkdir(exist_ok=True)

# Initialize client
client = BannerifyClient(API_KEY)
print(f"✅ Client initialized")

# Test 1: Create image with dict modifications
print("\n1️⃣ Test: Create image with dict modifications")
result = client.create_image(
    TEMPLATE_ID,
    modifications=[
        {"name": "title", "text": "Python SDK Test"},
        {"name": "subtitle", "text": "Using dict modifications"}
    ],
    format="png"
)

if "result" in result:
    output_path = output_dir / "test-dict.png"
    with open(output_path, "wb") as f:
        f.write(result["result"])
    print(f"✅ Image created: {output_path}")
    print(f"   Size: {len(result['result'])} bytes")
else:
    print(f"❌ Error: {result['error']['message']}")

# Test 2: Create image with Modification objects (type-safe!)
print("\n2️⃣ Test: Create image with Modification objects (type-safe)")
mods = [
    Modification(name="title", text="Type-Safe Python", color="#00ADD8"),
    Modification(name="subtitle", text="Using Pydantic models", visible=True)
]

result = client.create_image(TEMPLATE_ID, modifications=mods, format="png")

if "result" in result:
    output_path = output_dir / "test-typed.png"
    with open(output_path, "wb") as f:
        f.write(result["result"])
    print(f"✅ Image created: {output_path}")
    print(f"   Size: {len(result['result'])} bytes")
else:
    print(f"❌ Error: {result['error']['message']}")

# Test 3: Create JPEG
print("\n3️⃣ Test: Create JPEG image")
result = client.create_image(
    TEMPLATE_ID,
    modifications=[
        Modification(name="title", text="JPEG Output")
    ],
    format="jpeg"
)

if "result" in result:
    output_path = output_dir / "test-jpeg.jpg"
    with open(output_path, "wb") as f:
        f.write(result["result"])
    print(f"✅ JPEG created: {output_path}")
    print(f"   Size: {len(result['result'])} bytes")
else:
    print(f"❌ Error: {result['error']['message']}")

# Test 4: Generate signed URL
print("\n4️⃣ Test: Generate signed URL")
signed_url = client.generate_image_signed_url(
    TEMPLATE_ID,
    modifications=[
        Modification(name="title", text="Signed URL Test")
    ]
)
print(f"✅ Signed URL generated")
print(f"   URL: {signed_url[:80]}...")

# Test 5: Error handling
print("\n5️⃣ Test: Error handling")
result = client.create_image("invalid_template_id")
if "error" in result:
    print(f"✅ Error handling works")
    print(f"   Code: {result['error']['code']}")
    print(f"   Message: {result['error']['message']}")
else:
    print(f"❌ Should have returned error")

# Clean up
client.close()

print("\n✨ All tests completed! Check the output/ directory for generated images.")

