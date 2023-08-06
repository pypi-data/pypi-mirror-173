# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zwo']

package_data = \
{'': ['*']}

install_requires = \
['parsimonious>=0.10,<0.11', 'rich>=12.6,<13.0', 'typer[rich]>=0.6,<0.7']

setup_kwargs = {
    'name': 'zwolang',
    'version': '0.1.0',
    'description': 'Python toolkit for the ZWO minilang',
    'long_description': '# ZWO\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/zwolang)](https://pypi.org/project/zwolang/)\n[![PyPI](https://img.shields.io/pypi/v/zwolang)](https://pypi.org/project/zwolang/)\n[![PyPI - License](https://img.shields.io/pypi/l/zwolang?color=magenta)](https://github.com/sco1/zwolang/blob/master/LICENSE)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sco1/zwolang/main.svg)](https://results.pre-commit.ci/latest/github/sco1/zwolang/main)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)\n[![Open in Visual Studio Code](https://img.shields.io/badge/Open%20in-VSCode.dev-blue)](https://vscode.dev/github.com/sco1/zwolang)\n\nPython toolkit for the ZWO minilang.\n\n## Installation\nInstall from PyPi with your favorite `pip` invocation:\n\n```bash\n$ pip install zwolang\n```\n\n## The ZWO File Specification\nThe primary purpose of this package is to provide a simple, human-readable format for constructing Zwift workouts that can be used to generate the actual workout XML.\n\nZWO files are parsed using a [Parsimonious](https://github.com/erikrose/parsimonious) grammar, as specified below:\n<!-- [[[cog\nfrom textwrap import dedent\nimport cog\nfrom zwo.parser import RAW_GRAMMAR\ncog.out(\n    f"```{dedent(RAW_GRAMMAR)}```"\n)\n]]] -->\n```\nworkout   = (block elws*)+ emptyline*\nblock     = tag ws "{" (((message / value) ","?) / elws)+ "}"\nvalue     = tag ws (string / range / rangeval)\n\nmessage   = "@" ws duration ws string\nrange     = rangeval ws "->" ws rangeval\nrangeval  = (duration / numeric)\n\nduration  = number ":" number\npercent   = number "%"\nnumeric   = (percent / number)\nelws      = (ws / emptyline)\n\ntag       = ~"[A-Z]+"\nstring    = ~\'"[^\\"]+"\'\nnumber    = ~"\\d+"\nws        = ~"\\s*"\nemptyline = ws+\n```\n<!-- [[[end]]] -->\n\n### Syntax & Keywords\nLike Zwift\'s built-in workout builder, the ZWO minilang is a block-based system. Blocks are specified using a `<tag> {<block contents>}` format supporting arbitrary whitespace.\n\nEach ZWO file must begin with a `META` block containing comma-separated parameters:\n\n| Keyword       | Description             | Accepted Inputs                  | Optional? |\n|---------------|-------------------------|----------------------------------|-----------|\n| `NAME`        | Displayed workout name  | `str`                            | No        |\n| `AUTHOR`      | Workout author          | `str`                            | No        |\n| `DESCRIPTION` | Workout description     | `str`                            | No        |\n| `TAGS`        | Workout tags            | String of comma separated values | Yes       |\n| `FTP`         | Rider\'s FTP<sup>1</sup> | `int`                            | Yes       |\n\n1. If specified, the rider\'s FTP is not used by Zwift directly. It is instead used to optionally normalize the workout\'s target power percentages to watts\n\nFollowing the `META` block are your workout blocks:\n\n| Keyword       | Description        |\n|---------------|--------------------|\n| `FREE`        | Free ride          |\n| `INTERVALS`   | Intervals          |\n| `RAMP`        | Ramp               |\n| `SEGMENT`     | Steady segment     |\n| `WARMUP`      | Warmup<sup>1</sup> |\n\n1. I believe Zwift considers these the same as Ramp intervals, so the ZWO package does the same\n\nWorkout blocks can contain the following comma-separated parameters:\n\n| Keyword             | Description         | Accepted Inputs             | Optional?                |\n|---------------------|---------------------|-----------------------------|--------------------------|\n| `DURATION`          | Block duration      | `MM:SS`<sup>1</sup>         | No                       |\n| `CADENCE`           | Target cadence      | `int`<sup>1</sup>           | Yes                      |\n| `COUNT`             | Number of intervals | `int`                       | Only valid for intervals |\n| `POWER`             | Target power        | `int` or `int%`<sup>1</sup> | Mostly no<sup>2</sup>    |\n| `@`                 | Display a message   | `@ MM:SS str`<sup>3</sup>   | Yes                      |\n\n1. For Interval & Ramp segments, the range syntax can be used to set values for the work/rest segments (e.g. `65% -> 120%`)\n2. Power is optional for Free segments\n3. Message timestamps are relative to their containing block\n\n\n### Sample Workout\n```\nMETA {\n    NAME "My Workout",\n    AUTHOR "Some Author",\n    DESCRIPTION "Here\'s a description!",\n    TAGS "super, sweet, workout",\n    FTP 270,\n}\nFREE {DURATION 10:00}\nINTERVALS {\n    COUNT 3,\n    DURATION 1:00 -> 0:30,\n    POWER 55% -> 78%,\n    CADENCE 85 -> 110,\n}\nSEGMENT {DURATION 2:00, POWER 65%}\nRAMP {\n    DURATION 2:00,\n    POWER 120% -> 140%,\n    @ 0:00 "Here goes the ramp!",\n    @ 1:50 "10 seconds left!",\n}\nFREE {DURATION 10:00}\n```\n',
    'author': 'sco1',
    'author_email': 'sco1.git@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sco1/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
