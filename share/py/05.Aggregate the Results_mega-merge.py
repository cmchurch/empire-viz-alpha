
# coding: utf-8

# In[20]:

#CHRISTOPHER CHURCH
#ASSISTANT PROFESSOR OF HISTORY
#UNIVERSITY OF NEVADA, RENO

'''This script reads in the KWIC files and generates a count of all the terms to be used in geocoding.py'''

import codecs
import os
import unicodecsv
import pandas as pd

read_dir = "I:/Dropbox/NDAD/Visualizing-Empire/OpeNER/Output/kwic/kwic-merged/kwic-cleaned/"
write_dir = "I:/Dropbox/NDAD/Visualizing-Empire/OpeNER/Output/aggregate/all/"

for filename in os.listdir(read_dir):
    df = pd.read_csv(read_dir+filename, sep='\t')
    counts = df['TERM'].value_counts()
    


# In[22]:

years = df.groupby('source_year')['TERM'].value_counts()
for x in range(1880,1900):
    years[x].to_csv(write_dir+str(x)+'.tsv',sep="\t")


# In[ ]:



