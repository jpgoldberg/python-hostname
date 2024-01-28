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


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions: list[str] = [
    "sphinx.ext.autodoc",
    "sphinx_autodoc_typehints",
    "sphinx.ext.doctest",
]

extensions.append("sphinx.ext.intersphinx")
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "dns": ("https://dnspython.readthedocs.io/en/stable/", None),
}

templates_path = ["_templates"]
exclude_patterns: list[str] = []

rst_prolog = f"""
.. |project| replace:: **{project}**
.. |root| replace:: :mod:`hostname`
"""


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]
