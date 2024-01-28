import os
import sys
import tomllib

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("../.."))

from hostname import __about__  # noqa: E402

# Pull general sphinx project info from pyproject.toml
with open("../../pyproject.toml", "rb") as f:
    toml = tomllib.load(f)

version = __about__.__version__

pyproject = toml["project"]

project = pyproject["name"]
release = version
author = ",".join([author["name"] for author in pyproject["authors"]])
copyright = f"2024 {author}"


# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Hostname"
copyright = "2024, Jeffrey Goldberg"
author = "Jeffrey Goldberg"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions: list[str] = []

templates_path = ["_templates"]
exclude_patterns: list[str] = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]
