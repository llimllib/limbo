#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Thanks to Kenneth Reitz, I stole the template for this

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

PYTHON3 = sys.version_info[0] > 2

required = ['requests>=2.5', 'websocket-client==0.32.0', 'beautifulsoup4==4.3.2', 'pyfiglet==0.7.4', 'slackrtm==0.2.1']
if not PYTHON3:
    required += ['importlib>=1.0.3']

packages = ['limbo', 'limbo.plugins']

try:
    longdesc = open("README.rs").read()
except:
    longdesc = ''

setup(
    name='limbo',
    version='3.4.2',
    description='Simple and Clean Slack Chatbot',
    long_description=longdesc,
    author='Bill Mill',
    author_email='bill@billmill.org',
    url='https://github.com/llimllib/limbo',
    packages=packages,
    scripts = ['bin/limbo'],
    package_data={'': ['LICENSE',], '': ['limbo/plugins/*.py']},
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
        'Programming Language :: Python :: 3.4',
    ),
)
