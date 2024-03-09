#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from limbo import VERSION

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

appdir = os.path.dirname(os.path.realpath(__file__))
requirements = f"{appdir}/requirements.txt"
# should I bother to remove testing requirements?
required = [l.strip() for l in open(requirements) if not l.startswith("#")]

packages = ["limbo", "limbo.plugins"]

try:
    longdesc = open("README.rst").read()
except:
    longdesc = ""

setup(
    name="limbo",
    version=VERSION,
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
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="slack chatbot chat limbo",
)
