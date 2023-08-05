# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sans_db', 'sans_db.template_backends', 'sans_db.templatetags']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'django-sans-db',
    'version': '1.2.0',
    'description': 'Tools to limit database access in parts of your Django codebase ',
    'long_description': '# Django sans DB\n\nTools for limiting access to the database in parts of your Django code.\n\n## Installation\n\n```\npip install django-sans-db\n```\n\nIf you wish to use the `{% sansdb %}` template tag,\nyou will need to add `"sans_db"` to your `INSTALLED_APPS`.\n\n## Usage\n\n### Context manager\n\nYou can block access to your database for a section of your code using `block_db`:\n\n```python\nfrom sans_db.context_managers import block_db\n\nUser.objects.create(...)  # Works outside of block_db()\nwith block_db():\n    User.objects.get()  # Raises DatabaseAccessBlocked\n```\n\nIf you have multiple entries in your Django `DATABASES` setting,\nthen `block_db` will default to blocking all of them.\n\nIf you wish to block access to a subset of your databases,\npass a list of their aliases (the keys in the `DATABASES` dictionary).\n\n```python\nfrom sans_db.context_managers import block_db\n\nwith block_db(databases=["replica"]):\n    User.objects.using("primary").create(...)  # This DB isn\'t blocked.\n    User.objects.using("replica").get()  # Raises DatabaseAccessBlocked\n```\n\n\n### Decorator\n\nYou can decorate functions and methods with `block_db` to block database access in them. Eg:\n\n```python\nfrom sans_db.context_managers import block_db\n\nclass MyClass:\n    def allowed(self):\n        User.objects.create(...)  # Works outside of block_db()\n\n    @block_db()\n    def not_allowed(self):\n        User.objects.create(...)  # Raises DatabaseAccessBlocked\n```\n\n\n### Template backend\n\nYou can block access to the database when rendering Django templates with our custom template backend.\n\nNote: Currently, only Django templates are supported.\n\nYou can block database access in all of your templates\nby setting your templates backend to `"sans_db.template_backends.django_sans_db.DjangoTemplatesSansDB"`\n\nFor example:\n\n```python\n# settings.py\n\nTEMPLATES = [\n    {\n        "BACKEND": "sans_db.template_backends.django_sans_db.DjangoTemplatesSansDB",\n        "APP_DIRS": True,\n        "OPTIONS": {...},\n    },\n]\n```\n\nAttempts to query the database will now cause a `sans_db.exceptions.DatabaseAccessBlocked` to be raised.\n\nPlease refer to Django\'s docs on [support for template engines](https://docs.djangoproject.com/en/4.0/topics/templates/#support-for-template-engines)\nfor details on how to set this up as a secondary template renderer.\n\n\n### Template tag\n\nYou can block DB access in a portion of your template\nby wrapping it with the `{% sansdb %}` template tag.\n\nThe template tag accepts database aliases as either strings, or variables.\nIf passed as a variable, either strings or iterables of strings are accepted.\nIf no aliases are passed, all databases will be blocked.\n\nNote: `DatabaseAccessBlocked` is raised when an attempt is made to access the DB.\n\nTo block all databases:\n\n```django\n{% load sansdb %}\n{% sansdb %}\n    {# ... #}\n{% endsansdb %}\n```\n\nTo block a list of databases named in the template:\n\n```django\n{% load sansdb %}\n{% sansdb "second_db" "third_db" %}\n    {# ... #}\n{% endsansdb %}\n```\n\nTo block a list of databases from a context variable:\n\n```django\n{% load sansdb %}\n{% sansdb databases %}\n    {# ... #}\n{% endsansdb %}\n```\n',
    'author': 'Charlie Denton',
    'author_email': 'charlie@meshy.co.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/meshy/django-sans-db',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
