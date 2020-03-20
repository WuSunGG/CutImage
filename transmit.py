# -*- coding:utf8 -*-
"""
第一步：原图为.bmp格式，将其转换为.jpg格式；
第二步：将经过第一步处理后的图片剪裁为分辨率为750*350的图片，
由于对方给定的图片拍摄位置比较稳定，以原图中心点作为目标图片的中心点，
剪裁后得到的图片中包含有目标区域；

"""

import os
import sys
import mimetypes
from PIL import Image
import logging

logging.basicConfig(level=logging.DEBUG)


##################  class  #########################
class cutImage:
    cutconf = {
        "width": 750,
        "height": 350
    }

    def __init__(self, conf=None):
        if conf is not None:
            self.cutconf = conf

    def cut(self, source=None, target=None):
        if mimetypes.guess_type(source)[0] != 'image/bmp':
            logging.info("[{}] 图片类型不是 .bmp".format(source))
            return

        if source is None or target is None:
            logging.info("原图片与目标图片文件格式不能为空")
            return

        img = Image.open(source)
        pwidth, pheight = img.size

        # 计算坐标
        left = (pwidth - self.cutconf['width']) / 2
        top = (pheight - self.cutconf['height']) / 2
        right = left + self.cutconf['width']
        bottom = top + self.cutconf['height']
        # 顺序为[y0:y1, x0:x1]，其中原图的左上角是坐标原点。
        # cropped = img[top:bottom, left:right]  # 裁剪坐标为[y0:y1, x0:x1]
        logging.debug("[{}] source {}x{} -> target {}x{}".format(source, pwidth, pheight, self.cutconf['width'],
                                                                self.cutconf['height']))
        if pheight < self.cutconf['height'] and pwidth < self.cutconf['width']:
            logging.info("图片格式太小,不符合要求")
            return

        cropped = img.crop((left, top, right, bottom))  # (left, upper, right, lower)

        logging.debug("[{}] -> [{}]".format(source, target))
        # 最后我们用cv2.imwrite()方法将裁剪得到的图片保存到本地（第一个参数为图片名，第二参数为需要保存的图片），
        targetPath = os.path.dirname(target)
        if os.path.exists(targetPath) is False:
            logging.info("创建文件夹: " + targetPath)
            os.makedirs(targetPath)
        cropped.save(target)

##################  class  ######################

cutTool = cutImage()

# print(sys.argv)
# [
#   'D:/GZUniversity/CutImage/transmit.py',
#   'D:\\GZUniversity\\CutImage\\sfj',
#   'D:\\GZUniversity\\CutImage\\target'
# ]
transSourceDir = None
transTargetDir = None

def usage():
    print("用法: python tarnsmit.py souredir [targetdir]")
if len(sys.argv) < 2:
    usage()
    exit(0)
else:
    transSourceDir = sys.argv[1]
    if os.path.exists(transSourceDir) is False:
        print("转换文件夹不能为空\r\n")
        usage()
        exit(-1)

    if len(sys.argv) == 2:
        transTargetDir = os.path.join(os.getcwd(), 'target')
    else:
        transTargetDir = sys.argv[2]



def run(sourcePath, targetPath):
    # 获取当前目录的所有文件及文件夹
    currentFiles = os.listdir(sourcePath)
    for file in currentFiles:

        # 获取绝对路径
        currentFile = os.path.join(sourcePath, file)
        targetFile = os.path.join(targetPath, file)

        # 判断是否是文件夹
        if os.path.isdir(currentFile):

            # 如果是文件夹，就递归调用自己
            run(currentFile, targetFile)
        else:

            # 执行转换
            fileName = os.path.basename(currentFile)
            newFileName = os.path.splitext(fileName)[0] + "{}x{}.jpg".format(cutTool.cutconf['width'],
                                                                             cutTool.cutconf['height'])
            targetImageName = os.path.join(os.path.abspath(targetPath), newFileName)
            cutTool.cut(currentFile, targetImageName)


run(transSourceDir, transTargetDir)
