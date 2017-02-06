
# coding: utf-8

# In[21]:

#CHRISTOPHER CHURCH
#ASSISTANT PROFESSOR OF HISTORY
#UNIVERSITY OF NEVADA, RENO

'''This script reads in the KWIC files and generates a count of all the terms to be used in geocoding.py'''

import codecs
import os
import unicodecsv
import pandas as pd

read_dir = "I:/Dropbox/NDAD/Visualizing-Empire/OpeNER/Output/kwic/kwic-merged/"
write_dir = "I:/Dropbox/NDAD/Visualizing-Empire/OpeNER/Output/aggregate/"

for filename in os.listdir(read_dir):
    df = pd.read_csv(read_dir+filename, sep='\t')
    counts = df['TERM'].value_counts()
    with codecs.open(write_dir+filename+".aggregated.tsv",'w',encoding="utf8") as f:
        for key in counts.keys():
            f.write(key.decode('utf8')+"\t"+str(counts[key])+"\n")


# In[ ]:



