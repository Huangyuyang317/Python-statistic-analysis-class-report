import jieba
import jieba.posseg as pseg
from collections import Counter
import collections
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import PIL
import numpy as np

def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

fpath =r'C:\Users\黄煜旸\Desktop\microsoft-yahei.ttf'
file=[]
psfile=[]
with open (r'C:\Users\黄煜旸\Desktop\weibo.txt','r+',encoding="UTF-8") as f:         #打开文件
    while True:                                             #逐行读取文件
        line=f.readline()
        if not line: 
            break
        line=line.strip() 
        line=line.split()                                 #split分割文件
        txt=[]
        for i in line:
            if(is_Chinese(i)):                              #用ischinese判断哪个部分是文本部分
                txt=list(i)
        txts=[]
        for i in txt:
             if  '\u4e00' <= i <= '\u9fff':
                 txts.extend(i)                              #移除噪点
        txt1=list(jieba.cut("".join(txts)))                  #分词
        file.extend(txt1)
        txt2=list(pseg.cut("".join(txts),HMM=False))
        psfile.extend(txt2)                                  #根据词性分词
freq = Counter(file)
freq=collections.OrderedDict(sorted(freq.items(),key=lambda t:t[1],reverse=True))

stop1=[]
with open (r'C:\Users\黄煜旸\Desktop\停用词表.txt','r+',encoding="UTF-8") as f:
    lines=f.readlines()
    for line in lines:
        aline=line.strip()
        stop1.extend(aline)
stop=[]
for i in range(0,len(stop1)):
    for word in stop1[i].split():
         stop.append(word)                                    #建立停用词表

for i in list(freq.keys()):
    if i in stop:
        del freq[i]                                           #停用词表过滤

image_background=PIL.Image.open(r'C:\Users\黄煜旸\Desktop\weibo.jpg')
MASK=np.array(image_background)
wd = WordCloud(font_path=fpath,background_color='white', width=4000, height=2000, margin=10, max_words=200,mask=MASK)
wd.fit_words(freq)
plt.imshow(wd)
plt.axis('off')
plt.show()

ps=dict(list(map(tuple,psfile)))
pss=Counter(ps.values())
pos=set(ps.values())                                          #词性归纳
for i in pos:
    print('%s\t%s'%(i,pss[i]))                                #输出词性频率
print("请输入词性：")
p=input()
if p not in pos:
    print("Error")                                            #判断是不是属于词性
else:
    lis=[]
    for k in ps.keys():
        if ps[k]==p:
            lis.extend(k)                                     #选出特定词性的词
    lisfreq=Counter(lis)
    wd = WordCloud(font_path=fpath,background_color='white', width=4000, height=2000, margin=10, max_words=200)
    wd.fit_words(lisfreq)
    plt.imshow(wd)
    plt.axis('off')
    plt.show()                                                #绘制词云
    


