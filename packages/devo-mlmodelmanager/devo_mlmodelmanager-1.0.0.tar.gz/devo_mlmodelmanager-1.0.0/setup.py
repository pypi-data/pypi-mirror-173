# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['devo_ml', 'devo_ml.modelmanager']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0', 'validators>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'devo-mlmodelmanager',
    'version': '1.0.0',
    'description': "A client for Devo's ML model manager",
    'long_description': '# python-mlmodelmanager\n\nAn easy-to-use client for Devos’s Machine Learning Model Manager.\n\nBuilt on top of the widely used Requests library, it takes advantage of all the \nfeatures it provides and exposes a simplified interface for manage models.\n\nThe main purpose of this library is to allow you to focus in the machine learning \nworkflows and not worry about the integration with Devo’s ML Model Manager.\n\n## A simple example\n\n``` python\nfrom devo_ml.modelmanager import create_client_from_token\n\nurl = "<model-manager-server-url>"\ntoken = "<valid-access-token>"\n\nclient = create_client_from_token(url, token)\n\nclient.add_model(\n   "pokemon_onnx_regression",          # model name\n   "ONNX",                             # model engine\n   "~/models/pokemon.onnx",            # model file\n   description="A funny Pokemon prediction"\n)\n```\n\n## Requirements\n\n* Python 3.7+\n\n## Install\n\n``` console\n$ pip install devo-mlmodelmanager\n```\n\n## Documentation\n\nExplore the [documentation](https://devoinc.github.io/python-mlmodelmanager-client/) to learn more.\n',
    'author': 'Devo ML Team',
    'author_email': 'machine.learning@devo.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
