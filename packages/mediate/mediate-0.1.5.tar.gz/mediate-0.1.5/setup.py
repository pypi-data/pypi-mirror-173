# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mediate']

package_data = \
{'': ['*']}

install_requires = \
['roster>=0.1.11,<0.2.0', 'typing-extensions>=4.4.0,<5.0.0']

setup_kwargs = {
    'name': 'mediate',
    'version': '0.1.5',
    'description': 'Middleware for every occasion',
    'long_description': "# mediate\nMiddleware for every occasion\n\n## Installation\n```console\npip install mediate\n```\n\n## Usage\n```python\nimport mediate\n\nmiddleware = mediate.Middleware()\n\n@middleware\ndef shout(call_next, name):\n    return call_next(name.upper())\n\n@middleware\ndef exclaim(call_next, name):\n    return call_next(name + '!')\n\n@middleware.bind\ndef hello(name):\n    print(f'Hello, {name}')\n```\n\n```python\n>>> hello('sam')\nHello, SAM!\n```\n",
    'author': 'Tom Bulled',
    'author_email': '26026015+tombulled@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tombulled/middleware',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
