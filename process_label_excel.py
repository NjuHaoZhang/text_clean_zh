import os, sys
import re
import json
import xlwt, xlrd
import requests
import time


def translate(word):
    # 有道词典 api
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
    # 传输的参数，其中 i 为需要翻译的内容
    key = {
        'type': "AUTO",
        'i': word,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "ue": "UTF-8",
        "action": "FY_BY_CLICKBUTTON",
        "typoResult": "true"
    }
    # key 这个字典为发送给有道词典服务器的内容
    response = requests.post(url, data=key)
    # 判断服务器是否相应成功
    if response.status_code == 200:
        # 然后相应的结果
        try:
            # result = response.json()
            result = json.loads(response.text)
            return result['translateResult'][0][0]['tgt']
        except Exception as e:
            print(e)
            return 'null'
    else:
        print("有道词典调用失败")
        # 相应失败就返回空
        return 'null'


# 1-使用txt + 2-use 再加个过滤条件:
def get_info_from_txt_videonet(input_file, ouput_file):
    cnt = 0
    with open(input_file, 'r') as fr, open(ouput_file, 'w') as fs:
        tmp_line = 'vid\toriginal_url\toriginal_title\ttitle\ttitle_c\t' \
                   'tags\ttags_c\tcontent\tcontent_c\tcategory\tcategory_c\tuse\n'
        fs.write(tmp_line)
        print("start")
        for line in fr:
            try:
                all_info = json.loads(line.strip())
                vid = all_info["video_meta_settings"][0]["video_id"]
                original_url = all_info['original_url']
                original_title = all_info['original_title'].strip()
                title = all_info['title'].strip()
                tags = all_info['tags']
                vid_info = json.loads(all_info['doc_ext_kvs']['t_jwrapper_extract_result_all'])
                check = vid_info['use']  # 版权信息
                content = vid_info['description'].strip()  # 内容描述
                category = vid_info['category'].strip()  # 但是我在原始视频上没看到有category 这个字段

                if ('Royalty-FreeUse' in check) and ('Royalty-FreeEditorial Use Only' not in check):  # 只有这种情况可以用，另外一个字段已经被过滤了
                    use = 'ok'
                else:
                    use = 'bad'
                    continue  # 跳过这个视频

                title_c = translate(title)
                tags_c = []
                for tag in tags:
                    tags_c.append(translate(tag.strip()))
                content_c = translate(content)
                category_c = translate(category)

                line = "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
                    vid, original_url, original_title, title, title_c, tags, tags_c,
                    content, content_c, category, category_c, use)
                fs.write(line)
                fs.flush()
                cnt += 1
                time.sleep(0.1)
            except:
                print(vid)
                continue
        print("cnt: ", cnt)

# 1-使用txt + 2-use 再加个过滤条件:
def get_info_from_txt_coverr(input_file, ouput_file):
    cnt = 0
    with open(input_file, 'r') as fr, open(ouput_file, 'w') as fs:
        tmp_line = 'vid\toriginal_url\toriginal_title\ttitle\ttitle_c\t' \
                   'tags\ttags_c\tcontent\tcontent_c\tcategory\tcategory_c\tuse\n'
        fs.write(tmp_line)
        print("start")
        for line in fr:
            try:
                all_info = json.loads(line.strip())
                vid = all_info["video_meta_settings"][0]["video_id"]
                original_url = all_info['original_url']
                original_title = all_info['original_title'].strip()
                title = all_info['title'].strip()
                tags = all_info['tags']
                vid_info = json.loads(all_info['doc_ext_kvs']['t_jwrapper_extract_result_all'])
                content = vid_info['description'].strip()  # 内容描述
                category = vid_info['category'].strip()  # 但是我在原始视频上没看到有category 这个字段
                use = 'ok'

                title_c = translate(title)
                tags_c = []
                for tag in tags:
                    tags_c.append(translate(tag.strip()))
                content_c = translate(content)
                category_c = translate(category)

                line = "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
                    vid, original_url, original_title, title, title_c, tags, tags_c,
                    content, content_c, category, category_c, use)
                fs.write(line)
                fs.flush()
                cnt += 1
                time.sleep(0.1)
            except:
                print(vid)
                continue
        print("cnt: ", cnt)


def test_get_info_from_txt():
    root_data = '/share/zhanghao13/youdao'
    path_fiction_original_videvo = os.path.join(root_data, 'cp_commercialization_videvo_info_1130.txt')
    path_fiction_original_coverr = os.path.join(root_data, 'coverr.txt')
    out_videvo = os.path.join(root_data, 'videvo_info_all_update.txt')
    out_coverr = os.path.join(root_data, 'coverr_info_all_update.txt')

    input_file = path_fiction_original_videvo
    ouput_file = out_videvo
    get_info_from_txt_videonet(input_file, ouput_file)

    input_file = path_fiction_original_coverr
    ouput_file = out_coverr
    get_info_from_txt_coverr(input_file, ouput_file)


def get_label_excel(input_file, ouput_file, sheet_name='sheet1'):
    cnt = cnt_good = 0
    used = set()
    workbook = xlwt.Workbook()  # 新建一个工作簿
    sheet = workbook.add_sheet(sheet_name)  # 在工作簿中新建一个表格
    with open(input_file, 'r') as fr:
        for line in fr:
            datas = line.strip().split('\t')
            if line in used:
                print(line.strip())
                continue
            cnt += 1
            if cnt == 1:
                frist_row = ['vid', 'title_c', 'original_url']
                for idx in range(len(frist_row)):
                    sheet.write(cnt-1, idx, frist_row[idx])  # 像表格中写入数据（对应的行和列）
                continue
            vid = datas[0]
            original_url = datas[1]
            title_c = datas[4]
            sheet.write(cnt - 1, 0, vid)  # 像表格中写入数据（对应的行和列）
            sheet.write(cnt - 1, 1, title_c)  # 像表格中写入数据（对应的行和列）
            sheet.write(cnt - 1, 2, original_url)  # 像表格中写入数据（对应的行和列）
            used.add(line)
    workbook.save(ouput_file)
    print('total: {}'.format(cnt))


def test_get_label_excel():
    root_data = '/share/zhanghao13/youdao'
    in_videvo = os.path.join(root_data, 'videvo_info_all.txt')
    out_videvo = os.path.join(root_data, 'videvo_info_label.xls')
    get_label_excel(in_videvo, out_videvo)

    in_coverr = os.path.join(root_data, 'coverr_info_all.txt')
    out_coverr = os.path.join(root_data, 'coverr_info_label.xls')
    get_label_excel(in_coverr, out_coverr)


if __name__ == "__main__":
    test_get_info_from_txt() # get text (youdao api translate), 问下浩哥，youdao 被踢咋办？
    # test_get_label_excel() # get some item from text to write a excel
