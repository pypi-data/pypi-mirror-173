# poliduckie_segmentation
[![PyPI version](https://badge.fury.io/py/poliduckie_segmentation.svg)](https://badge.fury.io/py/poliduckie_segmentation)


A package ready to be installed that provides the work made by the Poliduckie team

### Example for segmentation
```python
from poliduckie_segmentation.segmentation import Segmentation

image = [...]
segmentation = Segmentation()

# To predict:
prediction = segmentation.predict(image)

# To get the model:
segmentation.get_model()

# To get the model summary:
segmentation.get_model_summary()

```

### Example for MPC
```python
from poliduckie_segmentation.control import MPC

M = MPC()

# x = state, r = reference (with N=10 be like r=[[0.1, 0.1]]*10)
next_action = M.mpc(x, r)

```
