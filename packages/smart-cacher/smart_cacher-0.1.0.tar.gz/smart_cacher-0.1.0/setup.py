# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['smart_cacher']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-storage>=2.5.0,<3.0.0']

setup_kwargs = {
    'name': 'smart-cacher',
    'version': '0.1.0',
    'description': '',
    'long_description': '# cloud-cache\nSet of caches using various cloud providers\n',
    'author': 'Sahand Johansen',
    'author_email': 'sahand.johansen@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
