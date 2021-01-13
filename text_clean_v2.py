from pathlib import Path
import numpy as np
import jieba
import jieba.analyse

#
def split_text_to_word(text):
    # 只提取关键词
    key_words = jieba.analyse.extract_tags(text, allowPOS=('adj', 'n', 'vn', 'v'))
    start_idx = 0
    word2idx = []
    for word in key_words:
        start_idx = text.index(word, start_idx)
        word2idx.append((word, start_idx))
    word2idx = sorted(word2idx, key=lambda x : x[1])
    words = [i[0] for i in word2idx]

    return words
    
    
#
def remove_unnecessary_words(words_list):
    
    return words_list

#
def get_text_embedding(text_list, feature_cache_dir):
    feature_cache_dir = Path(feature_cache_dir)
    feature_cache_dir.mkdir(exist_ok=True, parents=True)
    
    all_feature = []
    for word in text_list:
        if word == "":
            continue
        feat_file = feature_cache_dir / (word + ".txt")
        feature = feature_extract(word, feat_file)
        all_feature.append(feature)
    
    all_feature = np.array(all_feature, dtype=np.float32)
    
    return all_feature

def feature_extract(word, feat_cached_file):
    feature = None
    try: # 先用缓存的feature
        with open(feat_cached_file) as fp:
            feature = fp.readlines()
            feature = feature[0].strip()
            feature = [float(i) for i in feature.split(" ")]
    except:
        # feature = bert_client.encode([word])[0] # 使用api 对 word 抽特征
        with open(feat_cached_file, "w") as fp:
            for i in feature:
                fp.write("{} ".format(i))
                
    return feature

#
class NovelMaterial(Material):
    def __init__(self, novel_path, config):
        self.data = read_novel_data(novel_path)
        self.config = config
        # self.text_preprocess()

    def text_preprocess(self):
        # embedding提取模型初始化, 空境视频也需要这个function，后面可以考虑继承于一个基类
        self.novel_word_list = []
        for id in self.data:
            # 对小说简介进行分词
            content = self.data[id]["content"]
            content_split_word = split_text_to_word(content)

            # 去除无意义的词，或者没必要用来进行匹配的词
            content_split_word = remove_unnecessary_words(content_split_word)
            self.data[id]["content_split_words"] = content_split_word
            self.novel_word_list += content_split_word
            
        # self.word_embedding = get_text_embedding(self.novel_word_list, self.config.input_data["feature_cached_dir"])
