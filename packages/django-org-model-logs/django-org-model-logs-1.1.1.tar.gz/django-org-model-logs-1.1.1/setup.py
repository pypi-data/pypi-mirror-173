# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['org_model_logs', 'org_model_logs.migrations']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'django-org-model-logs',
    'version': '1.1.1',
    'description': 'A Django app to log actions and communications about models.',
    'long_description': None,
    'author': 'DBCA OIM',
    'author_email': 'asi@dbca.wa.gov.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
