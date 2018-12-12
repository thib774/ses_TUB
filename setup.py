from setuptools import setup

setup(name='ses_TUB',
      version='1.0',
      description='Python implementation of usefull data for Smart Energy Systems course at TU Berlin',
      author='Marcus Voss',
      author_email='marcus.voss@dai-labor.de',
      license=' BSD 3 clause',
      python_requires=">=3",
      install_requires = ['numpy','scipy','pytest','sklearn','pandas'],
      packages=['features', 'quantile', 'lpi_distance'],
      zip_safe=False)
