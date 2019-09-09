# -*- coding: utf-8 -*-
"""Installer for the collective.es.plone package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='collective.es.plone',
    version='1.0a1',
    description="Addon for ElasticSearch integration with Plone",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone',
    author='Jens W. Klein',
    author_email='jk@kleinundpartner.at',
    url='https://github.com/collective/collective.es.plone',
    project_urls={
        'PyPI': 'https://pypi.python.org/pypi/collective.es.plone',
        'Source': 'https://github.com/collective/collective.es.plone',
        'Tracker': 'https://github.com/collective/collective.es.plone/issues',
        # 'Documentation': 'https://collective.es.plone.readthedocs.io/en/latest/',
    },
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['collective', 'collective.es'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.6",
    install_requires=[
        'collective.es.ingestion',
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
    [console_scripts]
    update_locale = collective.es.plone.locales.update:update_locale
    """,
)
