#!/usr/bin/env python

import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

setup(
    name="pyxis",
    author="Brandon Sexton",
    version="0.1.0",
    packages=find_packages(),
)
