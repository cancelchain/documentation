# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'CancelChain'
copyright = '2023 Thomas Bohmbach, Jr.'
author = 'Thomas Bohmbach, Jr.'

release = '1.4'
version = '1.4.1'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosectionlabel',
    'sphinxcontrib.httpdomain',
    'sphinx-jsonschema'
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['static']
html_favicon = 'static/favicon.ico'
html_logo = 'static/cc-logo.png'
