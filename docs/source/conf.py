# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import gethash as pkg

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Gethash"
copyright = "2020-2023, xymy"
author = "xymy"
version = pkg.__version__
release = pkg.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "myst_parser",
    "sphinx_copybutton",
]
templates_path = ["_templates"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_title = f"{project} {release}"
html_static_path = ["_static"]

# -- Options for autodoc -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#module-sphinx.ext.autodoc

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "show-inheritance": True,
}

# -- Options for intersphinx -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#module-sphinx.ext.intersphinx

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
}

# -- Options for myst-parser -------------------------------------------------
# https://myst-parser.readthedocs.io/en/latest/

myst_enable_extensions = ["deflist", "tasklist"]
myst_heading_anchors = 3

# -- Options for sphinx-copybutton -------------------------------------------
# https://sphinx-copybutton.readthedocs.io/en/latest/

copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True
