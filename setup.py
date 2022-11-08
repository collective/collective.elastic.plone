# -*- coding: utf-8 -*-
"""Installer for the collective.elastic.plone package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='collective.elastic.plone',
    version='1.0',
    description="Addon for ElasticSearch integration with Plone",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone',
    author='Jens W. Klein',
    author_email='jk@kleinundpartner.at',
    url='https://github.com/collective/collective.elastic.plone',
    project_urls={
        'PyPI': 'https://pypi.python.org/pypi/collective.elastic.plone',
        'Source': 'https://github.com/collective/collective.elastic.plone',
        'Tracker': 'https://github.com/collective/collective.elastic.plone/issues',
        # 'Documentation': 'https://collective.elastic.plone.readthedocs.io/en/latest/',
    },
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['collective', 'collective.elastic'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.6",
    install_requires=[
        'collective.elastic.ingest',
        'jinja2',
        'plone.restapi',
        'setuptools',
    ],
    extras_require={
        'test': [
            'plone.app.contenttypes[test]'
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
