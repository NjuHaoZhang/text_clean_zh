import os, shutil, cv2, time, subprocess
from pathlib import Path
import numpy as np
from .img import cv2ImgAddText, pics2video, fps
from .util import run_in_shell


def gen_video_via_video_list(material_list, res_name, novel_info):
    res_name = Path(res_name)
    res_name_without_txt = res_name.parent / (res_name.stem + "_without_text" + res_name.suffix)
    
    # 空境视频只要前5s
    res_dir = "./tmp/{}".format(res_name.stem)
    cuted_video_list = []
    for video_path in material_list:
        cuted_video_name = video_cut(video_path, [[0, 6]], res_dir, thread_num=None)
        cuted_video_list.append(cuted_video_name[0])
        
    video_merge(cuted_video_list, res_name_without_txt)
    add_text_to_video(novel_info, str(res_name_without_txt), str(res_name))
    

def gen_video_via_img_list(pic_file_list, res_name, novel_info):
    res_name = Path(res_name)
    tmp_video_dir = res_name.parent / res_name.stem
    tmp_video_dir.mkdir(exist_ok=True, parents=True)
    video_list = pics2video(pic_file_list, tmp_video_dir)

    res_name_without_txt = res_name.parent / (res_name.stem + "_without_text" + res_name.suffix)
    video_merge(video_list, res_name_without_txt)

    add_text_to_video(novel_info, str(res_name_without_txt), str(res_name))

    
def video_cut(video_path, cut_point, res_dir, thread_num=None):
    """
    Args:
        video_path: str; input video filename
        cut_piont: list; [[s1, e1], [s2, e2], ...], s1, e1 are time point.
        res_dir: str; result file directory
    
    Return:
        None
    """
    
    res_dir = Path(res_dir)
    res_dir.mkdir(exist_ok=True, parents=True)
    video_path = Path(video_path)
    
    # use multi thread
    thead_pool = None
    if not thread_num is None:
        thead_pool = ThreadPoolExecutor(thread_num)
    
    res_name_list = []
    for clip in cut_point:
        res_name = res_dir / (video_path.stem + "_{}_{}{}".format(clip[0], clip[1], video_path.suffix))
        res_name_list.append(str(res_name))
        if res_name.exists():
            continue
            
        cmd = "ffmpeg -loglevel error -y -i '{}' -ss {} -to {} '{}'".format(video_path, clip[0], clip[1], res_name)
        
        if thread_num is None:
            run_in_shell(cmd)
        else:
            thead_pool.submit(run_in_shell, cmd)
            
    if not thread_num is None:
        thead_pool.shutdown(wait=True)
        
    return res_name_list

    
def gen_nodetxt(filelist, res_name):
    effect_list = ['directional','displacement','windowslice','bowtievertical','bowtiehorizontal','simplezoom','linearblur','waterdrop','invertedpageurl','glitchmemories','polkadotscurtain','stereoviewer',
                   'luminance_melt','perlin','directionalwarp','bounce','wiperight','wipeleft','wipedown','wipeup','morph','colourdistance','circlecrop','swirl',
                   'crosszoom','dreamy','gridflip','zoomincircles','radial','mosaic','undulatingrnout','crosshatch','cannabisleaf','crazyparametricfun','butterflywavescrawler','kaleidoscope',
                   'windowblinds','hexagonalize','glitchdisplace','dreamyzoom','doomscreentransition','ripple','pinwheel','angular','burn','circle','circleopen','colorphase',
                   'crosswarp','cube','directionalwipe','doorway','fade','fadecolor','fadegrayscale','flyeye','heart','luma','multiply_blend','pixelize',
                   'polar_function','randomsquares','rotate_scale_fade','squareswire','squeeze','swap','wind',
                   'bowtiewithparameter'
                   ]
    effect_name0 = "randomNoisex"
    nodetxt = "const concat = require('/usr/lib/node_modules/ffmpeg-concat')\n"
    nodetxt += "concat({\n"
    nodetxt += "output: '{}',\n".format(res_name)
    nodetxt += "videos: [\n"
    for file in filelist:
        nodetxt += "'{}',\n".format(file)
    nodetxt += "],\n"
    nodetxt += "transitions: [\n"
    for i in range(len(filelist)-1):
        nodetxt += "{\n"
        effect_name = "directionalwipe"
        nodetxt += "name: '{}',\n".format(effect_name)
        #if effect_name == "circleopen":
        nodetxt += "duration: {}\n".format(500)

        if i != len(filelist)-2:
            nodetxt += "},\n"
        else :
            nodetxt += "}\n"
    nodetxt += "]\n"
    nodetxt += "})\n"
    return nodetxt


