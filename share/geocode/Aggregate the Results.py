
# coding: utf-8

# In[1]:

#CHRISTOPHER CHURCH
#ASSISTANT PROFESSOR OF HISTORY
#UNIVERSITY OF NEVADA, RENO

'''This script reads in the KWIC files and generates a count of all the terms to be used in geocoding.py'''

import codecs
import os
import unicodecsv
wd = "I:/Dropbox/NDAD/Visualizing-Empire/OpeNER/test"
os.chdir(wd)
filename="1880-p1-txt-NER-kaf-KWIC-tsv-minimally-cleaned-for-test.tsv"

import pandas as pd
df = pd.read_csv(filename, sep='\t')
counts = df['TERM'].value_counts()
with codecs.open(filename+"aggregated.tsv",'w',encoding="utf8") as f:
    for key in counts.keys():
        f.write(key.decode('utf8')+"\t"+str(counts[key])+"\n")

