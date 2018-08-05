import matplotlib.pyplot as plt
import numpy as np

#Vars
#

#Curve classes
#Base curve class
class Curve:
	def __init__(self, xmin, xmax, ymin, ymax, border, step, x='', y=''):
		self.xmin, self.xmax = xmin, xmax
		self.step = step
		self.domain = domain = np.arange(xmin + border, xmax - border, step)
		if type(x) == str and type(y) == str:
			self.x = x = domain
			self.y = y = domain
		else: self.x, self.y = x, y
		self.points = [x, y]
		self.endpoints = ([ x[0] , y[0] ] , [ x[-1] , y[-1] ])
		self.label = 'Default'

#Supply curve class
class Supply(Curve):
	def __init__(self, *args, **kwargs):
		super(Supply, self).__init__(*args, **kwargs)
		x = self.x
		xmax = self.xmax
		self.y = y = (lambda x, xmax: 3 + ((x+3)**2)/xmax)(x, xmax)
		self.endpoints = ([ x[0] , y[0] ] , [ x[-1] , y[-1] ])
		self.points = [x, y]
		self.label = 'Supply'
		

#Demand curve class
class Demand(Curve):
	def __init__(self, *args, **kwargs):
		super(Demand, self).__init__(*args, **kwargs)
		x = self.x
		xmax = self.xmax
		self.y = y = (lambda x, xmax: xmax - (3 + ((x+3)**2)/xmax))(x, xmax)
		if not len(x) + len(y) < 4:
			self.endpoints = ([ x[0] , y[0] ] , [ x[-1] , y[-1] ])
		else:
			self.endpoints = None
		self.points = [x, y]
		self.label = 'Demand'


#Plotting functions
#Plots a curve with endpoints
def plot(curve, color):
	plt.plot(*curve.points, color)
	if not color.endswith('o'):
		for i in range(2): 
			plt.plot(*curve.endpoints[i], color + 'o')

#Add x, y labels and a title
def format(xlabel = '', ylabel = '', title='', grid=True):
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)
	plt.grid(grid)

#Plot the intersection(s) between two curves
def intersection(curve1, curve2, prefs):
	i = np.argwhere(np.isclose(curve1.y, curve2.y, atol=curve2.step)).reshape(-1)
	return Curve(x=curve1.x[i], y=curve1.y[i], **prefs)
	

#Plots all curves in dict
def plotdict(args):
	if 'style' in args:
		format(**args['style'])

	for i in args:
		if i != 'style':
			plot(i, args[i][1])
			plt.text(*i.endpoints[1],args[i][0])
	plt.show()


""" Example.py
#Generates a simple Supply-Demand curve
from widgets import *

prefs = {
	'xmin':0 
	'xmax':50
	'ymin':0
	'ymax':50
	'border':3
	'step':.01
}

#Curves
S = Supply(**prefs)
D = Demand(**prefs)

#Unused example curve
example = { S:[ r'Label', 'color'] }

#Format: 
#
#args = { 
#	'style': {STYLE DICT}, 
#	curve_1 : [ r'Label', 'color' ],
#	curve_2 : [ r'Label', 'color' ],
#	curve_n : [ r'Label', 'color' ]
#}
#

curves = { 
	S:[ r'$S_0$', 'g' ], 
	D:[ r'$D_0$', 'b'] 
}

style = { 
	'style':{ 
		'xlabel':'Quantity', 
		'ylabel':'Price', 
		'title':'Widgets', 
		'grid':1 
	} 
}

#Updates dictionary with intersection of two curves
curves.update({intersection(S,D):['','ko']})

#Combines the style and curves into one dict arg and then plots it.
args = dict()
for i in [curves, style]: args.update(i)
plotdict(args)

"""


