#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='simpay-api',
    version='2.1',
    description='Python wrapper for Simpay API',
    author='Rafał Więcek <kontakt@simpay.pl>',

    url='https://github.com/SimPaypl/SimPay-API-Python',

    packages=['payments'],
    install_required=[
        'requests'
    ]
)