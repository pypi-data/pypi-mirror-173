# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_allure_intersection']

package_data = \
{'': ['*']}

install_requires = \
['allure-pytest<=2.8.22', 'pytest<5']

entry_points = \
{'pytest11': ['allure_intersection = pytest_allure_intersection']}

setup_kwargs = {
    'name': 'pytest-allure-intersection',
    'version': '1.0.0',
    'description': '',
    'long_description': '<p align="center">\n  <img src="https://www.dropbox.com/s/yvztjxtcbtw6t6v/pytest-allure-intersection-logo.svg?raw=1" />\n</p>\n<p align="center" style="font-size:30px;font-weight:bolder;font-family:monospace;font-style:italic">pytest-allure-intersection</p>\n\n## Installation\n\n```bash\n> pip install pytest-allure-intersection\n```\n\n## Usage\n\nThis pytest plugin modifies the selection behavior of Allure selection options.\n\nIf you run:\n\n```bash\n> pytest --allure-epics=MyGreatEpic --allure-features=MyGreatFeature\n```\n\nBy default, this command would select all tests that are decorated *either* with `@allure.epic("MyGreatEpic")` or `@allure.feature("MyGreatFeature")`, *i.e.* the selection is based on the *union* of the flags.\n\nAfter installing the *pytest-allure-intersection* plugin, tests can be selected based on whether they match *both* criteria, *i.e.* a test is selected if its Allure decorators are a superset of the flags requested on the CLI.\n\nYou can enable that behavior by passing `--allure-selection-by-intersection`, otherwise the default behavior will not be affected in any way.\n\n## Contributing\n\n*pytest-allure-intersection* uses Poetry for its development. To run tests, use:\n\n```bash\n> poetry run tox\n```',
    'author': 'Jean Cruypenynck',
    'author_email': 'filaton@me.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
