#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='simple-django-tequila',
    version="2.0.2",
    packages=find_packages(),
    author="Maximilien Cuony",
    author_email="simple_django_tequila@fioupfioup.ch",
    description="Simple django login backend for tequila",
    install_requires=['requests'],
    include_package_data=True,

    url='https://github.com/the-glu/django-tequila',

    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries",
    ],

)
