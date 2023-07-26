import setuptools
from setuptools import setup

setup (
name="tourismapi",
version ="0.0.1",
author ="D. Bulloni, N. Margni",
author_email ="dyuman.bulloni@student.supsi.ch",
description ="Client Library for TourismAPI. ",
package_dir = {"": "."},
packages = setuptools.find_packages (where="."),
python_requires =">=3.6",
install_requires = ['pandas', 'requests', 'gmplot']
)
#python setup.py bdist_wheel