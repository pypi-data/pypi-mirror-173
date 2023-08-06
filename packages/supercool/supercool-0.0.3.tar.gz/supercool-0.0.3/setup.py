#!/usr/bin/env python3

import setuptools
import re

version = ""
logn_description = ""
with open('supercool/VERSION', 'r') as fd:
    version = fd.readline().strip()

with open("README.md", "r") as fh:
    long_description = fh.read().strip()

setuptools.setup(
    name = "supercool",
    version = version,
    author = "isaachan",
    author_email = "isaachanstar@gmail.com",
    description = "This is the SDK for example.",
    long_description = long_description,
    url = "http://example.com",
    install_requires = [
	'requests'
    ],
    packages = setuptools.find_packages(where="supercool"),
    scripts=['scripts/supercool'],
    classifiers = [
	'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
)


