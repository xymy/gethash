import sys
from importlib import import_module
from pathlib import Path

from setuptools import find_packages, setup

root = Path(__file__).parent

# Import this package from src directory and fetch metadata.
sys.path.insert(0, str(root / "src"))
package = import_module("gethash")
project = getattr(package, "__project__", None)
version = getattr(package, "__version__", None)
author = getattr(package, "__author__", None)
email = getattr(package, "__email__", None)

# Read metadata from files.
readme = (root / "README.md").read_text()
requirements = (root / "requirements.txt").read_text().splitlines()

classifiers = [
    "License :: OSI Approved",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Topic :: Security",
    "Topic :: Security :: Cryptography",
]

setup(
    name=project,
    version=version,
    license="MIT",
    description="A command-line tools that can generate or check hash values.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author=author,
    author_email=email,
    url="https://github.com/xymy/gethash",
    download_url="https://pypi.org/project/gethash/",
    classifiers=classifiers,
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "md5 = gethash.cli.md5:main",
            "sha1 = gethash.cli.sha1:main",
            "sha256 = gethash.cli.sha256:main",
            "sha512 = gethash.cli.sha512:main",
            "sha3-256 = gethash.cli.sha3_256:main",
            "sha3-512 = gethash.cli.sha3_512:main",
            "blake2b = gethash.cli.blake2b:main",
            "blake2s = gethash.cli.blake2s:main",
            # Legacy hash functions.
            "md2 = gethash.cli.md2:main [all]",
            "md4 = gethash.cli.md4:main [all]",
            "ripemd160 = gethash.cli.ripemd160:main [all]",
        ]
    },
    install_requires=requirements,
    extras_require={
        "all": ["pycryptodomex>=3.9"],
    },
    python_requires=">=3.6",
)
