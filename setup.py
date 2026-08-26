#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os

from setuptools import setup


def read(rel_path):
    with codecs.open(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), rel_path), "r"
    ) as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delimiter = '"' if '"' in line else "'"
            return line.split(delimiter)[1]
    else:
        raise RuntimeError("Unable to find version string.")


if os.environ.get("APPLICATION_VERSION"):
    version = os.environ["APPLICATION_VERSION"]
else:
    version = get_version("ImageGoNord/__init__.py")
print(f"Setup version is: {version}")
setup(
    version=version,
)

setup(
    name="image-go-nord",
    version="1.2.0",
    description="A tool to convert any RGB image or video to any theme or color palette input by the user",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/schroedinger-Hat/ImageGoNord-pip",
    download_url="https://github.com/schroedinger-Hat/ImageGoNord-pip/releases",
    keywords=[
        "nordtheme",
        "pillow",
        "image",
        "conversion",
        "rgb",
        "color-scheme",
        "color-palette",
        "linux-rice",
        "gruvbox",
        "catpuccin",
    ],
    author="Schroedinger Hat",
    author_email="dev@schroedinger-hat.org",
    license="AGPL-3.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    project_urls={
        "Homepage": "https://ign.schroedinger-hat.org",
        "Source": "https://github.com/schroedinger-Hat/ImageGoNord-pip",
        "Bug Reports": "https://github.com/schroedinger-Hat/ImageGoNord-pip/issues",
    },
    packages=find_packages(),
    package_data={"": ["*.txt", "palettes/*.txt"]},
    include_package_data=True,
    install_requires=["Pillow", "ffmpeg-python", "numpy", "requests"],
    extras_require={"AI": ["torch", "scikit-image", "torchvision"]},
    python_requires=">=3.5",
)
