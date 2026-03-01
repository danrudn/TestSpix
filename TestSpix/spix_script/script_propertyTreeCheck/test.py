#!/usr/bin/env python3
"""
Test QML Tree States
Compares current QML tree against recorded snapshots
"""

import xmlrpc.client
import time
import sys
from pathlib import Path
from qml_tree_utils import (
    dump_qml_tree, 
    load_tree_snapshot, 
    compare_trees, 
    save_tree_snapshot,
    read_state,
    check_state
)

server = xmlrpc.client.ServerProxy('http://localhost:9000')

# Setup directories
REFERENCE_DIR = Path(__file__).parent / "json_reference"
TEST_DIR = Path(__file__).parent / "json_test"
TEST_DIR.mkdir(exist_ok=True)

def test_routine(state_name: str, expected_state: str) -> bool:
    """
    Test current QML tree against reference snapshot.
    Also checks the state property.
    Returns True if match, False otherwise.
    """
    reference_path = REFERENCE_DIR / f"{state_name}.json"
    
    if not reference_path.exists():
        print(f"   ❌ Reference snapshot not found: {reference_path}")
        return False
    
    # Check state first
    current_state = read_state(server)
    if not check_state(expected_state, current_state):
        return False
    
    # Load reference
    reference = load_tree_snapshot(reference_path)
    
    # Capture current tree
    current = dump_qml_tree(server)
    
    # Save current tree for inspection
    test_path = TEST_DIR / f"{state_name}.json"
    save_tree_snapshot(current, test_path)
    
    # Compare
    is_equal, differences = compare_trees(reference, current)
    
    if is_equal:
        print(f"   ✅ QML tree matches reference")
        return True
    else:
        print(f"   ❌ QML tree differs from reference ({len(differences)} differences):")
        return False


print("🚀 Starting QML tree-based navigation test\n")

all_passed = True

# 1. Check initial state (Page 1)
print("Checking initial state (Page 1)...")
if not test_routine("page1", "page1"):
    all_passed = False
    print("\n❌ Test aborted: Tree comparison failed!")
    sys.exit(1)
time.sleep(1)

# 2. Navigate to Page 2 and verify
print("\n→ Going to Page 2")
server.command("gotoPage2", "")
time.sleep(1)
print("Testing Page 2 tree...")
if not test_routine("page2", "page2"):
    all_passed = False
    print("\n❌ Test aborted: Tree comparison failed!")
    sys.exit(1)
time.sleep(1)

# 3. Navigate to Page 3 and verify
print("\n→ Going to Page 3")
server.command("gotoPage3", "")
time.sleep(1)
print("Testing Page 3 tree...")
if not test_routine("page3", "page3"):
    all_passed = False
    print("\n❌ Test aborted: Tree comparison failed!")
    sys.exit(1)
time.sleep(1)

# 4. Navigate back to Page 1 and verify
print("\n→ Back to Page 1")
server.command("gotoPage1", "")
time.sleep(1)
print("Testing Page 1 return tree...")
if not test_routine("page1_return", "page1"):
    all_passed = False
    print("\n❌ Test aborted: Tree comparison failed!")
    sys.exit(1)

if all_passed:
    print("\n✅ All tests passed!")
    sys.exit(0)
else:
    print("\n❌ Some tests failed!")
    sys.exit(1)
