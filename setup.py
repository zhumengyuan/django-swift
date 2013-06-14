#!/usr/bin/env python

from setuptools import setup, find_packages

requires = [
    'python-swiftclient',
]

# Use part of the sphinx docs index for the long description

setup(
    name="django-swift",
    version='0.9',
    packages=find_packages(),
    install_requires=requires,
    author="duanhongyi",
    author_email="duanhongyi@doopai.com",
    license="BSD",
    url="https://github.com/swift/django-swift/",
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
