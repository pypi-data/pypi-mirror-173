import sys
import os
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    # name of the library
    name="simplefibcffi",
    version="0.3",
    description="Display simple Fibonacci sequence from C implementation wrapped with CFFI.",
    # py-file that will be uploaded to PyPI
    py_modules=["simplefibcffi"],
    package_dir={"": "src"},
    #
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: PyPy",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    # project url
    url = "https://github.com/zhuokaizhao/simplefib_cffi",
    author="Zhuokai Zhao",
    author_email="zhuokai@uchicago.edu",
    packages=find_packages(),
    install_requires=["cffi>=1.0.0"],
    setup_requires=["cffi>=1.0.0"],
    cffi_modules=[
        "./src/build_fib.py:ffibuilder",
    ],
)
