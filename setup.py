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

required = ['requests>=2.12', 'websocket-client==0.40.0',
        'beautifulsoup4==4.5.1', 'html5lib==0.999999999', 'pyfiglet==0.7.5',
        'certifi==2016.9.26']
if not PYTHON3:
    required += ['importlib>=1.0.4']

packages = ['limbo', 'limbo.plugins']

try:
    longdesc = open("README.rst").read()
except:
    longdesc = ''

setup(
    name='limbo',
    version='5.6.1',
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
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    keywords="slack chatbot chat limbo",
)
