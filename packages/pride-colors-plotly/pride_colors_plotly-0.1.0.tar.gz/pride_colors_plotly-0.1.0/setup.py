# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pride_colors_plotly']

package_data = \
{'': ['*']}

install_requires = \
['rich>=10.14.0,<11.0.0', 'typer[all]>=0.4.0,<0.5.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=4.5.0,<5.0.0']}

entry_points = \
{'console_scripts': ['pride_colors_plotly = pride_colors_plotly.__main__:app']}

setup_kwargs = {
    'name': 'pride-colors-plotly',
    'version': '0.1.0',
    'description': 'PlotLY and matplotlib pride flag color maps and templates to make your plots proud :)',
    'long_description': '# pride_colors_plotly\n\n<div align="center">\n\n[![Build status](https://github.com/pride_colors_plotly/pride_colors_plotly/workflows/build/badge.svg?branch=master&event=push)](https://github.com/pride_colors_plotly/pride_colors_plotly/actions?query=workflow%3Abuild)\n[![Python Version](https://img.shields.io/pypi/pyversions/pride_colors_plotly.svg)](https://pypi.org/project/pride_colors_plotly/)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/pride_colors_plotly/pride_colors_plotly/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pride_colors_plotly/pride_colors_plotly/blob/master/.pre-commit-config.yaml)\n[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/pride_colors_plotly/pride_colors_plotly/releases)\n[![License](https://img.shields.io/github/license/pride_colors_plotly/pride_colors_plotly)](https://github.com/pride_colors_plotly/pride_colors_plotly/blob/master/LICENSE)\n![Coverage Report](assets/images/coverage.svg)\n\nPlotLY and matplotlib pride flag color maps and templates to make your plots proud :)\n\n</div>\n\n\n## Installation\n\n```bash\npip install -U pride_colors_plotly\n```\n\nor install with `Poetry`\n\n```bash\npoetry add pride_colors_plotly\n```\n\nThen you can run\n\n```bash\npride_colors_plotly --help\n```\n\nor with `Poetry`:\n\n```bash\npoetry run pride_colors_plotly --help\n```\n\n## About\n\nAvailable flag color schemes:\n\n- Philadelphia pride flag \n\n<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Philadelphia_Pride_Flag.svg/2560px-Philadelphia_Pride_Flag.svg.png" alt="Philadelphia pride flag" height="75" width="100">\n\n- Rainbow flag \n\n<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Gay_Pride_Flag.svg/2560px-Gay_Pride_Flag.svg.png" alt="Rainbow flag" height="75" width="100">\n\n- Trans flag \n\n<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Transgender_Pride_flag.svg/220px-Transgender_Pride_flag.svg.png" alt="Trans flag" height="75" width="100">\n\n- Bisexual flag \n\n<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Bisexual_Pride_Flag.svg/220px-Bisexual_Pride_Flag.svg.png" alt="Bi flag" height="75" width="100">\n\n- Lesbian flag \n\n<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Lesbian_Pride_Flag_2019.svg/190px-Lesbian_Pride_Flag_2019.svg.png" alt="Lesbian flag" height="75" width="100">\n\n- Asexual flag \n\n<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Asexual_Pride_Flag.svg/220px-Asexual_Pride_Flag.svg.png" alt="Asexual flag" height="75" width="100">\n\n- Aromantic flag \n\n<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Aromantic_Pride_Flag.svg/220px-Aromantic_Pride_Flag.svg.png" alt="Aromantic flag" height="75" width="100">\n\n- Pan flag \n\n<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Pansexuality_Pride_Flag.svg/180px-Pansexuality_Pride_Flag.svg.png" alt="Pan flag" height="75" width="100">\n\n\n## Usage\n\n1) Set color cycle as plotly default color cycle:\n\n``` set_pride_template(flag="philadelphia")```\n\n2) Get a list of discrete colors (for use in either matplotlib or plotly):\n\n``` colors=pride_colors_plotly(flag="rainbow")```\n\n3) Get a continuous colorscale for use in plotly:\n\n```colorscale=pride_colors_plotly(flag=\'trans\',continuous_colorscale=True) ```\n\n4) Get a matplotlib colormap:\n\n```cmap=pride_colors_matplotlib(flag=\'bi\') ```\n\n## 📈 Releases\n\nYou can see the list of available releases on the [GitHub Releases](https://github.com/pride_colors_plotly/pride_colors_plotly/releases) page.\n\nWe follow [Semantic Versions](https://semver.org/) specification.\n\nWe use [`Release Drafter`](https://github.com/marketplace/actions/release-drafter). As pull requests are merged, a draft release is kept up-to-date listing the changes, ready to publish when you’re ready. With the categories option, you can categorize pull requests in release notes using labels.\n\n### List of labels and corresponding titles\n\n|               **Label**               |  **Title in Releases**  |\n| :-----------------------------------: | :---------------------: |\n|       `enhancement`, `feature`        |       🚀 Features       |\n| `bug`, `refactoring`, `bugfix`, `fix` | 🔧 Fixes & Refactoring  |\n|       `build`, `ci`, `testing`        | 📦 Build System & CI/CD |\n|              `breaking`               |   💥 Breaking Changes   |\n|            `documentation`            |    📝 Documentation     |\n|            `dependencies`             | ⬆️ Dependencies updates |\n\nYou can update it in [`release-drafter.yml`](https://github.com/pride_colors_plotly/pride_colors_plotly/blob/master/.github/release-drafter.yml).\n\nGitHub creates the `bug`, `enhancement`, and `documentation` labels for you. Dependabot creates the `dependencies` label. Create the remaining labels on the Issues tab of your GitHub repository, when you need them.\n\n## 🛡 License\n\n[![License](https://img.shields.io/github/license/pride_colors_plotly/pride_colors_plotly)](https://github.com/pride_colors_plotly/pride_colors_plotly/blob/master/LICENSE)\n\nThis project is licensed under the terms of the `GNU GPL v3.0` license. See [LICENSE](https://github.com/pride_colors_plotly/pride_colors_plotly/blob/master/LICENSE) for more details.\n\n## 📃 Citation\n\n```bibtex\n@misc{pride_colors_plotly,\nauthor = {E. Lastufka},\n  title = {PlotLY and matplotlib pride flag color maps and templates to make your plots proud :)},\n  year = {2022},\n  publisher = {GitHub},\n  journal = {GitHub repository},\n  howpublished = {\\url{https://github.com/pride_colors_plotly/pride_colors_plotly}}\n}\n```\n\n## Credits [![🚀 Your next Python package needs a bleeding-edge project structure.](https://img.shields.io/badge/python--package--template-%F0%9F%9A%80-brightgreen)](https://github.com/TezRomacH/python-package-template)\n\nThis project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template)\n',
    'author': 'pride_colors_plotly',
    'author_email': 'elastufka@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pride_colors_plotly/pride_colors_plotly',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
