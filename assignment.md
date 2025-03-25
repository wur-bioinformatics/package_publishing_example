# Python packaging workshop
25.03.2025

Authors: Rens Holmer, Laura Patino Medina, Elena Del Pup, Zijiang Yang

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

__all__ = ['add']
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
addopts = '--doctest-modules'
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


## Assignment 2: Publishing a package to bioconda

Objectives of this assignment
- [ ] Familiarize with conda recipes.
- [ ] Use Grayskull to generate a Bioconda recipe.
- [ ] Build and test the package locally.
- [ ] Be aware that submission to Bioconda requires further preparation.

In this second assignment we will work on automatically generating a conda recipe from a PyPI package, using Grayskull.
To publish a Bioconda package is neccessary to set a GitHub repository and a conda recipe, the latter outlines the steps needed to build a package from source code.


### Step 0
We will use an existing Python project from GitHub, if successfully completed the repository and the PyPi package was set up on the first assignment of the workshop.

### Step 1
Install [Grayskull](https://github.com/conda/grayskull) and [bioconda-utils](https://github.com/bioconda/bioconda-utils).

```bash
mamba create -n bioconda bioconda-utils grayskull
conda activate bioconda
```

### Step 2
In order to add the recipe to bioconda later, we will fork and clone the bioconda-recipes repository.
Go to the [bioconda-recipes](https://github.com/bioconda/bioconda-recipes) repository and click on the fork button in the top right corner.
Clone the forked repository to your local machine:

```bash
git clone https://github.com/AddYourGitHubIdHere/bioconda-recipes.git
cd bioconda-recipes/
```

### Step 3
Run Grayskull to automatically generate a conda recipe from a PyPi package.

```bash
cd recipes/
grayskull pypi package_publishing_example
```

This command will create a new folder called 'package_publishing_example'.
Inside, you will find the meta.yaml file, containing the metadata neccessary to create a conda package.

If it works you should see this message once grayskull is done:
`#### Recipe generated on /home/username/package_publishing_example for package_publishing_example ###`

### Step 4

After automatically generating the conda recipe you can edit the meta.yaml file.
If you did not use Grayskull, you will need to manually write the script.
Some of the lines in the meta.yaml generated by Grayskull are placeholders, though, and some others required by bioconda are missing.
Here is an example of a meta.yaml file for the package_publishing_example package with the changes compared to the one generated by Grayskull highlighted:

```diff
{% set name = "package_publishing_example" %}
{% set version = "0.0.4" %}

package:
  name: {{ name|lower }}
  version: {{ version }}

source:
-  url: https://pypi.org/packages/source/{{ name[0] }}/{{ name }}/package_publishing_example-{{ version }}.tar.gz
+  url: https://pypi.org/packages/source/{{ name }}/{{ name }}/{{ name }}-{{ version }}.tar.gz
  sha256: dd5ffdb8db6e6f2ba05546f230abc53ee897497d4eb81a1808fbe6290a07bf6f

build:
  entry_points:
    - ppe = package_publishing_example.cli:cli
  noarch: python
  script: {{ PYTHON }} -m pip install . -vv --no-deps --no-build-isolation
  number: 0
+  run_exports:
+    - {{ pin_subpackage('package_publishing_example', max_pin="x.x") }}

requirements:
  host:
    - python >=3.10
    - hatchling
-    - uv-dynamic-versioning
    - pip
  run:
    - python >=3.10
    - pytest >=8.3.5
    - ruff >=0.11.0
    - typer >=0.15.2
-    - uv-dynamic-versioning >=0.6.0

test:
  imports:
    - package_publishing_example
  commands:
    - pip check
    - ppe --help
  requires:
    - pip

about:
  summary: Add your description here
  license: MIT
-  license_file: LICENSE

extra:
  recipe-maintainers:
    - AddYourGitHubIdHere
```

### Step 5

When building a Bioconda package, bioconda-utils reads the metadata of the conda recipe and creates a conda package containing all the files in the build environment and the specified dependencies.
It validates the build by running the tests.
We will now build the package locally, for this we will use bioconda-utils, run this command from the root folder of your bioconda-recipes fork.

```bash
cd /path/to/bioconda-recipes
bioconda-utils build --packages package_publishing_example
```

### Step 6

If build was successful, conda will generate a package file in the conda-bld directory.
To locate this file, you can use this command from the terminal:

```bash
TODO
```

Once the package has been built, you can test it.
Create a conda environment and install your built package.

```bash
mamba create -n test_package_publishing_example --use-local test_package_publishing_example
conda activate test_package_publishing_example
test_package_publishing_example --help
```

### Step 7 (do NOT do in this workshop)

If it was successfully built and tested, the package is ready for submission to Bioconda.
Importantly, the packages that are published in Bioconda are strictly reviewed before is accepted.

In the bioconda-recipes directory, commit the changes to a new branch and push it to your fork:

```bash
git checkout -b add_package_publishing_example
git add recipes/package_publishing_example
git commit -m "Add package_publishing_example"
git push -u origin add_package_publishing_example
```

Then, go to your forked repository on GitHub and create a new pull request to the bioconda-recipes repository.
The automated tests will run and once these pass successfully, you may label the pull request by commenting "@BiocondaBot please add label".
After this has been done, the Bioconda team will review the package and merge it into the main repository.





## Assignment 3: Release Automation, Versioning & Sharing: Best Practices with GitHub

### 3.1 Consistent versioning via UV dynamic versioning

#### Step 1 - Add a version to your project

Update your `pyproject.toml` with this or confirm it is already present:

```{sh}
[tool.uv-dynamic-versioning]
vcs = "git"
style = "semver"
```

#### Step 2 – Make a release

To produce a clean, PyPI-compatible version (e.g. `0.1.0`) for publishing, you need to tag the current commit:

```{sh}
git tag v0.1.0
git push origin v0.1.0
```

Verify that you're on the tag:

```{sh}
git describe --tags --exact-match
```

If this returns v0.1.0, you're good to go. If it returns nothing, you're not on the tagged commit (you may need to re-tag or checkout the correct one).

#### Step 3 – Build again

```{sh}
uv build
```

If you have had previous build attempts, make sure to remove previous build files with `rm -rf dist/` and then rebuild.

After building, the generated wheel in `dist/` will have a clean version: `new_project-0.1.0-py3-none-any.whl`

#### Step 4 - Publish on pypi

Run:

```{sh}
uv publish
```

When prompted:

- Username: `__token__`
- Password: paste your PyPI API token (created at https://pypi.org/manage/account/token/)

Visit: `https://pypi.org/project/<your-package-name>` or for this example project at: https://pypi.org/project/package-publishing-example/

You can now install the latest version of your package with:

```{sh}
pip install <your-package-name>==0.1.0
```


### 3.2 Release-driven packaging to trigger pypi/conda package builds

#### Step 1 - Add a GitHub Actions workflow for PyPI publishing

Create a file at `.github/workflows/publish.yml`:

```{sh}
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  build-and-publish:
    name: Build and publish to PyPI
    runs-on: ubuntu-latest

    permissions:
      id-token: write  # Needed for trusted publishing
      contents: read

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install UV
        run: |
          curl -LsSf https://astral.sh/uv/install.sh | sh
          echo "$HOME/.cargo/bin" >> $GITHUB_PATH

      - name: Build the package
        run: uv build

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          skip-existing: true

```
💡 This setup uses Trusted Publishing — no token needed if your project is configured with PyPI.

If you're using API tokens instead, you can modify the last step:

```{sh}
      - name: Publish to PyPI (token-based)
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_API_TOKEN }}

```

In that case, remember to add your PYPI_API_TOKEN in GitHub → Settings → Secrets and variables → Actions.

#### Step 2 - Add Conda packaging workflow

If you're using Grayskull, you can automate Conda packaging with GitHub Actions. This workflow reuses the `meta.yaml` file you generated with Grayskull.

Create a file:
`.github/workflows/conda-publish.yml`

```{sh}
name: Conda Package Build

on:
  release:
    types: [published]

jobs:
  conda-build:
    name: Build Conda Package
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Miniconda
        uses: conda-incubator/setup-miniconda@v3
        with:
          auto-update-conda: true
          miniconda-version: "latest"
          activate-environment: build-env

      - name: Install build tools
        run: |
          conda install -y conda-build pip
          pip install grayskull

      - name: Generate Conda recipe with Grayskull
        run: |
          grayskull pypi package_publishing_example

      - name: Build Conda package
        run: |
          conda build package_publishing_example/

      - name: Show output location
        run: conda build package_publishing_example/ --output

```

💡 You may want to replace `package_publishing_example` with the real name of your package folder or make it dynamic later using ${{ github.event.release.tag_name }}.

#### Step 3 - Tag a release to trigger the workflows

1. Push your latest commit to `main`
2. Create a GitHub Release:
   - Go to "Releases" → "Draft a new release"
   - Tag version (e.g. v0.1.1)
   - Add release notes
   - Click "Publish release"
3. GitHub will:
   - Trigger the workflow
   - Build the package using UV
   - Upload it to PyPI and Conda automatically!
4. Go to the Actions tab → Watch the "Publish to PyPI" and “Conda Package Build” job run

#### Step 4 - Optional: Upload to Anaconda Cloud

You can extend the workflow to upload your Conda package to Anaconda.org by adding:

```{sh}
      - name: Upload to Anaconda Cloud
        env:
          ANACONDA_API_TOKEN: ${{ secrets.ANACONDA_API_TOKEN }}
        run: |
          anaconda -t $ANACONDA_API_TOKEN upload --user <your-conda-username> $(conda build package_publishing_example/ --output)
```

Replace `<your-conda-username>` and make sure you’ve added ANACONDA_API_TOKEN in your repo’s GitHub → Settings → Secrets.

### 3.3 Publishing code with a DOI via Zenodo

In this assignment, you will make your code citable by linking your GitHub repository to Zenodo, which will automatically archive your code and assign a DOI (Digital Object Identifier) every time you publish a GitHub release.

#### Step 1 – Link your GitHub repo to Zenodo

1. Go to: https://zenodo.org/account/settings/github/
2. Log in via GitHub
2. Under "GitHub repositories", toggle ON your workshop repo
3. Done! Now every GitHub release will be archived by Zenodo and a DOI will be assigned

#### Step 2 – Make a release on GitHub

Just like in Assignment 3.2:

```{sh}
git tag v0.1.0
git push origin v0.1.0
```

Or use the GitHub interface:
- Go to "Releases" → "Draft a new release"
- Select the tag (e.g. v0.1.3)
- Write a short changelog
- Click Publish

Zenodo will:
- Archive this specific snapshot
- Assign a unique DOI
- Group releases under a concept DOI (one DOI that always points to the latest version)

#### Step 3 – Add a DOI badge to your README

Once Zenodo finishes archiving (usually within a minute), go to your Zenodo record and:

1. Scroll to the "Cite as" section
2. Click "Get badge"
3. Copy the Markdown badge from your Zenodo deposit page and paste it in `README.md`:

```{sh}
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1234567.svg)](https://doi.org/10.5281/zenodo.1234567)
```

### 3.4 Deploying and hosting your documentation on GitHub Pages

#### Step 1 - Create a `docs/` folder and a `README.md`

Create a minimal structure for static Markdown-based documentation:

```{sh}
mkdir docs
echo "# Welcome to My Project Docs" > docs/index.md
```

Alternatively, use a tool like `mkdocs` or `sphinx` for nicer styling.

#### Step 2 – Add a GitHub Actions workflow to deploy docs

Create the workflow file: `.github/workflows/docs.yml`:

```{sh}
name: Deploy Docs

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Pages
        uses: actions/configure-pages@v3
      - name: Upload static content
        uses: actions/upload-pages-artifact@v2
        with:
          path: docs/
      - name: Deploy to GitHub Pages
        uses: actions/deploy-pages@v2
```

This workflow will upload and deploy the contents of docs/ every time you push to main.

#### Step 3 – Enable GitHub Pages in your repo settings

Go to Settings → Pages, choose the workflow, and save.

Your documentation should now be published at
`https://<username>.github.io/<repository>/`.

Check the documentation for this repository at: https://wur-bioinformatics.github.io/package_publishing_example/

## Assignment 4: Miscellaneous tips and tricks with github

### github action for CI/CD
In this assignment we will set up a github action workflow for continuous integration and continuous deployment (CI/CD) of a python package. The workflow will run tests on every push to the main branch, and publish a new version to the github container registry (GHCR) on every new version tag.
#### step 1
Setting up a github action workflow. If the `.github/workflows` Directory does not exist, create it:
```{sh}
mkdir -p .github/workflows
```
#### step 2
Define the CI/CD workflow file by creating a yaml file (e.g. ci-cd.yaml) within the workflows directory. The following example workflow file triggers on pushes to the main branch and pull requests to the main branch, and when a new version tag is pushed. The workflow runs on the latest version of the ubuntu runner, checks out the code, sets up Python 3.10, builds the package, and runs tests.
```{yaml}
name: CI/CD Pipeline

# Trigger the workflow on push or pull request to the main branch, and when a new version tag is pushed.
on:
  push:
    branches: [main]
    tags:
      - 'v*'
  pull_request:
    branches: [main]

# Define the jobs that run in the workflow.
jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Build package
        run: |
          python -m pip install --upgrade pip
          pip install -e .

      - name: Run tests
        run: |
          pip install pytest
          pytest
```

### github container registry (GHCR)
#### step 1
Define the dockerfile named `Dockerfile` for your repository in the root directory. The example Dockerfile below installs the project dependencies, builds the package, installs the package, and runs tests.
```dockerfile
# Use an official Python runtime (python3.10 in this case) as a parent image.
FROM python:3.10-slim

# Prevent Python from buffering stdout and stderr.
ENV PYTHONUNBUFFERED=1
# Disable uv-dynamic-versioning to avoid Git dependency during build.
ENV UV_DYNAMIC_VERSIONING_DISABLE=1

# Set the working directory in the container.
WORKDIR /app

# Copy the project files into the container.
COPY pyproject.toml .
COPY src/ ./src/
COPY tests/ ./tests/
COPY README.md .

# Update apt and install Git (if needed for your build backend)
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# Modify pyproject.toml:
# 1. Replace the dynamic version setting with a static version.
# 2. Remove the [tool.uv-dynamic-versioning] section without removing the following header.
RUN sed -i.bak 's/dynamic = \["version"\]/version = "0.1.0"/' pyproject.toml && \
    rm pyproject.toml.bak && \
    awk 'BEGIN {skip=0} \
         /^\[tool\.uv-dynamic-versioning\]/{skip=1; next} \
         /^\[/{skip=0} \
         {if (!skip) print}' pyproject.toml > pyproject.tmp && \
    mv pyproject.tmp pyproject.toml

# Upgrade pip and install the build tool.
RUN pip install --upgrade pip && \
    pip install build

# Build the package (creates wheel and sdist in the dist/ folder)
RUN python -m build
# Install the built package.
RUN pip install dist/*.whl
# Run pytest.
RUN pip install pytest && pytest

# Define the default command to verify installation.
CMD ["python", "-c", "import package_publishing_example; print('Package installed successfully!')"]
```
#### step 2
Define a workflow yaml file for building and testing the Docker image (e.g. ghcr.yaml). Below is a example workflow file that triggers on pushes that create tags starting with "v" (e.g. v1.0.0). The workflow checks out the code, logs in to GHCR, builds the Docker image, and pushes the image to GHCR.
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
Steps include:
- **Checkout code:** Pulls your repository into the runner.
- **Log in to GHCR:** Authenticates to GHCR using your github token.
- **Build Docker image:** Uses the Dockerfile in your repository to build the image.
- **Push Docker image:** Pushes the built image to GHCR.
