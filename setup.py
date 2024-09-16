#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os

from setuptools import setup


def read(rel_path):
    with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)), rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delimiter = '"' if '"' in line else "'"
            return line.split(delimiter)[1]
    else:
        raise RuntimeError("Unable to find version string.")


if __name__ == "__main__":

    if os.environ.get("APPLICATION_VERSION"):
        version = os.environ["APPLICATION_VERSION"]
    else:
        version = get_version("ImageGoNord/__init__.py")
    print(f"Setup version is: {version}")
    setup(
        version=version,
    )
