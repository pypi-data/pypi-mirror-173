#!/usr/bin/env python
# -*- coding:utf-8 -*-
#############################################
# File Name: setup.py
# Author: mage
# Mail: mage@woodcol.com
# Created Time:  2018-1-23 19:17:34
#############################################
from setuptools import setup, find_packages
setup(
    name="pyCeph",
    version="0.4.2",
    keywords=["pip", "pyCeph", "s3", "ceph"],
    description="ceph using tool",
    long_description="ceph using tool",
    license="MIT Licence",
    url="https://github.com/susufqx/pyCeph",
    author="susufqx",
    author_email="jiangsulirui@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        "aioboto3",
        "boto3",
        "urllib3",
    ]
)
