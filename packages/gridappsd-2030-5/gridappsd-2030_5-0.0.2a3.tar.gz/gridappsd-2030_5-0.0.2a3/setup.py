# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ieee_2030_5',
 'ieee_2030_5.client',
 'ieee_2030_5.data',
 'ieee_2030_5.models',
 'ieee_2030_5.persistance',
 'ieee_2030_5.server',
 'ieee_2030_5.simulation',
 'ieee_2030_5.types_',
 'ieee_2030_5.utils']

package_data = \
{'': ['*']}

install_requires = \
['Flask-Sessions>=0.1.5,<0.2.0',
 'Flask>=2.0.3,<3.0.0',
 'cryptography>=37.0.2,<38.0.0',
 'dataclasses-json>=0.5.7,<0.6.0',
 'gevent>=21.12.0,<22.0.0',
 'grequests>=0.6.0,<0.7.0',
 'gunicorn>=20.1.0,<21.0.0',
 'pickleDB>=0.9.2,<0.10.0',
 'pvlib>=0.9.0,<0.10.0',
 'pyOpenSSL>=22.0.0,<23.0.0',
 'simplekv>=0.14.1,<0.15.0',
 'trio>=0.21.0,<0.22.0',
 'tzlocal>=4.2,<5.0',
 'xsdata[cli]>=22.3,<23.0']

entry_points = \
{'console_scripts': ['2030_5_cert = ieee_2030_5.certs:_main',
                     '2030_5_proxy = ieee_2030_5.basic_proxy:_main',
                     '2030_5_server = ieee_2030_5.__main__:_main',
                     '2030_5_shutdown = ieee_2030_5.__main__:_shutdown']}

setup_kwargs = {
    'name': 'gridappsd-2030-5',
    'version': '0.0.2a3',
    'description': '',
    'long_description': 'None',
    'author': 'C. Allwardt',
    'author_email': '3979063+craig8@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
