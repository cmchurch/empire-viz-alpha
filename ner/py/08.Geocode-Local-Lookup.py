
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
read_dir = "I:/Dropbox/NDAD/Visualizing-Empire/OpeNER/Output/aggregate/"
write_dir = "I:/Dropbox/NDAD/Visualizing-Empire/OpeNER/Output/geocode/"
master_list_dir = "I:/Dropbox/NDAD/Visualizing-Empire/OpeNER/Output/geocode/"


# In[13]:

#load master lookup as a dictionary for reference below
filename = "location.masterlist.tsv.geocoded.csv"
lookup={}
with open(master_list_dir+filename,'r') as f: 
    locations = unicodecsv.reader(f,delimiter=",")
    locations.next() #skip the headers
    for location in locations: #build a lookup dictionary for all locations
         lookup[location[0]]=[float(location[1]),float(location[2])]


# In[21]:

#compare aggregate lists against the local geocoded list (gazetteer)
for filename in os.listdir(read_dir):
    with open(read_dir+filename,'r') as f:
        print "geocoding " + filename,
        cfile = unicodecsv.reader(f,delimiter="\t")
        output = codecs.open(write_dir+filename+".geocoded.csv","w",encoding="utf8")
        output.write("LOC,FREQ,LAT,LON\n")
        for row in cfile:
            term = row[0]
            #g=geocoder.google(row[0])  #google also includes g.city,g.state,g.country,
            if term=="(": continue #this line added because of dirty data during test run, will be removed once data is cleaned
            if term in lookup.keys():
                lat = lookup[term][0]
                lon = lookup[term][1]
            else:
                lat = ''
                lon = ''
            l=[unicode(row[0]),row[1],lat,lon]
            export_text=",".join(unicode(x) for x in l)+"\n"
            output.write(export_text)
            print ".",
        print
        output.close()

