# pride_colors_plotly

<div align="center">

[![Build status](https://github.com/pride_colors_plotly/pride_colors_plotly/workflows/build/badge.svg?branch=master&event=push)](https://github.com/pride_colors_plotly/pride_colors_plotly/actions?query=workflow%3Abuild)
[![Python Version](https://img.shields.io/pypi/pyversions/pride_colors_plotly.svg)](https://pypi.org/project/pride_colors_plotly/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/pride_colors_plotly/pride_colors_plotly/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pride_colors_plotly/pride_colors_plotly/blob/master/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/pride_colors_plotly/pride_colors_plotly/releases)
[![License](https://img.shields.io/github/license/pride_colors_plotly/pride_colors_plotly)](https://github.com/pride_colors_plotly/pride_colors_plotly/blob/master/LICENSE)
![Coverage Report](assets/images/coverage.svg)

PlotLY and matplotlib pride flag color maps and templates to make your plots proud :)

</div>


## Installation

```bash
pip install -U pride_colors_plotly
```

or install with `Poetry`

```bash
poetry add pride_colors_plotly
```

Then you can run

```bash
pride_colors_plotly --help
```

or with `Poetry`:

```bash
poetry run pride_colors_plotly --help
```

## About

Available flag color schemes:

- Philadelphia pride flag 

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Philadelphia_Pride_Flag.svg/2560px-Philadelphia_Pride_Flag.svg.png" alt="Philadelphia pride flag" height="75" width="100">

- Rainbow flag 

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Gay_Pride_Flag.svg/2560px-Gay_Pride_Flag.svg.png" alt="Rainbow flag" height="75" width="100">

- Trans flag 

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Transgender_Pride_flag.svg/220px-Transgender_Pride_flag.svg.png" alt="Trans flag" height="75" width="100">

- Bisexual flag 

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Bisexual_Pride_Flag.svg/220px-Bisexual_Pride_Flag.svg.png" alt="Bi flag" height="75" width="100">

- Lesbian flag 

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Lesbian_Pride_Flag_2019.svg/190px-Lesbian_Pride_Flag_2019.svg.png" alt="Lesbian flag" height="75" width="100">

- Asexual flag 

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Asexual_Pride_Flag.svg/220px-Asexual_Pride_Flag.svg.png" alt="Asexual flag" height="75" width="100">

- Aromantic flag 

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Aromantic_Pride_Flag.svg/220px-Aromantic_Pride_Flag.svg.png" alt="Aromantic flag" height="75" width="100">

- Pan flag 

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Pansexuality_Pride_Flag.svg/180px-Pansexuality_Pride_Flag.svg.png" alt="Pan flag" height="75" width="100">


## Usage

1) Set color cycle as plotly default color cycle:

``` set_pride_template(flag="philadelphia")```

2) Get a list of discrete colors (for use in either matplotlib or plotly):

``` colors=pride_colors_plotly(flag="rainbow")```

3) Get a continuous colorscale for use in plotly:

```colorscale=pride_colors_plotly(flag='trans',continuous_colorscale=True) ```

4) Get a matplotlib colormap:

```cmap=pride_colors_matplotlib(flag='bi') ```

## 📈 Releases

You can see the list of available releases on the [GitHub Releases](https://github.com/pride_colors_plotly/pride_colors_plotly/releases) page.

We follow [Semantic Versions](https://semver.org/) specification.

We use [`Release Drafter`](https://github.com/marketplace/actions/release-drafter). As pull requests are merged, a draft release is kept up-to-date listing the changes, ready to publish when you’re ready. With the categories option, you can categorize pull requests in release notes using labels.

### List of labels and corresponding titles

|               **Label**               |  **Title in Releases**  |
| :-----------------------------------: | :---------------------: |
|       `enhancement`, `feature`        |       🚀 Features       |
| `bug`, `refactoring`, `bugfix`, `fix` | 🔧 Fixes & Refactoring  |
|       `build`, `ci`, `testing`        | 📦 Build System & CI/CD |
|              `breaking`               |   💥 Breaking Changes   |
|            `documentation`            |    📝 Documentation     |
|            `dependencies`             | ⬆️ Dependencies updates |

You can update it in [`release-drafter.yml`](https://github.com/pride_colors_plotly/pride_colors_plotly/blob/master/.github/release-drafter.yml).

GitHub creates the `bug`, `enhancement`, and `documentation` labels for you. Dependabot creates the `dependencies` label. Create the remaining labels on the Issues tab of your GitHub repository, when you need them.

## 🛡 License

[![License](https://img.shields.io/github/license/pride_colors_plotly/pride_colors_plotly)](https://github.com/pride_colors_plotly/pride_colors_plotly/blob/master/LICENSE)

This project is licensed under the terms of the `GNU GPL v3.0` license. See [LICENSE](https://github.com/pride_colors_plotly/pride_colors_plotly/blob/master/LICENSE) for more details.

## 📃 Citation

```bibtex
@misc{pride_colors_plotly,
author = {E. Lastufka},
  title = {PlotLY and matplotlib pride flag color maps and templates to make your plots proud :)},
  year = {2022},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/pride_colors_plotly/pride_colors_plotly}}
}
```

## Credits [![🚀 Your next Python package needs a bleeding-edge project structure.](https://img.shields.io/badge/python--package--template-%F0%9F%9A%80-brightgreen)](https://github.com/TezRomacH/python-package-template)

This project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template)
