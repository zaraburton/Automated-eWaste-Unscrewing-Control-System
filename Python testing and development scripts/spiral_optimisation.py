#SPRIAL OPTIMISATION PLOTTING

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection
from pylab import *
import math
from scipy.integrate import odeint

def circles(x, y, s, c='b', vmin=None, vmax=None, **kwargs):
	"""
	Make a scatter of circles plot of x vs y, where x and y are sequence 
	like objects of the same lengths. The size of circles are in data scale.

	Parameters
	----------
	x,y : scalar or array_like, shape (n, )
		Input data
	s : scalar or array_like, shape (n, ) 
		Radius of circle in data unit.
	c : color or sequence of color, optional, default : 'b'
		`c` can be a single color format string, or a sequence of color
		specifications of length `N`, or a sequence of `N` numbers to be
		mapped to colors using the `cmap` and `norm` specified via kwargs.
		Note that `c` should not be a single numeric RGB or RGBA sequence 
		because that is indistinguishable from an array of values
		to be colormapped. (If you insist, use `color` instead.)  
		`c` can be a 2-D array in which the rows are RGB or RGBA, however. 
	vmin, vmax : scalar, optional, default: None
		`vmin` and `vmax` are used in conjunction with `norm` to normalize
		luminance data.  If either are `None`, the min and max of the
		color array is used.
	kwargs : `~matplotlib.collections.Collection` properties
		Eg. alpha, edgecolor(ec), facecolor(fc), linewidth(lw), linestyle(ls), 
		norm, cmap, transform, etc.

	Returns
	-------
	paths : `~matplotlib.collections.PathCollection`

	Examples
	--------
	a = np.arange(11)
	circles(a, a, a*0.2, c=a, alpha=0.5, edgecolor='none')
	plt.colorbar()

	License
	--------
	This code is under [The BSD 3-Clause License]
	(http://opensource.org/licenses/BSD-3-Clause)
	"""
	import numpy as np
	import matplotlib.pyplot as plt
	from matplotlib.patches import Circle
	from matplotlib.collections import PatchCollection

	if np.isscalar(c):
		kwargs.setdefault('color', c)
		c = None
	if 'fc' in kwargs: kwargs.setdefault('facecolor', kwargs.pop('fc'))
	if 'ec' in kwargs: kwargs.setdefault('edgecolor', kwargs.pop('ec'))
	if 'ls' in kwargs: kwargs.setdefault('linestyle', kwargs.pop('ls'))
	if 'lw' in kwargs: kwargs.setdefault('linewidth', kwargs.pop('lw'))

	patches = [Circle((x_, y_), s_) for x_, y_, s_ in np.broadcast(x, y, s)]
	collection = PatchCollection(patches, **kwargs)
	if c is not None:
		collection.set_array(np.asarray(c))
		collection.set_clim(vmin, vmax)

	ax = plt.gca()
	ax.add_collection(collection)
	ax.autoscale_view()
	if c is not None:
		plt.sci(collection)
	return collection



## Creating spiral points
z = 0.9
# lists to store x and y axis points 
xdata, ydata = [0], [0] 
x2data, y2data = [0], [0] 



# get data points 


#green !!

for i in range(0,30): 



	#ARCHIMEDES SPIRAL
	r = 0.1*i
	
	# x, y values to be plotted 
	x = r*np.sin(i) 
	y = r*np.cos(i) 

	# appending new points to x, y axes points list 
	xdata.append(x) 
	ydata.append(y) 


## 2. appending over existing point 

# combining into one array of all spiral points
sp0 = np.vstack((xdata, ydata)).T
# removing first point
sp = sp0[1:20]


current_position = [0,0]

# array of 19 same positions to add to spiral coords
cp = np.tile(current_position, (19,1))


## 3. making figure
figure(figsize=(5,4))
ax=subplot(aspect='equal')
ax.set_xlabel('(mm)')
ax.set_ylabel('(mm)')

# first spiral
circles(xdata, ydata, 0.45, c='g', alpha=0.1, edgecolor='none')
plt.plot(xdata, ydata, c='#CC684C',alpha=0.2)
plt.scatter(xdata, ydata, c='#CC684C')



plt.show()







