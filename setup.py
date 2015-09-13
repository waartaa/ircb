#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().spitlines()

setup(
    name='ircb',
    version='0.0.1',
    description='A IRC bouncer',
    long_description=''.join(open('README.md').readlines()),
    keywords='irc, client, bouncer',
    author='Ratnadeep Debnath',
    author_email='rtnpro@gmail.com',
    license='MIT',
    install_requires=requirements,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        ]
)
