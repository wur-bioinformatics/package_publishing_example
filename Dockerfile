# Use an official Python runtime as a parent image.
FROM python:3.10-slim

LABEL authors="zijiang"

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
# Optionally, run tests if you have a test suite.
RUN pip install pytest && pytest

# Define the default command to verify installation.
CMD ["python", "-c", "import package_publishing_example; print('Package installed successfully!')"]

