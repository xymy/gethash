import sys
from importlib import import_module
from pathlib import Path

from setuptools import find_packages, setup

# Import this package from src directory and fetch metadata.
sys.path = [str(Path(__file__).with_name('src'))] + sys.path
package = import_module('gethash')
project = package.__project__
version = package.__version__
author = package.__author__

# Read metadata from files.
root = Path(__file__).parent
readme = (root / 'README.md').read_text()
requirements = (root / 'requirements.txt').read_text().splitlines()

classifiers = [
    'License :: OSI Approved',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Topic :: Security',
    'Topic :: Security :: Cryptography',
]

setup(
    name=project,
    version=version,
    license='MIT',

    description='A command-line tools that can generate or check hash values.',
    long_description=readme,
    long_description_content_type='text/markdown',

    author=author,
    author_email='thyfan@163.com',
    url='https://github.com/xymy/gethash',

    classifiers=classifiers,

    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'getmd5 = gethash.getmd5:main',
            'getsha1 = gethash.getsha1:main',
            'getsha256 = gethash.getsha256:main',
            'getsha512 = gethash.getsha512:main',
            'getblake2b = gethash.getblake2b:main',
            'getblake2s = gethash.getblake2s:main',

            'md5 = gethash.getmd5:main',
            'sha1 = gethash.getsha1:main',
            'sha256 = gethash.getsha256:main',
            'sha512 = gethash.getsha512:main',
            'blake2b = gethash.getblake2b:main',
            'blake2s = gethash.getblake2s:main',
        ]
    },

    install_requires=requirements,
    python_requires='>=3.6'
)
