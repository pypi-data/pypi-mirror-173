# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['schatsi', 'schatsi.models', 'schatsi.processor', 'schatsi.reader']

package_data = \
{'': ['*']}

install_requires = \
['PyMuPDF>=1.20.2,<2.0.0',
 'dask[diagnostics,distributed]>=2022.10.0,<2023.0.0',
 'loguru>=0.6.0,<0.7.0',
 'nltk>=3.7,<4.0',
 'pandas>=1.5.1,<2.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'schatsi',
    'version': '0.1.1',
    'description': '',
    'long_description': "# SCHA.T.S.I\n(GERMAN VERSION AT THE BOTTOM OF EACH CHAPTER)\n\nSCHA.T.S.I - An abbreviation for '**SCH**eduling *A*lgorithm for **T**ext **S**each **I**ntelligence'.\nThis project is located at the Chair of Service Operation at the University of Rostock. As development progresses, the software is intended to accelerate the analysis of scientific papers and publications and to provide the user with an overview of the interrelationships between papers and a prioritization of publications for the user with respect to his self-imposed specifications, even when hundreds of publications are involved.\nIn addition to the analysis, the results will be provided not only in tabular form, but additionally in a graphical overview to be able to penetrate the relationships between the papers and their authors.\nFor this purpose, techniques of text analysis, natural language processing (NLP) and machine learning (ML) are used.\n\nCurrently, SCHA.T.S.I can be used on Windows and Linux and with Release 1.3 a Beta version for MacOS accessible (No Guarrentee - Feedback is Welcome) :-)\n\n## Getting Started\n\npip install poetry\npoetry install\n\n\n\npoetry build\npoetry config pypi-token.pypi <token>\npoetry publish",
    'author': 'robnoflop',
    'author_email': 'info@robertkasseck.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/robnoflop/Schatsi',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
