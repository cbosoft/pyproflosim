"""
PFS - Process Flow Simulator
"""

from codecs import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pfs',

    version='0.0.1',  # do not forget to change this

    python_requires='>=3.6',

    description='Process flow simulation',

    long_description=long_description,

    url='https://gitlab.com/cbo77/pfs',

    author='Christopher Boyle',

    author_email='christopher.boyle.101@strath.ac.uk',

    packages=find_packages('src'),
    package_dir={'': 'src'},

    entry_points={
        'console_scripts': [
            'pfs=pfs.main:main'
        ]
    },

    install_requires=['networkx', 'pubchempy', 'sympy', 'numpy', 'matplotlib']
)
