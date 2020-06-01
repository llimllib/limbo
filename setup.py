#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Thanks to Kenneth Reitz, I stole the template for this

import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

required = []
packages = ["limbo", "limbo.plugins"]

try:
    longdesc = open("README.rst").read()
except:
    longdesc = ""

setup(
    name="limbo",
    version="8.1.0",
    description="Simple and Clean Slack Chatbot",
    long_description=longdesc,
    author="Bill Mill",
    author_email="bill@billmill.org",
    url="https://github.com/llimllib/limbo",
    packages=packages,
    scripts=["bin/limbo"],
    package_data={"": ["LICENSE", "limbo/plugins/*.py"]},
    include_package_data=True,
    install_requires=required,
    license="MIT",
    python_requires=">=3.4",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    keywords="slack chatbot chat limbo",
)
