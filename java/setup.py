# -*- coding: utf-8 -*-

"""setup.py: setuptools control."""

import os.path

from codecs import open

from setuptools import setup, find_packages

cwd = os.path.abspath(os.path.dirname(__file__))

setup(
    version='0.1.0',
    name='examples',
    description='Small helper to access Platform.sh environment variables.',
    packages=find_packages(),
)
