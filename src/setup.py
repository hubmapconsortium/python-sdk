# coding: utf-8

"""
    HuBMAP Software Development Kit

    The HuBMAP SDK is a client-library that facilitates simplified interaction with the Entity API, Search Api, Uuid Api
    and Ingest Api

    Contact: help@hubmapconsortium.org
"""

from setuptools import setup, find_packages  # noqa: H301

NAME = "hubmap_sdk"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["certifi==2021.10.8", "chardet==4.0.0", "idna==2.10", "requests==2.25.1", "urllib3==1.26.7"]

setup(
    name=NAME,
    version=VERSION,
    description="HuBMAP Sdk",
    author_email="help@hubmapconsortium.org",
    url="",
    keywords=["HuBMAP Sdk"],
    install_requires=REQUIRES,
    packages="hubmap_sdk",
    include_package_data=True,
    long_description="""\
    The HuBMAP SDK is a client-library that facilitates simplified interaction with the Entity API, Search Api, Uuid Api
    and Ingest Api 
    """
)

