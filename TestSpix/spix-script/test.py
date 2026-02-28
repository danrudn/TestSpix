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


def compare_images(reference_path, test_path):
    """
    Compare two images using SSIM (Structural Similarity Index).
    
    SSIM ranges from -1 to 1, where 1 means identical.
    Requires SSIM = 1.0 for pixel-perfect match.

    checks properties (edges, geometric patterns, brightness), it is not a pixel comparison.
    I did pixel comparison before but because of aliasing whatever there is still a missmatch between ref und test image
    """
    try:
        # Load images
        ref_image = io.imread(str(reference_path))
        test_image = io.imread(str(test_path))
        
        # Calculate SSIM
        ssim_score = metrics.structural_similarity(
            ref_image, 
            test_image, 
            channel_axis=2 if len(ref_image.shape) == 3 else None,
            data_range=ref_image.max() - ref_image.min()
        )
        
        if ssim_score == 1.0:
            print(f"   ✅ Images are identical (SSIM: {ssim_score:.4f})")
            return True
        else:
            print(f"   ❌ Images differ (SSIM: {ssim_score:.4f} < 1.0)")
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

