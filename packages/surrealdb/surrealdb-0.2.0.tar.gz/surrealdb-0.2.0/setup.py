# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['surrealdb', 'surrealdb.clients', 'surrealdb.common', 'surrealdb.models']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1', 'httpx>=0.23.0']

setup_kwargs = {
    'name': 'surrealdb',
    'version': '0.2.0',
    'description': 'The official SurrealDB library for Python.',
    'long_description': '<p align="center">\n    <img width="300" src="https://raw.githubusercontent.com/surrealdb/surrealdb/main/img/icon.png" alt="SurrealDB Icon">\n</p>\n\n<br>\n\n<p align="center">\n    <a href="https://surrealdb.com#gh-dark-mode-only" target="_blank">\n        <img width="300" src="https://raw.githubusercontent.com/surrealdb/surrealdb/main/img/white/logo.svg" alt="SurrealDB Logo">\n    </a>\n    <a href="https://surrealdb.com#gh-light-mode-only" target="_blank">\n        <img width="300" src="https://raw.githubusercontent.com/surrealdb/surrealdb/main/img/black/logo.svg" alt="SurrealDB Logo">\n    </a>\n</p>\n\n<h3 align="center">\n    <a href="https://surrealdb.com#gh-dark-mode-only" target="_blank">\n        <img src="https://raw.githubusercontent.com/surrealdb/surrealdb/main/img/white/text.svg" height="15" alt="SurrealDB">\n    </a>\n    <a href="https://surrealdb.com#gh-light-mode-only" target="_blank">\n        <img src="https://raw.githubusercontent.com/surrealdb/surrealdb/main/img/black/text.svg" height="15" alt="SurrealDB">\n    </a>\n    is the ultimate cloud <br> database for tomorrow\'s applications\n</h3>\n\n<h3 align="center">Develop easier. &nbsp; Build faster. &nbsp; Scale quicker.</h3>\n\n<br>\n\n<p align="center">\n    <a href="https://github.com/surrealdb/surrealdb.py"><img src="https://img.shields.io/badge/status-beta-ff00bb.svg?style=flat-square"></a>\n    &nbsp;\n    <a href="https://surrealdb.com/docs/integration/libraries/python"><img src="https://img.shields.io/badge/docs-view-44cc11.svg?style=flat-square"></a>\n    &nbsp;\n    <a href="https://github.com/surrealdb/surrealdb.py"><img src="https://img.shields.io/badge/license-Apache_License_2.0-00bfff.svg?style=flat-square"></a>\n    &nbsp;\n    <a href="https://twitter.com/surrealdb"><img src="https://img.shields.io/badge/twitter-follow_us-1d9bf0.svg?style=flat-square"></a>\n    &nbsp;\n    <a href="https://dev.to/surrealdb"><img src="https://img.shields.io/badge/dev-join_us-86f7b7.svg?style=flat-square"></a>\n    &nbsp;\n    <a href="https://www.linkedin.com/company/surrealdb/"><img src="https://img.shields.io/badge/linkedin-connect_with_us-0a66c2.svg?style=flat-square"></a>\n</p>\n\n<p align="center">\n\t<a href="https://surrealdb.com/blog"><img height="25" src="https://raw.githubusercontent.com/surrealdb/surrealdb/main/img/social/blog.svg" alt="Blog"></a>\n\t&nbsp;\n\t<a href="https://github.com/surrealdb/surrealdb"><img height="25" src="https://raw.githubusercontent.com/surrealdb/surrealdb/main/img/social/github.svg" alt="Github\t"></a>\n\t&nbsp;\n    <a href="https://www.linkedin.com/company/surrealdb/"><img height="25" src="https://raw.githubusercontent.com/surrealdb/surrealdb/main/img/social/linkedin.svg" alt="LinkedIn"></a>\n    &nbsp;\n    <a href="https://twitter.com/surrealdb"><img height="25" src="https://raw.githubusercontent.com/surrealdb/surrealdb/main/img/social/twitter.svg" alt="Twitter"></a>\n    &nbsp;\n    <a href="https://www.youtube.com/channel/UCjf2teVEuYVvvVC-gFZNq6w"><img height="25" src="https://raw.githubusercontent.com/surrealdb/surrealdb/main/img/social/youtube.svg" alt="Youtube"></a>\n    &nbsp;\n    <a href="https://dev.to/surrealdb"><img height="25" src="https://raw.githubusercontent.com/surrealdb/surrealdb/main/img/social/dev.svg" alt="Dev"></a>\n    &nbsp;\n    <a href="https://surrealdb.com/discord"><img height="25" src="https://raw.githubusercontent.com/surrealdb/surrealdb/main/img/social/discord.svg" alt="Discord"></a>\n    &nbsp;\n    <a href="https://stackoverflow.com/questions/tagged/surrealdb"><img height="25" src="https://raw.githubusercontent.com/surrealdb/surrealdb/main/img/social/stack-overflow.svg" alt="StackOverflow"></a>\n\n</p>\n\n# surrealdb.py\n\nThe official SurrealDB library for Python.\n',
    'author': 'SurrealDB',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
