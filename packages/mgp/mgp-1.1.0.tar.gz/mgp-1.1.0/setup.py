# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mgp']
setup_kwargs = {
    'name': 'mgp',
    'version': '1.1.0',
    'description': "Memgraph's module for developing MAGE modules. Used only for type hinting!",
    'long_description': '# mgp\n\nPyPi package used for type hinting when creating query modules. Repository of already available query modules is called [MAGE](https://github.com/memgraph/mage).\n\n## 🎬 Get started\n \n To learn more, head over to the [docs for the query modules Python API](https://memgraph.com/docs/memgraph/reference-guide/query-modules/api/python-api). To get started with query modules, check out the [how-to guide](https://memgraph.com/docs/memgraph/how-to-guides/query-modules) on Memgraph docs. \n\n ## 🔢 Versioning\n\n - mgp v1.1 is compatible with Memgraph >= 2.4.0\n',
    'author': 'katarinasupe',
    'author_email': 'katarina.supe@memgraph.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