def add_text_to_video(novel_info, input_video, res_name):
    fps, _, _ = get_video_info(input_video)
    title = novel_info["title"]
    tag = novel_info["tags"]
    tag = ",".join(tag)
    txt = novel_info["content"]
    tgt_h, tgt_w = 1280, 720
    imgbase = np.zeros((tgt_h, tgt_w, 3), np.uint8)

    txt = txt[:15 * 6]
    length = 15
    txts = ''
    for i in range(len(txt) // length + 1):
        txts += txt[i * length:(i + 1) * length]
        txts += '\n'
    # print('txts')
    # print(txts)

    title = "《" + title + "》"
    imgbase = cv2ImgAddText(imgbase, novel_info["debug_info"], 32, 32, (255, 255, 255), textSize=15)
    # imgbase = cv2ImgAddText(imgbase, title, 80, 160, (255, 255, 255), textSize=(560 // (len(title))))
    imgbase = cv2ImgAddText(imgbase, txts, 40, 880, (255, 255, 255), textSize=40)
    

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(res_name, fourcc, fps, (tgt_w, tgt_h))
    cap = cv2.VideoCapture(input_video)
    succ, frame = cap.read()
    while succ:
        if succ:
            img = imgbase[:]
            img = cv2ImgAddText(img, tag, 32, 32, (255, 255, 255), textSize=30)
            frame = cv2.resize(frame, (720, 404))
            img[400:400 + 404, :, :] = frame
            out.write(img)
        succ, frame = cap.read()
    out.release()

    os.remove(input_video)

    
def get_video_info(video_path):
    fps = None
    width = None
    height = None
    
    cmd = "ffprobe -v quiet -print_format json -show_streams '{}'".format(video_path)
    try:
        output = subprocess.check_output(
            cmd,
            shell=True,
            stderr=subprocess.STDOUT
        )
        output = eval(output)["streams"]
        for each_stream in output:
            stream_fps = each_stream["avg_frame_rate"]

            if stream_fps.split("/")[-1] != "0":
                width = each_stream["width"]
                height = each_stream["height"]
                fps = eval(stream_fps)
    except:
        print("Error, Cannot get video fps. ffprobe output is: {}".format(output))
    
    return fps, width, height
    

def video_audio_merge(video_path, audio_path, res_path):
    cmd = "ffmpeg -loglevel error -y -i '{}' -i '{}'  -c:v copy -c:a aac -strict experimental -map 0:v:0 -map 1:a:0 -shortest   '{}'".format(video_path, audio_path, res_path)
    run_in_shell(cmd)


def video_merge(video_list, res_name):
    """
    Args:
        video_list: list; input video filename list
        res_name: str; result file name

    Return:
        None
    """
    res_name = Path(res_name)
    nodetxt = gen_nodetxt(video_list, res_name)
    node_js_file = "./tmp/{}.js".format(res_name.stem)
    with open(node_js_file, "w", encoding='utf-8') as f:
        f.write(str(nodetxt))
        f.close()

    run_in_shell('xvfb-run --auto-servernum --server-num=1 -s "-ac -screen 0 1280x1024x24"  node "{}"'.format(node_js_file))

    # delete tmp file
    video_file = Path(video_list[0])
    shutil.rmtree(str(video_file.parent))
    
    
def get_video_duration(video_path):
    cmd = 'ffprobe -i {} -show_entries format=duration -v quiet -of csv="p=0"'.format(video_path)
    output = subprocess.check_output(
        cmd,
        shell=True,
        stderr=subprocess.STDOUT
    )

    return float(output)

def auto_video_crop(filename, res_name):
    _, width, height = get_video_info(filename)
    video_ratio = width / height
    target_ratio = None
    target_height = None
    target_width = None

    if (width / height) > 1:  # 横屏视频，这块需要再仔细想想
        target_width = 1280
        target_height = 720
        target_ratio = target_width / target_height
    else:
        target_width = 720
        target_height = 1280
        target_ratio = target_width / target_height
        
    if abs(video_ratio - target_ratio) > 0.1: # 直接drop
        logger.log("Cannot crop {}, passed!", "error")
        return None, None
    
    # 如果比例在可容忍范围内，则直接resize
    resize_cmd = "ffmpeg -loglevel error -y -i {} -vcodec h264 -s {} {}".format(filename, (target_width, target_height), res_name)
    run_in_shell(resize_cmd)
   
    return target_width, target_height
