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
