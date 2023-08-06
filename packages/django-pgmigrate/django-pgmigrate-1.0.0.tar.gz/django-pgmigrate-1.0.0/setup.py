# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pgmigrate', 'pgmigrate.management', 'pgmigrate.management.commands']

package_data = \
{'': ['*']}

install_requires = \
['django-pglock<2', 'django>=2']

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['importlib_metadata>=4']}

setup_kwargs = {
    'name': 'django-pgmigrate',
    'version': '1.0.0',
    'description': 'Less downtime during migrations.',
    'long_description': "django-pgmigrate\n################\n\n``django-pgmigrate`` helps you avoid costly downtime with Postgres migrations.\n\nImagine the following happens:\n\n1. A long-running task queries a model in a transaction and keeps the transaction open.\n2. ``python manage.py migrate`` tries to change a field on the model.\n\nBecause of how Postgres queues locks, this common scenario causes **every**\nsubsequent query on the model to block until the query from 1) has finished.\n\n``django-pgmigrate`` provides the following features to alleviate problematic locking\nscenarios when running migrations:\n\n* Detect blocking queries and terminate them automatically (the default behavior).\n* Print blocking queries so that you can inspect\n  and terminate them manually.\n* Set the lock timeout so that migrations are terminated if they block too long.\n\nInstallation\n============\n\nInstall django-pgmigrate with::\n\n    pip3 install django-pgmigrate\n\nAfter this, add ``pgactivity``, ``pglock``, and ``pgmigrate`` to the ``INSTALLED_APPS``\nsetting of your Django project.\n\nQuick Start\n===========\n\nAfter following the installation instructions, running\n``python manage.py migrate`` will automatically terminate any blocking\nqueries. Here's an example of what it looks like:\n\n.. image:: docs/static/terminate_blocking.png\n\nThere are two additional outputs in the ``migrate`` command versus the original:\n\n1. The first output line shows the Postgres process ID. This is useful for\n   querying activity that's blocking the process.\n2. The yellow text shows when a blocking query was detected and terminated.\n   In our case, it was blocking auth migration 12.\n\nYou can configure ``django-pgmigrate`` to show blocked queries instead of automatically\nkilling them, and you can also set the lock timeout to automatically cancel migrations if\nthey block for too long.\nSee the documentation section below for more details.\n\nCompatibility\n=============\n\n``django-pgmigrate`` is compatible with Python 3.7 - 3.10, Django 2.2 - 4.1, and Postgres 10 - 15.\n\n\nDocumentation\n=============\n\n`View the django-pgmigrate docs here\n<https://django-pgmigrate.readthedocs.io/>`_ to learn more about:\n\n* How blocking queries are automatically terminated.\n* Configuring the command to show blocking activity instead of terminating it, along\n  with instructions on how to manually view and terminate activity.\n* Configuring lock timeouts to automatically stop migrations if they block for too long.\n* Advanced usage such as creating custom actions to run when queries are blocked.\n\nContributing Guide\n==================\n\nFor information on setting up django-pgmigrate for development and\ncontributing changes, view `CONTRIBUTING.rst <CONTRIBUTING.rst>`_.\n\nPrimary Authors\n===============\n\n- `Wes Kendall <https://github.com/wesleykendall>`__\n- `Paul Gilmartin <https://github.com/PaulGilmartin>`__\n",
    'author': 'Opus 10 Engineering',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Opus10/django-pgmigrate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.0,<4',
}


setup(**setup_kwargs)
