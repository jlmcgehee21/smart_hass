#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'PyYAML>=3.0',
    'Jinja2>=2.9.0',
]

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest',
]

setup(
    name='smart_hass',
    version='0.2.0',
    description="Tools I find useful in my interactions with Home Assistant.",
    long_description=readme + '\n\n' + history,
    author="Jeff McGehee",
    author_email='jlmcgehee21@gmail.com',
    url='https://github.com/jlmcgehee21/smart_hass',
    packages=find_packages(include=['smart_hass']),
    entry_points={
        'console_scripts': [
            'smass=smart_hass.cli:cli'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='smart_hass',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
