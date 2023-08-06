# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['podping_schemas',
 'podping_schemas.org',
 'podping_schemas.org.podcastindex',
 'podping_schemas.org.podcastindex.podping',
 'podping_schemas.org.podcastindex.podping.hivewriter']

package_data = \
{'': ['*']}

install_requires = \
['capnpy>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'podping-schemas',
    'version': '0.1.0a7',
    'description': '',
    'long_description': '# podping-schemas-python',
    'author': 'Alecks Gates',
    'author_email': 'alecks@podping.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
