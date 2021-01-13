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
