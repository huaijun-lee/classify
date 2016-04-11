# -*- coding: utf-8 -*-
import os
from os import path
import pandas as pd
import collections
from pickle import dump, load
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report,accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib

from classify_seg import getseg

def sort_by_count(d):
    d = collections.OrderedDict(sorted(d.items(), key = lambda t: -t[1]))  
    return d
def classify_model(train_seg,train_y,vect):	
	train_X = vect.transform(train_seg)
	clf_RFC = RandomForestClassifier(n_estimators=550,min_samples_split=1)
	clf_RFC.fit(train_X, train_y)
	return clf_RFC
def model_test(vect,clf_RFC,test_doc):    
    test_seg = test_doc['seg_word']
    test_X = vect.transform(test_seg)
    pre_RFC = clf_RFC.predict(test_X)
    test_doc['pre_sen'] = pre_RFC
    return test_doc
rootdir = os.getcwd()
tempdir = path.join(str(rootdir), 'temp_march')
if not path.isdir(tempdir):
    os.mkdir(tempdir)
train_dir = path.join(rootdir,'qifu_big_data.txt')
try:
    train_doc = load(open(path.join(tempdir,'train_doc.pickle'),'rb'))
    print('成功加载缓存分词数据')
except (IOError, NameError, FileNotFoundError):
    word_seg = getseg(arg = True)
    train_doc = word_seg.get_seg_word(train_dir)
    dump(train_doc,open(path.join(tempdir,'train_doc.pickle'),'wb'))
'''
train_seg = train_doc['seg_word']
train_y = train_doc['sentiment']
try:
    clf_RFC = joblib.load(path.join(tempdir,'pre_RFC.model'))
    vect = load(open(path.join(tempdir,'march_vect.pickle'),'rb'))
    print('成功加载模型')
except (IOError, NameError, FileNotFoundError):
    clf_RFC,vect = classify_model(train_seg,train_y)
    joblib.dump(clf_RFC,path.join(tempdir,'pre_RFC.model'))
    dump(vect,open(path.join(tempdir,'march_vect.pickle'),'wb'))
'''
#test_doc.to_csv(path.join(rootdir, '启赋feb_pro.txt'), encoding = 'utf-8',sep='\t', index=False)
testdir = path.join(rootdir,'rawdata')
dirs = os.listdir(testdir)
dirs = [ ele for ele in dirs if  ele.endswith('_raw.txt')]
try:
    vect = joblib.load(path.join(tempdir,'march_vect.bigidf'))
    print('成功加载bigidf')
except (IOError, NameError, FileNotFoundError):
    total_seg = []
    total_seg.append(train_doc['seg_word'])
    for ele in dirs:
        name = ele.split('_')[0]
        try:
            test_doc = load(open(path.join(tempdir,name +'_test_doc.pickle'),'rb'))
        except (IOError, NameError, FileNotFoundError):
            word_seg = getseg(arg = True)
            testdir = path.join(rootdir,'rawdata')
            test_doc = word_seg.get_seg_word(path.join(testdir, ele))        
            dump(test_doc,open(path.join(tempdir,name +'_test_doc.pickle'),'wb'))      
        total_seg.append(test_doc['seg_word'])
    all_seg = pd.concat(total_seg)
    vect = TfidfVectorizer(ngram_range=(1,2), min_df=1, max_features=10000)    
    vect.fit(all_seg)
    joblib.dump(vect,path.join(tempdir,'march_vect.bigidf'))
result_doc_list = []
for ele in dirs:
    name = ele.split('_')[0]
    train_seg = train_doc[train_doc['str']== name]['seg_word']
    train_y = train_doc[train_doc['str']== name]['sentiment']
    clf_RFC = classify_model(train_seg,train_y,vect)
    test_doc = load(open(path.join(tempdir,name +'_test_doc.pickle'),'rb'))    
    doc_resu = model_test(vect,clf_RFC,test_doc)
    result_doc_list.append(doc_resu)
result_doc = pd.concat(result_doc_list)
result_doc.to_csv(path.join(rootdir, '启赋march_independent_count.txt'), encoding = 'utf-8',sep='\t', index=False)
