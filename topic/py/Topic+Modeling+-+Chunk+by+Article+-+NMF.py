
# coding: utf-8

# In[ ]:

from IPython.core.display import display,HTML
display(HTML("<style>.container { width:100% !important; }</style>")) #increase the width of the IPYTHON Cells
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# In[10]:

from BeautifulSoup import BeautifulSoup as bs
import os
import codecs

#chunk it by article to get topics by article

veronis_french_stop_words = ["Ap.", "Apr.", "GHz", "MHz", "USD", "a", "afin", "ah", "ai", "aie", "aient", "aies", "ait", "alors", "après", "as", "attendu", "au", "au-delà", "au-devant", "aucun", "aucune", "audit", "auprès", "auquel", "aura", "aurai", "auraient", "aurais", "aurait", "auras", "aurez", "auriez", "aurions", "aurons", "auront", "aussi", "autour", "autre", "autres", "autrui", "aux", "auxdites", "auxdits", "auxquelles", "auxquels", "avaient", "avais", "avait", "avant", "avec", "avez", "aviez", "avions", "avons", "ayant", "ayez", "ayons", "b", "bah", "banco", "ben", "bien", "bé", "c", "c'", "c'est", "c'était", "car", "ce", "ceci", "cela", "celle", "celle-ci", "celle-là", "celles", "celles-ci", "celles-là", "celui", "celui-ci", "celui-là", "celà", "cent", "cents", "cependant", "certain", "certaine", "certaines", "certains", "ces", "cet", "cette", "ceux", "ceux-ci", "ceux-là", "cf.", "cg", "cgr", "chacun", "chacune", "chaque", "chez", "ci", "cinq", "cinquante", "cinquante-cinq", "cinquante-deux", "cinquante-et-un", "cinquante-huit", "cinquante-neuf", "cinquante-quatre", "cinquante-sept", "cinquante-six", "cinquante-trois", "cl", "cm", "cm²", "comme", "contre", "d", "d'", "d'après", "d'un", "d'une", "dans", "de", "depuis", "derrière", "des", "desdites", "desdits", "desquelles", "desquels", "deux", "devant", "devers", "dg", "différentes", "différents", "divers", "diverses", "dix", "dix-huit", "dix-neuf", "dix-sept", "dl", "dm", "donc", "dont", "douze", "du", "dudit", "duquel", "durant", "dès", "déjà", "e", "eh", "elle", "elles", "en", "en-dehors", "encore", "enfin", "entre", "envers", "es", "est", "et", "eu", "eue", "eues", "euh", "eurent", "eus", "eusse", "eussent", "eusses", "eussiez", "eussions", "eut", "eux", "eûmes", "eût", "eûtes", "f", "fait", "fi", "flac", "fors", "furent", "fus", "fusse", "fussent", "fusses", "fussiez", "fussions", "fut", "fûmes", "fût", "fûtes", "g", "gr", "h", "ha", "han", "hein", "hem", "heu", "hg", "hl", "hm", "hm³", "holà", "hop", "hormis", "hors", "huit", "hum", "hé", "i", "ici", "il", "ils", "j", "j'", "j'ai", "j'avais", "j'étais", "jamais", "je", "jusqu'", "jusqu'au", "jusqu'aux", "jusqu'à", "jusque", "k", "kg", "km", "km²", "l", "l'", "l'autre", "l'on", "l'un", "l'une", "la", "laquelle", "le", "lequel", "les", "lesquelles", "lesquels", "leur", "leurs", "lez", "lors", "lorsqu'", "lorsque", "lui", "lès", "m", "m'", "ma", "maint", "mainte", "maintes", "maints", "mais", "malgré", "me", "mes", "mg", "mgr", "mil", "mille", "milliards", "millions", "ml", "mm", "mm²", "moi", "moins", "mon", "moyennant", "mt", "m²", "m³", "même", "mêmes", "n", "n'avait", "n'y", "ne", "neuf", "ni", "non", "nonante", "nonobstant", "nos", "notre", "nous", "nul", "nulle", "nº", "néanmoins", "o", "octante", "oh", "on", "ont", "onze", "or", "ou", "outre", "où", "p", "par", "par-delà", "parbleu", "parce", "parmi", "pas", "passé", "pendant", "personne", "peu", "plus", "plus_d'un", "plus_d'une", "plusieurs", "pour", "pourquoi", "pourtant", "pourvu", "près", "puisqu'", "puisque", "q", "qu", "qu'", "qu'elle", "qu'elles", "qu'il", "qu'ils", "qu'on", "quand", "quant", "quarante", "quarante-cinq", "quarante-deux", "quarante-et-un", "quarante-huit", "quarante-neuf", "quarante-quatre", "quarante-sept", "quarante-six", "quarante-trois", "quatorze", "quatre", "quatre-vingt", "quatre-vingt-cinq", "quatre-vingt-deux", "quatre-vingt-dix", "quatre-vingt-dix-huit", "quatre-vingt-dix-neuf", "quatre-vingt-dix-sept", "quatre-vingt-douze", "quatre-vingt-huit", "quatre-vingt-neuf", "quatre-vingt-onze", "quatre-vingt-quatorze", "quatre-vingt-quatre", "quatre-vingt-quinze", "quatre-vingt-seize", "quatre-vingt-sept", "quatre-vingt-six", "quatre-vingt-treize", "quatre-vingt-trois", "quatre-vingt-un", "quatre-vingt-une", "quatre-vingts", "que", "quel", "quelle", "quelles", "quelqu'", "quelqu'un", "quelqu'une", "quelque", "quelques", "quelques-unes", "quelques-uns", "quels", "qui", "quiconque", "quinze", "quoi", "quoiqu'", "quoique", "r", "revoici", "revoilà", "rien", "s", "s'", "sa", "sans", "sauf", "se", "seize", "selon", "sept", "septante", "sera", "serai", "seraient", "serais", "serait", "seras", "serez", "seriez", "serions", "serons", "seront", "ses", "si", "sinon", "six", "soi", "soient", "sois", "soit", "soixante", "soixante-cinq", "soixante-deux", "soixante-dix", "soixante-dix-huit", "soixante-dix-neuf", "soixante-dix-sept", "soixante-douze", "soixante-et-onze", "soixante-et-un", "soixante-et-une", "soixante-huit", "soixante-neuf", "soixante-quatorze", "soixante-quatre", "soixante-quinze", "soixante-seize", "soixante-sept", "soixante-six", "soixante-treize", "soixante-trois", "sommes", "son", "sont", "sous", "soyez", "soyons", "suis", "suite", "sur", "sus", "t", "t'", "ta", "tacatac", "tandis", "te", "tel", "telle", "telles", "tels", "tes", "toi", "ton", "toujours", "tous", "tout", "toute", "toutefois", "toutes", "treize", "trente", "trente-cinq", "trente-deux", "trente-et-un", "trente-huit", "trente-neuf", "trente-quatre", "trente-sept", "trente-six", "trente-trois", "trois", "très", "tu", "u", "un", "une", "unes", "uns", "v", "vers", "via", "vingt", "vingt-cinq", "vingt-deux", "vingt-huit", "vingt-neuf", "vingt-quatre", "vingt-sept", "vingt-six", "vingt-trois", "vis-à-vis", "voici", "voilà", "vos", "votre", "vous", "w", "x", "y", "z", "zéro", "à", "ç'", "ça", "ès", "étaient", "étais", "était", "étant", "étiez", "étions", "été", "étée", "étées", "étés", "êtes", "être", "ô"]
os.chdir("I:/Dropbox/NDAD/Visualizing-Empire/TopicModeling")
CORPUS_PATH = os.path.join('data', 'jdv_cleaned_utf-8')
filenames = sorted([os.path.join(CORPUS_PATH, fn) for fn in os.listdir(CORPUS_PATH)])
filename = filenames[0]


