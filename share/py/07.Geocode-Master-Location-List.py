
# coding: utf-8

# In[1]:

#CHRISTOPHER CHURCH
#ASSISTANT PROFESSOR OF HISTORY
#UNIVERSITY OF NEVADA, RENO

"""This script will geocode the facets exported from OpenRefine (i.e. the locations identified through OpeNER).
It uses the python module https://geocoder.readthedocs.io/"""

import geocoder
import codecs
import os
import unicodecsv
import requests
read_dir = "I:/Dropbox/NDAD/Visualizing-Empire/OpeNER/Output/geocode/"
write_dir = read_dir

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


# In[ ]:

import sys

filename = "location.masterlist2.tsv"
session = requests.Session() #having a single session should speed up the API requests
count=0
starting_point = 34256
length = file_len(read_dir+filename)

with codecs.open(read_dir+filename,'r',encoding="utf8") as locations:
    output = codecs.open(write_dir+filename+".geocoded.csv","a",encoding="utf8")
    #output.write("LOC,LAT,LON\n") #comment to stop from adding the headers
    
    for location in locations:
        count = count+1
        print "\r","geocoding " + str(count) + " out of " +str(length), #status indicator
        if count < starting_point: continue #skip to pick up where left off
        location = location.rstrip('\r\n')
        #g=geocoder.google(location)  #google also includes g.city,g.state,g.country,
        
        for attempt in range(10):
            try:
                g = geocoder.arcgis(location)
                break
            except:
                continue
        else:
            print "Network Connection Timeout - Failed after 10 attempts"
            sys.exit(1)
    
        if g.latlng:
            lat = g.latlng[0]
            lon = g.latlng[1]
        else:
            lat=''
            lon=''
        l=[unicode(location),lat,lon]
        export_text=",".join(unicode(x) for x in l)+"\n"
        output.write(export_text)
        #print l
    output.close()


# In[17]:

output.close()


# In[ ]:



