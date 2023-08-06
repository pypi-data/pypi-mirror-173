# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiosmtplib', 'docs', 'tests']

package_data = \
{'': ['*']}

extras_require = \
{'docs': ['sphinx>=4,<5', 'sphinx_autodoc_typehints>=1.7.0,<2.0.0'],
 'uvloop': ['uvloop>=0.14,<0.15']}

setup_kwargs = {
    'name': 'aiosmtplib',
    'version': '2.0.0',
    'description': 'asyncio SMTP client',
    'long_description': 'aiosmtplib\n==========\n\n|circleci| |codecov| |pypi-version| |pypi-python-versions| |pypi-status| |downloads|\n|pypi-license| |black|\n\n------------\n\naiosmtplib is an asynchronous SMTP client for use with asyncio.\n\nFor documentation, see `Read The Docs`_.\n\nQuickstart\n----------\n\n.. code-block:: python\n\n    import asyncio\n    from email.message import EmailMessage\n\n    import aiosmtplib\n\n    message = EmailMessage()\n    message["From"] = "root@localhost"\n    message["To"] = "somebody@example.com"\n    message["Subject"] = "Hello World!"\n    message.set_content("Sent via aiosmtplib")\n\n    loop = asyncio.get_event_loop()\n    loop.run_until_complete(aiosmtplib.send(message, hostname="127.0.0.1", port=25))\n\n\nRequirements\n------------\nPython 3.7+, compiled with SSL support, is required.\n\n\nBug Reporting\n-------------\nBug reports (and feature requests) are welcome via `Github issues`_.\n\n\n\n.. |circleci| image:: https://circleci.com/gh/cole/aiosmtplib/tree/main.svg?style=shield\n           :target: https://circleci.com/gh/cole/aiosmtplib/tree/main\n           :alt: "aiosmtplib CircleCI build status"\n.. |pypi-version| image:: https://img.shields.io/pypi/v/aiosmtplib.svg\n                 :target: https://pypi.python.org/pypi/aiosmtplib\n                 :alt: "aiosmtplib on the Python Package Index"\n.. |pypi-python-versions| image:: https://img.shields.io/pypi/pyversions/aiosmtplib.svg\n.. |pypi-status| image:: https://img.shields.io/pypi/status/aiosmtplib.svg\n.. |pypi-license| image:: https://img.shields.io/pypi/l/aiosmtplib.svg\n.. |codecov| image:: https://codecov.io/gh/cole/aiosmtplib/branch/main/graph/badge.svg\n             :target: https://codecov.io/gh/cole/aiosmtplib\n.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n           :target: https://github.com/ambv/black\n           :alt: "Code style: black"\n.. |downloads| image:: https://pepy.tech/badge/aiosmtplib\n               :target: https://pepy.tech/project/aiosmtplib\n               :alt: "aiosmtplib on pypy.tech"\n.. _Read The Docs: https://aiosmtplib.readthedocs.io/en/stable/overview.html\n.. _Github issues: https://github.com/cole/aiosmtplib/issues\n',
    'author': 'Cole Maclean',
    'author_email': 'hi@colemaclean.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/cole/aiosmtplib',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
