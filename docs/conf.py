# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../'))

# -- Project information -----------------------------------------------------

project = 'auto-emailer'
copyright = '2019, Adam Stueckrath'
author = 'Adam Stueckrath'

# The full version, including alpha/beta/rc tags
release = '0.0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon'
]

# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'https://docs.python.org/': None}

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    'description': 'auto-emailer library for Python',
    'github_button': True,
    'github_user': 'adamstueckrath',
    'github_repo': 'auto-emailer',
    'github_banner': True,
    'travis_button': True,
    'font_family': "'Roboto', Georgia, sans",
    'head_font_family': "'Roboto', Georgia, serif",
    'code_font_family': "'Roboto Mono', 'Consolas', monospace",
    'show_powered_by': True,
    'show_relbars': True,
    'fixed_sidebar': True
}

# Custom sidebar templates, maps document names to template names.
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
        'searchbox.html'
    ]
}

# Output file base name for HTML help builder.
htmlhelp_basename = 'auto-emailerdoc'

# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'auto-emailer.tex', 'auto-emailer Documentation',
     'Adam Stueckrath', 'manual'),
]

# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'auto-emailer', 'auto-emailer Documentation',
     [author], 1)
]

# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'auto-emailer', 'auto-emailer Documentation',
     author, 'auto-emailer', 'One line description of project.',
     'Miscellaneous'),
]

# -- Options for autodoc extension -------------------------------------------

# Include Python objects as they appear in source files
# http://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#confval-autodoc_member_order
# Default: alphabetically ('alphabetical' or 'groupwise' or 'bysource')
autodoc_member_order = 'bysource'

# Default flags used by autodoc directives
# autodoc_default_flags = ['members', 'undoc-members', 'private-members',
#                          'special-members', 'show-inheritance']

# This is already the default behavior; here for explicitness
autodoc_inherit_docstrings = True
autodoc_default_flags = ['members', 'inherited-members', 'private-members']
autoclass_content = 'both'

# -- Options for autosummary extension ---------------------------------------

# Generate autodoc stubs with summaries from code
generate_autosummary_docs = True

# -- Options for custom css --------------------------------------------------

# Define a setup function in your conf.py that adds your stylesheet:


def setup(app):
    app.add_stylesheet('custom.css')
