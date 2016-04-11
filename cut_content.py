# -*- coding: utf-8 -*-
import os
from os import path
import re
import pandas as pd
import jieba
from time import clock
from pickle import dump, load
import collections
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

def isstr(var):
    return isinstance(var, str)
def filter_stop(input_text):
    for token in input_text:
        if token not in STOP_WORDS_LIST:
            yield token
def cut_word(sent):
    words = filter_stop(jieba.cut(sent, cut_all=False))
    return ','.join(words)
def load_txt(file):
    with open(file,'r',encoding = 'utf-8') as f_h:
        res = [line.encode('utf-8', 'ignore').decode('utf-8', 'ignore') for line in f_h]
        return res
def get_seg_word(testfile):
    doc = pd.read_table(testfile)
    isstrl = doc['content'].map(isstr)
    start_time = clock()
    print('分词任务开始')
    index=0
    #check if there exists illegal characters.
    for item in isstrl:
        if item:
            index = index + 1
        else:
            print(index, doc['content'].iloc[index])
            break
    doc['seg_word'] = doc['content'].map(cut_word)
    end_time = clock()
    print('分词任务结束，用时',str((end_time-start_time)/60)+'mins')
    return doc

def count_word(seg_words):  
    result = {}
    for words in seg_words:
        for word in words.split(','):  
            if word not in result:  
                result[word] = 1  
            else:
                result[word] += 1                 
    return result  
def sort_by_count(d):  
    #字典排序  
    d = collections.OrderedDict(sorted(d.items(), key = lambda t: -t[1]))  
    return d  

rootdir = os.getcwd()
STOP_WORDS_LIST = load_txt(path.join(rootdir, 'stopwords_utf8.txt'))
STOP_WORDS_LIST = set([re.sub('\n', '', item) for item in STOP_WORDS_LIST])
jieba.load_userdict(path.join(rootdir,'user_dict.txt'))
'''
try:
    haifeisi_segword = load(open(path.join(rootdir,'aitamei_segword.pickle'),'rb'))
    seg_exist = True
    print('成功加载分词数据')
except (IOError, NameError, FileNotFoundError):
    seg_exist = False'''
  
filedir = path.join(rootdir,'haifeisi_content.txt')
haifeisi_segword = get_seg_word(filedir)
#dump(aitamei_segword,open(path.join(rootdir,'aitamei_segword.pickle'),'wb'))

seg_words = haifeisi_segword['seg_word']

tf = count_word(seg_words)
result = sort_by_count(tf)
tf_file = pd.DataFrame()
tf_file['term'] =result.keys()
tf_file['value'] =result.values()
tf_file.to_csv(path.join(rootdir, 'haifeisi_seg_tf.txt'), encoding = 'utf-8',sep='\t', index=False)
'''
#idf_word = idf_word(tf_word,segwords)
tf_idf_trans = TfidfVectorizer(ngram_range=(1,1), min_df=1, max_features=10000)
tf_idf_trans.fit_transform(seg_words)
idf = pd.DataFrame()
idf['terms'] = tf_idf_trans.get_feature_names()
idf['idf'] = list(tf_idf_trans.idf_)
#print(type(seg_words[1]))

tf_result = count_word(seg_words)
aitamei_segword.to_csv(path.join(rootdir, 'aitamei_doc.txt'), encoding = 'utf-8',sep='\t', index=False)
result = sort_by_count(tf_result)
tf_file = pd.DataFrame()
tf_file['term'] =result.keys()
tf_file['value'] =result.values()
tf_file.to_csv(path.join(rootdir, 'aitamei_seg_tf.txt'), encoding = 'utf-8',sep='\t', index=False)'''