'''
1- 分词
2- 过滤其他字符/停用词
3- 命名实体识别
3- 提取名词 （人名，地名，背景，）
'''


# pathinfo
root_local = '/Users/haozhang/Desktop/new_project'



def get_token():
    # encoding:utf-8
    import requests

    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    API_KEY = 'N1DN2kyKdEffhjeRUiGv2w1k'
    client_secret = 'CYg4HfrfWTFgPRIrGja0qxvcLf4r0mHA'
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(API_KEY, client_secret)
    response = requests.get(host)
    if response:
        print(response.json())


# 只保留有效的数据，包括汉字、字母、数字、中文符号等信息，其他乱码进行清除
def is_uchar(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
            return True
    """判断一个unicode是否是数字"""
    if uchar >= u'\u0030' and uchar<=u'\u0039':
            return True
    """判断一个unicode是否是英文字母"""
    if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
            return True
    if uchar in ('，','。','：','？','“','”','！','；','、','《','》','——'):
            return True
    return False


# coding=utf-8

import sys,os
import json
import base64
import time


# make it work in both python2 both python3
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.parse import quote_plus


# skip https auth
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
#
API_KEY = 'N1DN2kyKdEffhjeRUiGv2w1k'
SECRET_KEY = 'CYg4HfrfWTFgPRIrGja0qxvcLf4r0mHA'

COMMENT_TAG_URL = "https://aip.baidubce.com/rpc/2.0/nlp/v1/lexer"

"""  TOKEN start """
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'


"""
    get token
"""
def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    # if (IS_PY3):
    post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print(err)
    # if (IS_PY3):
    result_str = result_str.decode()
    result = json.loads(result_str)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not 'brain_all_scope' in result['scope'].split(' '):
            print('please ensure has check the  ability')
            exit()
        return result['access_token']
    else:
        print('please overwrite the correct API_KEY and SECRET_KEY')
        exit()

"""
    call remote http server
"""
def make_request(url, comment):
    print("---------------------------------------------------")
    print("原始文本：")
    print("    " + comment)
    print("\n结构化结果：")

    response = request(url, json.dumps(
    {
        "text": comment,
        # 13为3C手机类型评论，其他类别评论请参考 https://ai.baidu.com/docs#/NLP-Apply-API/09fc895f
        # "type": 13
    }))

    data = json.loads(response)

    if "error_code" not in data or data["error_code"] == 0:
        #  display result, TODO
        # data = str(data).replace("\'", "\"")
        # data = {str(key).replace("\'", "\""):val for key,val in data.items()}
        # print(data)
        return data
    else:
        # print error response
        print(response)

    # 防止qps超限
    time.sleep(0.5)

"""
    call remote http server
"""
def request(url, data):
    req = Request(url, data.encode('utf-8'))
    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read()
        # if (IS_PY3):
        result_str = result_str.decode()
        return result_str
    except  URLError as err:
        print(err)


def baidu_api_test():
    content = "千古一笑，笑煞千古，绝然傲情，狂歌傲舞！忍辱负重，破茧重生，十年鬼窟，修魔成神！" \
              "“如果有一天，我真的成了魔，你们还会爱我吗？”独孤绝笑，白发红眸，绝世容颜，似魔非魔，笑魅众生。曾经，她也单纯的笑过，单纯的爱过，" \
              "用尽了一生痴傻。现在，也许恨都成了奢侈，万众瞩目时，白色的发丝张扬的飞舞，" \
              "绝色的女子用着血色双眸看着这世间百态，轻浅的笑容，悠远而飘渺，妩媚且娇娆，" \
              "好似不属于这尘世间的美丽…“今天，只要我想，在场的所有人都不可能活着离开…”"
    # content = "谢尔盖·科罗廖夫（1907年1月12日－1966年1月14日），原苏联宇航事业的伟大设计师与组织者 ，" \
    #           "第一枚射程超过8000公里的洲际火箭（弹道导弹）的设计者，第一颗人造地球卫星的运载火箭的设计者、第一艘载人航天飞船的总设计师。"

    # get access token
    token = fetch_token()

    # concat url
    url = COMMENT_TAG_URL + "?charset=UTF-8&access_token=" + token

    data = make_request(url, content)
    items = data.get("items", "-1")

    # parse
    nw_list = set()
    ne_dict = {}
    for it in items:
        #
        if it['pos'] == "n":
            nw_list.add(it['item'])
        elif it['ne'] != "":
            if it['ne'] not in ne_dict.keys():
                ne_dict[it['ne']] = []
            else:
                ne_dict[it['ne']].append(it['item'])
        else:
            pass

    print("nw_list: ", nw_list)
    print("ne_dict: ", ne_dict)




def filer_dushi(file_path, out_dushi_path, out_dssh_path):
    import csv

    # 读取csv至字典
    with open(file_path, "r") as csvFile, open(out_dushi_path, "a+") as ds_fp, open(out_dssh_path, "a+") as dssh_fp:
        reader = csv.reader(csvFile, delimiter='\t')
        writer_ds = csv.writer(ds_fp, delimiter='\t')
        writer_dssh = csv.writer(dssh_fp, delimiter='\t')

        # 建立空字典
        result = {}
        for item in reader:
            # 忽略第一行
            if reader.line_num == 1:
                writer_ds.writerow(item)
                writer_dssh.writerow(item)
                continue
            # print("item: ", item)
            content = item[2].split(',')
            if "都市" in content[0] or "都市" in content[1]:
                writer_ds.writerow(item)
            if content[1] == "都市生活":
                writer_dssh.writerow(item)

        # print(result)


def test_filer_dushi():

    file_path = os.path.join(root_local, "dataset", "refine/novel_full_text.csv")
    out_dushi_path = os.path.join(root_local, "dataset", "refine/dushi_text.csv")
    out_dssh_path = os.path.join(root_local, "dataset", "refine/dssh_text.csv")
    result = filer_dushi(file_path, out_dushi_path, out_dssh_path)
    # print("result: ", result)


def fliter_dushi_qidian():
    pass


if __name__ == '__main__':
    # test_filer_dushi()
    baidu_api_test()
