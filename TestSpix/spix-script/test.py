#!/usr/bin/env python3
"""
Einfaches Spix Test Script
Zeigt grundlegende Interaktionen mit der TestSpix-Anwendung
"""

import xmlrpc.client
import time
import os
from pathlib import Path
from skimage import io, metrics
import numpy as np
import shutil

server = xmlrpc.client.ServerProxy('http://localhost:9000')

# Setup directories
REFERENCE_DIR = Path(__file__).parent / "reference-images"
TEST_DIR = Path(__file__).parent / "test-images"

# Clean up test directory - remove all existing images
if TEST_DIR.exists():
    shutil.rmtree(TEST_DIR)
TEST_DIR.mkdir(exist_ok=True)

# function for reading state property of the root Item in main.qml Item{ states[]...}
def read_state():
    return server.getStringProperty("mainWindow/rootItem", "state")


def take_screenshot(page_name):
    """Take a screenshot and save it to test-images directory"""
    screenshot_path = str(TEST_DIR / f"{page_name}.png")
    try:
        server.takeScreenshot("mainWindow", screenshot_path)
        print(f"   📸 Screenshot saved: {screenshot_path}")
        return screenshot_path
    except Exception as e:
        print(f"   ❌  Screenshot failed: {e}")
        return None


def compare_images(reference_path, test_path, tolerance_percent=0.01):
    """
    Compare two images with minimal tolerance for anti-aliasing differences.
    Returns True if images are identical or differ by less than tolerance_percent.
    Default tolerance: 0.01% (allows minor anti-aliasing/rendering differences)
    """
    try:
        # Load images
        ref_image = io.imread(str(reference_path))
        test_image = io.imread(str(test_path))
        
        # Check if images are identical
        if np.array_equal(ref_image, test_image):
            print(f"   ✅ Images are identical")
            return True
        else:
            # Calculate how many pixels differ
            diff_pixels = np.sum(ref_image != test_image)
            total_pixels = ref_image.size
            diff_percent = (diff_pixels / total_pixels) * 100
            
            if diff_percent <= tolerance_percent:
                print(f"   ✅ Images match within tolerance ({diff_pixels} pixels / {diff_percent:.4f}% ≤ {tolerance_percent}%)")
                return True
            else:
                print(f"   ❌ Images differ too much ({diff_pixels} pixels / {diff_percent:.4f}% > {tolerance_percent}%)")
                return False
            
    except FileNotFoundError as e:
        print(f"   ❌   Image not found: {e.filename}")
        return False
    except Exception as e:
        print(f"   ❌   Image comparison failed: {e}")
        return False


def check_state(expected_state, current_state):
    if current_state == expected_state:
        print(f"   ✅ Current state: {current_state} (expected: {expected_state})")
        return True
    else:
        print(f"   ❌ FAILED: Current state: {current_state} (expected: {expected_state})")
        return False


print("🚀 Starting navigation test\n")

# 1. Check initial state
print("Checking initial state...")
check_state("page1", read_state())
screenshot = take_screenshot("page1")
if screenshot:
    if not compare_images(REFERENCE_DIR / "page1.png", screenshot):
        print("\n❌ Test aborted: Image comparison failed!")
        exit(1)
time.sleep(1)

# 2. Navigate to Page 2 and verify
print("\n→ Going to Page 2")
server.command("gotoPage2", "")
time.sleep(1)
check_state("page2", read_state())
screenshot = take_screenshot("page2")
time.sleep(1)
if screenshot:
    if not compare_images(REFERENCE_DIR / "page2.png", screenshot):
        print("\n❌ Test aborted: Image comparison failed!")
        exit(1)

# 3. Navigate to Page 3 and verify
print("\n→ Going to Page 3")
server.command("gotoPage3", "")
time.sleep(1)
check_state("page3", read_state())
screenshot = take_screenshot("page3")
time.sleep(1)
if screenshot:
    if not compare_images(REFERENCE_DIR / "page3.png", screenshot):
        print("\n❌ Test aborted: Image comparison failed!")
        exit(1)

# 4. Navigate back to Page 1 and verify
print("\n→ Back to Page 1")
server.command("gotoPage1", "")
time.sleep(1)
check_state("page1", read_state())
screenshot = take_screenshot("page1_return")
time.sleep(1)
if screenshot:
    if not compare_images(REFERENCE_DIR / "page1_return.png", screenshot):
        print("\n❌ Test aborted: Image comparison failed!")
        exit(1)

print("\n✅ Done!")

