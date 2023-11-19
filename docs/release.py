import argparse
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

from rich.console import Console
from rich.markup import escape


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean", action="store_true", help="clean the build directory")
    parser.add_argument("--no-clean", action="store_false", dest="clean", help="do not clean the build directory")
    parser.add_argument("--dist", action="store_true", help="build a distribution")
    parser.add_argument("--no-dist", action="store_false", dest="dist", help="do not build a distribution")
    args = parser.parse_args()

    console = Console(soft_wrap=True, emoji=False, highlight=False)

    import gethash as pkg

    docs_dir = Path(__file__).parent
    source_dir = docs_dir / "source"
    build_dir = docs_dir / "build"
    html_dir = build_dir / "html"
    doctrees_dir = build_dir / "doctrees"

    console.print(f"Docs dir: [u]{docs_dir}[/u]", style="b magenta")
    console.print(f"Source dir: [u]{source_dir}[/u]", style="b magenta")
    console.print(f"Build dir: [u]{build_dir}[/u]", style="b magenta")
    console.print()

    if args.clean and build_dir.exists():
        shutil.rmtree(build_dir)
        console.print(f"Clean the build directory [u]{escape(str(build_dir))}[/u]", style="b blue")

    subprocess.run(
        [sys.executable, "-m", "sphinx.cmd.build", "-b", "html", "-d", doctrees_dir, source_dir, html_dir], check=True
    )

    if args.dist:
        dist_dir = docs_dir / "dist"
        dist_dir.mkdir(parents=True, exist_ok=True)
        dist_name = f"{pkg.__title__}-{pkg.__version__}-docs"
        dist_path = dist_dir / f"{dist_name}.tar.xz"

        with tarfile.open(dist_path, "w:xz") as tar:
            tar.add(html_dir, dist_name)
        console.print(f"Build a distribution [u]{escape(str(dist_path))}[/u]", style="b green")


if __name__ == "__main__":
    main()
