# Fast ELM Kernel
This package provides fast calculation of an Extreme Learning Machine kernel.

## Usage
`pip install fast-elm-kernel`

```python
from fast_elm_kernel import elm_kernel_vec, elm_kernel
import numpy as np

# Note that for vector operations elm_kernel_vec is prefered and faster

X = np.array([
  [17, 24, 1, 8, 15],
  [23, 5, 7, 14, 16],
  [4, 6, 13, 20, 22],
  [10, 12, 19, 21, 3],
  [11, 18, 25, 2, 9]
])

print(elm_kernel(X, X))

print(elm_kernel_vec(np.array([1, 2, 3]), np.array([100, 0.5, 0.3])))

```