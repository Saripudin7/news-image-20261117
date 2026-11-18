#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261117.

Copies the pre-rendered infographic (entry.png, drawn by draw_news.py)
into the output directory make.fun expects. Standard library only,
no network, fully deterministic: two runs write byte-identical files.
"""
import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    if not os.path.isfile(src):
        print("error: entry.png not found next to main.py", file=sys.stderr)
        sys.exit(1)
    dst = os.path.join(out_dir, "entry.png")
    if os.path.abspath(src) == os.path.abspath(dst):
        print("already in place:", dst)
        return
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    main()
