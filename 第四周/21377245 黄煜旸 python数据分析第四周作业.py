import jieba
import copy
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
def collect():
    date_to_text=dict()
    with open (r'C:\Users\黄煜旸\Desktop\weibo.txt','r',encoding='utf-8') as f:
        lines=f.readlines()
        for line in lines:
            l=line.strip()
            l=l.split()
            for i in l:
                if '\u4e00' <= i[0] <= '\u9fff':
                    txt=i
                    break
            if line[-31:-20] not in date_to_text.keys():
                date_to_text[line[-31:-20]]=i
            else:
                date_to_text[line[-31:-20]]=date_to_text[line[-31:-20]]+'\t'+i
    return date_to_text

def wash(dic):
    with open (r'C:\Users\黄煜旸\Desktop\停用词表.txt','r',encoding='utf-8') as f:
        stop=f.readlines()
        for i in range(len(stop)):
            stop[i]=stop[i].strip()
    for i in dic.keys():
        txt=dic[i]
        t=[]
        for j in txt:
            if '\u4e00' <= j <= '\u9fff':
                t.append(j)
        t=list(jieba.cut(''.join(t)))
        t1=copy.deepcopy(t)
        for j in t1:
            if j in stop:
                t.remove(j)
        t=' '.join(t)
        dic[i]=t
    return dic

def matrix(dic):
    dic1={}
    for i in dic.keys():
        vectorizer=CountVectorizer()
        count=vectorizer.fit_transform(dic[i].split())
        dic1[i]=count
    with open (r'C:\Users\黄煜旸\Desktop\dic1.json','w+',encoding='utf-8') as f:
        json.dump(dic1,f)
    return dic1

def topic_analysis(dic):
    dic2={}
    for i in dic.keys():
        vectorizer=CountVectorizer()
        count=vectorizer.fit_transform(dic[i].split())
        lda=LatentDirichletAllocation(n_components=8)
        lda.fit(count)
        topics=25
        names=vectorizer.get_feature_names_out()
        tword=[]
        for topic in lda.components_:
            stopic=' '.join(names[j] for j in topic.argsort()[:-26:-1])
            tword.append(stopic)
            print(stopic)
        dic2[i]=topic
    with open (r'C:\Users\黄煜旸\Desktop\dic2.json','w+',encoding='utf-8') as f:
        json.dump(dic2,f)
    return dic2
topic_analysis(wash(collect()))
matrix(wash(collect()))


