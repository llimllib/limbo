#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Thanks to Kenneth Reitz, I stole the template for this

import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

PYTHON3 = sys.version_info[0] > 2

required = []
if not PYTHON3:
    required += ["importlib>=1.0.4"]

packages = ["limbo", "limbo.plugins"]

try:
    longdesc = open("README.rst").read()
except:
    longdesc = ""

setup(
    name="limbo",
    version="7.3.0",
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
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    keywords="slack chatbot chat limbo",
)
