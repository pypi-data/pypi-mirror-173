#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'celery==5.2.7']

test_requirements = ['pytest>=3', ]

setup(
    author="Concular GmbH",
    author_email='amit@concular.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="celery debounce without cache",
    entry_points={
        'console_scripts': [
            'celery_debounce=celery_debounce.cli:main',
        ],
    },
    install_requires=requirements,
    long_description_content_type="text/markdown",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='celery_debounce',
    name='celery_debounce',
    packages=find_packages(include=['celery_debounce', 'celery_debounce.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Concular/celery_debounce',
    version='0.2.0',
    zip_safe=False,
)
