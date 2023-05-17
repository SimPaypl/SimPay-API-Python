#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='simpay-api',
    version='3.0',
    description='Python wrapper for Simpay API',
    author='Rafał Więcek <kontakt@simpay.pl>',
    url='https://github.com/SimPaypl/SimPay-API-Python',
    python_requires=">3.0",
    packages=find_packages(exclude=["tests*", "examples*"]),
    test_suite="tests",
    include_package_data=True,
    install_requires=['requests'],
)