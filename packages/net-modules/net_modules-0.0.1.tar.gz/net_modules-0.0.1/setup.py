# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 10:02:18 2022

@author: ashoaib
"""

from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

#with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
#    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'upgrade and deploy networks'
LONG_DESCRIPTION = 'A package that allows to upgrade/ deploy vnf/cnf in a network.'

# Setting up
setup(
    name="net_modules",
    version=VERSION,
    author="Nokia",
    author_email="<mail@neuralnine.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['paramiko','scp',  'regex', 'ipywidgets', 'ipython', 'tqdm', 'ipyfilechooser', 'openpyxl'],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)