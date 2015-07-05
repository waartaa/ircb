#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup, find_packages

setup(
    name='ircb',
    version='0.0.1',
    description='A IRC bouncer',
    long_description=''.join(open('README.rst').readlines()),
    keywords='some, keywords',
    author='Ratnadeep Debnath',
    author_email='rtnpro@gmail.com',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        ]
)
