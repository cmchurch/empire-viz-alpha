
# coding: utf-8

# In[7]:

#CHRISTOPHER M. CHURCH
#ASSISTANT PROFESSOR OF HISTORY
#UNIVERSITY OF NEVADA, RENO

'''This script will generate a hexbin heatmap based on the locations identified from the NER.'''

import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib import cm as cm
from matplotlib.colors import ListedColormap
import matplotlib.pylab as pl
import os
import unicodecsv


#convert to meters for hexbin
def convert_lon_lat_points_to_meters_using_transform(points, tran):
    # maybe there is a better way to get long/lat into meters but this works ok
    return np.array([tran(long,lat) for long,lat in points])

#set working directory
wd = "I:/Dropbox/NDAD/Visualizing-Empire/OpeNER/test"
#wd = "F:/Dropbox/NDAD/Visualizing-Empire/OpeNER/test"
os.chdir(wd)             

#set matplotlib render settings
#%matplotlib notebook
#%matplotlib qt
#%matplotlib inline

# miller projection
m = Basemap(projection='mill',lon_0=0)

#make figure
fig = plt.figure(figsize=(12,5))


#draw label meridians and parallels.
#m.drawparallels(np.arange(-90,90,30),labels=[1,0,0,0])
#m.drawmeridians(np.arange(map.lonmin,map.lonmax+30,60),labels=[0,0,0,1])

# fill continents 'lightgray' (with zorder=0), color wet areas 'lightblue'
#m.drawmapboundary(fill_color='lightblue')
#m.fillcontinents(color='lightgray',lake_color='lightblue')

# plot coastlines
m.drawcoastlines(linewidth="0.1")

#get latlons
points =[]
size=[]
lat=[]
lon=[]
filename="1880-p1-test.csv.geocoded.csv"
with open(filename,'r') as f:
    cfile = unicodecsv.reader(f,delimiter=",")
    next(cfile, None)  # skip the headers
    for row in cfile:
        #points.append([int(row[1]),float(row[2]),float(row[3])]) #size,lat,lon
        size.append(int(row[1]))
        lat.append(float(row[2]))
        lon.append(float(row[3]))

#translate lat lon into map coordinates (meters) based on map projection
points=zip(lon,lat)
points = convert_lon_lat_points_to_meters_using_transform(points, m.projtran)

#add points to map
#m.plot(x, y, 'ko', markersize=1)
#m.plot(points[:,0],points[:,1], 'ko', markersize=1)

#add alpha transparency to color ramp
# Choose colormap
cmap = pl.cm.OrRd

# Get the colormap colors
my_cmap = cmap(np.arange(cmap.N))

# Set alpha
my_cmap[:,-1] = np.linspace(0, 1, cmap.N)

# Create new colormap
my_cmap = ListedColormap(my_cmap)

# make plot using hexbin
bins = 100
CS = m.hexbin(points[:,0],points[:,1],gridsize=bins,cmap=my_cmap)
#m.colorbar(location="bottom",label="Z") # draw colorbar

plt.title('Places Mentioned in the Journal Day Voyages')
plt.gcf().set_size_inches(8,5)
plt.show()

