#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    #'nailgun',
    'import_string',
    'jinja2',
    'six',
    'PyYAML',
    'coloredlogs'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='satellite_populate',
    version='0.1.2',
    description="Populate and Validate the System using YAML",
    long_description=readme + '\n\n' + history,
    author="Bruno Rocha",
    author_email='rochacbruno@gmail.com',
    url='https://github.com/SatelliteQE/satellite-populate',
    packages=[
        'satellite_populate',
    ],
    package_dir={'satellite_populate':
                 'satellite_populate'},
    entry_points={
        'console_scripts': [
            'satellite-populate=satellite_populate.commands:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='satellite_populate',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
