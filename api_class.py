# -*- coding: utf-8 -*-

import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import urlencode
from collections import OrderedDict

class LTP:
    """返回结果说明
    在json格式的单词对象{}中，需含键值名为id, cont；
    id 为句子中的词的序号，其值从0 开始，
    cont为分词内容；
    可选键值名为 pos, ne, parent, relate；
    pos 的内容为词性标注内容；
    ne 为命名实体内容；
    parent 与 relate 成对出现，
    parent 为依存句法分析的父亲结点id号，
    relate 为相对应的关系；
    semparent 与 semrelate 成对出现，
    semparent 为语义依存分析的父亲结点id号，
    semrelate 为相对应的关系"""
    def __init__(self, api_key):
        self.api_key = api_key
        self.uri_base = "http://api.ltp-cloud.com/analysis/"
        self.format = 'json'
        self.pattern = 'srl'
        self.xml_input = 'false'
        self.has_key = 'true'
        self.only_ner = 'false'
    def analyze(self,text):
        data = {
            'api_key' :self.api_key,
            'text':text,
            'format':self.format,
            'pattern':self.pattern
        }
        params = urlencode(data).encode('utf-8')
        try:
            req = Request(self.uri_base,params)
            response = urlopen(req)
        except HTTPError:
            print(HTTPError)
        content = response.read()
        content = content.decode('utf-8')
        print(content)
        result = json.loads(content,object_pairs_hook=OrderedDict)
        return result