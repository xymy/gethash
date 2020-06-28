import sys
from importlib import import_module
from pathlib import Path

from setuptools import find_packages, setup

# Import this package from src directory.
sys.path = [str(Path(__file__).with_name('src'))] + sys.path
package = import_module('gethash')
__project__ = package.__project__
__version__ = package.__version__
__author__ = package.__author__

readme = Path(__file__).with_name('README.md').read_text()

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
    name=__project__,
    version=__version__,
    license='MIT',

    description='Generate or check hash values.',
    long_description=readme,
    long_description_content_type='text/markdown',

    author=__author__,
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

            'md5 = gethash.getmd5:main',
            'sha1 = gethash.getsha1:main',
            'sha256 = gethash.getsha256:main',
            'sha512 = gethash.getsha512:main',
        ]
    },

    install_requires=[
        'click>=7.1',
        'colorama>=0.4; sys_platform == "win32"',
        'tqdm >= 4.46'
    ],
    python_requires='>=3.6'
)
