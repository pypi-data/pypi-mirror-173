# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyntc',
 'pyntc.devices',
 'pyntc.devices.system_features',
 'pyntc.devices.system_features.vlans',
 'pyntc.devices.tables',
 'pyntc.devices.tables.jnpr',
 'pyntc.utils',
 'pyntc.utils.templates']

package_data = \
{'': ['*']}

install_requires = \
['f5-sdk>=3.0.21,<4.0.0',
 'importlib-metadata==4.13.0',
 'junos-eznc>=2.6,<3.0',
 'netmiko>=4.0,<5.0',
 'pyeapi>=0.8.4,<0.9.0',
 'pynxos>=0.0.5,<0.0.6',
 'requests>=2.28,<3.0',
 'scp>=0.14,<0.15']

entry_points = \
{'console_scripts': ['pyntc = pyntc.cli:main']}

setup_kwargs = {
    'name': 'pyntc',
    'version': '0.20.3',
    'description': 'SDK to simplify common workflows for Network Devices.',
    'long_description': '# Pyntc\n\n<p align="center">\n  <img src="https://raw.githubusercontent.com/networktocode/pyntc/develop/docs/images/pyntc_logo.png" class="logo" height="200px">\n  <br>\n  <a href="https://github.com/networktocode/pyntc/actions"><img src="https://github.com/networktocode/pyntc/actions/workflows/ci.yml/badge.svg?branch=main"></a>\n  <a href="https://pyntc.readthedocs.io/en/latest"><img src="https://readthedocs.org/projects/pyntc/badge/"></a>\n  <a href="https://pypi.org/project/pyntc/"><img src="https://img.shields.io/pypi/v/pyntc"></a>\n  <a href="https://pypi.org/project/pyntc/"><img src="https://img.shields.io/pypi/dm/pyntc"></a>\n  <br>\n</p>\n\n## Overview\n\nA Python library that is a SDK to simplify common workflows for Network Devices.\n\n## Documentation\n\nFull web-based HTML documentation for this library can be found over on the [Pyntc Docs](https://pyntc.readthedocs.io) website:\n\n- [User Guide](https://pyntc.readthedocs.io/en/latest/user/lib_overview/) - Overview, Using the library, Getting Started.\n- [Administrator Guide](https://pyntc.readthedocs.io/en/latest/admin/install/) - How to Install, Configure, Upgrade, or Uninstall the library.\n- [Developer Guide](https://pyntc.readthedocs.io/en/latest/dev/contributing/) - Extending the library, Code Reference, Contribution Guide.\n- [Release Notes / Changelog](https://pyntc.readthedocs.io/en/latest/admin/release_notes/).\n- [Frequently Asked Questions](https://pyntc.readthedocs.io/en/latest/user/faq/).\n\n### Contributing to the Docs\n\nAll the Markdown source for the library documentation can be found under the [docs](https://github.com/networktocode/pyntc/tree/develop/docs) folder in this repository. For simple edits, a Markdown capable editor is sufficient - clone the repository and edit away.\n\nIf you need to view the fully generated documentation site, you can build it with [mkdocs](https://www.mkdocs.org/). A container hosting the docs will be started using the invoke commands (details in the [Development Environment Guide](https://pyntc.readthedocs.io/en/latest/dev/dev_environment/#docker-development-environment)) on [http://localhost:8001](http://localhost:8001). As your changes are saved, the live docs will be automatically reloaded.\n\nAny PRs with fixes or improvements are very welcome!\n\n## Questions\n\nFor any questions or comments, please check the [FAQ](https://pyntc.readthedocs.io/en/latest/user/faq/) first. Feel free to also swing by the [Network to Code Slack](https://networktocode.slack.com/) (channel `#networktocode`), sign up [here](http://slack.networktocode.com/) if you don\'t have an account.\n',
    'author': 'Network to Code, LLC',
    'author_email': 'info@networktocode.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pyntc.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
