# package_publishing_example
[![PyPI version](https://badge.fury.io/py/package-publishing-example.svg)](https://pypi.org/project/package-publishing-example/)


[![DOI](https://zenodo.org/badge/951219694.svg)](https://doi.org/10.5281/zenodo.15082110)


[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/wur-bioinformatics/package_publishing_example/blob/main/example.ipynb)


This repository contains an example python codebase with accompanying CLI to demonstrate how to set up and publish such a project with modern[^1] tools. 

The contents of this repository themselves are published as a [python package](https://pypi.org/project/package-publishing-example/) that can be imported in python, but also contains a CLI wrapper.

Installing the package
```{sh}
pip install package_publishing_example 
```

Testing it out
```{python}
>>> from python_packaging_example import revcomp
>>> revcomp('ACGTA')
'TACGT'
```

```{sh}
$ ppe revcomp ACGTA
TACGT
```

This codebase uses the following tools: 
- [uv](https://docs.astral.sh/uv/) for project management and publishing to [pypi](https://pypi.org/)
- [ruff](https://docs.astral.sh/ruff/) for linting and formatting
- [pytest](https://docs.pytest.org/en/stable/) for running tests
- [typer](https://typer.tiangolo.com/) for creating a CLI
- [uv-dynamic-versioning](https://pypi.org/project/uv-dynamic-versioning/) to read the package version from a git tag 

The assignments consist of following the steps that were followed to end up with this repository repository structure, e.g. downloading and initializing the tools.
Assignment 1 focuses on python package management and publishing with uv, assignment 2 deals with publishing to conda, assignment 3 contains miscellaneous tips in tricks for working with github and linking/synchronizing packages.

[^1]: 'Modern' at the time of writing (19.03.2025)