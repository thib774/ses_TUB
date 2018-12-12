from setuptools import setup

setup(name='lpi_python',
      version='1.0',
      description='Python implementation of local permutation invariant distanc (LPI), adjusted error and approximation of mean in terms of LPI',
      author='Marcus Voss',
      author_email='marcus.voss@dai-labor.de',
      license=' BSD 3 clause',
      python_requires=">=3",
      install_requires = ['numpy','scipy','pytest'],
      packages=['lpi_python'],
      zip_safe=False)