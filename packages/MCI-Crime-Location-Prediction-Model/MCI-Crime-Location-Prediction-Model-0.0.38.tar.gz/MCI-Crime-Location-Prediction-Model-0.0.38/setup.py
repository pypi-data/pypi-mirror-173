#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from setuptools import find_packages, setup


other = {}
ROOT_DIR = Path(__file__).resolve().parent
REQUIREMENTS_DIR = ROOT_DIR / 'requirements'
PACKAGE_DIR = ROOT_DIR / 'mci_model'
with open(PACKAGE_DIR / "VERSION") as f:
    _version = f.read().strip()
    other["__version__"] = _version


def list_reqs(filename="requirements.txt"):
    ''' Install requirements for setup script '''
    with open(REQUIREMENTS_DIR / filename) as f:
        return f.read().splitlines()


setup(
    name='MCI-Crime-Location-Prediction-Model',
    version=other["__version__"],
    description="MCI regression model containing train and testing data",
    long_description="MCI regression model containing train and testing data",
    long_description_content_type="text/markdown",
    author="MohamedBenaicha",
    author_email="mohamed.benaicha@hotmail.com",
    python_requires=">=3.9.0",
    url="https://github.com/mohbenaicha/mci-production-package",
    packages=find_packages(exclude=("tests",)),
    package_data={"mci_model": ["VERSION"]},# this is included here despite 
                                            # despite also being under MANIFEST.in
    install_requires=list_reqs(), # in place of setup_requires as per PEP 517
    extras_require={},
    include_package_data=True,
    license='Apache License 2.0',
    license_files=("LICENSE.txt",), 
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"
    ])