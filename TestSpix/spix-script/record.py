#!/usr/bin/env python3
"""
Einfaches Spix Test Script
Zeigt grundlegende Interaktionen mit der TestSpix-Anwendung
"""

import xmlrpc.client
import time
import os
from pathlib import Path

server = xmlrpc.client.ServerProxy('http://localhost:9000')

# Create reference-images directory if it doesn't exist
REFERENCE_DIR = Path(__file__).parent / "reference-images"
REFERENCE_DIR.mkdir(exist_ok=True)

# function for reading state property of the root Item in main.qml Item{ states[]...}
def read_state():
    return server.getStringProperty("mainWindow/rootItem", "state")


def take_screenshot(page_name):
    """Take a screenshot and save it to reference-images directory"""
    screenshot_path = str(REFERENCE_DIR / f"{page_name}.png")
    try:
        # Take screenshot using Spix (correct method name is takeScreenshot)
        server.takeScreenshot("mainWindow", screenshot_path)
        print(f"   📸 Screenshot saved: {screenshot_path}")
        return True
    except Exception as e:
        print(f"   ⚠️  Screenshot failed: {e}")
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
take_screenshot("page1")
time.sleep(1)

# 2. Navigate to Page 2 and verify
print("\n→ Going to Page 2")
server.command("gotoPage2", "")
time.sleep(1)
take_screenshot("page2")
time.sleep(1)

# 3. Navigate to Page 3 and verify
print("\n→ Going to Page 3")
server.command("gotoPage3", "")
time.sleep(1)
take_screenshot("page3")
time.sleep(1)

# 4. Navigate back to Page 1 and verify
print("\n→ Back to Page 1")
server.command("gotoPage1", "")
take_screenshot("page1_return")
time.sleep(1)

print("\n✅ Done!")

