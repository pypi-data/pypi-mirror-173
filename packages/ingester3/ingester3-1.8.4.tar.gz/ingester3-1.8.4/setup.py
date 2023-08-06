# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ingester3']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=36.0,<37.0',
 'diskcache>=5.0.0,<6.0.0',
 'levenshtein>=0.20,<0.21',
 'numpy>=1.20,<2.0',
 'pandas>=1.2.3,<2.0.0',
 'psycopg2>=2.8.1,<3.0.0',
 'python-dotenv>=0.18,<0.19',
 'sqlalchemy>=1.3,<2.0']

setup_kwargs = {
    'name': 'ingester3',
    'version': '1.8.4',
    'description': 'Data ingester for ViEWS3.',
    'long_description': '# Ingester3\n\nIngester3 is the Pandas extension-based system for ingesting data in the ViEWS3 system.\n\n',
    'author': 'Mihai Croicu',
    'author_email': 'mihai.croicu@pcr.uu.se',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/UppsalaConflictDataProgram/ingester3>',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
