#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', 'protobuf', 'twisted', 'pyopenssl', 'service-identity']

setup_requirements = []

test_requirements = []

setup(
    author="Marcus Santos",
    author_email='marcus@marcus-santos.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="A python client wraper for the publicly available protobuf-based API developed by Spotware",
    entry_points={
        'console_scripts': [
            'spotware_connect=spotware_connect.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='spotware_connect',
    name='spotware_connect',
    packages=find_packages(include=['spotware_connect']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/marcus-santos/spotware_connect',
    version='0.1.0',
    zip_safe=False,
)
