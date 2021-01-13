import cv2
import os
import shutil
from multiprocessing import Pool
import subprocess
import shutil
import cv2
import os
import PIL

def refine_text(path_input_file, path_out_file):
    # 去掉 novel_text.txt 中的  category (错误信息)
    # 实现是: 先读后写

    file_data = ''
    with open(path_input_file, 'r') as fr:
        for line in fr:
            datas = line.strip().split('\t')
            del datas[1] # 删除 list 中 某一个 item
            print("datas: ", datas)
            texts = '\t'.join(datas) + '\n'
            file_data += texts

    with open(path_out_file, "w", encoding="utf-8") as f:
        f.write(file_data)


def test_refine_text():
    path_input_file = '/Users/haozhang/Desktop/Project/dataset/novel_text.txt'
    path_out_file = '/Users/haozhang/Desktop/Project/dataset/novel_text_refine.txt'
    refine_text(path_input_file, path_out_file)


def test_sorted_ret_idx():
    nums = [4, 1, 5, 2, 9, 6, 8, 7]
    sorted_nums = sorted(enumerate(nums), key=lambda x: x[1])
    idx = [i[0] for i in sorted_nums]
    nums = [i[1] for i in sorted_nums]
    print("idx: ", idx)
    print("nums: ", nums)


def extract_image_ffmpeg(root_in, root_out):

    # 有 bug, ffmpeg 命令 返回提取帧结果为空，原因check TODO

    for video in os.listdir(root_in):
        cur_video = os.path.join(root_in, video)
        print("cur_video: ", cur_video)
        filename, extension = os.path.splitext(video)
        path_out_imgs = os.path.join(root_out, filename)
        print("path_out_imgs: ", path_out_imgs)
        if not os.path.exists(path_out_imgs):
            os.makedirs(path_out_imgs)
        # cl = 'ffmpeg -i {} -vf "select=eq(pict_type\,I)"  -vsync vfr -qscale:v 2 -f image2 {}/%08d.jpg'.format(
        #     cur_video, path_out_imgs  # 抽一个video里面多个关键帧
        # )
        cl = 'ffmpeg -i {} -qscale:v 1 {}/img_%06d.jpg'.format(
            cur_video, path_out_imgs
        )
        print("cl: ", cl)
    print(subprocess.call(cl, shell=True))  # shell参数为false，则，命令以及参数以列表的形式给出

def test_extract_image_ffmpeg():
    root_in = '/home/zhanghao13/.jupyter/dataset/text2image/videos'
    root_out = '/home/zhanghao13/.jupyter/dataset/text2image/empty_scene'
    extract_image_ffmpeg(root_in, root_out)


def extract_image_opencv(root_in, root_out, interval=5):
    """
    Args:
        video_name:输入视频名字
        interval: 保存图片的帧率间隔
    Returns:
    """
    import shutil

    for video in os.listdir(root_in):
        cur_video = os.path.join(root_in, video)
        print("cur_video: ", cur_video)
        filename, extension = os.path.splitext(video)
        path_out_imgs = os.path.join(root_out, filename)
        print("path_out_imgs: ", path_out_imgs)
        if not os.path.exists(path_out_imgs):
            os.makedirs(path_out_imgs)

        # 开始读视频
        video_capture = cv2.VideoCapture(cur_video)
        i = 0
        j = 0

        while True:
            success, frame = video_capture.read()
            i += 1
            if i % interval == 0:
                # 保存图片
                j += 1
                save_name = str(j) + '_' + str(i) + '.jpg'
                save_path = os.path.join(path_out_imgs, save_name)
                if success:
                    cv2.imwrite(save_path, frame)
                    print('image of %s is saved' % save_path)
            if not success:
                print('video is all read')
                break


def test_extract_image_opencv():
    root_in = '/home/zhanghao13/.jupyter/dataset/text2image/videos'
    root_out = '/home/zhanghao13/.jupyter/dataset/text2image/empty_scene_opencv'
    extract_image_opencv(root_in, root_out)


def extract_image_opencv_multiprocess(root_in, root_out, interval=5, num_worker=10):
    """
    Args:
        video_name:输入视频名字
        interval: 保存图片的帧率间隔
        多进程版本-多核并行 代替 单核串行，有点 bug, fix todo
    Returns:
    """

    def worker(root_in, root_out, interval, video):
        cur_video = os.path.join(root_in, video)
        print("cur_video: ", cur_video)
        filename, extension = os.path.splitext(video)
        path_out_imgs = os.path.join(root_out, filename)
        print("path_out_imgs: ", path_out_imgs)
        if not os.path.exists(path_out_imgs):
            os.makedirs(path_out_imgs)

        # 开始读视频
        video_capture = cv2.VideoCapture(cur_video)
        i = 0
        j = 0

        while True:
            success, frame = video_capture.read()
            i += 1
            if i % interval == 0:
                # 保存图片
                j += 1
                save_name = str(j) + '_' + str(i) + '.jpg'
                save_path = os.path.join(path_out_imgs, save_name)
                if success:
                    cv2.imwrite(save_path, frame)
                    print('image of %s is saved' % save_path)
            if not success:
                print('video is all read')
                break

    pool = Pool(num_worker)  # 创建一个5个进程的进程池
    for video in os.listdir(root_in):
        pool.apply_async(func=worker, args=(root_in, root_out, interval, video))


