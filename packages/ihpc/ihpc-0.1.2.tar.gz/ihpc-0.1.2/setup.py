# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hpc',
 'hpc.base',
 'hpc.compat',
 'hpc.impl',
 'hpc.mngr',
 'hpc.mngr.lsf',
 'hpc.mngr.lsf.extra']

package_data = \
{'': ['*']}

install_requires = \
['paramiko>=2.11.0,<3.0.0']

extras_require = \
{'full': ['typing-extensions>=4.3.0,<5.0.0'],
 'type': ['typing-extensions>=4.3.0,<5.0.0']}

setup_kwargs = {
    'name': 'ihpc',
    'version': '0.1.2',
    'description': 'Python Interface for Scheduling HPC Jobs',
    'long_description': '<!-- Template from https://github.com/othneildrew/Best-README-Template -->\n<div id="top"></div>\n\n\n\n<!-- PROJECT LOGO -->\n<br />\n<div align="center">\n  <a href="https://github.com/iydon/hpc">\n    🔵⬜⬜⬜🟦<br />\n    🟦🟦⬜🟦🟦<br />\n    🟦⬜🟦⬜🟦<br />\n    🟦🟦⬜🟦🟦<br />\n    🟦⬜⬜⬜🟦<br />\n  </a>\n\n  <h3 align="center">iHPC</h3>\n\n  <p align="center">\n    Python Interface for Scheduling HPC Jobs\n    <br />\n    <a href="https://ihpc.readthedocs.io"><strong>Explore the docs »</strong></a>\n    <br />\n    <br />\n    <a href="https://github.com/iydon/hpc">View Demo</a>\n    ·\n    <a href="https://github.com/iydon/hpc/issues">Report Bug</a>\n    ·\n    <a href="https://github.com/iydon/hpc/issues">Request Feature</a>\n  </p>\n</div>\n',
    'author': 'Iydon Liang',
    'author_email': 'liangiydon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/iydon/hpc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
