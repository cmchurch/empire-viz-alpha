
# coding: utf-8

# In[2]:

import os
import codecs
from unidecode import unidecode


# In[3]:

os.chdir("I:/Dropbox/NDAD/Visualizing-Empire/TopicModeling")

lexique_list_path = "data/lexique-3/lexique.txt"
lexique_words = []
with codecs.open(lexique_list_path,"r",encoding="utf8") as f:
    for line in f:
        lexique_words.append(unidecode(line.rstrip()))
print "Loaded lexique filter list: ", lexique_words[:15]    
lexique_words=set(lexique_words)


# In[ ]:




# In[4]:

#adapted from PETER NORVIG SPELLCHECKER (http://norvig.com/spell-correct.html)
import re, collections, csv
from math import log

alphabet = 'abcdefghijklmnopqrstuvwxyzùàâûüæçéèêëïîôœABCDEFGHIJKLMNOPQRSTUVWXYZÙÀÂÛÜÆÇÉÈÊËÏÎÔŒ'
alpharegex = r"[" + re.escape(alphabet) + r"]\S+"
trained_data_path = os.path.join('data', 'lexique-3','lexique-with-freq.tsv')

def readgrams(f):
    with open(f,'r') as tsvin:
        tsvin = csv.reader (tsvin, delimiter="\t")
        model = collections.defaultdict(lambda: 1)
        for row in tsvin:
            #print row[0],row[1]
            model[row[0]]+=float(row[1])
        return model
    
NWORDS = readgrams(trained_data_path)

def edits1(word):
    splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
    replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts    = [a + c + b     for a, b in splits for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)


# In[5]:

CORPUS_PATH = os.path.join('data', 'jdv_cleaned_utf-8')
filenames = sorted([os.path.join(CORPUS_PATH, fn) for fn in os.listdir(CORPUS_PATH)])
print "Loaded data filenames: ", filenames[:2]    


# In[6]:

from nltk.tokenize import word_tokenize

for filename in filenames:
    revised_tokens=[]
    discarded_tokens = []
    revised_text=""
    corrected=0
    with codecs.open(filename,"r",encoding="utf8") as f:
        text = f.read().replace("'"," ").replace("."," ").replace("-"," ")
    tokens = word_tokenize(text)
    token_count = float(len(tokens))
    print token_count, " tokens loaded."
    
    for index,token in enumerate(tokens):
        if index%200 ==0: #keep the user updated about status
            try:
                print '\r ' + filename + " " + str(index/token_count*100) +"% done: " + str(index) + " out of " + str(token_count) + "corrected: " + str(corrected),
            except:
                pass       
        if token[0].isupper() or token.lower() in lexique_words:
            revised_tokens.append(token)
        elif any(c.isalpha() for c in token): #see if it is just numbers
            token = token.encode('utf8')
            corrected_token = correct(token).decode('utf8')
            if unidecode(corrected_token) in lexique_words:
                corrected+=1
                revised_tokens.append(corrected_token)
        else:
            discarded_tokens.append(token)
    revised_text = " ".join(revised_tokens)
    outpath = "data/jdv_filtered_utf-8/"
    basename = os.path.basename(filename)+".filtered"
    with codecs.open(outpath+basename,"w",encoding="utf8") as f:
        f.write(revised_text)
    discarded_set = set(discarded_tokens)


# In[ ]:

discarded_set = set(discarded_tokens)
for word in discarded_set:
    print word


# In[ ]:

len(discarded_tokens)


# In[ ]:

len(tokens)


# In[ ]:



