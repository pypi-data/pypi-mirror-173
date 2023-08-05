# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['code_commenter']

package_data = \
{'': ['*']}

install_requires = \
['pyperclip>=1.8.2,<2.0.0']

entry_points = \
{'console_scripts': ['generate-comment = code_commenter.cli:run_cli']}

setup_kwargs = {
    'name': 'code-commenter',
    'version': '0.0.1',
    'description': 'Lightweight tool to generate decorative code comments to enhance readability',
    'long_description': '# Code Commenter\nGenerate stylized code comment headers to help make your code more readable\n\n## Basic Usage\nTo print a comment header to the console run\n```bash\ngenerate-comment -t My_Script_Heading\n```\nand if you wish to have it copied to your clipboard, add the `-c` flag\n```bash\ngenerate-comment -t My_Script_Heading -c\n```\nCode commenter supports multiple language comments. The default is Python but if you wish to generate a comment for example, Golang, set the `-lang` flag.\n```bash\ngenerate-comment -t My_Script_Heading -lang GO\n```\n',
    'author': 'Tristan Naidoo',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