def test_extract_image_opencv_multiprocess():
    root_in = '/home/zhanghao13/.jupyter/dataset/text2image/videos'
    root_out = '/home/zhanghao13/.jupyter/dataset/text2image/empty_scene_multiProcess'
    extract_image_opencv_multiprocess(root_in, root_out)


def extract_a_key_frame(root_in, root_out, keys_frame=1):

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
        path_out_imgs
        with open(path_save_txt, "w") as fp:

def test_extract_a_key_frame():
    root_in = '/home/zhanghao13/.jupyter/dataset/text2image/videos'
    root_out = '/home/zhanghao13/.jupyter/dataset/text2image/empty_scene_a_key_frame'
    extract_a_key_frame(root_in, root_out)


def gen_path_txt(path_in, path_out):
    for sub_dir in os.listdir(path_in):
        cur_dir = os.path.join(path_in, sub_dir)
        img = os.listdir(cur_dir)[0]  # 只有一张
        img_path = os.path.join(cur_dir, img)
        print("img_path: ", img_path)
        with open(path_out, "a", encoding="utf-8") as f:
            f.write(img_path+"\n")


def test_gen_path_txt():
    path_in = '/share/zhanghao13/dataset_tmp/empty_scene'
    path_out = '/share/zhanghao13/dataset_tmp/empty_scene.txt'
    gen_path_txt(path_in, path_out)

def addTextOnImage(root_txt_list, root_out=None):

    # 返回指定路径图像的拉普拉斯算子边缘模糊程度值
    def getImageVar(img_path):
        image = cv2.imread(img_path)
        img2gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        imageVar = cv2.Laplacian(img2gray, cv2.CV_64F).var()
        return imageVar

    # 返回给定文件夹下所有图片的路径列表
    def listFolderImgPath(folder_img_path):
        img_path_list = []
        for filename in os.listdir(folder_img_path):
            filepath = os.path.join(folder_img_path, filename)
            img_path_list.append(filepath)
        return img_path_list

    # 给单张图片添加文字(图片路径，文字)
    def writeText(img_path, text):
        # # 加载背景图片
        # # img的类型是np.ndarray数组
        # # img = cv2.imread(img_path)
        # paint_chinese_opencv(img_path, str, point, color)
        #
        # # 在图片上添加文字信息
        # # 颜色参数值可用颜色拾取器获取（(255,255,255)为纯白色）
        # # 最后一个参数bottomLeftOrigin如果设置为True，那么添加的文字是上下颠倒的
        # composite_img = cv2.putText(img, text, (100, 680), cv2.FONT_HERSHEY_SIMPLEX,
        #                             2.0, (255, 255, 255), 5, cv2.LINE_AA, False)
        img = cv2.imread(img_path)
        content = '\n'.join(text.split(','))
        if img is None:
            return
        composite_img = cv2ImgAddText(img, content, 0, 0, (255, 255, 0), 20)
        cv2.imwrite(img_path, composite_img)

    import cv2
    import numpy
    from PIL import Image, ImageDraw, ImageFont

    def cv2ImgAddText(img, text, left, top, textColor=(0, 255, 0), textSize=20):
        if (isinstance(img, numpy.ndarray)):  # 判断是否OpenCV图片类型
            img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img)
        fontText = ImageFont.truetype(
            "font/simsun.ttc", textSize, encoding="utf-8")
        draw.text((left, top), text, textColor, font=fontText)
        return cv2.cvtColor(numpy.asarray(img), cv2.COLOR_RGB2BGR)

    # 文件夹路径
    # folder_img_path = root_in

    # 图片路径
    # img_path = '../../imgs/f_cotton-g_top (813).jpg'
    # print(getImageVar(img_path))
    # print(listFolderImgPath(folder_img_path))

    # 获取图片路径列表
    # img_path_list = listFolderImgPath(folder_img_path)

    # 循环处理每张图片
    for txt in os.listdir(root_txt_list):
        root_txt = os.path.join(root_txt_list, txt)
        print("root_txt: ", root_txt)
        with open(root_txt, 'r') as f:
            for line in f:
                img_path, text = line.split('\t\t')
                # 获取该张图片模糊值
                # imageVar = getImageVar(img_path)
                # 创建需写入文字信息
                # 将文字写入图片
                writeText(img_path, text)

                # img = cv2.imread(img_path)
                # cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)
                # cv2.imshow('image', img)
                # cv2.waitKey(1)


def test_addTextOnImage():
    root_txt_list = '/home/zhanghao13/.jupyter/dataset/image_data_1w/image_data_hash2tag'
    addTextOnImage(root_txt_list)

    
# 抽取首帧
def extract_a_key_frame(root_in, root_out, keys_frame=1):

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
        path_out_imgs
        with open(path_save_txt, "w") as fp:
            pass    
    
if __name__ == '__main__':
    # test_refine_text()
    # test_sorted_ret_idx()
    # test_extract_image_ffmpeg()
    # test_extract_image_opencv()
    # test_extract_image_opencv_multiprocess()
    # test_extract_a_key_frame()
    # test_gen_path_txt()
    # test_addTextOnImage()
    pass
