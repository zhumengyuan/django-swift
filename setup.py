#!/usr/bin/env python

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

requires = [
    'python-swiftclient',
]

# Use part of the sphinx docs index for the long description

setup(
    name="django_swift",
    version='0.9.1',
    packages=find_packages(),
    install_requires=requires,
    description = 'a django storage for swift',
    long_description=README,
    author="duanhongyi",
    author_email="duanhongyi@doopai.com",
    license="BSD",
    url="https://github.com/duanhongyi/django_swift/",
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)
