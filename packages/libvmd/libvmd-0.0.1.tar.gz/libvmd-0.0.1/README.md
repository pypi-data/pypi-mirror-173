# LIBVMD: Python library for variational mode decomposition for both 1D and 2D

This package's functions are translations of MATLAB source codes by Dragomiretskiy and Zosso (2013; 2015)

Related source codes and articles are as below

vmd: [MATLAB code](https://www.mathworks.com/matlabcentral/fileexchange/44765-variational-mode-decomposition), [Article](https://link.springer.com/chapter/10.1007/978-3-319-14612-6_15)

vmd2: [MATLAB code](https://www.mathworks.com/matlabcentral/fileexchange/45918-two-dimensional-variational-mode-decomposition), [Article](https://link.springer.com/chapter/10.1007/978-3-319-14612-6_15)

## Installation

```
pip install libvmd
```
or
```
git clone https://github.com/hyoddubi1/libvmd
setup.py install
```

## Example codes

1-dimensional VMD

```python
from libvmd.vmd import vmd
```

2-dimensional VMD

```python
from libvmd.vmd import vmd2
```
