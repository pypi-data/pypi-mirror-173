# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neuronest',
 'neuronest.core',
 'neuronest.core.google',
 'neuronest.core.schemas',
 'neuronest.core.schemas.bigquery',
 'neuronest.core.schemas.training_metrics',
 'neuronest.core.serialization',
 'neuronest.core.services']

package_data = \
{'': ['*']}

install_requires = \
['ffmpeg-python>=0.2.0,<0.3.0',
 'google-cloud-aiplatform>=1.18.2,<2.0.0',
 'google-cloud-bigquery>=2.34.4,<3.0.0',
 'google-cloud-storage>=2.5.0,<3.0.0',
 'librosa>=0.9.2,<0.10.0',
 'moviepy>=1.0.3,<2.0.0',
 'numpy>=1.23.3,<2.0.0',
 'opencv-contrib-python==4.5.5.64',
 'opencv-python-headless==4.5.5.64',
 'opencv-python==4.5.5.64',
 'pandas>=1.5.0,<2.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'neuronest',
    'version': '0.1.12',
    'description': 'Neuronest core project',
    'long_description': 'None',
    'author': 'Côme Arvis',
    'author_email': 'come.arvis@neuronest.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
