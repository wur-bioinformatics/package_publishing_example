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
addopts = --doctest-modules
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

In this second assignment we will work on automatically generating a conda recipe from a PyPI package, using Grayskull.
To publish a Bioconda package is neccessary to set a GitHub repository and a conda recipe, the latter outlines the steps needed to build a package from source code.

Objectives of this aasignment

✔️ Familiarize with conda recipes.
✔️ Use Grayskull to generate a Bioconda recipe.
✔️ Build and test the package locally.
✔️ Be aware that submission to Bioconda requires further preparation. 

### Step 1

We will use an existing Python project from GitHub, ideally the repository and the pypi package was set up on the first assignment of the workshop, if successfully completed.

### Step 2
Install [Grayskull](https://github.com/conda/grayskull)



```python
pip install grayskull
```

### Step 3

Run Gray skull to automatically generate a conda recipe from a python package.


```python
grayskull pypi new_project
```


```python
grayskull pypi package_publishing_example 
```

License type: MIT
License file: ['LICENSE']
Build requirements:
  <none>
Host requirements:
  - python >=3.10
  - hatchling
  - uv-dynamic-versioning
  - pip
Run requirements:
  - python >=3.10
  - pytest >=8.3.5
  - ruff >=0.11.0
  - typer >=0.15.2
  - uv-dynamic-versioning >=0.6.0

RED: Package names not available on conda-forge
YELLOW: PEP-725 PURLs that did not map to known package
GREEN: Packages available on conda-forge
Using default recipe maintainer: AddYourGitHubIdHere

Maintainers:
   - AddYourGitHubIdHere
#### Recipe generated on /home/patin005/workshop/package_publishing_example for package_publishing_example ###

This command will create a new folder called 'new_project'. Inside, you will find the meta.yaml file, containing the metadata neccessary to create a conda package.


```python
new_project/
├── meta.yaml #Main recipe file, contains the build, test information
```

### Step 4

After automatically generating the conda recipe you can edit the meta.yaml file. If you did not use Grayskull, you will need to manually write the script. 

For the example Pypi package named "package_publishing_example", the following meta.yaml is generated by Grayskull:


```python
{% set name = "package_publishing_example" %}
{% set version = "0.0.4" %}

package:
  name: {{ name|lower }}
  version: {{ version }}

source:
  url: https://pypi.org/packages/source/{{ name[0] }}/{{ name }}/package_publishing_example-{{ version }}.tar.gz
  sha256: dd5ffdb8db6e6f2ba05546f230abc53ee897497d4eb81a1808fbe6290a07bf6f

build:
  entry_points:
    - ppe = package_publishing_example.cli:cli
  noarch: python
  script: {{ PYTHON }} -m pip install . -vv --no-deps --no-build-isolation
  number: 0

requirements:
  host:
    - python >=3.10
    - hatchling
    - uv-dynamic-versioning
    - pip
  run:
    - python >=3.10
    - pytest >=8.3.5
    - ruff >=0.11.0
    - typer >=0.15.2
    - uv-dynamic-versioning >=0.6.0

test:
  imports:
    - package_publishing_example
  commands:
    - pip check
    - ppe --help
  requires:
    - pip

about:
  home: 
  summary: Add your description here
  license: MIT
  license_file: LICENSE

extra:
  recipe-maintainers:
    - AddYourGitHubIdHere
```



### Step 5

When building a Bioconda package, conda-build reads the metadata or the conda recipe and creates a conda package containing all the files in the build environment and the specified build dependencies. If recipe includes tests it also tests the new conda package. 


```python
conda install -y conda-build
```

### Step 6
We will now build the package locally, for this we will use conda build, , run this command from the root folder (of your username). [Conda build](https://conda.org/blog/2023-05-18-how-to-use-conda-build/)



```python
conda build new_project
```

If build was successful, Conda will generate a package file in the conda-bld directory. To locate this file, you can use this command from the terminal:


```python
conda build new_project --output
```

???? THIS STEP IS NOT WORKING
```
Could not solve for environment specs
The following package could not be installed
└─ uv-dynamic-versioning =* * does not exist (perhaps a typo or a missing channel).
```

### Step 7

Once the package has been built, you can test it. Create a conda environmet and install your built package.


```python
conda create -n test_environment
conda activate test_env
conda install --use-local new_project
conda activate test_environment
new_project --help
```

If it was successfully built and tested, the package is ready for submission to Bioconda. Importantly, the packages that are published in Bioconda are strictly reviewed before is accepted.

### Step 7 (Do not run it in this workshop)

Finally, once you have build a conda package ideally you will submit a request to pubish your package. This step cannot be performed for the example python package created in this workshop, however is still explained with the purpose of showing the publishing process.

To upload your package to [Anaconda](https://anaconda.org/):


```python
anaconda upload /path/to/my_package-1.0-0.tar.bz2
```

Using Grayskull and conda-build to create and manage a pypi package simplifies and automatizes the process of distribution and installation. 




## Assignment 3: Miscellaneous tips and tricks with github