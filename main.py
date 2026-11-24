#!/usr/bin/env python3
"""Entry point for news-image-20261123.

Copies the pre-drawn front page (entry.png, built by build_image.py)
to $MAKEFUN_OUTPUT_DIR/entry.png (default /output). Standard library
only, no network, deterministic: the same bytes every run.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    sys.exit(main())
