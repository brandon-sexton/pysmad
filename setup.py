#!/usr/bin/env python

import pathlib

from setuptools import find_packages, setup
from sphinx.setup_command import BuildDoc

here = pathlib.Path(__file__).parent.resolve()
cmdclass = {"build_sphinx": BuildDoc}
name = "pyxis"
version = "0.1"
release = "0.1.0"
setup(
    name=name,
    author="Brandon Sexton",
    version=release,
    cmdclass=cmdclass,
    packages=find_packages(),
    # these are optional and override conf.py settings
    command_options={
        "build_sphinx": {
            "project": ("setup.py", name),
            "version": ("setup.py", version),
            "release": ("setup.py", release),
            "source_dir": ("setup.py", "./docs"),
        }
    },
)
