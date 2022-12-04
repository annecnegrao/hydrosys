import pygrib
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.ticker import MaxNLocator

folder = './gribs/'
datai = dt.date(2015,2,1)
dataf = dt.date(2015,3,31)
lonmin = -71.
lonmax = -67.
latmin = -12.
latmax = -8.

def plot_grid(lons, lats, grid, lonmin, lonmax, latmin, latmax):
	levels = MaxNLocator(nbins=15).tick_values(grid.min(), grid.max())
	# Colormap
	# cmap = plt.get_cmap('plasma')
	cmap = plt.get_cmap('hsv')
	newcolors = cmap(np.linspace(0.5,1,15))
	branco = np.array([1., 1., 1., 1.])
	newcolors[:1, :] = branco
	newcmp = ListedColormap(newcolors)
	axis_font = {'size':'8'} #'fontname':'Arial',
	# Normalization
	norm = BoundaryNorm(levels, ncolors=newcmp.N, clip=True)
	# Create a new figure.
	fig = plt.figure(1, figsize=(16, 8)) #inches
	# Add axes rect = [left, bottom, width, height]
	ax0 = plt.axes([0.125,0.1,0.78,0.75], facecolor='w')
	# Create a pseudocolor plot with a non-regular rectangular grid.
	#im = ax0.pcolormesh(lon, lat, precip, cmap=cmap, norm=norm)
	im = ax0.pcolormesh(lons, lats, grid, cmap=newcmp, vmin=0, vmax=60, shading='auto')
	estados = pd.read_csv('estadosBrasil.csv')
	plt.plot(estados.longitude, estados.latitude, color='k', linewidth=1.5)
	bacia = pd.read_csv('ottobacia_RioAcre_WGS84_Points.csv')
	plt.plot(bacia.longitude, bacia.latitude, color='r', linewidth=1.5)
	# Configure the grid lines.
	plt.grid(True, which='both')
	# Plot limits
	plt.xlim(lonmin, lonmax)
	plt.ylim(latmin, latmax)
	# Get the current axes and set the aspect of the scaling
	plt.gca().set_aspect('equal', adjustable='box')
	# Título
	dia = dt.datetime.strftime(data,'%Y-%m-%d')
	plt.title(f'Precipitação (mm/dia) INPE-MERGE {dia}', fontsize = 12)
	plt.xlabel('Longitude [degrees]')
	plt.ylabel('Latitude [degrees]')
	# Colorbar
	fig.colorbar(im, ax=ax0)
	plt.savefig(f'./plots/{dia}.png', bbox_inches='tight')
	fig.clear()
	#plt.show()
	return


'''
for grb in grbs:
    print(grb)

print(grb.keys())

grbs.rewind()

for grb in grbs:
    print(grb.validDate)
    print(grb.parameterName)

grbs.rewind()

for grb in grbs:
    lats, lons = grb.latlons()
    grid = grb.values
    print(lats, lons)
    print(grid)
'''

dias = pd.date_range(datai, dataf)
for dia in dias:
	strdia = dt.datetime.strftime(dia, '%Y%m%d')
	file = f'MERGE_CPTEC_{strdia}.grib2'
	grbs = pygrib.open(folder + file)
	grb = grbs[1]
	lats, lons = grb.latlons()
	grid = grb.values
	data = grb.validDate
	#print(data)
	# Convertendo range da longitude de 0:360 para -180:180
	lons = lons - 360
	#print(grid.shape)
	plot_grid(lons, lats, grid, lonmin, lonmax, latmin, latmax)

print('Fim! =D')