# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['microscopemetrics',
 'microscopemetrics.analysis',
 'microscopemetrics.devices',
 'microscopemetrics.model',
 'microscopemetrics.samples',
 'microscopemetrics.utilities']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.1.5,<2.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'scikit-image>=0.19.3,<0.20.0',
 'scipy>=1.5.4,<2.0.0']

setup_kwargs = {
    'name': 'microscopemetrics',
    'version': '0.1.0',
    'description': 'A package providing analysis routines to measure the performance of micrsocopes used in biomedical research',
    'long_description': '# OMERO.metrics\nA python library to run micrsocope metrology\n\nTry it here [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/juliomateoslangerak/microscope-metrics/HEAD)\n',
    'author': 'Julio Mateos Langerak',
    'author_email': 'julio.matoes-langerak@igh.cnrs.fr',
    'maintainer': 'Julio Mateos Langerak',
    'maintainer_email': 'julio.matoes-langerak@igh.cnrs.fr',
    'url': 'https://github.com/MontpellierRessourcesImagerie/microscope-metrics',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
