#!/usr/bin/env python3
"""
Unpack and restore original extensions from transfer directory.
Uses .manifest.json to revert .txt files back to .jsx, .tsx, etc.
"""

import os
import json
import shutil
from pathlib import Path

REACT_ROOT = Path(__file__).parent
TRANSFER_DIR = REACT_ROOT / "transfer"
MANIFEST_FILE = TRANSFER_DIR / ".manifest.json"
OUTPUT_DIR = REACT_ROOT / "restored"

UNSAFE_EXTENSIONS = {".jsx": ".txt", ".tsx": ".txt"}


def main():
    if not MANIFEST_FILE.exists():
        print("❌ Error: .manifest.json not found in transfer directory")
        print("   Make sure you're running this from the same directory as package_safe.py")
        return

    with open(MANIFEST_FILE, "r") as f:
        manifest = json.load(f)

    print(f"🔄 Restoring files from: {TRANSFER_DIR}")

    # Clean output directory
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Copy all files first
    for item in TRANSFER_DIR.rglob("*"):
        if item.name == ".manifest.json":
            continue

        rel_path = item.relative_to(TRANSFER_DIR)
        dest_path = OUTPUT_DIR / rel_path

        if item.is_dir():
            dest_path.mkdir(parents=True, exist_ok=True)
        else:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest_path)

    # Restore original extensions using manifest
    restored_count = 0
    for converted_path, original_path in manifest.items():
        converted = OUTPUT_DIR / converted_path
        original = OUTPUT_DIR / original_path

        if converted.exists():
            original.parent.mkdir(parents=True, exist_ok=True)
            os.rename(converted, original)
            restored_count += 1

    print(f"✅ Restore complete!")
    print(f"   Files restored: {restored_count}")
    print(f"   Output directory: {OUTPUT_DIR}")
    print(f"   You can copy the restored directory contents back to your project")


if __name__ == "__main__":
    main()
