# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xbmini']

package_data = \
{'': ['*']}

install_requires = \
['dash-bootstrap-components>=1.2,<2.0',
 'dash>=2.6,<3.0',
 'kaleido>=0.2,<0.3,!=0.2.1.post1',
 'pandas>=1.5,<2.0',
 'plotly>=5.10,<6.0',
 'sco1-misc>=0.1,<0.2',
 'typer[rich]>=0.6,<0.7']

entry_points = \
{'console_scripts': ['xbmini = xbmini.cli:xbmini_cli']}

setup_kwargs = {
    'name': 'xbmini-py',
    'version': '0.2.0',
    'description': 'Python Toolkit for the GCDC HAM',
    'long_description': '# xbmini-py\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/xbmini-py)](https://pypi.org/project/xbmini-pyxbmini-py/)\n[![PyPI](https://img.shields.io/pypi/v/xbmini-py)](https://pypi.org/project/xbmini-py/)\n[![PyPI - License](https://img.shields.io/pypi/l/xbmini-py?color=magenta)](https://github.com/sco1/xbmini-py/blob/master/LICENSE)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sco1/xbmini-py/main.svg)](https://results.pre-commit.ci/latest/github/sco1/xbmini-py/main)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)\n[![Open in Visual Studio Code](https://img.shields.io/badge/Open%20in-VSCode.dev-blue)](https://vscode.dev/github.com/sco1/xbmini-py)\n\nPython Toolkit for the [GCDC HAM](http://www.gcdataconcepts.com/ham.html)\n\n## Known Firmware Compatibility\nThis package is currently tested against firmware versions `1379` and `2108`, compatibility with other firmware versions is not guaranteed.\n\n## Installation\nInstall from PyPi with your favorite `pip` invocation:\n\n```bash\n$ pip install xbmini-py\n```\n\nYou can confirm proper installation via the `xbmini` CLI:\n<!-- [[[cog\nimport cog\nfrom subprocess import PIPE, run\nout = run(["xbmini", "--help"], stdout=PIPE, encoding="ascii")\ncog.out(\n    f"```\\n$ xbmini --help\\n{out.stdout.rstrip()}\\n```"\n)\n]]] -->\n```\n$ xbmini --help\n                                                                               \n Usage: xbmini [OPTIONS] COMMAND [ARGS]...                                     \n                                                                               \n+- Options -------------------------------------------------------------------+\n| --help          Show this message and exit.                                 |\n+-----------------------------------------------------------------------------+\n+- Commands ------------------------------------------------------------------+\n| batch-combine  Batch combine XBM files for each logger and dump a           |\n|                serialized `XBMLog` instance to CSV.                         |\n| dash           Dash UI launchers                                            |\n+-----------------------------------------------------------------------------+\n```\n<!-- [[[end]]] -->\n\n## Usage\n### `xbmini batch-combine`\nBatch combine XBM files for each logger and dump a serialized `XBMLog` instance to a CSV in its respective logger\'s directory.\n#### Input Parameters\n| Parameter       | Description                                            | Type         | Default                                |\n|-----------------|--------------------------------------------------------|--------------|----------------------------------------|\n| `--top-dir`     | Path to top-level log directory to search.<sup>1</sup> | `Path\\|None` | GUI Prompt                             |\n| `--log-pattern` | XBMini log file glob pattern.<sup>2</sup>              | `str`        | `"*.CSV"`                              |\n| `--dry-run`     | Show processing pipeline without processing any files. | `bool`       | `False`                                |\n| `--skip-strs`   | Skip files containing any of the provided substrings.  | `list[str]`  | `["processed", "trimmed", "combined"]` |\n\n1. Log searching will be executed recursively starting from the top directory\n2. Case sensitivity is deferred to the host OS\n\n### `xbmini dash`\nA series of helper UIs are provided by [Dash](https://dash.plotly.com/). Running the CLI commands will start a local server for the user to interact with.\n\n**WARNING:** These apps are intended for use on a development server only. Do not use them in a production environment.\n\nA list of available UIs can be accessed via the command line:\n<!-- [[[cog\nimport cog\nfrom subprocess import PIPE, run\nout = run(["xbmini", "dash", "--help"], stdout=PIPE, encoding="ascii")\ncog.out(\n    f"```\\n$ xbmini dash --help\\n{out.stdout.rstrip()}\\n```"\n)\n]]] -->\n```\n$ xbmini dash --help\n                                                                               \n Usage: xbmini dash [OPTIONS] COMMAND [ARGS]...                                \n                                                                               \n Dash UI launchers                                                             \n                                                                               \n+- Options -------------------------------------------------------------------+\n| --help          Show this message and exit.                                 |\n+-----------------------------------------------------------------------------+\n+- Commands ------------------------------------------------------------------+\n| trim     Helper UI for trimming serialized XBMLog CSVs.                     |\n+-----------------------------------------------------------------------------+\n```\n<!-- [[[end]]] -->\n',
    'author': 'sco1',
    'author_email': 'sco1.git@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sco1/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
