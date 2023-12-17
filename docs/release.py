import shutil
import subprocess
import sys
import tarfile
from pathlib import Path
from typing import Final

import click
from rich.console import Console
from rich.markup import escape

CONTEXT_SETTINGS: Final = dict(help_option_names=["-h", "--help"], max_content_width=120)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("--clean/--no-clean", default=False, help="Whether or not to clean the build directory.")
@click.option("--dist/--no-dist", default=False, help="Whether or not to build a distribution.")
def release(*, clean: bool, dist: bool) -> None:
    import gethash as pkg

    console = Console(soft_wrap=True, emoji=False, highlight=False)

    docs_dir = Path(__file__).parent
    source_dir = docs_dir / "source"
    build_dir = docs_dir / "build"
    html_dir = build_dir / "html"
    doctrees_dir = build_dir / "doctrees"

    console.print(f"Docs dir: [u]{docs_dir}[/u]", style="b magenta")
    console.print(f"Source dir: [u]{source_dir}[/u]", style="b magenta")
    console.print(f"Build dir: [u]{build_dir}[/u]", style="b magenta")
    console.print()

    if clean and build_dir.exists():
        shutil.rmtree(build_dir)
        console.print(f"Clean the build directory [u]{escape(str(build_dir))}[/u]", style="b blue")

    subprocess.run(
        [sys.executable, "-m", "sphinx.cmd.build", "-b", "html", "-d", doctrees_dir, source_dir, html_dir], check=True
    )

    if dist:
        dist_dir = docs_dir / "dist"
        dist_dir.mkdir(parents=True, exist_ok=True)
        dist_name = f"{pkg.__title__}-{pkg.__version__}-docs"
        dist_path = dist_dir / f"{dist_name}.tar.xz"

        with tarfile.open(dist_path, "w:xz") as tar:
            tar.add(html_dir, dist_name)
        console.print(f"Build a distribution [u]{escape(str(dist_path))}[/u]", style="b green")


def main() -> int:
    try:
        return release(windows_expand_args=False)
    except Exception:  # noqa: BLE001
        console = Console()
        console.print_exception()
        return 1


if __name__ == "__main__":
    sys.exit(main())
