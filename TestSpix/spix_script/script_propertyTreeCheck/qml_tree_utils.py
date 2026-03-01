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
    Compare two QML trees using simple JSON equality.
    
    Args:
        reference: Reference tree (expected)
        current: Current tree (actual)
        path: Unused (kept for API compatibility)
        
    Returns:
        Tuple of (is_equal, list_of_differences)
    """
    if reference == current:
        return (True, [])
    else:
        return (False, ["QML trees are different"])
