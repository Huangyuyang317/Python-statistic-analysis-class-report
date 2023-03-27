import jieba
import gensim

class TextAnalyzer:
    def __init__(self, text_path, model_path, pretrained_model_path,vector_size=200, window=5):
        self.text_path = text_path
        self.model_path = model_path
        self.pretrained_model_path=pretrained_model_path
        self.vector_size = vector_size
        self.window = window
        self.text = None
        self.sentences = None
        self.model = None
        self.pretrained_model = None
    
    def load_text(self):
        with open(self.text_path, 'r', encoding='utf-8') as f:
            self.text = f.read()
        
    def preprocess_text(self):
        # 分词
        self.sentences = []
        for line in self.text.split('\n'):
            words = jieba.lcut(line)
            # 去除停用词和标点符号
            words = [word for word in words if word not in stopwords and word.strip() != '']
            self.sentences.append(words)
            
    def train_word2vec(self):
        self.model = gensim.models.Word2Vec(self.sentences, vector_size=self.vector_size, window=self.window, min_count=1, workers=4)
        self.model.save(self.model_path)
        
    def load_pretrained_model(self):
        self.pretrained_model = gensim.models.KeyedVectors.load(self.pretrained_model_path)
        
    def find_similar_words(self, word, topn=10):
        similar_words1 = self.model.wv.most_similar(word, topn=topn)
        similar_words2 = self.pretrained_model.wv.most_similar(word, topn=topn)
        return similar_words1,similar_words2

# 停用词表
stopwords = set()
with open(r'C:\Users\黄煜旸\Desktop\停用词表.txt', 'r+',encoding='utf-8') as f:
    for line in f:
        stopwords.add(line.strip())
# 初始化对象
text_analyzer = TextAnalyzer(r'C:\Users\黄煜旸\Desktop\weibo.txt',r'C:\Users\黄煜旸\Desktop\test_model\test.model', r'C:\Users\黄煜旸\Desktop\python5-pre-trained-weibo-word2vec\weibo_59g_embedding_200.model')
# 加载文本
text_analyzer.load_text()
# 预处理文本
text_analyzer.preprocess_text()
# 训练Word2Vec模型
text_analyzer.train_word2vec()
# 加载预训练的Word2Vec模型
text_analyzer.load_pretrained_model()
# 寻找相似词汇
similar_words1,similar_words2 = text_analyzer.find_similar_words('亮眼')
print(similar_words1)
print(similar_words2)
