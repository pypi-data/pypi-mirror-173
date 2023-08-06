from setuptools import setup
from Cython.Build import cythonize

harmonic_mean = cythonize('src/imppkg/harmonic_mean.pyx')

setup(ext_modules=harmonic_mean)
