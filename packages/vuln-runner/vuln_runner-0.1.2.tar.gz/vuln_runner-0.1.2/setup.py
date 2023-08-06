# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docker_vuln_runner']

package_data = \
{'': ['*']}

install_requires = \
['gitpython>=3.1.29,<4.0.0',
 'python-on-whales>=0.53.0,<0.54.0',
 'pyyaml>=6.0,<7.0',
 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['vuln-runner = docker_vuln_runner.main:app']}

setup_kwargs = {
    'name': 'vuln-runner',
    'version': '0.1.2',
    'description': 'A Docker runner for docker-based vulnerable environments.',
    'long_description': '<h1 align="center">\n  <br>\n    <img src="https://raw.githubusercontent.com/cybersecsi/docker-vuln-runner/main/logo.png" alt= "Docker Vuln Runner" width="300px">\n</h1>\n<p align="center">\n    <b>Docker Vuln Runner</b> <br />\n    A Docker runner for docker-based vulnerable environments. \n<p>\n<p align="center">\n  <a href="https://github.com/cybersecsi/docker-vuln-runner/blob/main/README.md"><img src="https://img.shields.io/badge/Documentation-complete-green.svg?style=flat"></a>\n  <a href="https://github.com/cybersecsi/docker-vuln-runner/blob/main/LICENSE.md"><img src="https://img.shields.io/badge/License-GNU%20GPL-blue"></a>\n</p>\n\n## Table of Contents\n- [Overview](#overview)\n- [Install](#install)\n- [Usage](#usage)\n- [Demo](#demo)\n- [Development](#development)\n- [Credits](#credits)\n- [License](#license)\n\n## Overview\n``vuln-runner``  is a tool that allows you to quickly run the docker vulnerable stacks. \n\nThe vulnerable stack actually supported are: \n* [vulhub repo](https://github.com/vulhub/vulhub)\n\nAt [SecSI](https://secsi.io) we found it useful to reproduce vulnerable environments for training purposes. To reproduce vulnerable environment easily, take a look at [DSP](https://secsi.io/docker-security-playground/).\n\n## Install\nYou can easily install it by running:\n```\npip install vuln-runner\n```\n\n## Usage\n```\nvuln-runner --help\n```\n\nThis will display help for the tool. Here are all the switches it supports.\n\n```\nUsage: vuln-runner [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  down              Down a list of vulnerable projects\n  down-env          Down an environment\n  generate-vulnenv  Generate <no_env> vulnerable environments composed of...\n  init\n  list              List the vulnerable names\n  run               Run a list of vulnerable projects\n  run-env           Run an environment taken from a JSON configuration file\n  update            Update the vulnerable git repositories\n\n```\n\n* **Initialized the vulnerable environment:**  \n```\nvuln-runner init\n```\n\n[![asciicast](https://asciinema.org/a/nYJEd62OzL3WLUuigyjeChLIE.svg)](https://asciinema.org/a/nYJEd62OzL3WLUuigyjeChLIE)\n\n\n* **List the vulnerable stacks:**\n```\nvuln-runner list\n```  \n\n\n[![asciicast](https://asciinema.org/a/raziKJLlR6vWSbiIwY1w8kqaq.svg)](https://asciinema.org/a/raziKJLlR6vWSbiIwY1w8kqaq)  \n\n* **Run a list of vulnerable stacks:**\n\n```\nvuln-runner run vulhub.CVE-2014-3120,vulhub.CVE-2018-1270\n```\n\n[![asciicast](https://asciinema.org/a/wIOCYSrD9o5ZE6NmuCWLTTD8A.svg)](https://asciinema.org/a/wIOCYSrD9o5ZE6NmuCWLTTD8A)  \n\n\n* **Down the list of vulnerable stacks:**\n```\nvuln-runner down vulhub.CVE-2014-3120,vulhub.CVE-2018-1270\n```\n\n[![asciicast](https://asciinema.org/a/fAuTCMJHdxa5sRK0VlbfAKqcV.svg)](https://asciinema.org/a/fAuTCMJHdxa5sRK0VlbfAKqcV)  \n\n### Advanced usage: vulnerable environment  \nWith the previous commands you can already manage your vulnerable stacks and manually run and stop them. \nAnyway, you can also create *vulnerable environments*. \nA vulnerable environment is a set of vulnerable docker-compose stacks that has not ports\' conflicts.   \nYou can generate a vulnerable environment descriptor in JSON format with the `generate-vulnenv` command:   \n``` \nvuln-runner generate-vulnenv NO_VULNS [--no-env=<default=1>]\n```  \n\n* `NO_VULNS` defines the number of vulnerable stacks for each environment. \n* `--no-env` defines the number of environments. It is useful if you want to run vuln-runner in different hosts, where each host runs a single environment.   \n\nFor example, to create a JSON vulnerable descriptor with two vulnerable stack and two environments: \n```\nvuln-runner generate-vulnenv 2 --no-env=2  \n```\n\n[![asciicast](https://asciinema.org/a/KxRWBVOMLymUQiWgjDDm4f6JS.svg)](https://asciinema.org/a/KxRWBVOMLymUQiWgjDDm4f6JS)   \n\nYou can output into the JSON descriptor into a file an reuse with two commands: \n* **run-env**: run the set of stacks belonging to a vulnerable environment.   \n```\nvuln-runner run-env output.json 1\n```\n[![asciicast](https://asciinema.org/a/vuL2l5vL8bqRefx9EAqYlqxFC.svg)](https://asciinema.org/a/vuL2l5vL8bqRefx9EAqYlqxFC)\n\n* **down-env**: down the vulnerable environment.  \n\n```\nvuln-runner down-env output.json 1\n```\n[![asciicast](https://asciinema.org/a/fAuTCMJHdxa5sRK0VlbfAKqcV.svg)](https://asciinema.org/a/fAuTCMJHdxa5sRK0VlbfAKqcV)  \n\n\n## Development  \nThe [poetry](https://python-poetry.org/) packaging and management tool was used to build the project.  \nTo initialize the project: \n```\npoetry install \n```  \n\nTo run the several commands, you can use poetry as follows:  \n\n``` \npoetry run vuln-runner <command>  \n```\n\n\n\n## Credits\nDeveloped by gx1 [@SecSI](https://secsi.io)\n\n## License\n*Docker Vuln Runner* is released under the [GPL LICENSE](https://github.com/cybersecsi/docker-vuln-runner/blob/main/LICENSE.md)\n',
    'author': 'SecSI',
    'author_email': 'dev@secsi.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
