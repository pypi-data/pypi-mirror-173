# Author: Zhang Yunjun, Jan 2021
# Copyright 2020, by the California Institute of Technology.


# always prefer setuptools over distutils
import os
import setuptools
import sys
from numpy.distutils.core import setup, Extension

# Grab version from version.py
# link: https://stackoverflow.com/questions/53648900
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from pysolid.version import version

# Grab from README file: long_description
with open("README.md", "r") as f:
    long_description = f.read()

# specify fortran extensions to build with numpy.f2py
solid_ext = Extension(name='pysolid.solid', sources=['src/pysolid/solid.for'])

setup(
    name='pysolid',
    version=version,
    description="A Python wrapper for solid to compute solid Earth tides",
    url="https://github.com/insarlab/PySolid",
    download_url=("https://github.com/insarlab/PySolid/archive/v{}.tar.gz".format(version)),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Zhang Yunjun, Dennis Milbert",
    author_email="yunjunzgeo@gmail.com",
    license="GPL-3.0-or-later",
    license_files=("LICENSE",),

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    keywords="solid Eartth tides, deformation, geodesy, geophysics",

    project_urls={
        "Bug Reports": "https://github.com/insarlab/PySolid/issues",
        "Source": "https://github.com/insarlab/PySolid",
    },

    # package discovery
    packages=setuptools.find_packages("src"),  # include all packages under src
    package_dir={"": "src"},                   # tell distutils packages are under src

    # build fortran deps with numpy.f2py
    ext_modules=[solid_ext],

    # dependencies
    python_requires=">=3.6",
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
        'scikit-image',
    ],

    # data files
    include_package_data=True,
    package_data={
        "pysolid": ["solid.for"],
    },
)
