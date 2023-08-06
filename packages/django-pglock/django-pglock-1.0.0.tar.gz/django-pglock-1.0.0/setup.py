# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pglock', 'pglock.management', 'pglock.management.commands']

package_data = \
{'': ['*']}

install_requires = \
['django-pgactivity>=1.1,<2', 'django>=2']

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['importlib_metadata>=4']}

setup_kwargs = {
    'name': 'django-pglock',
    'version': '1.0.0',
    'description': 'Postgres locking routines and lock table access.',
    'long_description': 'django-pglock\n#############\n\n``django-pglock`` performs advisory locks, table locks, and helps manage blocking locks.\nHere\'s some of the functionality at a glance:\n\n* ``pglock.advisory`` for application-level locking, for example, ensuring that tasks don\'t overlap.\n* ``pglock.model`` for locking an entire model.\n* ``pglock.timeout`` for dynamically setting the timeout to acquire a lock.\n* ``pglock.prioritize`` to kill blocking locks for critical code, such as migrations.\n* The ``PGLock`` and ``BlockedPGLock`` models for querying active and blocked locks.\n* The ``pglock`` management command that wraps the models and provides other utilities.\n\nQuickstart\n==========\n\nAdvisory Locks\n--------------\n\nUse ``pglock.advisory`` to acquire a `Postgres advisory lock <https://www.postgresql.org/docs/current/explicit-locking.html#ADVISORY-LOCKS>`__:\n\n.. code-block:: python\n\n    import pglock\n\n    with pglock.advisory("my_lock_id"):\n        # This code blocks until the "my_lock_id" lock is available\n\n\nAbove our code will block until the lock is available, meaning\nno instances of the function will run simultaneously. Use\nthe ``timeout`` argument to configure how long to wait for\nthe lock. A timeout of zero will return immediately:\n\n.. code-block:: python\n\n    with pglock.advisory("my_lock_id", timeout=0) as acquired:\n        if acquired:\n            # The lock is acquired\n\nUse ``side_effect=pglock.Raise`` to raise a ``django.db.utils.OperationalError`` if\nthe lock can\'t be acquired. When using the decorator, you can also use\n``side_effect=pglock.Skip`` to skip the function if the lock can\'t be acquired:\n\n.. code-block:: python\n\n    @pglock.advisory(timeout=0, side_effect=pglock.Skip)\n    def non_overlapping_func():\n        # This function will not run if there\'s another one already running.\n        # The decorator lock ID defaults to <module_name>.<function_name>\n\nModel Locks\n-----------\n\n``pglock.model`` can take a lock on an entire model during a transaction. For example:\n\n.. code-block:: python\n\n    from django.db import transaction\n    import pglock\n\n    with transaction.atomic():\n        pglock.model("auth.User")\n\n        # Any operations on auth.User will be exclusive here. Even read access\n        # for other transactions is blocked\n\n``pglock.model`` uses `Postgres\'s LOCK statement <https://www.postgresql.org/docs/current/sql-lock.html>`__,\nand it accepts the lock mode as a argument. See the\n`Postgres docs for more information <https://www.postgresql.org/docs/current/sql-lock.html>`__.\n\n**Note** ``pglock.model`` is similar to ``pglock.advisory``. Use the ``timeout`` argument\nto avoid waiting for locks, and supply the appropriate ``side_effect`` to adjust runtime behavior.\n\nPrioritizing Blocked Code\n-------------------------\n\n``pglock.prioritize`` will terminate any locks blocking the wrapped code:\n\n.. code-block:: python\n\n    import pglock\n\n    @pglock.prioritize()\n    def my_func():\n        # Any other statements that have conflicting locks will be killed on a\n        # periodic interval.\n        MyModel.objects.update(val="value")\n\n``pglock.prioritize`` is useful for prioritizing code, such as migrations, to avoid\nsituations where locks are held for too long.\n\nSetting the Lock Timeout\n------------------------\n\nUse ``pglock.timeout`` to dynamically set `Postgres\'s lock_timeout runtime\nsetting <https://www.postgresql.org/docs/current/runtime-config-client.html>`__:\n\n.. code-block:: python\n\n    import pglock\n\n    @pglock.timeout(1)\n    def do_stuff():\n        # This function will throw an exception if any code takes longer than\n        # one second to acquire a lock\n\nQuerying Locks\n--------------\n\nUse ``pglock.models.PGLock`` to query active locks. It wraps\n`Postgres\'s pg_locks view <https://www.postgresql.org/docs/current/view-pg-locks.html>`__.\nUse ``pglock.models.BlockedPGLock`` to query locks and join the activity that\'s blocking\nthem.\n\nUse ``python manage.py pglock`` to view and kill locks from the command line. It has\nseveral options for dynamic filters and re-usable configuration.\n\nCompatibility\n=============\n\n``django-pglock`` is compatible with Python 3.7 - 3.10, Django 2.2 - 4.1, and Postgres 10 - 15.\n\nDocumentation\n=============\n\n`View the django-pglock docs here\n<https://django-pglock.readthedocs.io/>`_ to learn more about:\n\n* Using advisory locks.\n* Locking models.\n* Setting dynamic lock timeouts.\n* Killing blocking locks.\n* The proxy models and custom queryset methods.\n* Using and configuring the management command.\n\nInstallation\n============\n\nInstall django-pglock with::\n\n    pip3 install django-pglock\n\nAfter this, add both ``pgactivity`` and ``pglock`` to the ``INSTALLED_APPS``\nsetting of your Django project.\n\nContributing Guide\n==================\n\nFor information on setting up django-pglock for development and\ncontributing changes, view `CONTRIBUTING.rst <CONTRIBUTING.rst>`_.\n\nPrimary Authors\n===============\n\n- `Wes Kendall <https://github.com/wesleykendall>`__\n- `Paul Gilmartin <https://github.com/PaulGilmartin>`__\n',
    'author': 'Opus 10 Engineering',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Opus10/django-pglock',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.0,<4',
}


setup(**setup_kwargs)
