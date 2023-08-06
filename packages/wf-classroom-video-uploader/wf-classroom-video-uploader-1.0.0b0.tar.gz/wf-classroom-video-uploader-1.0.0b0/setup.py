# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uploader', 'uploader.cleanup']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=4.2b1',
 'click>=7.0',
 'minio>=4.0.17',
 'pytelegraf>=0.3.3',
 'redis>=3.2.1',
 'wf-video-io>=3.0.3']

setup_kwargs = {
    'name': 'wf-classroom-video-uploader',
    'version': '1.0.0b0',
    'description': '',
    'long_description': '# TODO',
    'author': 'Paul J DeCoursey',
    'author_email': 'paul@decoursey.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
