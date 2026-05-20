#!/usr/bin/env python3
"""
Package React app files to a transfer directory with email-safe extensions.
Converts .jsx and .tsx to .txt, stores mapping in .manifest.json
"""

import os
import json
import shutil
from pathlib import Path

REACT_ROOT = Path(__file__).parent
TRANSFER_DIR = REACT_ROOT / "transfer"
MANIFEST_FILE = TRANSFER_DIR / ".manifest.json"

# Extensions to convert
UNSAFE_EXTENSIONS = {".jsx": ".txt", ".tsx": ".txt"}

# Directories and files to skip
SKIP_DIRS = {".git", "node_modules", ".next", "build", "dist", "transfer", ".env"}
SKIP_FILES = {".manifest.json", "package_safe.py", "unpack_safe.py"}


def should_skip(path_obj):
    """Check if path should be skipped."""
    if path_obj.name in SKIP_FILES:
        return True
    for skip_dir in SKIP_DIRS:
        if skip_dir in path_obj.parts:
            return True
    return False


def copy_with_mapping(src, dest, manifest):
    """Copy files, converting unsafe extensions, and record in manifest."""
    for src_path in src.rglob("*"):
        if should_skip(src_path):
            continue

        # Calculate relative path and destination
        rel_path = src_path.relative_to(src)
        dest_path = dest / rel_path

        if src_path.is_dir():
            dest_path.mkdir(parents=True, exist_ok=True)
        else:
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            # Check if extension needs conversion
            suffix = src_path.suffix
            if suffix in UNSAFE_EXTENSIONS:
                new_suffix = UNSAFE_EXTENSIONS[suffix]
                new_name = src_path.stem + new_suffix
                actual_dest = dest_path.parent / new_name

                # Record mapping
                rel_dest = actual_dest.relative_to(dest)
                manifest[str(rel_dest)] = str(rel_path)

                shutil.copy2(src_path, actual_dest)
            else:
                shutil.copy2(src_path, dest_path)


def main():
    print(f"📦 Packaging React app to: {TRANSFER_DIR}")

    # Clean transfer directory
    if TRANSFER_DIR.exists():
        shutil.rmtree(TRANSFER_DIR)
        print("   Cleared existing transfer directory")

    TRANSFER_DIR.mkdir(exist_ok=True)

    # Copy files with mapping
    manifest = {}
    copy_with_mapping(REACT_ROOT, TRANSFER_DIR, manifest)

    # Save manifest
    with open(MANIFEST_FILE, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"✅ Packaging complete!")
    print(f"   Converted extensions: {', '.join(UNSAFE_EXTENSIONS.keys())}")
    print(f"   Files in transfer: {sum(1 for _ in TRANSFER_DIR.rglob('*') if _.is_file())}")
    print(f"   Manifest saved to: {MANIFEST_FILE}")


if __name__ == "__main__":
    main()
