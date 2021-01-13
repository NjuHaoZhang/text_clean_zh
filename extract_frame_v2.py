import time
import os
import shutil
import cv2


# 抽取首帧
def extract_a_key_frame(root_in, root_out, path_save_txt, keys_frame=1):

    # 直接提取 关键帧，给定关键帧的序号: keys_frame
    # 但是我有个问题没搞清楚：keys_frame 到底是 整个视频中的 frame_id, 还是 关键帧序列 key_frame_lsit 中的 id ?
    # 上面问题，check TODO

    cnt = 0
    for video in os.listdir(root_in):  # 列出每一个xxx.mp4
        cur_video = os.path.join(root_in, video)
        print("cur_video: ", cur_video)
        filename, extension = os.path.splitext(video)
        path_out_imgs = os.path.join(root_out, filename)
        print("path_out_imgs: ", path_out_imgs)
        if not os.path.exists(path_out_imgs):
            os.makedirs(path_out_imgs)
        cap = cv2.VideoCapture(cur_video)
        cap.set(cv2.CAP_PROP_POS_FRAMES, keys_frame)  # keys_frame为关键帧的序号
        save_name = 'key_frame_{}.jpg'.format(keys_frame)
        save_path = os.path.join(path_out_imgs, save_name)
        flag, frame = cap.read()  #  frame为关键帧图片，Mat类型。
        if flag:
            cv2.imwrite(save_path, frame)
            print('image of %s is saved' % save_path)
        #
        # 路径写入 txt
        with open(path_save_txt, "w") as fp:
            fp.write(save_path+'\n')


def test_extract_a_key_frame():
    root_in = '/share/yangfan/zhouweihao/fiction_coverr_videonet_clean_without_watermark_998'
    root_out = '/share/yangfan/zhouweihao/fiction_coverr_videonet_clean_without_watermark_998_frist_frame'
    path_save_txt = '/share/yangfan/zhouweihao'
    # fiction_coverr_videonet_clean_without_watermark_998_frist_frame.txt
    dir_list = os.listdir(root_in)
    print("dir_list: ", dir_list)
    for dir_cur in dir_list:
        root_in_cur = os.path.join(root_in, dir_cur)
        root_out_cur = os.path.join(root_out, dir_cur)
        if not os.path.exists(root_out_cur):
            os.makedirs(root_out_cur)
        path_save_txt_cur = os.path.join(path_save_txt, dir_cur+'_998_frist_frame.txt')
        extract_a_key_frame(root_in_cur, root_out_cur, path_save_txt_cur)

# 使用shutil来mv file, 其实速度远远不如 shell 的 mv dir/* dest_dir
def get_all_videos(src_path, target_path):
    while True:
        time.sleep(3)
        file_list = os.listdir(src_path)
        if len(file_list) > 0:
            for file in file_list:
                shutil.move(src_path + file, target_path + file)


def test_get_all_videos():
    src_path = '/share/zhanghao13/all_videos'
    target_path = 'all_videos_tmp'

    for cur_dir in os.listdir(src_path):
        path_cur = os.path.join(src_path, cur_dir)
        get_all_videos(path_cur, target_path)


def combine_txt(input_file_1, input_file_2, output_file):
    cnt_1, cnt_2 = 0, 0
    with open(input_file_1, 'r') as fr_1, open(input_file_2, 'r') as fr_2,  open(output_file, "a+") as fw:

        # 第1个文本
        for line in fr_1:
            cnt_1 += 1
            #
            fw.write(line)

        # 第2个文本
        for line in fr_2:
            cnt_2 += 1
            if cnt_2 == 1:
                continue
            #
            fw.write(line)
    print("total lineZ: ", cnt_1+cnt_2)


def test_combine_txt():
    input_file_1 = ''
    input_file_2 = ''
    output_file = ''
    combine_txt(input_file_1, input_file_2, output_file)


if __name__ == '__main__':
    test_extract_a_key_frame()


