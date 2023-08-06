import importlib
import os
import re

from django.conf import settings
from django.db import connections
from django.test.utils import setup_databases


def get_db_backend(connection):
    vendor_map = {
        "sqlite": "django_migrations_ci.backends.sqlite3",
        "postgresql": "django_migrations_ci.backends.postgresql",
    }
    return importlib.import_module(vendor_map[connection.vendor])


def setup_test_db():
    # Based on https://github.com/django/django/blob/d62563cbb194c420f242bfced52b37d6638e67c6/django/test/runner.py#L1051-L1054  # noqa: E501
    aliases = list(settings.DATABASES.keys())
    for alias, db_conf in settings.DATABASES.items():
        test_conf = db_conf.setdefault("TEST", {})
        if not test_conf.get("NAME"):
            test_conf["NAME"] = connections[alias].creation._get_test_db_name()

    setup_databases(verbosity=True, interactive=False, aliases=aliases)


def clone_test_db(parallel, is_pytest=False, database="default"):
    db_conf = settings.DATABASES[database]

    try:
        db_conf["NAME"] = db_conf["TEST"]["NAME"]
    except KeyError:
        pass

    connection = connections[database]
    for index in range(parallel):
        if is_pytest:
            # pytest-django use test_db_gwN, from 0 to N-1.
            # e.g. test_db_gw0, test_db_gw1, ...
            # https://github.com/pytest-dev/pytest-django/blob/e0c77b391ea54c3b8d6ffbb593aa25188a0ce7e9/pytest_django/fixtures.py#L61  # noqa: E501
            suffix = f"gw{index}"
        else:
            # Django use test_db_N, from 1 to N.
            # e.g. test_db_1, test_db_2, ...
            suffix = f"{index + 1}"

        connection.creation.clone_test_db(suffix=suffix, verbosity=True, keepdb=False)

        settings_dict = connection.creation.get_test_db_clone_settings(suffix)
        django_db_name = settings_dict["NAME"]
        if is_pytest and connection.vendor == "sqlite" and "." in django_db_name:
            # Django clone_test_db create file db_gw0.sqlite3, but pytest-django
            # expects db.sqlite3_gw0. Lets rename the file.
            pytest_db_name = re.sub(r"(_gw\d+)\.(.+)$", r".\2\1", django_db_name)

            # Move db_gw0.sqlite3 to db.sqlite3_gw0.
            os.rename(django_db_name, pytest_db_name)
