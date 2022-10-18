import os
import subprocess
import sys
import tarfile
from importlib import import_module
from pathlib import Path

if not (python := sys.executable):
    print("Error: Python is unable to retrieve the real path to its executable.", file=sys.stderr)
    sys.exit(1)

src_dir = Path(__file__).resolve().parents[1].joinpath("src")
sys.path.insert(0, os.fsdecode(src_dir))
gethash = import_module("gethash")

docs_dir = Path(__file__).resolve().parent
build_dir = docs_dir / "build"
build_dir.mkdir(parents=True, exist_ok=True)
dist_dir = docs_dir / "dist"
dist_dir.mkdir(parents=True, exist_ok=True)

doctrees_dir = build_dir / "doctrees"
source_dir = docs_dir / "source"
html_dir = build_dir / "html"
subprocess.run([python, "-m", "sphinx.cmd.build", "-b", "html", "-d", doctrees_dir, source_dir, html_dir])

name = f"{gethash.__title__}-{gethash.__version__}-doc"
with tarfile.open(dist_dir / f"{name}.tar.gz", "w:gz") as tar:
    tar.add(html_dir, name)
