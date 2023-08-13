import pandas as pd

# loading
title_pd = pd.read_excel(r'news_text_example.xlsx', index_col=[0])#news raw text

print('loading finish')

key_word_pd = pd.read_excel(r'OpRDic.xlsx')# OpRDic
key_word_not = pd.read_excel(r'Non-OpRDic.xlsx')# Non-OpRDic

for  no,title in title_pd.iloc[:,0:4].iterrows():
    print(title['title'])
    # print(no)
    if pd.isnull(title['time']):
        print('The publish time is empty')
    else:
        year = title['time'][:4]
        print('year=',year)
        title_pd.loc[no, "year"] = year

    flags = []
    notflags = []
    for word in key_word_pd["keyword"]:
        if word in title['title']:# for article，title[0]
            flags.append(word)
    title_pd.loc[no,"flags"] = ' '.join(flags) #add column'flags'
    for word2 in key_word_not["keyword_not"]:
        if word2 in title['title']:# for article，title[0]
            notflags.append(word2)
    title_pd.loc[no,"notflags"] = ' '.join(notflags) #add column'notflags'

    if title_pd.loc[no,"flags"]:
        title_pd.loc[no, "keyworddo"] = 1 # If the keyword matches the operational risk title, it is marked as 1
    else:
        title_pd.loc[no, "keyworddo"] = 0
        
    if title_pd.loc[no,"notflags"]:
        title_pd.loc[no, "keyworddo"] = 0
    print(no)

title_pd.to_excel(r'text_all_mark.xlsx') #If you process too many items at once, you may exceed the storage limit of to_excel, and you can save them in CSV form first


mark = title_pd[title_pd.keyworddo.isin([1])]#Take out all the marked ones (ie, filtered operational risk news)
mark.to_excel(r'text_OR_mark.xlsx')