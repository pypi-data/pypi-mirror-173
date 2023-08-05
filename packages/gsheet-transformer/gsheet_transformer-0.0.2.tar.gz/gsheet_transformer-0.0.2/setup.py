"""Python setup.py for gsheet-transformer package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("python_packages_template", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


requirements = [
    "pandas",
    "gspread"
]

requirements_test = [
    "pytest",
    "coverage",
    "flake8",
    "black",
    "isort",
    "pytest-cov",
    "codecov",
    "mypy",
    "gitchangelog",
    "mkdocs",
    "twine"
]


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="gsheet_transformer",
    version=read("gsheet_transformer", "VERSION"),
    description="gsheet_transformer created by Koinworks Data Team",
    url="https://gitlab-engineering.koinworks.com/data-team/gsheet-transformer",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Koinworks Data Team",
    packages=find_packages(exclude=[]),
    install_requires=requirements,
    extras_require={"test": requirements_test},
)
