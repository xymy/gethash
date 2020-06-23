from pathlib import Path

from setuptools import find_packages, setup

__project__ = 'gethash'
__version__ = '0.1'
__author__ = 'xymy'

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
            'getsha1 = gethash.getsha1:main',
        ]
    },

    install_requires=[
        'click>=7.0',
    ],
    python_requires='>=3.6'
)
