#!/usr/bin/env python

from setuptools import find_packages
from setuptools import setup


with open("README.md") as f:
    long_description = f.read()


requirements_files = [
    'requirements-server.txt',
    'requirements-client.txt',
    'requirements-flow.txt',
]

requirements = []
for f in requirements_files:
    with open(f"requirements/{f}") as f:
        requirements += [line for line in f.readlines()]

with open("requirements/requirements-test.txt") as f:
    test_requirements = [line for line in f.readlines()]

extras = {
    "dev": ["flake8"],
    "test": test_requirements
}

setup(
    author="Christopher Lo",
    author_email="lochristopherhy@gmail.com",
    python_requires="==3.8.*",
    description="Boilerplate for an end-to-end data app.",
    install_requires=requirements,
    extras_require=extras,
    long_description=long_description,
    include_package_data=True,
    keywords="datathon-mlapp-starter",
    name="datathon-mlapp-starter",
    url="https://github.com/topher-lo/datathon-mlapp-starter",
    version="0.0.1",
)
