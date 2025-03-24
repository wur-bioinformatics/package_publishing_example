# Python packaging workshop
25.03.2025

## Assignment 1: python package management with uv
In this assignment we will initialize a new python project using [uv](https://docs.astral.sh/uv/). Some of the things uv will do for us: structure/configure `pyproject.toml`, add/remove dependencies, manage python versions and virtual environments, run linters and tests, publish to pypi.

### step 1
Create a new git repository, either on the commandline or in the github user interface.

Commandline:

```{sh}
$ mkdir new_project
$ cd new_project
$ git init 
```

Github:
Create a new repository in the [user interface](https://github.com/new) and copy the project url.

```{sh}
$ git clone <NEW_PROJECT_URL>
$ cd new_project
```

### step 2
Install [uv](https://docs.astral.sh/uv/)

```{sh}
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```

### step 3
Initialize a new python project using uv. In this workshop we will focus on building a python package, but uv can also be used for smaller projects such a single scripts. See https://docs.astral.sh/uv/concepts/projects/init/ for various options on how to initialize a project.

```{sh}
$ uv init --package
```

This should give you a relatively barebones `pyproject.toml` file containing all your projects configuration, and a few minimal folders and files for your python project. Note the `.python-version` file: this is uv's way (and also e.g. pyenv's way) of tracking which python version is used for the project, and will be used in the project's virtual environment. The following steps add functionality and dependencies to the project, which you can track in the `pyproject.toml` file.

### Step 3
We're going to add some code!

Uv already created a folder structure and `__init__.py` with some minimal content, so let's update that a bit. There are many options for structuring this, for now we'll try to keep our `__init__.py` clean so we'll create a separate file with some code, and import that code in `__init__.py` (The bonus assignment expands this a little bit).


You can come up with something yourself, or past the below code in `src/new_project/add.py`.

```{python}
# Goes in add.py

def add(number1: int | float, number2: int | float) -> int:
    """
    Integer addition, if floats are provided they will be first 
    converted to integers by rounding down

    Examples:
        >>> add(1, 2)
        3

        >>> add(2.3, 4.5)
        6
  
    Args:
        number1 (int | float): first number for addition
        number2 (int | float): second number for addition
  
    Returns:
        int: sum of (possibly rounded down) inputs
    """
    return int(number1) + int(number2)
```

In addition, make sure to update your `__init__.py`!

```{python}
# Goes in __init__.py
from .add import add

__all__ = ['add']l
```
### Step 4

Let's add and run a linter/formatter to see if our code meets current best practices

```{sh}
$ uv add ruff
$ uv run ruff check
```

### Step 5

Let's add a testing framework to check our code for correctness. If you've used the code example above you can run a test on the examples in the docstring (i.e. a doctest), otherwise it is common to specify tests in a `tests` folder, e.g. in `tests/test_add.py`.

```{sh}
$ uv add pytest
$ uv run pytest --doctest-modules
```

Note that we had to specify explicitly that we wanted pytest to run doctests. If you always want to do this, you can add the following lines to you `pyproject.toml`:

```{toml}
[pytest]
addopts = "--doctest-modules"
```

This way pytest always runs with the doctest option enabled, so the command for running tests would simplify to `uv run pytest`. 

### Step 6

Now that we have a functioning and tested codebase, there is one step left before we can think about publishing to pypi!

To publish to pypi, your source code has to be 'built' into something that can be distributed (for some more background see the workshop slides and https://packaging.python.org/en/latest/tutorials/packaging-projects/#choosing-a-build-backend). Since we have specified we are building a package when initializing uv, the following lines were already added to our `pyproject.toml`:

```{toml}
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

These lines indicate that uv will use [hatch](https://hatch.pypa.io/latest/), or more specifically it's build backend [hatchling](https://github.com/pypa/hatch/tree/master/backend) to build our code into e.g. a [wheel](https://packaging.python.org/en/latest/specifications/binary-distribution-format/#binary-distribution-format).

With a build system specified, building is as easy as running
```{sh}
uv build
```

This creates a few files in the folder `dist`, which can be used to publish to pypi. Find these files, and notice that the project version is part of the the file names!

### Step 7

Publishing to pypi.

All that is left to publish your codebase to pypi is making sure you have a pypi account, and [creating an access token](https://pypi.org/manage/account/token/).
The first time you publish a project you'll need an access token with full account access, after that you can also use project-specific tokens. 

Make sure you copy and save your token somewhere once you've created it!

To publish to pypi, run the following code. Enter `__token__` as username, and the *actual token* as password. 

```{sh}
uv publish
```

Congratualations, you have published your package to pypi with the help of uv!

### Bonus

With a few lines of code and some configuration, and the help of [typer](https://typer.tiangolo.com/), you can expose some parts of your code base as command line interface (CLI)!


Add typer as a dependency for the project
```{sh}
uv add typer
```

Create a `cli.py` file in `src/<new_project>/` with the following content (this wraps the `add` function to that it prints instead of returns, and uses floats as type signatures since typer currently does not support union types such as `int | float`):

```{python}
import typer
from . import add

cli = typer.Typer()


@cli.command(name="add")
def add_wrapper(input1: float, input2: float):
    print(add(input1, input2))
```

Add the following configuration lines to your `pyproject.toml`:
```{toml}
[project.scripts]
cli = "testproject.cli:cli"
```

This now exposes a CLI that you can test with uv:

```{sh}
uv run cli --help
```

And that will be available as `cli` from the commandline once you've pip-installed the published package!


## Assignment 2: Publishing a package to conda

## Assignment 3: Miscellaneous tips and tricks with github

### github action for CI/CD
#### step 1 
Setting up a github action workflow. Create a `.github/workflows` Directory:
```{sh}
mkdir -p .github/workflows
```
#### step 2
Define the workflow file. Create a yaml file (e.g. ci-cd.yaml) within the workflows directory to define the CI/CD pipeline.
```{yaml}
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  push:
    tags:
      - 'v*'
```
The workflow is triggered on push/pull requests to the main branch, and when a new version tag (starting with "v") is pushed.
```{yaml}
jobs:
  build-and-test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3,11]
```
The build-and-test job runs on Ubuntu and uses a matrix strategy to test package across multiple python versions (3.9, 3.10, 3.11 in this case).
```{yaml}
    steps:
      - name: Checkout code
      uses: actions/checkout@v3

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
        python-verson: ${{ matrix.python-version }}

      - name: Build package
        run: |
          python -m pip install --upgrade pip
          pip install build
          python -m build

      - name: Run tests
        run: |
          pip install pytest
          pytest
```
The above steps include:
- **Checkout code:** clone the repository to the runner.
- **Set up Python:** configure python environment based on versions in the matrix.
- **Build package:** build the package using the pyproject.toml file.
- **Run tests:** install pytest and runs the test.
### github container registry (GHCR)
#### step 1
Define the dockerfile named `Dockerfile` for your repository.
```dockerfile
# Use an official Python runtime as a parent image.
FROM python:3.9-slim

# Prevent Python from buffering stdout and stderr.
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container.
WORKDIR /app

# Copy the project files into the container.
# Adjust file paths as necessary for your repository structure.
COPY pyproject.toml .
COPY package_publishing_example/ ./package_publishing_example/

# Upgrade pip and install build tool.
RUN pip install --upgrade pip
RUN pip install build

# Build the package (creates wheel and sdist in the dist/ folder).
RUN python -m build

# Install the package from the built wheel.
RUN pip install $(ls dist/*.whl)

# Optionally, run tests here if you have a test suite.
# RUN pip install pytest && pytest

# Define the default command to verify installation.
# Replace with your application's start command if needed.
CMD ["python", "-c", "import package_publishing_example; print('Package installed successfully!')"]
```
#### step 2
Define another workflow yaml file for containerize and publish (e.g. container-publish.yaml).
```{yaml}
name: Docker build and publish

on:
  push:
    tags:
      - 'v*'

jobs:
  containerize:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
        
      - name: Log in to GHCR
        uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build Docker image
        run: |
          docker build -t ghcr.io/${{ github.repository_owner }}/my-python-project:latest .

      - name: Push Docker image
        run: |
          docker push ghcr.io/${{ github.repository_owner }}/my-python-project:latest
```
This workflow triggers on pushes that create tags starting with "v" (e.g. v1.0.0).
Steps include:
- **Checkout code:** Pulls your repository into the runner.
- **Log in to GHCR:** Authenticates to GHCR using your github token.
- **Build Docker image:** Uses the Dockerfile in your repository to build the image.
- **Push Docker image:** Pushes the built image to GHCR.

