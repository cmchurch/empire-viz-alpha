
# coding: utf-8

# In[2]:

#CHRISTOPHER CHURCH
#ASSISTANT PROFESSOR OF HISTORY
#UNIVERSITY OF NEVADA, RENO

"""This script will geocode the facets exported from OpenRefine (i.e. the locations identified through OpeNER).
It uses the python module https://geocoder.readthedocs.io/"""

import geocoder
import codecs
import os
import unicodecsv
read_dir = "I:/Dropbox/NDAD/Visualizing-Empire/OpeNER/Output/geocode/"
write_dir = read_dir


# In[3]:

filename = "location.masterlist.tsv"
with codecs.open(read_dir+filename,'r',encoding="utf8") as locations:
    print "geocoding " + filename,
    output = codecs.open(write_dir+filename+".geocoded.csv","w",encoding="utf8")
    output.write("LOC,LAT,LON\n")
    for location in locations:
        location = location.rstrip('\n')
        #g=geocoder.google(row[0])  #google also includes g.city,g.state,g.country,
        g=geocoder.arcgis(location)
        if g.latlng:
            lat = g.latlng[0]
            lon = g.latlng[1]
        l=[unicode(location),lat,lon]
        export_text=",".join(unicode(x) for x in l)+"\n"
        output.write(export_text)
        print l
        #        print ".",
    output.close()


# In[4]:

output.close()
print location


# In[10]:

export_text


# In[18]:

for location in locations:
    print location


# In[ ]:



