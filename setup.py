#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='simpay-api',
    version='1.0',
    description='Python wrapper for Simpay API',
    author='DarkGL <r.wiecek@simpay.pl>',

    url='https://github.com/SimPaypl/SimPay-API-Python',

    packages=['payments'],
    install_required=[
        'requests'
    ]
)
