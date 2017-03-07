
# coding: utf-8

# In[ ]:

import multiprocessing #import the multiprocessing library
import operator #import the operator library (used during the reduce function)
import os
import codecs
from unidecode import unidecode
import re, collections, csv
from math import log
import sys

def readgrams(f):
        with open(f,'r') as tsvin:
            tsvin = csv.reader (tsvin, delimiter="\t")
            model = collections.defaultdict(lambda: 1)
            for row in tsvin:
                #print row[0],row[1]
                model[row[0]]+=float(row[1])
            return model

def edits1(word):
    alphabet = 'abcdefghijklmnopqrstuvwxyzùàâûüæçéèêëïîôœABCDEFGHIJKLMNOPQRSTUVWXYZÙÀÂÛÜÆÇÉÈÊËÏÎÔŒ'
    alpharegex = r"[" + re.escape(alphabet) + r"]\S+"
    splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
    replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts    = [a + c + b     for a, b in splits for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

def known_edits2(word,NWORDS):
	return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words,NWORDS): return set(w for w in words if w in NWORDS)

def correct(word,NWORDS):
	candidates = known([word],NWORDS) or known(edits1(word),NWORDS) or known_edits2(word,NWORDS) or [word]
	return max(candidates, key=NWORDS.get)

def chunker(tokens, chunks):
    '''this function -- generator -- chunks a set of tokens based on a number of chunks; each "chunk" of tokens will be sent to a separate process'''
    length = len(tokens) #the total number of tokens in the original
    chunk_size = len(tokens) / chunks #the size of each chunk (num of tokens / chunk)
    for x in xrange(0, length, chunk_size): #go through the original tokens in an increment equal to the size of each chunk
        yield tokens[x:x+chunk_size] #and return subsets equal to the size of the chunks

def worker(tokens):
    '''worker function for each process in the pool -- receives a chunk of tokens (tokens) and returns that chunk uppercase'''
    os.chdir("F:/Dropbox/NDAD/Visualizing-Empire/TopicModeling")

    lexique_list_path = "data/lexique-3/lexique.txt"
    lexique_words = []
    revised_tokens=[]
    punctuation = [".", "," , ";", ":", "!", "?"]

    with codecs.open(lexique_list_path,"r",encoding="utf8") as f:
        for line in f:
            lexique_words.append(unidecode(line.rstrip()))
    
    trained_data_path = os.path.join('data', 'lexique-3','lexique-with-freq.tsv')
    NWORDS = readgrams(trained_data_path)
    corrected=0
    for token in tokens:
        if token[0].isupper() or token.lower() in lexique_words or token in punctuation:
            revised_tokens.append(token)
        elif any(c.isalpha() for c in token): #see if it is just numbers
            token = token.encode('utf8')
            corrected_token = correct(token, NWORDS).decode('utf8')
            if unidecode(corrected_token) in lexique_words:
                corrected+=1
                revised_tokens.append(corrected_token)
    return revised_tokens #return the chunk of tokens

def parallel_process(chunks,tokens):
    '''how many chunks do we want; equals the number of processes'''
    partitioned_text = list(chunker(tokens, chunks)) #partition the tokens up into X number of chunks [it's a nested list]
    p = multiprocessing.Pool(chunks) #create a pool of processes equal to the number of chunks
    process_text = p.map(func=worker,iterable=partitioned_text) #using map, send the partitioned_chunk nested list to the processes in the pool
    p.close() #close the pool of processes
    process_text = reduce(operator.add,process_text) #now reduce the returned chunks into a single list again
    return process_text


# In[ ]:

if __name__ == '__main__':

    os.chdir("F:/Dropbox/NDAD/Visualizing-Empire/TopicModeling")

    lexique_list_path = "data/lexique-3/lexique.txt"
    lexique_words = []
    with codecs.open(lexique_list_path,"r",encoding="utf8") as f:
        for line in f:
            lexique_words.append(unidecode(line.rstrip()))
    lexique_words=set(lexique_words)    

    CORPUS_PATH = os.path.join('data', 'jdv_cleaned_utf-8')
    filenames = sorted([os.path.join(CORPUS_PATH, fn) for fn in os.listdir(CORPUS_PATH)])

    from nltk.tokenize import word_tokenize
    from BeautifulSoup import BeautifulSoup as bs

    for filename in filenames:
        discarded_tokens = []
        corrected=0
        with codecs.open(filename,"r",encoding="utf8") as f:
            text = f.read()
        text = text.encode('utf-8').decode('ascii', 'ignore')
        soup = bs(text)
        article_tags = soup.findAll("article")
        corrected=0
        articles=[]
        article_count=len(article_tags)

        
        for index,article in enumerate(article_tags):
            tokens = word_tokenize(article.text)
            revised_tokens=[]
            print '\r Processing: ' + filename + ", " + str(index) + " out of " + str(article_count) + "(" + str(index/float(article_count)*100)+"%)",
            revised_tokens = parallel_process(2,tokens)
            article = " ".join(revised_tokens)
            article = "<article>"+article+"</article>"
            articles.append(article)
        revised_text = " ".join(articles)
        outpath = "data/jdv_filtered_utf-8/"
        basename = os.path.basename(filename)+".filtered"
        with codecs.open(outpath+basename,"w",encoding="utf8") as f:
            f.write(revised_text)
        discarded_set = set(discarded_tokens)
        print "Output success: ", filename

