# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['py_frontmatter', 'py_frontmatter.core']

package_data = \
{'': ['*']}

install_requires = \
['ruamel.yaml>=0.17.21,<0.18.0']

setup_kwargs = {
    'name': 'py-frontmatter',
    'version': '0.1.0',
    'description': 'Manipulate YAML front matter.',
    'long_description': '# py-frontmatter\nTo manipulate front matter (WIP)\n',
    'author': 'King-On Yeung',
    'author_email': 'koyeung@gmail.com',
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
