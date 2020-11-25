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

class bangla_analysis():

    recieved_sentence = ""

    def __init__(self, sentence):
        self.recieved_sentence = sentence

    def start_analysis(self):
        sent = self.recieved_sentence

        classDict = {'neg': 0, 'pos': 1, 'ntr': 2}
        label2id = []

        def read_File():
            sentences = []
            labels = []
            scrip_dir = os.path.dirname(os.path.realpath('__file__'))
            rel_path = "data.txt"
            abs_file_path = os.path.join(scrip_dir, rel_path)
            with open(abs_file_path, encoding='utf-8') as f:
                for line in f:
                    word = line.split()
                    labels.append(word[0])
                    label2id.append(classDict[word[0]])
                    sentence = re.sub(word[0] + '\t', '', line)
                    sentences.append(sentence)
            print('read file complete')

            return sentences, labels

        sentences, labels = read_File()
        data = {'label': labels,
                'sentence': sentences
                }

        df = pd.DataFrame(data, columns=['label', 'sentence'])

        df.head()

        # %%

        df.describe(include='all')
        print(df.describe(include='all'))
        df['label'].value_counts().plot(kind="bar", rot=0)
        #plt.show()

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

        df.loc[15, 'sentence']

        for i, sent in enumerate(df['sentence'].tolist()):
            df.loc[i, 'clean_sentence'] = clean_sentence(sent)
        test = df.loc[15, 'clean_sentence']
        print(test)

        stop_words = {'এ', 'হয়', 'কি', 'কী', 'এর', 'কে', 'যে', 'এই', 'বা', 'সব', 'টি', 'তা',
                      'সে', 'তাই', 'সেই', 'তার', 'আগে', 'যদি', 'আছে', 'আমি', 'এবং', 'করে', 'কার', 'এটি', 'হতে', 'যায়',
                      'আরও', 'যাক', 'খুব', 'উপর', 'পরে', 'হবে', 'কেন', 'কখন', 'সকল', 'হয়', 'ঠিক', 'একই', 'কোন',
                      'ছিল', 'খুবই', 'কোনো', 'অধীন', 'যারা', 'তারা', 'গুলি', 'তাকে', 'সেটা', 'সময়', 'আমার', 'আমরা', 'সবার',
                      'উভয়', 'একটা', 'আপনি', 'নিয়ে', 'একটি', 'বন্ধ', 'জন্য', 'শুধু', 'যেটা', 'উচিত', 'মাঝে', 'থেকে',
                      'করবে',
                      'আবার', 'উপরে', 'সেটি', 'কিছু', 'কারণ', 'যেমন', 'তিনি', 'মধ্যে', 'আমাকে', 'করছেন', 'তুলনা', 'তারপর',
                      'নিজেই', 'থাকার', 'নিজের', 'পারেন', 'একবার', 'সঙ্গে', 'ইচ্ছা', 'নীচের', 'এগুলো', 'আপনার', 'অধীনে',
                      'কিংবা',
                      'এখানে', 'তাহলে', 'কয়েক', 'জন্যে', 'হচ্ছে', 'তাদের', 'কোথায়', 'কিন্তু', 'নিজেকে', 'যতক্ষণ',
                      'আমাদের',
                      'দ্বারা', 'হয়েছে', ' সঙ্গে', 'সেখানে', 'কিভাবে', 'মাধ্যমে', 'নিজেদের', 'তুলনায়', 'প্রতিটি',
                      'তাদেরকে', 'ইত্যাদি', 'সম্পর্কে', 'সর্বাধিক', 'বিরুদ্ধে', 'অন্যান্য'}

        def remove_stop_words(text):
            text = [w for w in text if not w in stop_words]
            text = ' '.join(text)
            return text

        def tokenized_data(sent):
            tokenized_text = sent.split()
            return tokenized_text

        t_data = tokenized_data(test)
        r_word = remove_stop_words(t_data)
        print('befor :', test)
        print('after :', r_word)

        df['clean_data'] = [remove_stop_words(tokenized_data(sent)) for sent in df['clean_sentence'].tolist()]
        # del df['sentence']
        df.to_csv('sentiment_analysis_clean_data.csv', encoding='utf-8', index=False)

        stpGram = {}
        word_vectorizerGram = CountVectorizer(analyzer='word', ngram_range=(1, 2), min_df=1, lowercase=False,
                                              token_pattern=u'[\S]+', tokenizer=None)

        word_vectorizerGram.fit_transform(df['clean_sentence'])
        stpGram = word_vectorizerGram.get_feature_names()

        print(len(stpGram))

        word_vectorizerGram_rsw = CountVectorizer(analyzer='word', ngram_range=(1, 2), min_df=1, lowercase=False,
                                                  token_pattern=u'[\S]+', tokenizer=None)

        word_vectorizerGram_rsw.fit_transform(df['clean_data'])
        stpGram_rsw = word_vectorizerGram_rsw.get_feature_names()

        print(len(stpGram_rsw))
        print('sample of bigram : ', stpGram_rsw[20])
        f = open("demofile3.txt", "a",encoding="utf-8")
        print(stpGram_rsw)
        n = 0
        for i in stpGram_rsw:
            print(' '+ i)
            f.write(stpGram_rsw[n]+',')
            n= n+1
        f.close()
        print(n)

        def sentence_to_vector_transform(line, stpGram):
            vec = CountVectorizer(analyzer='word', ngram_range=(1, 2), min_df=1, lowercase=False, token_pattern=u'[\S]+',
                                  tokenizer=None, vocabulary=stpGram)
            tList = []
            tList.append(line)
            sent = vec.transform(tList)
            sent = sent.toarray()
            sent = np.squeeze(np.asarray(sent))
            return sent

        def sentence_to_vector(data, stpGram):
            dataForSVM = []
            colName = []
            dataVec = []
            dataVec.append(colName)

            for idx, sent in enumerate(data):

                sent = sentence_to_vector_transform(sent, stpGram)
                sentLst = list(sent)
                dtList = []
                try:
                    dtList.append(label2id[idx])
                    dataForSVM.append(sent)
                except:
                    print(idx)
                for item in sentLst:
                    dtList.append(item)
                lengthOfEV = len(dtList)
                dataVec.append(dtList)

            return dataForSVM

        dataForSVM = sentence_to_vector(df['clean_data'], stpGram_rsw)
        dataForSVM[0:4]

        X_train, X_test, y_train, y_test = train_test_split(dataForSVM, label2id, test_size=0.2, random_state=0)

        C = 1.0  # SVM regularization parameter
        linear_svc = SVC(kernel='linear', C=C)
        linear_svc = linear_svc.fit(X_train, y_train)

        filename = 'svc_model.sav'
        joblib.dump(linear_svc, filename)



        sent = clean_sentence(sent)
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