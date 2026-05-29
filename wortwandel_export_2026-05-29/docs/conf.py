import os
import sys
sys.path.insert(0, os.path.abspath('../pylib'))

project = 'wortwandel'
author = 'Edwin Wiese'
release = '1.0'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]
templates_path = ['_templates']
exclude_patterns = ['_build']
html_theme = 'alabaster'
autodoc_default_options = {'members': True, 'undoc-members': True}
