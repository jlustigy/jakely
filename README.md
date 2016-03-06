# jakely
A suite of simple python tools

-------------

## Examples

```python
import jakely
```

#### Hexbin Dots

Ever wanted to encode more information in a 2D density histogram? With `jakely.plot_hexbin_dots()` you can visualize intrisic properties of the points that fall within each histogram bin to trace gradients in a variable z atop an x,y density distribution.  

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec

# Set number of scatter points
N = 5000

# Generate random data
x = np.random.normal(size=N)
y = np.random.normal(size=N)
z = 10 * x  # In this example z is correlated with x

# Create hexbin dots plot
fig = plot_hexbin_dots(x,y,z, label_hex='Hex Density', label_dots='Median Value per Hex')

# Customize axes with returned figure object
ax = fig.get_axes()[2]
ax.set_xlim([-4,4]); ax.set_ylim([-4,4])
ax.set_xlabel('x [units]'); ax.set_ylabel('y [units]') 
```
<img src="https://github.com/jlustigy/jakely/blob/master/examples/example_hexbin_dots2.png" width="100%" height="100%" align="middle" />
