#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import random
from PIL import Image
import shutil
import argparse

# 获取文件夹中的文件路径
def getFilePathList(dirPath, partOfFileName=''):
    allFileName_list = list(os.walk(dirPath))[0][2]
    fileName_list = [k for k in allFileName_list if partOfFileName in k]
    filePath_list = [os.path.join(dirPath, k) for k in fileName_list]
    return filePath_list

# 选出一部分像素足够，即长，宽都大于416的图片，复制到新文件夹中
def selectSomeQualifiedImages(dirPath, sample_number, new_dirPath):
    jpgFilePath_list = getFilePathList(dirPath, '.JPEG')
    random.shuffle(jpgFilePath_list)
    if not os.path.isdir(new_dirPath):
        os.makedirs(new_dirPath)
    i = 0
    for jpgFilePath in jpgFilePath_list:
        image = Image.open(jpgFilePath)
        width, height = image.size
        if width >= 416 and height >= 416:
            i += 1
            new_jpgFilePath = os.path.join(new_dirPath, '%03d.jpg' %i)
            shutil.copy(jpgFilePath, new_jpgFilePath)
        if i == sample_number:
            break

# 解析运行代码文件时传入的参数
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dirPath', type=str, help='directory path')
    parser.add_argument('-n', '--number', type=int, default=200)
    parser.add_argument('-o', '--out', type=str, default='01_selectedImages')
    argument_namespace = parser.parse_args()
    return argument_namespace  
    
if __name__ == '__main__':
    argument_namespace = parse_args()
    dirPath = argument_namespace.dirPath
    sample_number = argument_namespace.number
    new_dirPath = argument_namespace.out
    selectSomeQualifiedImages(dirPath, sample_number, new_dirPath)
            