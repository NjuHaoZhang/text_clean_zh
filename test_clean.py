import jionlp
import os
import re
import regex


def clean_text(text):
    """
    清洗文本，步骤包括
    去除 html 标签、去除异常字符、去除冗余字符、去除括号补充内容、去除 URL、去除 E-mail、去除电话号码，将全角字母数字空格替换为半角，
    一般用于将其当做无关噪声，处理分析数据。
    TODO:

    ref from
    https://github.com/dongrixinyu/jio/blob/master/jio/rule/rule_pattern.py
    https://github.com/dongrixinyu/jio/wiki/%E6%AD%A3%E5%88%99%E6%8A%BD%E5%8F%96%E4%B8%8E%E8%A7%A3%E6%9E%90-%E8%AF%B4%E6%98%8E%E6%96%87%E6%A1%A3#user-content-%E6%B8%85%E6%B4%97%E6%96%87%E6%9C%AC
    https://github.com/2hip3ng/chinese-text-clean/blob/master/%E5%93%88%E5%B7%A5%E5%A4%A7%E5%81%9C%E7%94%A8%E8%AF%8D%E8%A1%A8.txt
    https://github.com/2hip3ng/chinese-text-clean/blob/master/data_clean.py

    please install
    https://github.com/dongrixinyu/jio
    jionlp & its requirements.txt
    regex

    """

    def re_clean(text):

        sub_list = [
            '--',
            '^_^',
            '........',
        ]
        for sub in sub_list:
            text = re.sub(sub, '', text)

        sub_list_r2l = [
            r'^! 群：[0-9]+，\n$',  # bug fix TODO
        ]
        # for sub in sub_list_r2l:
        #     text = regex.sub(sub, '', text)

        return text

    filter_list = [
        # 处理常见情况
        jionlp.remove_email,
        jionlp.remove_url,
        jionlp.remove_phone_number,
        jionlp.remove_ip_address,
        jionlp.remove_id_card,
        jionlp.remove_qq,
        jionlp.remove_html_tag,
        jionlp.remove_parentheses,
        jionlp.remove_exception_char,
        # 下面是我自己手写的正则，处理特殊情况
        re_clean,
    ]

    for filter in filter_list:
        text = filter(text)

    return text


def test_clean_text():

    input_file = path_novel_text
    flags = 'novel'
    path_output = path_novel_clean_output
    #
    cnt = 0
    text_list = []
    with open(input_file, 'r') as fr:
        for line in fr:
            datas = line.strip().split('\t')
            cnt += 1
            if cnt == 1:
                continue
            texts = datas[1:] if flags == 'novel' else datas[1:-1]
            concat_text = ' '.join(texts)
            text = clean_text(concat_text+'\n')
            text_list.append(text)
    with open(path_novel_clean_output, "w") as fp:
        fp.writelines(text_list)


if __name__ == '__main__':
    # my test data
    root_data = '/Users/haozhang/Desktop/Project/dataset'
    path_novel_text = os.path.join(root_data, 'novel_text_refine.txt')  # 已经 refine 过 (去掉 category)
    path_fiction_text = os.path.join(root_data, 'fiction_text.txt')
    path_fiction_tag = os.path.join(root_data,
                                    'fiction_videos_tag_refine.xlsx')  # 使用的 refine version (excel有问题，修正后(删掉不一致的tag 构建 tag字典)再使用这个excel, TODO)
    #
    path_novel_clean_output = os.path.join(root_data, 'path_novel_clean.txt')

    test_clean_text()