
# coding: utf-8

# In[1]:

#CHRISTOPHER M. CHURCH
#ASSISTANT PROFESSOR OF HISTORY
#UNIVERSITY OF NEVADA, RENO

'''This script will generate a hexbin heatmap based on the locations identified from the NER.'''

import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib import cm as cm
from matplotlib.colors import ListedColormap
import os
import unicodecsv


#convert to meters for hexbin
def convert_lon_lat_points_to_meters_using_transform(points, tran):
    # maybe there is a better way to get long/lat into meters but this works ok
    return np.array([tran(long,lat) for long,lat in points])

#make a custom colormap
def make_colormap(seq):
    """Return a LinearSegmentedColormap
    seq: a sequence of floats and RGB-tuples. The floats should be increasing
    and in the interval (0,1).
    """
    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
    return mcolors.LinearSegmentedColormap('CustomMap', cdict)


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
import matplotlib.colors as mcolors
c = mcolors.ColorConverter().to_rgb
cmap = make_colormap([c('blue'),c('darkblue')])

#cmap = cm.OrRd

# Get the colormap colors
my_cmap = cmap(np.arange(cmap.N))

# Set alpha
my_cmap[:,-1] = np.linspace(0, 1, cmap.N)

# Create new colormap
my_cmap = ListedColormap(my_cmap)

# make plot using hexbin
bins = 200
CS = m.hexbin(points[:,0],points[:,1],gridsize=bins,cmap=my_cmap)
#m.colorbar(location="bottom",label="Z") # draw colorbar

plt.title('Places Mentioned in the Journal Day Voyages')
plt.gcf().set_size_inches(8,5)
plt.show()


# In[ ]:




# In[ ]:



