# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['custom_plotly_templates']

package_data = \
{'': ['*']}

install_requires = \
['plotly>=5.8.0']

setup_kwargs = {
    'name': 'custom-plotly-templates',
    'version': '0.1.1',
    'description': 'Custom templates and configurations for Plotly',
    'long_description': '# Custom plotly templates\n\nCustom templates and configurations for Plotly. Developed primary for my personal use.',
    'author': 'Ruslan Mukhametshin',
    'author_email': 'rusmux21@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/rusmux/custom-plotly-templates',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
