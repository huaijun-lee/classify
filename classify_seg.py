# -*- coding: utf-8 -*-
import os
from os import path
import re
import pandas as pd
import numpy as np
import jieba
from time import clock
import collections
#import itertools
#import random
class getseg():
	"""docstring for getseg"""
	def __init__(self, arg):
		super(getseg, self).__init__()
		self.arg = arg
		self.rootdir = os.getcwd()
		self.STOP_WORDS_LIST = self.load_txt(path.join(self.rootdir, 'stopwords_utf8.txt'))
		self.STOP_WORDS_LIST = set([re.sub('\n', '', item) for item in self.STOP_WORDS_LIST])
		self.feature_words_list = self.load_txt(path.join(self.rootdir,'featureword.txt'))
		self.feature_words_list = set([re.sub('\n','',item) for item in self.feature_words_list])
	def isstr(self,var):
	    return isinstance(var, str)
	def strjoin(self,str_a,str_b):
		return str(str_a) + ' ' + str(str_b)
	def filter_stop(self,input_text):
	    if self.arg == True:
             
             for token in input_text:
                if token not in self.STOP_WORDS_LIST and token in self.feature_words_list:
                    yield token
	    else:
	    	for token in input_text:
		        if token not in self.STOP_WORDS_LIST:
		        	yield token
	def cut_word(self,sent):
	    words = self.filter_stop(jieba.cut(sent, cut_all=False))
	    return ' '.join(words)
	def load_txt(self,file):
	    with open(file,'r',encoding = 'utf-8') as f_h:
	        res = [line.encode('utf-8', 'ignore').decode('utf-8', 'ignore') for line in f_h]
	        return res
	def get_seg_word(self,testfile):
	    doc = pd.read_table(testfile)
	    doc['newtext'] = list(map(self.strjoin,doc['title'],doc['content']))
	    isstrl = doc['newtext'].map(self.isstr)
	    jieba.load_userdict(path.join(self.rootdir,'user_dict.txt'))
	    start_time = clock()
	    print('分词任务开始')
	    index=0
	    #check if there exists illegal characters.
	    for item in isstrl:
	        if item:
	            index = index + 1
	        else:
	            print(index, doc['newtext'].iloc[index])
	            break
	    doc['seg_word'] = doc['newtext'].map(self.cut_word)
	    #doc.to_csv(path.join(self.rootdir, '启赋big_分词.csv'), encoding = 'utf-8',sep='\t', index=False)
	    end_time = clock()
	    print('分词任务结束，用时',str((end_time-start_time)/60)+'mins')
	    if self.arg == True:
	    	return doc
	    else:
	    	return doc
	def select_test(self,doc):
         sampler = np.random.randint(0, len(doc), size=500)
         draw_test = doc.take(sampler)
         bool_draw = doc['url'].isin(draw_test['url'])
         bool_d = [ not bool_ for bool_ in bool_draw] 
         doc_train = doc[bool_d]
         return doc_train,draw_test

class tfcount():
	"""docstring for tfcount
	arg 为True，则返回值词频的字典
	arg 为False，则返回值为词数的字典"""
	def __init__(self, arg):
		super(tfcount, self).__init__()
		self.arg = arg

	def count_word(self,seg_words): 
	    t_count = {}
	    n = 0
	    for words in seg_words:
             
             words_list = words.split(' ')
             n += len(words_list)
             for word in words_list:  
                 if word not in t_count:  
                     t_count[word] = 1  
                 else:
                     t_count[word] += 1
	    if not self.arg :
	    	return t_count
	    else:
             tf = {}
             for i in t_count.keys():
                 tf[i] = t_count[i] / n
             return tf