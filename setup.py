#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = "ipminify",
    version = "0.1.0",
    packages = find_packages("src"),
    package_dir = { "": "src"},
    author = "Naftuli Kay",
    author_email = "me@naftuli.wtf",
    url = "https://github.com/naftulikay/python-ipminify",
    install_requires = [
        "setuptools",
    ],
    dependency_links = [],
    entry_points = {
        "console_scripts": [
            # example: 'ipminify = ipminify:main'
        ]
    },
)
