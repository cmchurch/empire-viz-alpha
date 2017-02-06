
# coding: utf-8

# In[48]:

#CHRISTOPHER M. CHURCH
#ASSISTANT PROFESSOR OF HISTORY
#UNIVERSITY OF NEVADA, RENO

'''this script will read in the KWICs created by KafNafParser.py, which were separated into two parts matching the original
PDFs to avoid overflows in Java using OpeNER. The files produced by the script will then be read by "Aggregate the Results.py"
and fed into "geocoding.py"'''

import codecs
import os
import unicodecsv
import pandas as pd
wd = "I:/Dropbox/NDAD/Visualizing-Empire/OpeNER/Output/kwic"
os.chdir(wd)

f_by_y = {}


for f in os.listdir('.'): #walk through the working directory and look for KAF files
    if f.endswith('.KWIC.tsv'):
        year = f[0:4]
        if str(year) in f_by_y:
            f_by_y[str(year)].append(f)
        else:
            f_by_y[str(year)]=[f]


# In[68]:

keys = f_by_y.keys()

combined_dfs=[]

for key in keys:
    csvs = []
    for idx,f in enumerate(f_by_y[key]):
        csv = pd.read_csv(f, sep='\t')
        csv ['source_year']=key+"-"+str(idx+1)
        csvs.append(csv)
    df = pd.concat(csvs)
    df.to_csv("kwic-merged/"+key+".KWIC.tsv",sep="\t")

