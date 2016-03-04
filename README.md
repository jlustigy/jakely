# jakely
A suite of simple python tools that I use regularly

-------------

## Examples

```python
import jakely
```

#### Hexbin Dots

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

# Create figure for hexbin dots
fig = plt.figure(figsize=(10,14))
gs = gridspec.GridSpec(3,1, height_ratios=[0.1,1,0.1])
ax = plt.subplot(gs[1])
cbar_ax1 = plt.subplot(gs[0])
cbar_ax2 = plt.subplot(gs[2])

# Add hexbin dots to figure
jakely.plot.hexbin_dots(x, y, z, ax, cbar_ax1, cbar_ax2)

fig.tight_layout()
```
<img src="https://github.com/jlustigy/jakely/blob/master/examples/example_hexbin_dots1.png" width="50%" height="50%" align="middle" />
