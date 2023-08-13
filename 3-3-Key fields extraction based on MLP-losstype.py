# -*- coding: utf-8 -*-

import re

import jieba as jb
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2
from sklearn.neural_network import MLPClassifier

#load data
df = pd.read_excel(r'train.xlsx', index_col=[0])
print("total data: %d ." % len(df))

#clean empty
print("there are %d empty record in column title." % df['title'].isnull().sum())
print("there are %d empty record in column article." % df['article'].isnull().sum())
print("there are %d empty record in column losstype." % df['losstype'].isnull().sum())

df[df.isnull().values==True]
df = df[pd.notnull(df['article'])]
df = df[pd.notnull(df['losstype'])]

print("there are %d empty record in column title." % df['title'].isnull().sum())
print("there are %d empty record in column article." % df['article'].isnull().sum())
print("there are %d empty record in column losstype." % df['losstype'].isnull().sum())
print("total data: %d ." % len(df))
#Count the number of individual losstype
d = {'losstype':df['losstype'].value_counts().index, 'count': df['losstype'].value_counts()}
df_losstype = pd.DataFrame(data=d).reset_index(drop=True)


#data pre-processing，Convert the losstype class to id, which facilitates the training of  classification models
df['losstype_id'] = df['losstype'].factorize()[0]#The factorize function can map the nominal type data in the Series as a set of numbers, and the same nominal type maps to the same number.
losstype_id_df = df[['losstype', 'losstype_id']].drop_duplicates().sort_values('losstype_id').reset_index(drop=True)#Remove duplicate rows
losstype_to_id = dict(losstype_id_df.values)
id_to_losstype = dict(losstype_id_df[['losstype_id', 'losstype']].values)


#Define a function that removes all symbols except letters, numbers, Chinese characters
def remove_punctuation(line):
    line = str(line)
    if line.strip()=='':
        return ''
    rule = re.compile(u"[^a-zA-Z0-9\u4E00-\u9FA5]")
    line = rule.sub('',line)
    return line 

def stopwordslist(filepath):  
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]  
    return stopwords  
 
#load stopwords
stopwords = stopwordslist('stopwords.txt')
#Delete all symbols except letters, numbers and Chinese characters
df['clean_title'] = df['title'].apply(remove_punctuation)
df['clean_article'] = df['article'].apply(remove_punctuation)
#Segmentation of words, and filtering of stop words
df['cut_title'] = df['clean_title'].apply(lambda x: " ".join([w for w in list(jb.cut(x)) if w not in stopwords]))
df['cut_article'] = df['clean_article'].apply(lambda x: " ".join([w for w in list(jb.cut(x)) if w not in stopwords]))

tfidf = TfidfVectorizer(norm='l2', ngram_range=(1, 2))
features = tfidf.fit_transform(df.cut_article)
labels = df.losstype_id
print(features.shape)
print('-----------------------------')
print(features)

# The chi-square test method finds the two most relevant words and two word pairs in each cluster.
N = 2
for losstype, losstype_id in sorted(losstype_to_id.items()):
    features_chi2 = chi2(features, labels == losstype_id)
    indices = np.argsort(features_chi2[0])
    feature_names = np.array(tfidf.get_feature_names())[indices]
    unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
    bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
    print("# '{}':".format(losstype))
    print("  .The two words most relevant to this classification:\n       . {}".format('\n       . '.join(unigrams[-N:])))
    print("  . The two most relevant word pairs:\n       . {}".format('\n       . '.join(bigrams[-N:])))

#load NER+reason+business classification result
df2 = pd.read_excel(r'result-factor+business.xlsx', index_col=[0])
print("total data: %d ." % len(df2))

#clean empty
print("there are %d empty record in column title." % df2['title'].isnull().sum())
print("there are %d empty record in column article." % df2['article'].isnull().sum())

df2[df2.isnull().values==True]
df2 = df2[pd.notnull(df2['article'])]

print("there are %d empty record in column title." % df2['title'].isnull().sum())
print("there are %d empty record in column article." % df2['article'].isnull().sum())

print("total data: %d ." % len(df2))


#train model
X_train = df['article']
y_train = df['losstype']
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X_train)
 
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
 
clf = MLPClassifier(hidden_layer_sizes = 60, alpha = 1e-4,activation = 'relu', max_iter = 500)

#predict function
def myPredict(sec):
    format_sec=" ".join([w for w in list(jb.cut(remove_punctuation(sec))) if w not in stopwords])
    vect = count_vect.transform([format_sec])
    pred_losstype_id=clf.predict(tfidf_transformer.transform(vect))
    print(pred_losstype_id[0])
    return pred_losstype_id[0]

for no,article in df2.iloc[:,0:15].iterrows():
    result = myPredict(article['article'])
#     print(result)
    df2.loc[no,"losstype"] = ''.join(result)
    
print('losstype model:',clf)
df2.to_excel(r'result-finall-factor+business+losstype.xlsx',encoding="utf_8_sig")



