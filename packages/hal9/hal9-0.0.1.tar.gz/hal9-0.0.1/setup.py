# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['hal9']
install_requires = \
['fastapi>=0.79.0,<0.80.0', 'uvicorn[standard]>=0.18.3,<0.19.0']

setup_kwargs = {
    'name': 'hal9',
    'version': '0.0.1',
    'description': 'Design Interactive Data Apps Without Web Dev',
    'long_description': '# bussin\n\nDesign Interactive Data Apps Without Web Dev\n\n## Installation\n\n```bash\n$ pip install hal9\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`hal9` was created by Anchit Sadana, Kevin Kuo and Javier Luraschi. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`hal9` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Anchit Sadana',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
