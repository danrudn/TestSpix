#!/usr/bin/env python3
"""
QML Tree Dump Utilities
Provides functions to dump and compare QML object trees via Spix
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Tuple


def read_state(server) -> str:
    """Read the current state from mainWindow/rootItem."""
    return server.getStringProperty("mainWindow/rootItem", "state")


def check_state(expected_state: str, current_state: str) -> bool:
    """Check if current state matches expected state."""
    if current_state == expected_state:
        print(f"   ✅ Current state: {current_state} (expected: {expected_state})")
        return True
    else:
        print(f"   ❌ State mismatch: {current_state} (expected: {expected_state})")
        return False


def dump_qml_tree(server) -> Dict:
    """
    Dump the complete QML object tree via Spix.
    
    Args:
        server: XMLRPC ServerProxy connected to Spix
        
    Returns:
        Dictionary containing the complete QML tree
    """
    # Trigger dump command
    server.command("dumpQmlTree", "")
    time.sleep(0.1)  # Wait for dump to complete
    
    # Read tree from mainWindow property
    tree_json = server.getStringProperty("mainWindow", "_qmlTreeJson")
    
    if not tree_json:
        raise RuntimeError("Failed to dump QML tree: empty response")
    
    return json.loads(tree_json)


def save_tree_snapshot(tree: Dict, filepath: Path):
    """Save QML tree to JSON file."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(tree, f, indent=2)


def load_tree_snapshot(filepath: Path) -> Dict:
    """Load QML tree from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def compare_trees(reference: Dict, current: Dict, path: str = "") -> Tuple[bool, List[str]]:
    """
    Compare two QML trees and return differences.
    
    Args:
        reference: Reference tree (expected)
        current: Current tree (actual)
        path: Current path in tree (for error messages)
        
    Returns:
        Tuple of (is_equal, list_of_differences)
    """
    differences = []
    
    # Compare object names
    ref_name = reference.get("objectName", "")
    cur_name = current.get("objectName", "")
    if ref_name != cur_name:
        differences.append(f"{path}: objectName mismatch: '{ref_name}' != '{cur_name}'")
    
    # Compare class names
    ref_class = reference.get("className", "")
    cur_class = current.get("className", "")
    if ref_class != cur_class:
        differences.append(f"{path}: className mismatch: '{ref_class}' != '{cur_class}'")
    
    # Compare properties
    ref_props = reference.get("properties", {})
    cur_props = current.get("properties", {})
    
    # Check for missing or changed properties
    for prop_name, ref_value in ref_props.items():
        if prop_name not in cur_props:
            differences.append(f"{path}.{prop_name}: missing in current tree")
        elif cur_props[prop_name] != ref_value:
            differences.append(
                f"{path}.{prop_name}: '{ref_value}' != '{cur_props[prop_name]}'"
            )
    
    # Check for extra properties
    for prop_name in cur_props:
        if prop_name not in ref_props:
            differences.append(f"{path}.{prop_name}: unexpected property in current tree")
    
    # Compare children
    ref_children = reference.get("children", [])
    cur_children = current.get("children", [])
    
    if len(ref_children) != len(cur_children):
        differences.append(
            f"{path}: children count mismatch: {len(ref_children)} != {len(cur_children)}"
        )
    
    # Recursively compare children
    for i, (ref_child, cur_child) in enumerate(zip(ref_children, cur_children)):
        child_path = f"{path}/[{i}]"
        _, child_diffs = compare_trees(ref_child, cur_child, child_path)
        differences.extend(child_diffs)
    
    return (len(differences) == 0, differences)


def print_tree_summary(tree: Dict, indent: int = 0):
    """Print a summary of the QML tree structure."""
    prefix = "  " * indent
    obj_name = tree.get("objectName", "<unnamed>")
    class_name = tree.get("className", "")
    
    print(f"{prefix}• {obj_name} ({class_name})")
    
    # Print key properties
    props = tree.get("properties", {})
    for key in ["text", "state", "source", "visible"]:
        if key in props:
            print(f"{prefix}  └─ {key}: {props[key]}")
    
    # Recursively print children
    for child in tree.get("children", []):
        print_tree_summary(child, indent + 1)
