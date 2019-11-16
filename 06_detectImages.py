#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image
import os
import cv2
import time
import numpy as np
from keras_retinanet import models
from keras_retinanet.utils.image import read_image_bgr, preprocess_image
from keras_retinanet.utils.visualization import draw_box, draw_caption
from keras_retinanet.utils.colors import label_color

# 获取文件夹中的文件路径
import os
def get_filePathList(dirPath, partOfFileName=''):
    allFileName_list = list(os.walk(dirPath))[0][2]
    fileName_list = [k for k in allFileName_list if partOfFileName in k]
    filePath_list = [os.path.join(dirPath, k) for k in fileName_list]
    return filePath_list
    
# 检测单张图片，返回画框后的图片
def get_detectedImage(retinanet_model, imageFilePath):
    labels_to_names = {0:'fish', 1:'human_face'}
    startTime = time.time()
    image = read_image_bgr(imageFilePath)
    new_size = (416, 416)    
    image = cv2.resize(image, new_size, interpolation=cv2.INTER_LANCZOS4)  
    draw = image.copy()
    draw = cv2.cvtColor(draw, cv2.COLOR_BGR2RGB)
    image = preprocess_image(image)
    boxes, scores, labels = retinanet_model.predict_on_batch(np.expand_dims(image, axis=0))
    for box, score, label in zip(boxes[0], scores[0], labels[0]):
        if score < 0.5:
            break
        color = label_color(label)
        b = box.astype(int)
        draw_box(draw, b, color=color)
        caption = "{} {:.3f}".format(labels_to_names[label], score)
        draw_caption(draw, b, caption)
    usedTime = time.time() - startTime
    print("检测这张图片用时%.2f秒"  %usedTime)
    return draw

# 对若干图片做目标检测
def detect_images(modelFilePath, imageFilePath_list, out_mp4FilePath=None):
    retinanet_model = models.load_model(modelFilePath, backbone_name='resnet50')
    cv2.namedWindow('result', cv2.WINDOW_NORMAL)
    width = 1000
    height = 618
    size = (width, height)
    cv2.resizeWindow('result', width, height)
    if out_mp4FilePath is not None:
        fourcc = cv2.VideoWriter_fourcc('M', 'P', 'E', 'G')
        videoWriter = cv2.VideoWriter(out_mp4FilePath, fourcc, 1.7, size)
    for imageFilePath in imageFilePath_list:
        out_image_ndarray = get_detectedImage(retinanet_model, imageFilePath)
        resized_image_ndarray = cv2.resize(out_image_ndarray, size, interpolation=cv2.INTER_LANCZOS4)  
        # 图片第1维是宽，第2维是高，第3维是RGB
        # PIL库图片第三维是RGB，cv2库图片第三维正好相反，是BGR
        cv2.imshow('result', resized_image_ndarray[...,::-1])
        time.sleep(0.4)
        if out_mp4FilePath is not None:
            videoWriter.write(resized_image_ndarray[...,::-1])
        if cv2.waitKey(1) and 0xFF == 27:
            break
    cv2.destroyAllWindows()

# 解析运行代码文件时传入的参数
import argparse
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dirPath', type=str, help='directory path', default='./n01440764')    
    parser.add_argument('-s', '--suffix', type=str, default='.JPEG')
    parser.add_argument('-m', '--modelFilePath', type=str, default='./retinanet_inference.h5')
    parser.add_argument('-o', '--out_mp4FilePath', type=str, default='fish_output.avi')
    argument_namespace = parser.parse_args()
    return argument_namespace  

# 主函数 
if __name__ == '__main__':
    argument_namespace = parse_args()
    dirPath = argument_namespace.dirPath
    suffix = argument_namespace.suffix
    modelFilePath = argument_namespace.modelFilePath
    out_mp4FilePath = argument_namespace.out_mp4FilePath
    imageFilePath_list = get_filePathList(dirPath, suffix)
    detect_images(modelFilePath, imageFilePath_list, out_mp4FilePath)