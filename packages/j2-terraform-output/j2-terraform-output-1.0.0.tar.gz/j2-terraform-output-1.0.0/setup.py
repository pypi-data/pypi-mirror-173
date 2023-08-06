#!/usr/bin/env python
from distutils.core import setup
import setuptools

version = None
with open('jinja_terraform_output/__init__.py', 'r') as f:
    for line in f.readlines():
        if '__version__' in line:
            version = line.split('=')[1].replace('\'', '').strip()

setup(
    name = "j2-terraform-output",
    version = version,
    author = "Arnold",
    author_email = "arnoldjohnson401@gmail.com",
    description = ("A Jinja extension to fetch terraform state output versions"),
    long_description = ("A Jinja extension to fetch terraform state output versions"),
    license = "MIT",
    packages=setuptools.find_packages(),
    install_requires=[
        'Jinja2 < 4',
        'requests < 3',
    ],
)
