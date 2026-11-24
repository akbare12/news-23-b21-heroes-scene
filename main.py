#!/usr/bin/env python3
"""Copy entry.png to MAKEFUN_OUTPUT_DIR/entry.png.

The grader runs this program with a read-only /bot and a writable
output directory, so the program must never write next to itself:
the only output is os.environ["MAKEFUN_OUTPUT_DIR"]/entry.png
"""
import hashlib
import os
import shutil
import struct
import sys


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    dst = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    with open(src, "rb") as f:
        data = f.read()
    # PNG header: width/height are big-endian uint32 at bytes 16..24.
    width, height = struct.unpack(">II", data[16:24])
    assert (width, height) == (1024, 1024), f"unexpected size {width}x{height}"
    # Deterministic copy: both grader runs must write the same bytes.
    shutil.copyfile(src, dst)
    with open(dst, "rb") as f:
        out = f.read()
    assert hashlib.sha256(out).hexdigest() == hashlib.sha256(data).hexdigest()
    print(f"OK: wrote {dst} ({len(out)} bytes, sha256 "
          f"{hashlib.sha256(out).hexdigest()[:16]}...)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
