# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pgactivity', 'pgactivity.management', 'pgactivity.management.commands']

package_data = \
{'': ['*']}

install_requires = \
['django>=2']

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['importlib_metadata>=4']}

setup_kwargs = {
    'name': 'django-pgactivity',
    'version': '1.1.1',
    'description': 'Monitor, kill, and analyze Postgres queries.',
    'long_description': 'django-pgactivity\n#################\n\n``django-pgactivity`` makes it easy to view, filter, and kill\nactive Postgres queries.\n\nSome of the features at a glance:\n\n* The ``PGActivity`` proxy model and ``pgactivity`` management command\n  for querying and filtering the `Postgres pg_stat_activity view <https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STAT-ACTIVITY-VIEW>`__.\n* ``pgactivity.context`` and ``pgactivity.middleware.ActivityMiddleware``\n  for annotating queries with application metadata, such as the request URL.\n* ``pgactivity.cancel`` and ``pgactivity.terminate`` for canceling\n  and terminating queries. The ``PGActivity`` model manager also has\n  these methods.\n* ``pgactivity.timeout`` for dynamically setting the statement timeout.\n\nQuick Start\n===========\n\nBasic Command Usage\n-------------------\n\nUse ``python manage.py pgactivity`` to view and filter active queries. Output looks like the following::\n\n    39225 | 0:01:32 | IDLE_IN_TRANSACTION | None | lock auth_user in access exclusiv\n    39299 | 0:00:15 | ACTIVE | None | SELECT "auth_user"."id", "auth_user"."password\n    39315 | 0:00:00 | ACTIVE | None | WITH _pgactivity_activity_cte AS ( SELECT pid\n\nThe default output attributes are:\n\n1. The process ID of the connection.\n2. The duration of the query.\n3. The state of the query (see the `Postgres docs <https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STAT-ACTIVITY-VIEW>`__ for values).\n4. Attached context using ``pgactivity.context``.\n5. The query SQL.\n\nApply filters with ``-f`` (or ``--filter``). Here we query for all active queries that have a duration\nlonger than a minute::\n\n    python manage.py pgactivity -f state=ACTIVE -f \'duration__gt=1 minute\'\n\nCancel or terminate activity with ``--cancel`` or ``--terminate``.\nHere we terminate a query based on the process ID::\n\n    python manage.py pgactivity 39225 --terminate\n\nAttaching Context\n-----------------\n\nYou can attach context to queries to better understand where they originate\nusing ``pgactivity.context`` or by adding ``pgactivity.middleware.ActivityMiddleware``\nto ``settings.MIDDLEWARE``.\nUnderneath the hood, a comment is added to the SQL statement and surfaced in\n``django-pgactivity``.\n\nWhen using the middleware, the ``url`` of the request and the ``method`` of\nthe request are automatically added. Here\'s what the output looks like\nwhen using the ``pgactivity`` command::\n\n    39299 | 0:00:15 | ACTIVE | {"url": "/admin/", "method": "GET"} | SELECT "auth_use\n\nProxy Model\n-----------\n\nUse the ``pgactivity.models.PGActivity`` proxy model to query\nthe `Postgres pg_stat_activity view <https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STAT-ACTIVITY-VIEW>`__.\nThe model contains most of the fields from the view, and the ``cancel`` and ``terminate``\nmethods can be applied to the queryset.\n\nSetting the Statement Timeout\n-----------------------------\n\nDynamically set the SQL statement timeout of code using ``pgactivity.timeout``:\n\n.. code-block:: python\n\n    import pgactivity\n\n    @pgactivity.timeout(0.5)\n    def my_operation():\n        # Any queries in this operation that take over 500 milliseconds will throw\n        # django.db.utils.OperationalError.\n\nCompatibility\n=============\n\n``django-pgactivity`` is compatible with Python 3.7 - 3.10, Django 2.2 - 4.1, and Postgres 10 - 15.\n\nDocumentation\n=============\n\n`View the django-pgactivity docs here\n<https://django-pgactivity.readthedocs.io/>`_ to learn more about:\n\n\n* The proxy models and custom queryset methods.\n* Attaching application context to queries.\n* Using and configuring the management command.\n* Setting dynamic statement timeouts.\n\nInstallation\n============\n\nInstall django-pgactivity with::\n\n    pip3 install django-pgactivity\n\nAfter this, add ``pgactivity`` to the ``INSTALLED_APPS``\nsetting of your Django project.\n\nContributing Guide\n==================\n\nFor information on setting up django-pgactivity for development and\ncontributing changes, view `CONTRIBUTING.rst <CONTRIBUTING.rst>`_.\n\nPrimary Authors\n===============\n\n- `Wes Kendall <https://github.com/wesleykendall>`__\n- `Paul Gilmartin <https://github.com/PaulGilmartin>`__\n',
    'author': 'Opus 10 Engineering',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Opus10/django-pgactivity',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.0,<4',
}


setup(**setup_kwargs)
