#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='python-bghive',
    author='John Dilley',
    author_email = 'john@johndilley.me.uk',
    version = '0.0.1',
    description = 'Library for interfacing to British Gas Hive',
    url = 'https://github.com/johnmdilley/python-bghive',
    packages=find_packages(),
    install_requires = ["requests"],
    )

