# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['metrics_render']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.25.3,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'flask>=2.2.2,<3.0.0',
 'kaleido==0.2.1',
 'minio>=7.1.12,<8.0.0',
 'plotly>=5.10.0,<6.0.0',
 'prometheus-client>=0.15.0,<0.16.0',
 'promqlpy>=1.0.5,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'waitress>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'metrics-render',
    'version': '0.1.4',
    'description': '',
    'long_description': '# metrics-render\nHTTP service that rendering promql into image, support alerting rules expression\n',
    'author': 'laixintao',
    'author_email': 'laixintaoo@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
