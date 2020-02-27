#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['protobuf', 'twisted', 'pyopenssl', 'service-identity']

setup_requirements = []

test_requirements = []

setup(
    author="Marcus Santos",
    author_email='marcus@marcus-santos.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Framework :: Twisted',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A python client wraper for Spotware Open API 2.0",
    entry_points={
        'console_scripts': [
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='spotware openapi2',
    name='spotware_connect',
    packages=find_packages(include=['spotware_connect', 'spotware_connect.messages']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/marcus-santos/spotware_connect',
    version='0.1.2',
    zip_safe=False,
)
