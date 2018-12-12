# PyForesee Local Permutation Invariant (LPI) Distance Package

## Introduction
This package contains Python implementations of the LPI distance, the adjusted p-norm error, as well the majorize minimize approximation of the mean in terms of the LPI distance.

## Install

To install package download the source and install the package using pip in the top directory. 
```
pip install .
```

Alternatively , we recommend using a conda virtual environments like that:
```
conda create -n lpi python=3.6 numpy pytest scipy
```

Then activate the virtual environment:
```
source activate lpi # Linux, or
activate lpi # Windows
```
Then in the folder pyforesee.lpi run:
```
pip install .
```

To verify the installation change into the tests directory and run pytest:
```
cd tests
pytest
```