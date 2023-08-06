 # -*- coding: utf-8 -*-
"""
ATOM SIMULATOR squareatoms
Created on Mon Nov 15 14:45:06 2021
@author: Asari

"""
from setuptools import setup, find_packages


setup(
    name='PyAtoms_test',
    version='1.0',
    license='UCLA',
    author="Asari Prado",
    author_email='asariprado@physics.ucla.edu',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/asariprado/PyAtoms',
    keywords='PyAtoms_test',
    install_requires=[
          'numpy', 'matplotlib', 'PyQt5', 'math', 'scipy.ndimage'
      ],

)