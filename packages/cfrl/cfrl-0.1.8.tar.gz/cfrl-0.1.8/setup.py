# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cfrl',
 'cfrl.agents',
 'cfrl.experiments',
 'cfrl.nn',
 'cfrl.optimizers',
 'cfrl.policies',
 'cfrl.utils',
 'cfrl.wrappers']

package_data = \
{'': ['*']}

install_requires = \
['gym[classic_control]==0.23.1',
 'numpy>=1.23.3,<2.0.0',
 'packaging>=21.3,<22.0',
 'stable-baselines3==1.2.0',
 'tensorboard>=2.10.1,<3.0.0',
 'torch>=1.12.1,<2.0.0',
 'wandb>=0.13.3,<0.14.0']

setup_kwargs = {
    'name': 'cfrl',
    'version': '0.1.8',
    'description': '',
    'long_description': '# cfrl\n\nCFRL is a Python library for reinforcement learning.\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install cfrl.\n\n```bash\npip install cfrl\n```\n\n## Usage\n\n```python\nimport cfrl\n```\n\n## Contributing\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Chufan Chen',
    'author_email': 'chenchufan@zju.edu.cn',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
