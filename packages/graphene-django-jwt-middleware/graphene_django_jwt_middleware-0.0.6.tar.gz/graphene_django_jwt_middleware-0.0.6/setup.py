# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graphene_django_jwt_middleware']

package_data = \
{'': ['*']}

install_requires = \
['django', 'pyjwt>=2.4.0,<3.0.0']

setup_kwargs = {
    'name': 'graphene-django-jwt-middleware',
    'version': '0.0.6',
    'description': 'Middleware to check JWT validation in GraphQL schemas',
    'long_description': '# Graphene Django JWT Middleware\n\nThis is a [Graphene Django](https://docs.graphene-python.org/projects/django/en/latest/) middleware to check JWT in GraphQL schemas.\n\n## Installing\n\nwith pipenv:\n\n```bash\npipenv install graphene-django-jwt-middleware\n```\n\nor poetry:\n\n```bash\npoetry add graphene-django-jwt-middleware\n```\n\n## Usage\n\nIn your django `settings.py` file, find `GRAPHENE` configuration and insert at the `MIDDLEWARE` section:\n\n```python\n...\n\nGRAPHENE = {\n    "SCHEMA": "...",\n    \'MIDDLEWARE\': [\n        \'graphene_django_jwt_middleware.middleware.JWTAuthorizationMiddleware\'\n    ]\n}\n\n...\n```\n',
    'author': 'Instruct Developers',
    'author_email': 'oss@instruct.com.br',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/instruct-br/graphene-django-jwt-middleware',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
