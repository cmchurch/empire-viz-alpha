
# coding: utf-8

# In[ ]:

#CHRISTOPHER M. CHURCH
#ASSISTANT PROFESSOR OF HISTORY
#UNIVERSITY OF NEVADA, RENO

'''This script will generate a hexbin heatmap based on the locations identified from the NER.

This is a fork of the original map test that explodes out the points, so that hexbin counts them all, rather than using weighting.
Weighting was messing up the results due to some normalization algorithm I couldn't find documentation for.

This isn't elegant, but it works.'''


#make sure to set these two variables before running
exclude_France="True" #do we want to exclude france from the results? (False=no; True=yes)
bins=60 #how many bins?


import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib import cm as cm
from matplotlib.colors import ListedColormap
import os
import unicodecsv
from shapely.geometry.polygon import Polygon
from shapely.geometry.point import Point
from shapely.geometry import MultiPoint


#convert to meters for hexbin
#def convert_lon_lat_points_to_meters_using_transform(points, tran):
    # maybe there is a better way to get long/lat into meters but this works ok
#    return np.array([tran(lon,lat) for lon,lat,size in points])

#convert to meters for hexbin
def convert_lon_lat_points_to_meters_using_transform(points, tran):
    # maybe there is a better way to get long/lat into meters but this works ok
    l = []
    for lon,lat in points:
        transform = tran(lon,lat)
        l.append([transform[0],transform[1]])
    return np.array(l)

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

#define an isnumber function to see if LAT,LON exist and to avoid error
def isnumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#set working directory
wd = "I:/Dropbox/NDAD/Visualizing-Empire/OpeNER/Output/geocode"
output_dir="I:/Dropbox/NDAD/Visualizing-Empire/OpeNER/Output/map/"
shape_file = "I:/Dropbox/NDAD/Visualizing-Empire/OpeNER/GADM-Shape-Files/FRA_adm0"
#wd = "F:/Dropbox/NDAD/Visualizing-Empire/OpeNER/test"
os.chdir(wd)             

#set matplotlib render settings
#%matplotlib notebook
#%matplotlib qt
#%matplotlib inline


#get latlons

filename="1880-p1-test.csv.geocoded.csv"
for filename in os.listdir('.'):
    if filename.endswith('.KWIC.tsv.aggregated.tsv.geocoded.csv'):
        with open(filename,'r') as f:
            year=filename[0:4]
            size=[]
            lat=[]
            lon=[]
            flags=str(bins)+ "-bins"
            cfile = unicodecsv.reader(f,delimiter=",")
            next(cfile)  # skip the headers
            
            
            # Create the map with the miller projection
            m = Basemap(projection='mill',lon_0=0)

            #get shape file of France to check if files inside
           
            if exclude_France=="True":
                m.readshapefile(shape_file,'France')

                for shape in m.France:
                    if shape == m.France[0]:
                        poly = MultiPoint(shape).convex_hull
                    else:
                        poly = poly.union(MultiPoint(shape).convex_hull)

                for row in cfile:
                    if isnumber(row[1]) and isnumber(row[2]) and isnumber(row[3]):
                        x=float(row[3])
                        y=float(row[2])
                        po = Point(m(x,y))
                        if not poly.contains(po):
                            for i in range(0,int(row[1])):
                                lat.append(y)
                                lon.append(x)
            else:
                for row in cfile:
                    if isnumber(row[1]) and isnumber(row[2]) and isnumber(row[3]):
                        for i in range(0,int(row[1])):
                            lat.append(float(row[2]))
                            lon.append(float(row[3]))



            #make figure
            fig = plt.figure(figsize=(12,5))

           
            #x,y = poly.exterior.xy
            
            #draw label meridians and parallels.
            #m.drawparallels(np.arange(-90,90,30),labels=[1,0,0,0])
            #m.drawmeridians(np.arange(map.lonmin,map.lonmax+30,60),labels=[0,0,0,1])

            # fill continents 'lightgray' (with zorder=0), color wet areas 'lightblue'
            #m.drawmapboundary(fill_color='lightblue')
            #m.fillcontinents(color='lightgray',lake_color='lightblue')

            # plot coastlines
            m.drawcoastlines(linewidth="0.1")

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
            #adjusted color map for legibility
            cmap = make_colormap([c('#FFFFFF'),c('#A83E3E'),0.5,c('#A83E3E'),c('#690303')])
            #straight linear colormap
            #cmap = make_colormap([c('white'),c('darkred')])

            # make plot using hexbin
            CS = m.hexbin(x=points[:,0],y=points[:,1],gridsize=bins,cmap=cmap) #without weighting -- weighting comes from list explosion
            m.colorbar(location="bottom",label="mentions in bin") # draw colorbar

            if exclude_France=="True":
                flags+="_France-excluded"
            else:
                flags+="_France-included"
            plt.title('Locations Mentioned in the Journal Day Voyages: '+year+"\n"+flags)
            fig.set_size_inches(11,8.5)
            outfile=output_dir+flags+year+".png"
            fig.savefig(outfile)
            print "Saved: "+ outfile
            plt.close(fig)
print "Done!"

