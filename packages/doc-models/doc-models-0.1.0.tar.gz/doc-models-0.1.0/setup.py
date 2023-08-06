# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['doc_models',
 'doc_models.classification',
 'doc_models.clustering',
 'doc_models.components',
 'doc_models.images',
 'doc_models.ocr',
 'doc_models.visualization',
 'doc_models.visualization.impl',
 'doc_models.visualization.tools']

package_data = \
{'': ['*']}

install_requires = \
['Unidecode>=1.3.6,<2.0.0',
 'opencv-python>=4.6.0,<5.0.0',
 'pandas>=1.5.1,<2.0.0',
 'pdf2image>=1.16.0,<2.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'pytesseract>=0.3.10,<0.4.0',
 'python-poppler>=0.3.0,<0.4.0',
 'ready-logger>=0.1.5,<0.2.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'doc-models',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Dan Kelleher',
    'author_email': 'kelleherjdan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
