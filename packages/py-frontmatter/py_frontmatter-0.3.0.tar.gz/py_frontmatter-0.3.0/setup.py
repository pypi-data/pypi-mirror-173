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
['jsonpath-ng>=1.5.3,<2.0.0', 'ruamel.yaml>=0.17.21,<0.18.0']

entry_points = \
{'console_scripts': ['frontmatter = py_frontmatter.console.application:main']}

setup_kwargs = {
    'name': 'py-frontmatter',
    'version': '0.3.0',
    'description': 'Manipulate YAML front matter.',
    'long_description': '# py-frontmatter\nTo manipulate front matter in document file.\n\n## Installation\n\n```shell\npip install py-frontmatter\n```\n\n## Usage\n\nGiven text file:\n```markdown\n---\ntitle: Hacker\'s note\ntags: [a, b]\n---\n# header\ntext\n```\n\n### Get or set whole section of front matter\n\nTo retrieve front matter as JSON:\n```commandline\n% frontmatter get note.md | jq\n{\n  "title": "Hacker\'s note",\n  "tags": [\n    "a",\n    "b"\n  ]\n}\n```\n\nTo replace the front matter:\n```commandline\n% echo \'{"title": "My note", "tags": ["a", "b", "c"]}\' | frontmatter set note.md \n% cat note.md \n---\ntitle: My note\ntags:\n- a\n- b\n- c\n---\n# header\ntext\n```\n\n### Add or remove item from front matter\n\n```commandline\n% frontmatter add-item --jsonpath \'$.tags\' --item d note.md\n% cat note.md \n---\ntitle: My note\ntags:\n- a\n- b\n- c\n- d\n---\n# header\ntext\n%\n% frontmatter remove-item --jsonpath \'$.tags\' --item d note.md\n% cat note.md                                                 \n---\ntitle: My note\ntags:\n- a\n- b\n- c\n---\n# header\ntext\n```\n\n### Specialize commands to add/remove tag\n\n```commandline\n% frontmatter add-tag --tag d note.md\n% cat note.md \n---\ntitle: My note\ntags:\n- a\n- b\n- c\n- d\n---\n# header\ntext\n% frontmatter remove-tag --tag d note.md\n% cat note.md                           \n---\ntitle: My note\ntags:\n- a\n- b\n- c\n---\n# header\ntext\n```\n',
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
