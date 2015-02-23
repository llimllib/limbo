#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Thanks to Kenneth Reitz, I stole the template for this

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

required = ['requests>=2.5']
packages = ['slask', 'slask.slackclient', 'slask.plugins']

try:
    longdesc = open("README.md").read()
except:
    longdesc = ''

setup(
    name='slask',
    version='3.0.0a1',
    description='Simple and Clean Slack Chatbot',
    long_description=longdesc,
    author='Bill Mill',
    author_email='bill@billmill.org',
    url='https://github.com/llimllib/slask',
    packages=packages,
    scripts = ['bin/slask'],
    package_data={'': ['LICENSE',], '': ['slask/plugins/*.py']},
    include_package_data=True,
    install_requires=required,
    license='MIT',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ),
)
