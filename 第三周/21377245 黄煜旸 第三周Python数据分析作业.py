import jieba
import re
import matplotlib.pyplot as plt

def is_Chinese(word):
    '''判断文档是不是中文'''
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

jieba.load_userdict(r'C:\Users\黄煜旸\Desktop\emotion_lexicon\anger.txt')
jieba.load_userdict(r'C:\Users\黄煜旸\Desktop\emotion_lexicon\disgust.txt')
jieba.load_userdict(r'C:\Users\黄煜旸\Desktop\emotion_lexicon\fear.txt')
jieba.load_userdict(r'C:\Users\黄煜旸\Desktop\emotion_lexicon\joy.txt') 
jieba.load_userdict(r'C:\Users\黄煜旸\Desktop\emotion_lexicon\sadness.txt')   

anger=[]
disgust=[]
fear=[]
joy=[]
sadness=[]
with open (r'C:\Users\黄煜旸\Desktop\emotion_lexicon\anger.txt','r+',encoding='utf-8') as f:
    anger=f.read().splitlines()
with open (r'C:\Users\黄煜旸\Desktop\emotion_lexicon\disgust.txt','r+',encoding='utf-8') as f:
    disgust=f.read().splitlines()
with open (r'C:\Users\黄煜旸\Desktop\emotion_lexicon\fear.txt','r+',encoding='utf-8') as f:
    fear=f.read().splitlines()
with open (r'C:\Users\黄煜旸\Desktop\emotion_lexicon\joy.txt','r+',encoding='utf-8') as f:
    joy=f.read().splitlines()
with open (r'C:\Users\黄煜旸\Desktop\emotion_lexicon\sadness.txt','r+',encoding='utf-8') as f:
    sadness=f.read().splitlines()

def analysis(tx):
    '''判断混合情绪的函数,并且返回最大的情绪向量'''
    vec={'anger':0,'disgust':0,'fear':0,'joy':0,'sadness':0}
    def emotion():                                      
        for i in tx:
            if i in anger:
                vec['anger']+=1
            elif i in disgust:
                vec['disgust']+=1
            elif i in fear:
                vec['fear']+=1
            elif i in joy:
                vec['joy']+=1
            elif i in sadness:
                vec['sadness']+=1
            else:
                pass
        return ''.join(list (vec.keys()) [list (vec.values()).index (max(list(vec.values())))] )             #返回最大所对应的情绪
    return emotion

def mode(statement):
    weeks = [i[0:3] for i in time]
    months = [i[4:7] for i in time]
    hours = [i[11:13] for i in time]
    week_dict = {'Mon':0,'Tue':0,'Wed':0,'Thu':0,'Fri':0,'Sat':0,'Sun':0}           #创建月份字典
    month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    month_dict = {}
    month_dict = month_dict.fromkeys(month,0)              #创建小时字典
    hour_dic = ['{:0>2d}'.format(i) for i in range(0,24)]
    hour_dict = {}
    hour_dict = hour_dict.fromkeys(hour_dic,0)
    n=len(emo)
    if statement[1]=='hour':
        for i in range(n):
            if emo[i]==statement[0]:
                hour_dict[hours[i]]+=1
        x = list(hour_dict.values())
        y = list(hour_dict.keys())
        plt.plot(y,x)
        plt.xlabel("hours")
        plt.ylabel("times")
        plt.show()
    elif statement[1] == 'month':
        for i in range(n):
            if emo[i] == statement[0]:              
                month_dict[months[i]] += 1                  
        x = list(month_dict.values())
        y = list(month_dict.keys())
        plt.plot(y,x)
        plt.xlabel("months")
        plt.ylabel("times") 
        plt.show()
    elif statement[1] == 'week':
        for i in range(n):
            if emo[i] == statement[0]:
                week_dict[weeks[i]] +=1
        x = list(week_dict.values())
        y = list(week_dict.keys())
        plt.plot(y,x)
        plt.xlabel("weeks")
        plt.ylabel("times")
        plt.show()
    else:
        pass

print("请输入分析的情绪与时间：")
statement=input().split()                                #根据输入的情绪与时间，输出图表
time=[]
emo=[]
with open (r'C:\Users\黄煜旸\Desktop\weibo.txt','r+',encoding='utf-8') as f:
    while True:                                             #逐行读取文件
        line=f.readline()
        if not line: 
           break
        line=line.strip()
        time.append(line[-30:])
        line=line.split()                                   #split分割文件
        txt=[]
        txts=[]
        for i in line:
            if(is_Chinese(i)):                              #用ischinese判断哪个部分是文本部分
                txt=list(i)
        for i in txt:
            if  '\u4e00' <= i <= '\u9fff':
                 txts.extend(i)                              #移除噪点
        t=jieba.lcut(''.join(txts))
        emo.append(analysis(t)())
for i in range(len(emo)):
    print(emo[i])                               
mode(statement)
        
        