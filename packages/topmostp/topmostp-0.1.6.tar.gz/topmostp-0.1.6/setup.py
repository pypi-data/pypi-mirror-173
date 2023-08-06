# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['topmostp']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0', 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['topmostp = topmostp.main:app']}

setup_kwargs = {
    'name': 'topmostp',
    'version': '0.1.6',
    'description': 'A simple CLI tool to retrieve the N top most used ports',
    'long_description': '<h1 align="center">\n  <br>\n    <img src="https://raw.githubusercontent.com/cybersecsi/topmostp/main/logo.png" alt= "topmostp" width="300px">\n</h1>\n<p align="center">\n    <b>topmostp</b>\n<p>\n\n<p align="center">\n  <a href="https://github.com/cybersecsi/topmostp/blob/main/README.md"><img src="https://img.shields.io/badge/Documentation-complete-green.svg?style=flat"></a>\n  <a href="https://github.com/cybersecsi/topmostp/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg"></a>\n</p>\n\n## Table of Contents\n- [Overview](#overview)\n- [Install](#install)\n- [Usage](#usage)\n- [Demo](#demo)\n- [Credits](#credits)\n- [License](#license)\n\n## Overview\n``topmostp`` (**Topmost P**orts) is a tool that allows you to quickly retrieve the **most used ports**. The source of the ranking is the ``nmap-services`` in the [nmap repo](https://raw.githubusercontent.com/nmap/nmap/master/nmap-services).\n\nAt [SecSI](https://secsi.io) we found it useful to get this information to use it in a **pipeline of scripts**.\n\n## Install\nYou can easily install it by running:\n```\npip install topmostp\n```\n\n## Usage\n```\ntopmostp --help\n```\n\nThis will display help for the tool. Here are all the switches it supports.\n\n```\n Usage: topmostp [OPTIONS] COMMAND [ARGS]...                                      \n                                                                                  \n╭─ Options ──────────────────────────────────────────────────────────────────────╮\n│ --help       Show this message and exit.                                       │\n╰────────────────────────────────────────────────────────────────────────────────╯\n╭─ Commands ─────────────────────────────────────────────────────────────────────╮\n│ all         Retrieve list of all ports (both TCP, UDP and SCTP) by frequency   │\n│ find        Find info about about a specific service                           │\n│ sctp        Retrieve list of SCTP ports by frequency                           │\n│ stats       Retrieve stats about a port                                        │\n│ tcp         Retrieve list of TCP ports by frequency                            │\n│ udp         Retrieve list of UDP ports by frequency                            │\n│ update      Update ports list                                                  │\n╰────────────────────────────────────────────────────────────────────────────────╯\n```\n\nA pratical example is the following:\n```\nnaabu -p $(topmostp all 15 --silent) -host secsi.io\n```\n\nIn this snippet the output of ``topmostp`` is used to retrieve the list of the top 10 ports and it is chained with the ``naabu`` port scanning tool.\n\n\n## Demo\n[![demo](https://asciinema.org/a/531844.svg)](https://asciinema.org/a/531844?autoplay=1)\n\n## Credits\nDeveloped by Angelo Delicato [@SecSI](https://secsi.io)\n\n## License\n*topmostp* is released under the [MIT LICENSE](https://github.com/cybersecsi/topmostp/blob/main/LICENSE.md)',
    'author': 'SecSI',
    'author_email': 'dev@secsi.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/cybersecsi/topmostp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