# In[11]:

articles = []
for filename in filenames:
    with codecs.open(filename,"r",encoding="utf-8") as f:
        text = f.read()
        text = text.encode('utf-8').decode('ascii', 'ignore') #something is causing the utf-8 files to choke in beautiful soup, and it seems to be random (eg. some files weren't choking, then with no changes, they were)
        try:
            soup = bs(text)
            print filename
        except: 
            print "error: ", filename
            break
    article_tags = soup.findAll("article")
    for article in article_tags:
        articles.append(article.text)
len(articles)


# In[12]:

import numpy as np
import sklearn.feature_extraction.text as text
vectorizer = text.CountVectorizer(stop_words=veronis_french_stop_words, min_df=10,max_df=100,encoding=u'utf-8')
dtm = vectorizer.fit_transform(articles).toarray()
vocab = np.array(vectorizer.get_feature_names())


# In[13]:

# By analogy with LDA, we will use NMF to get a document-topic matrix (topics here will also be referred to as “components”) 
# and a list of top words for each topic. 
# We will make analogy clear by using the same variable names: doctopic and topic_words

from sklearn import decomposition
num_topics = 20
num_top_words = 20
clf = decomposition.NMF(n_components=num_topics, random_state=1)

# this next step may take some time
doctopic = clf.fit_transform(dtm)


# In[ ]:

# words associated with topics
topic_words = []
for topic in clf.components_:
    word_idx = np.argsort(topic)[::-1][0:num_top_words]
    topic_words.append([vocab[i] for i in word_idx])
    
# To make the analysis and visualization of NMF components similar to that of LDA’s topic proportions, 
# we will scale the document-component matrix such that the component values associated with each document sum to one.
doctopic = doctopic / np.sum(doctopic, axis=1, keepdims=True)


# In[ ]:

sys.setdefaultencoding('ascii')
for t in range(len(topic_words)):
    print "\nTopic:",t, " ",
    for word in topic_words[t]:
        print word,


# In[ ]:

#years=[]
#for fn in filenames:
#    basename = os.path.basename(fn)
#    name, ext = os.path.splitext(basename)
#    name = name.split(".")[0]
#    years.append(name)


# In[ ]:

# turn this into an np array so we can use NumPy functions
art_array = np.asarray(articles)

doctopic_orig = doctopic.copy()

# use method described in preprocessing section
num_groups = len(set(years))

doctopic_grouped = np.zeros((num_groups, num_topics))

for i, name in enumerate(sorted(set(years))):
    doctopic_grouped[i, :] = np.mean(doctopic[years == name, :], axis=0) 

doctopic = doctopic_grouped


# In[ ]:

#Even though the NMF fit “discards” the fine-grained detail recorded in the matrix of word frequencies, 
#the matrix factorization performed allows us to reconstruct the salient details of the underlying matrix.

#As we did in the previous section, let us identify the most significant topics for each text in the corpus. 
#This procedure does not differ in essence from the procedure for identifying the most frequent words in each text.

years = sorted(set(years))

print("Top NMF topics in...")
for i in range(len(doctopic)):
    top_topics = np.argsort(doctopic[i,:])[::-1][0:3]
    top_topics_str = ' '.join(str(t) for t in top_topics)
    print("{}: {}".format(years[i], top_topics_str))


# In[6]:

text = text.encode('utf-8').decode('ascii', 'ignore')
type(text)


# In[7]:

soup = bs(text)


# In[ ]:

text.find(u'\xe0')


# In[ ]:




# In[ ]:



