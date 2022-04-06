# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
# Copyright (C) 2021      TU Wien.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""User profiles module for Invenio."""

import os
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

tests_require = [
    'pytest-invenio>=1.4.7',
]

extras_require = {
    'admin': [
        'invenio-admin>=1.2.0',
    ],
    'docs': [
        'Sphinx>=4.2.0,<5',
    ],
    'mysql': [
        'invenio-db[mysql,versioning]>=1.0.14',
    ],
    'postgresql': [
        'invenio-db[postgresql,versioning]>=1.0.14',
    ],
    'sqlite': [
        'invenio-db[versioning]>=1.0.14',
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for name, reqs in extras_require.items():
    if name in ('mysql', 'postgresql', 'sqlite'):
        continue
    extras_require['all'].extend(reqs)

setup_requires = [
    'Babel>=2.8',
]

install_requires = [
    'Flask-WTF>=0.15.1',
    'invenio-accounts>=1.4.4',
    'invenio-mail>=1.0.2',
]

packages = find_packages()


# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('invenio_userprofiles', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='invenio-userprofiles',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords='invenio profile account user',
    license='MIT',
    author='CERN',
    author_email='info@inveniosoftware.org',
    url='https://github.com/inveniosoftware/invenio-userprofiles',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'invenio_admin.views': [
            'invenio_userprofiles_view = '
            'invenio_userprofiles.admin:user_profile_adminview',
        ],
        'invenio_base.api_apps': [
            'invenio_userprofiles = invenio_userprofiles:InvenioUserProfiles',
        ],
        'invenio_base.api_blueprints': [
            'invenio_userprofiles'
            ' = invenio_userprofiles.views:blueprint_api_init',
        ],
        'invenio_base.apps': [
            'invenio_userprofiles = invenio_userprofiles:InvenioUserProfiles',
        ],
        'invenio_base.blueprints': [
            'invenio_userprofiles'
            ' = invenio_userprofiles.views:blueprint_ui_init',
        ],
        'invenio_db.alembic': [
            'invenio_userprofiles = invenio_userprofiles:alembic',
        ],
        'invenio_db.models': [
            'invenio_userprofiles = invenio_userprofiles.models',
        ],
        'invenio_i18n.translations': [
            'messages = invenio_userprofiles',
        ],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Development Status :: 5 - Production/Stable',
    ],
)
