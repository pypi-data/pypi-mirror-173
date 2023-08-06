# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['goodmap', 'goodmap.db']

package_data = \
{'': ['*'], 'goodmap': ['static/*', 'templates/*']}

install_requires = \
['Babel>=2.10.3,<3.0.0',
 'Flask-Babel>=2.0.0,<3.0.0',
 'Flask>=2.1.1,<3.0.0',
 'PyYAML>=6.0,<7.0',
 'google-cloud-storage>=2.3.0,<3.0.0',
 'gunicorn>=20.1.0,<21.0.0',
 'platzky>=0.1.12,<0.2.0',
 'pytest>=7.1.2,<8.0.0']

setup_kwargs = {
    'name': 'goodmap',
    'version': '0.1.7',
    'description': 'Map engine to serve all the people :)',
    'long_description': '![Github Actions](https://github.com/problematy/goodmap/actions/workflows/python-app.yml/badge.svg)\n[![Coverage Status](https://coveralls.io/repos/github/Problematy/goodmap/badge.png)](https://coveralls.io/github/Problematy/goodmap)\n\n# Good Map\n\nMap engine to serve all the people ;) \n\n## Running App locally\n\n### Configuration\n\nRename config-template.yml to config.yml and change it\'s contents according to your needs.\nValues descriptions you can find inside config-template.yml.\n\n### Backend \n\nAll dependencies are specified in __pyproject.toml__ file. To install them in your onw environment:\n* go to project directory\n* use `poetry install`\n* get into poetry shell `poetry shell`\n* Run `FLASK_ENV=development;FLASK_APP=goodmap.goodmap flask run`\n\n### Frontend (optional)\nIn production environment javascript is served as static files, but for ease of development you can run javascript\nserver locally:\n* go to frontend directory\n* install all dependencies with `nmp install`\n* run server with `npm run serve`\n* set `development_overwrites` for wanted endpoints, otherwise application will use compiled files.\n\n## Database\n\nDatabase consists of three sections:\n\n- `categories` - which informs on what categories data of points is divided\n- `visible_data` - list of categories which will be visible by application users\n- `data` - actual data splitted into `categories`\n\n\n### `categories`\nFully configurable map where key is name of category and value is list of allowed types. E.g.\n* "car_elements": ["mirror", "wheel", "steering wheel"]\n* "color": ["red", "blue", "green"]\n\n### `data`\nData consists of two parts:\n* obligatory and constant\n  * `name` - name of the object\n  * `position` - coordinates of object\n* category dependent - depending on your `categories` setup it varies. See example of config below.\n\n### Examples\nYou can find examples of working configuration and database in `tests/e2e_tests` named:\n- `e2e_test_config.yml`\n- `e2e_test_data.json`\n\n## Version History\n\n### 0.1 - Initial Release - in development\n#### 0.1.5 - in development\n  * better looking frontend\n\n#### 0.1.4 - Makeover\n  * frontend for mobile version\n\n#### 0.1.3 - Simplification\n  * Simplified and standarized configuration in code\n  * Extracted project dependencies to other repositoriesq\n  * Updated dependencies\n\n#### 0.1.1 - Static frontend\n  * Using frontend served in npm  \n\n#### 0.1.0 - First working version\n * JSON and Google hosted JSON database\n * Map displays points from database\n',
    'author': 'Krzysztof Kolodzinski',
    'author_email': 'krzysztof.kolodzinski@problematy.pl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
