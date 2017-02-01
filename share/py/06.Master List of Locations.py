
# coding: utf-8

# In[1]:

#CHRISTOPHER M. CHURCH
#ASSISTANT PROFESSOR OF HISTORY
#UNIVERSITY OF NEVADA, RENO
import os
import unicodecsv
import codecs

'''this script generates a master list of all possible locations from the aggregate KWICs that will be fed into "geocoding.py"'''

write_dir = "I:/Dropbox/NDAD/Visualizing-Empire/OpeNER/Output/geocode/"
read_dir = "I:/Dropbox/NDAD/Visualizing-Empire/OpeNER/Output/aggregate/"

locations=[]
print "working"

for filename in os.listdir(read_dir):
    print ".",
    with open(read_dir+filename,'r') as f:
        cfile = unicodecsv.reader(f,delimiter="\t")
        for row in cfile:
            if row[0] not in locations:
                locations.append(row[0])

print "done"
    


# In[ ]:

locations


# In[5]:

print "writing."
with codecs.open(write_dir+"location.masterlist.tsv",'w',encoding="utf8") as output:
    for location in locations:
        output.write(location+"\n")
print "done."


# In[ ]:



