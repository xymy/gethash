import sys
from importlib import import_module
from pathlib import Path

from setuptools import find_packages, setup

root = Path(__file__).parent

# Import this package from src directory and fetch metadata.
sys.path = [str(root / "src")] + sys.path
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
    classifiers=classifiers,
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "md5 = gethash.md5:main",
            "sha1 = gethash.sha1:main",
            "sha256 = gethash.sha256:main",
            "sha512 = gethash.sha512:main",
            "sha3-256 = gethash.sha3_256:main",
            "sha3-512 = gethash.sha3_512:main",
            "blake2b = gethash.blake2b:main",
            "blake2s = gethash.blake2s:main",
            # Legacy hash functions.
            "md2 = gethash.md2:main",
            "md4 = gethash.md4:main",
            "ripemd160 = gethash.ripemd160:main",
        ]
    },
    install_requires=requirements,
    python_requires=">=3.6",
)
