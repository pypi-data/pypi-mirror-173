# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['checkjpy2hkd']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0', 'tomli>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['checkjpy2hkd = checkjpy2hkd.__main__:main']}

setup_kwargs = {
    'name': 'checkjpy2hkd',
    'version': '0.1.0',
    'description': 'Check the latest JPY to HKD exchange rates',
    'long_description': '# checkjpy2hkd\nCheck the latest JPY to HKD exchange rates\n\n## Installation\nYou can install the JPY to HKD Exchange Rate Checker from [PyPI](https://pypi.org/project/checkjpy2hkd/):\n\n    python -m pip install checkjpy2hkd\n\n## How to use\nThe JPY to HKD Exchange Rate Checker is a command line application, named `checkjpy2hkd`.\n\nYou can also call the JPY to HKD Exchange Rate Checker in your own Python code, by importing from the `reader` package:\n\n    >>> from checkjpy2hkd import xxx\n    >>> xxx()',
    'author': 'Alex Cheng',
    'author_email': 'alex28.biz@gmail.com',
    'maintainer': 'Alex Cheng',
    'maintainer_email': 'alex28.biz@gmail.com',
    'url': 'https://github.com/alexcheng628/checkjpy2hkd',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
