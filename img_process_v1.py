import os, cv2, time
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import random
import numpy as np
import shutil
from .util import run_in_shell


f_height = 720
f_width = 1280
fps = 60

def save_to_video_enlarge(pic_file, output_video_file, frame_rate):
    # 拿一张图片确认宽高
    img0 = cv2.imread(pic_file)
    img0 = cv2.resize(img0, (f_width, f_height))
    # print(img0)
    height, width, layers = img0.shape
    # 视频保存初始化 VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    videowriter = cv2.VideoWriter(output_video_file, fourcc, frame_rate, (width, height))
    # 核心，保存的东西
    ratio = height / width

    for j in range(360):
        i = j / 3
        # print("saving..." + f)
        # img = cv2.imread(os.path.join(output_path, pic_name))
        img = img0[int(i * ratio):int(height - i * ratio - 1), int(i):int(width - i - 1)]
        img = cv2.resize(img, (width, height))
        # print(img.shape)
        videowriter.write(img)
    videowriter.release()
    cv2.destroyAllWindows()
    # print('Enlarge: Success save %s!' % output_video_file)


def save_to_video_shrink(pic_file, output_video_file, frame_rate):
    # 拿一张图片确认宽高
    img0 = cv2.imread(pic_file)
    img0 = cv2.resize(img0, (1920, 1080))
    # print(img0)
    height, width, layers = img0.shape
    # 视频保存初始化 VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    videowriter = cv2.VideoWriter(output_video_file, fourcc, frame_rate, (width, height))
    # 核心，保存的东西
    ratio = height / width

    for i in range(360):
        # print("saving..." + f)
        # img = cv2.imread(os.path.join(output_path, pic_name))
        j = (360 - i) / 5
        img = img0[int(j * ratio):int(height - j * ratio - 1), int(j):int(width - j - 1)]
        img = cv2.resize(img, (width, height))
        # print(img.shape)
        videowriter.write(img)
    videowriter.release()
    cv2.waitKey(10)
    cv2.destroyAllWindows()
    # print('Shrink: Success save %s!' % output_video_file)
    pass


def save_to_video_translationUp(pic_file, output_video_file, frame_rate):
    # 拿一张图片确认宽高
    img0 = cv2.imread(pic_file)
    img0 = cv2.resize(img0, (1920, 1080))
    # print(img0)
    height, width, layers = img0.shape
    # 视频保存初始化 VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    videowriter = cv2.VideoWriter(output_video_file, fourcc, frame_rate, (width, height))
    # 核心，保存的东西
    ratio = height / width

    for j in range(360):
        i = j / 5
        # print("saving..." + f)
        # img = cv2.imread(os.path.join(output_path, pic_name))
        img = img0[int(360 / 5 - i):int(height - i),
              int((width - (height - 360 / 5) / ratio) / 2):int((width + (height - 360 / 5) / ratio) / 2)]
        img = cv2.resize(img, (width, height))
        # print(img.shape)
        videowriter.write(img)
    videowriter.release()
    cv2.waitKey(10)
    cv2.destroyAllWindows()
    # print('translationUp: Success save %s!' % output_video_file)
    pass


def save_to_video_translationDown(pic_file, output_video_file, frame_rate):
    # 拿一张图片确认宽高
    img0 = cv2.imread(pic_file)
    img0 = cv2.resize(img0, (1920, 1080))
    # print(img0)
    height, width, layers = img0.shape
    # 视频保存初始化 VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    videowriter = cv2.VideoWriter(output_video_file, fourcc, frame_rate, (width, height))
    # 核心，保存的东西
    ratio = height / width

    for j in range(360):
        i = j / 5
        # print("saving..." + f)
        # img = cv2.imread(os.path.join(output_path, pic_name))
        img = img0[int(i):int(i + height - 360 / 5),
              int((width - (height - 360 / 5) / ratio) / 2):int((width + (height - 360 / 5) / ratio) / 2)]
        img = cv2.resize(img, (width, height))
        # print(img.shape)
        videowriter.write(img)
    videowriter.release()
    cv2.waitKey(10)
    cv2.destroyAllWindows()
    # print('translationDown: Success save %s!' % output_video_file)
    pass

def pics2video(pic_file_list, video_path):
    randomlist = [0, 1, 2, 3]
    video_list = []
    for pic_file in pic_file_list:

        video_file = os.path.join(video_path, (pic_file.split('/')[-1]).split('.', 1)[0] + '.mp4')
        video_list.append(video_file)

        # print("pic_file: " + pic_file + " video_file: " + video_file)

        # randomflag = random.choice(randomlist)
        randomflag = 0
        if randomflag == 0:
            # 图片变视频
            save_to_video_enlarge(pic_file, video_file, fps)
        elif randomflag == 1:
            # 图片变视频
            save_to_video_shrink(pic_file, video_file, fps)
        elif randomflag == 2:
            save_to_video_translationUp(pic_file, video_file, fps)
        elif randomflag == 3:
            save_to_video_translationDown(pic_file, video_file, fps)

    return video_list


def cv2ImgAddText(img, text, left, top, textColor=(255, 255, 255), textSize=150,
                  align='center', spacing=16, stroke_width=6, stroke_fill=(0, 0, 0),
                  font='./models/SimHei.ttf'):
    if isinstance(img, np.ndarray):
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    fontText = ImageFont.truetype(font, size=textSize, encoding="utf-8")
    draw.multiline_text((left, top), text, textColor, font=fontText, align=align, 
                        spacing=spacing, stroke_width=stroke_width, stroke_fill=stroke_fill)
    
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def get_image_size(filename):
    img = cv2.imread(filename)
    width = img.shape[1]
    height = img.shape[0]
    
    return width, height


def auto_image_crop(filename, res_name):
    img = cv2.imread(filename)
    width = img.shape[1]
    height = img.shape[0]
    img_ratio = width / height
    target_ratio = None
    target_height = None
    target_width = None

    if (width / height) > 1:  # 横屏图片
        target_width = 1280
        target_height = 720
        target_ratio = target_width / target_height
    else:
        target_width = 720
        target_height = 1280
        target_ratio = target_width / target_height
        
    if abs(img_ratio - target_ratio) > 0.1: # 直接drop
        logger.log("Cannot crop {}, passed!", "error")
        return None, None
    
    # 如果比例在可容忍范围内，则直接resize
    img = cv2.resize(img, (target_width, target_height))
    cv2.imwrite(res_name, img)
   
    return target_width, target_height



