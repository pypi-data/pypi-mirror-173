# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flakow1stprojectdef']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'flakow1stprojectdef',
    'version': '0.1.0',
    'description': 'primeiro projetao caraio',
    'long_description': '# package_name\n\nDescription. \nThe package package_name is used to:\n\t- \n\t-\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install package_name\n\n```bash\npip install package_name\n```\n\n## Usage\n\n```python\nfrom package_name.module1_name import file1_name\nfile1_name.my_function()\n```\n\n## Author\nAntonio carlos\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)',
    'author': 'flakow',
    'author_email': 'tonyimportsmg@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
