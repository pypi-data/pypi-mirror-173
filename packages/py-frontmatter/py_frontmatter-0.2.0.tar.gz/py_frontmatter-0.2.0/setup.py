# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['py_frontmatter',
 'py_frontmatter.console',
 'py_frontmatter.console.commands',
 'py_frontmatter.core']

package_data = \
{'': ['*']}

install_requires = \
['ruamel.yaml>=0.17.21,<0.18.0']

entry_points = \
{'console_scripts': ['frontmatter = py_frontmatter.console.application:main']}

setup_kwargs = {
    'name': 'py-frontmatter',
    'version': '0.2.0',
    'description': 'Manipulate YAML front matter.',
    'long_description': '# py-frontmatter\nTo manipulate front matter in document file.\n\n## Installation\n\n```shell\npip install py-frontmatter\n```\n\n## Usage\n\n```\n% cat note.md \n---\ntitle: Hacker\'s note\ntags: [a, b]\n---\n# header\ntext\n```\n\nTo retrieve front matter as JSON:\n```\n% frontmatter get note.md | jq\n{\n  "title": "Hacker\'s note",\n  "tags": [\n    "a",\n    "b"\n  ]\n}\n```\n\nTo replace the front matter:\n```\n% echo \'{"title": "My note", "tags": ["a", "b", "c"]}\' | frontmatter set note.md \n% cat ~/today/note.md \n---\ntitle: My note\ntags:\n- a\n- b\n- c\n---\n# header\ntext\n```\n',
    'author': 'YEUNG King On',
    'author_email': 'koyeung@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
