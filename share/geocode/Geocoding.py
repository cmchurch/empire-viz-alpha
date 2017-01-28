
# coding: utf-8

# In[46]:

#CHRISTOPHER CHURCH
#ASSISTANT PROFESSOR OF HISTORY
#UNIVERSITY OF NEVADA, RENO

"""This script will geocode the facets exported from OpenRefine (i.e. the locations identified through OpeNER).
It uses the python module https://geocoder.readthedocs.io/"""

import geocoder
import codecs
import os
import unicodecsv
wd = "I:/Dropbox/NDAD/Visualizing-Empire/OpeNER/test"
os.chdir(wd)

filename="1880-p1-test.csv"


# In[ ]:

with open(filename,'r') as f:
    cfile = unicodecsv.reader(f,delimiter=",")
    output = codecs.open(filename+".geocoded.csv","w",encoding="utf8")
    output.write("LOC,FREQ,LAT,LON\n")
    for row in cfile:
        #g=geocoder.google(row[0])  #google also includes g.city,g.state,g.country,
        g=geocoder.arcgis(row[0])
        if g.latlng:
            lat = g.latlng[0]
            lon = g.latlng[1]
        l=[unicode(row[0]),row[1],lat,lon]
        export_text=",".join(unicode(x) for x in l)+"\n"
        output.write(export_text)
        print "OUTPUT: "+export_text,
    output.close()


# In[50]:

output.close()


# In[ ]:



