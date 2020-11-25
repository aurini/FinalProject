import os
import nltk
import pandas
import re
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import joblib

class Bangla_analyzer:
    recieved_sentence = ""

    def __init__(self, sentence):
        self.recieved_sentence = sentence

    def start_analysis(self):
        sentence = self.recieved_sentence
        classDict = {'neg': 0, 'pos': 1, 'ntr': 2}
        filename = 'svc_model.sav'

        def clean_sentence(sent):
            sent = re.sub('[?.`*^()!°¢܌Ͱ̰ߒנ~×Ҡߘ:ҰߑÍ|।;!,&%\'@#$><A-Za-z0+-9=./''""_০-৯]', '', sent)
            sent = re.sub(r'(\W)(?=\1)', '', sent)
            sent = re.sub(r'https?:\/\/.*[\r\n]*', '', sent, flags=re.MULTILINE)
            sent = re.sub(r'\<a href', ' ', sent)
            sent = re.sub(r'&amp;', '', sent)
            sent = re.sub(r'<br />', ' ', sent)
            sent = re.sub(r'\'', ' ', sent)
            sent = re.sub(r'ߑͰߑ̰ߒנ', '', sent)
            sent = re.sub(r'ߎɰߎɰߎɍ', '', sent)

            sent = sent.strip()
            return sent

        def sentence_to_vector_transform(line, stpGram):
            vec = CountVectorizer(analyzer='word', ngram_range=(1, 2), min_df=1, lowercase=False, token_pattern=u'[\S]+',
                                  tokenizer=None, vocabulary=stpGram)
            tList = []
            tList.append(line)
            sent = vec.transform(tList)
            sent = sent.toarray()
            sent = np.squeeze(np.asarray(sent))
            return sent

        stpGram_rsw = open('bigGram.txt', encoding="utf-8").read().split(",")

        sent = clean_sentence(sentence)
        sent2vec = sentence_to_vector_transform(sent, stpGram_rsw)
        sent_list = list()
        sent_list.append(sent2vec)

        loaded_model = joblib.load(filename)
        predictions = loaded_model.predict(sent_list)
        print(predictions)
        ans = ""
        print(classDict)
        for key, value in classDict.items():
            if value == predictions[0]:
                ans = key
        print("Answere -", ans)
        return ans

