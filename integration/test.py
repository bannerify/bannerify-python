#!/usr/bin/env python3
"""Integration test for Bannerify Python SDK"""

import os
import sys

# Add parent directory to path for local testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from bannerify import BannerifyClient


def main():
    api_key = os.getenv("BANNERIFY_API_KEY")
    template_id = os.getenv("BANNERIFY_TEMPLATE_ID")

    if not api_key or not template_id:
        print("⚠️  Skipping integration tests - BANNERIFY_API_KEY or BANNERIFY_TEMPLATE_ID not set")
        return 0

    print("Running Bannerify Python SDK integration tests...\n")

    failed = False

    # Test 1: Create client
    print("Test 1: Creating client... ", end="")
    try:
        client = BannerifyClient(api_key)
        print("✓ PASSED")
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return 1

    # Test 2: Generate signed URL
    print("Test 2: Generating signed URL... ", end="")
    try:
        signed_url = client.generate_image_signed_url(
            template_id,
            modifications=[{"name": "title", "text": "Integration Test"}]
        )
        
        if signed_url.startswith("https://api.bannerify.co/v1/templates/signedurl"):
            print("✓ PASSED")
            print(f"   URL: {signed_url[:80]}...")
        else:
            print("✗ FAILED: Invalid URL format")
            failed = True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        failed = True

    # Test 3: Create image (SVG)
    print("Test 3: Creating image (SVG format)... ", end="")
    try:
        result = client.create_image(
            template_id,
            format="svg",
            modifications=[{"name": "title", "text": "Python SDK Test"}]
        )
        
        if "result" in result:
            svg = result["result"]
            if isinstance(svg, bytes):
                svg = svg.decode("utf-8")
            if "<svg" in svg:
                print("✓ PASSED")
                print(f"   SVG size: {len(svg)} chars")
            else:
                print("✗ FAILED: Response doesn't contain SVG")
                failed = True
        else:
            error_msg = result.get("error", {}).get("message", "Unknown error")
            print(f"✗ FAILED: {error_msg}")
            failed = True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        failed = True

    # Test 4: Create image (PNG)
    print("Test 4: Creating image (PNG format)... ", end="")
    try:
        result = client.create_image(
            template_id,
            modifications=[{"name": "title", "text": "Python SDK Test PNG"}]
        )
        
        if "result" in result:
            png = result["result"]
            if len(png) > 0:
                print("✓ PASSED")
                print(f"   PNG size: {len(png)} bytes")
            else:
                print("✗ FAILED: Empty response")
                failed = True
        else:
            error_msg = result.get("error", {}).get("message", "Unknown error")
            print(f"✗ FAILED: {error_msg}")
            failed = True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        failed = True

    # Test 5: Error handling
    print("Test 5: Testing error handling... ", end="")
    try:
        result = client.create_image("invalid_template_id")
        
        if "error" in result:
            print("✓ PASSED")
            print(f"   Error code: {result['error']['code']}")
        else:
            print("✗ FAILED: Should have returned error")
            failed = True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        failed = True

    # Clean up
    client.close()

    if failed:
        print("\n❌ Some tests failed")
        return 1

    print("\n✅ All integration tests passed!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
