#!/usr/bin/env python3
"""
Record QML Tree Snapshots
Creates reference snapshots for each page state
"""

import xmlrpc.client
import time
from pathlib import Path
from qml_tree_utils import dump_qml_tree, save_tree_snapshot, print_tree_summary

server = xmlrpc.client.ServerProxy('http://localhost:9000')

# Setup directories
REFERENCE_DIR = Path(__file__).parent / "json_reference"
REFERENCE_DIR.mkdir(exist_ok=True)

print("🎬 Recording QML tree snapshots...\n")

# 1. Capture Page 1
print("📝 Recording Page 1 state...")
tree1 = dump_qml_tree(server)
save_tree_snapshot(tree1, REFERENCE_DIR / "page1.json")
print("   ✅ Saved to page1.json")
time.sleep(1)

# 2. Navigate to Page 2
print("\n📝 Recording Page 2 state...")
server.command("gotoPage2", "")
time.sleep(1)
tree2 = dump_qml_tree(server)
save_tree_snapshot(tree2, REFERENCE_DIR / "page2.json")
print("   ✅ Saved to page2.json")
time.sleep(1)

# 3. Navigate to Page 3
print("\n📝 Recording Page 3 state...")
server.command("gotoPage3", "")
time.sleep(1)
tree3 = dump_qml_tree(server)
save_tree_snapshot(tree3, REFERENCE_DIR / "page3.json")
print("   ✅ Saved to page3.json")
time.sleep(1)

# 4. Back to Page 1
print("\n📝 Recording Page 1 return state...")
server.command("gotoPage1", "")
time.sleep(1)
tree4 = dump_qml_tree(server)
save_tree_snapshot(tree4, REFERENCE_DIR / "page1_return.json")
print("   ✅ Saved to page1_return.json")

print("\n✅ Recording complete!")
print(f"   Snapshots saved to: {REFERENCE_DIR}")
print("\n📊 Page 1 structure preview:")
print_tree_summary(tree1)
