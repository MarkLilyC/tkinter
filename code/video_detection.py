'''
Author: your name
Date: 2021-09-14 16:48:06
LastEditTime: 2021-09-14 17:21:29
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \code\video_detection.py
'''
import os
import sys
import io
import datetime
import subprocess
import ana_excel
import cv2
import numpy as np
import sub_find_Back
import time


def video_read(string_video_path:str, int_capread_delay:int, int_initread_delay:int):
    '''读取视频并保存待识别帧

    Parameters
    ----------
    string_video_path : str
        视频地址
    int_capread_delay : int
        视频截取间隔
    int_initread_delay : int
        视频初始截取帧数

    Returns
    -------
        1：str：此视频结果文件路径
        2：list[str1,str2,....]：截取图片文件路径
    '''
    time_stamp = datetime.datetime.now()
    time_stamp = time_stamp.strftime('%m-%d-%H-%M')
    str_resfolder = string_video_path.replace(string_video_path.split('.')[1], 'res-')
    str_resfolder += time_stamp # 结果文件文件夹
    os.mkdir(str_resfolder)
    str_resfolder_oripics = str_resfolder + '//results' # 结果图片文件夹
    os.mkdir(str_resfolder_oripics)
    list_path_pics = []
    cap = cv2.VideoCapture(string_video_path)
    flag = cap.isOpened()
    c = 1
    while flag:
        ret, frame = cap.read()
        if ret:
            if (c-int_initread_delay) % int_capread_delay == 0:
                print("开始截取视频第：" + str(c+int_initread_delay) + " 帧")
                tmp_pic_path = str_resfolder_oripics + "//capture_image_" + str(c) + '.jpg'
                cv2.imwrite(tmp_pic_path, frame)
                list_path_pics.append(tmp_pic_path)
            c += 1
            cv2.waitKey(0)
        else:
            print("所有帧都已经保存完成")
            break
    cap.release()
    return str_resfolder, list_path_pics

def subFiltter(img, filtter: int):
    '''图片过滤器

    Args:
        img (ndarray): 待过滤图片
        filtter (int): 过滤阈值
    '''
    imginfo = img.shape
    hei = imginfo[0]
    wid = imginfo[1]
    # 设置阈值将二者转换为白色底图
    for i in range(hei):
        for j in range(wid):
            if img[i, j] < filtter:
                img[i, j] = 255
            else:
                continue

def subGetBack(img1_path: str, img2_path: str, res_path: str):
    '''根据原始图像获得背景

    Args:
        img1_path (str): 原图1地址
        img2_path (str): 原图2地址
        res_path (str): 结果文件夹地址

    Returns:
        背景图像(ndarray): 背景图像
    '''
    # 图片相减
    img1 = cv2.imread(img1_path, 0)
    img2 = cv2.imread(img2_path, 0)
    sub_str = img1 - img2
    sub_back = img2 - img1
    imgInfo = img1.shape
    hei = imgInfo[0]
    wid = imgInfo[1]
    # 为去除图片边框被识别为边框，将图片内压缩1像素，此步骤一定在进行相减后立马进行
    for i in range(hei):
        sub_str[i, wid - 1] = 255
        sub_str[i, 0] = 255
        sub_back[i, wid - 1] = 255
        sub_back[i, 0] = 255
    for i in range(wid):
        sub_str[hei - 1, i] = 255
        sub_str[0, i] = 255
        sub_back[hei - 1, i] = 255
        sub_back[0, i] = 255
    # 设置阈值将二者转换为白色底图
    subFiltter(sub_str, 20)
    subFiltter(sub_back, 20)
    # 将过滤后的差图转换为二值图
    ret_str, bin_str = cv2.threshold(sub_str, 127, 255, cv2.THRESH_BINARY)
    ret_back, bin_back = cv2.threshold(sub_back, 127, 255, cv2.THRESH_BINARY)
    # 为保障背景取景的真实，只做开操作
    kernel = np.ones((3, 3), np.uint8)
    bin_str_open = cv2.morphologyEx(bin_str, cv2.MORPH_OPEN, kernel, 1)
    bin_back_open = cv2.morphologyEx(bin_back, cv2.MORPH_OPEN, kernel, 1)
    for i in range(hei):
        bin_str_open[i, wid - 1] = 255
        bin_str_open[i, 0] = 255
        bin_back_open[i, wid - 1] = 255
        bin_back_open[i, 0] = 255
    for i in range(wid):
        bin_str_open[hei - 1, i] = 255
        bin_str_open[0, i] = 255
        bin_back_open[hei - 1, i] = 255
        bin_back_open[0, i] = 255
    # 边框检测
    contours_str, hierarchy_str = cv2.findContours(bin_str_open, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours_back, hierarchy_back = cv2.findContours(bin_back_open, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # 去除图框被识别为边框的影响
    contours_str_f = []
    contours_back_f = []
    for i in contours_str:
        if len(i) == (hei + wid) * 2 - 4:
            continue
        else:
            contours_str_f.append(i)
    for i in contours_back:
        if len(i) == (hei + wid) * 2 - 4:
            continue
        else:
            contours_back_f.append(i)
    # 创建空白模板
    dst = np.zeros(imgInfo, np.uint8)
    for i in range(hei):
        for j in range(wid):
            dst[i, j] = 255
    dst2 = np.zeros(imgInfo, np.uint8)
    for i in range(hei):
        for j in range(wid):
            dst2[i, j] = 255

    for i in range(hei):
        dst[i, wid - 1] = 255
        dst[i, 0] = 255
    for i in range(wid):
        dst2[hei - 1, i] = 255
        dst2[0, i] = 255
    # 在空白模板中绘制边框，code设为填充
    cv2.drawContours(dst, contours_str_f, -1, (0, 255, 0), thickness=-1)
    cv2.drawContours(dst2, contours_back_f, -1, (0, 255, 0), thickness=-1)
    # 记录绘制的边框填充图中黑色像素的位置, 填充图中黑色像素越多，最后
    list1 = []
    for i in range(hei):
        for j in range(wid):
            if dst[i, j] == 0:
                list1.append([i, j])
            else:
                continue
    list2 = []
    for i in range(hei):
        for j in range(wid):
            if dst2[i, j] == 0:
                list2.append([i, j])
            else:
                continue
    # 合成背景
    list_out = list1 + list2
    for [i, j] in list_out:
        if img1[i, j] < img2[i, j]:
            img1[i, j] = img2[i, j]
        else:
            img2[i, j] = img1[i, j]
    tmp = res_path + '\\background.jpg'
    cv2.imwrite(tmp, img2)
    return img2

def person_count(background:np.ndarray, img1_path:str):
    '''1-输入待识别图像与背景图像识别以识别人数
       2-将
    Args:
        background (ndarray): 背景图像
        img1_path (ndarray): 待识别图像

    Returns:
        int: 识别人数
    '''
    path_whitebg = img1_path.replace('.jpg','dst_nobg.jpg')
    path_realbg = img1_path.replace('.jpg','dst_bg.jpg')
    img1 = cv2.imread(img1_path, 0)
    # 读取shape
    imgInfo = img1.shape
    hei = imgInfo[0]
    wid = imgInfo[1]
    # 正反相减
    sub = background - img1
    sub_back = img1 - background
    # 过滤为白色底图
    subFiltter(sub, 20)
    subFiltter(sub_back, 20)
    # 二值化
    ret_sub, bS = cv2.threshold(sub, 80, 255, cv2.THRESH_BINARY_INV)
    ret_sub_2, bB = cv2.threshold(sub_back, 200, 255, cv2.THRESH_BINARY_INV)
    # 相加
    add = cv2.add(bS, bB)
    # 闭操作
    kernel1 = np.ones((5, 5), np.uint8)
    close = cv2.morphologyEx(add, cv2.MORPH_CLOSE, kernel1, 1)
    # 空白模板
    dst2 = np.zeros((hei, wid, 1), np.uint8)
    for i in range(hei):
        for j in range(wid):
            dst2[i, j] = 255
    counts = 0
    # 边框识别
    contours_back, hierarchy_back = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for i in contours_back:
        # 当当前检测的面积小于阈值
        rea = cv2.contourArea(i)
        if rea > 400:
            (x, y, w, h) = cv2.boundingRect(i)
            counts += 1
            cv2.rectangle(dst2, (x, y), (x + w, y + h), (0, 0, 0), 2)
            cv2.rectangle(img1, (x, y), (x + w, y + h), (0, 0, 0), 2)
    cv2.imwrite(path_realbg, img1)
    cv2.imwrite(path_whitebg, dst2)
    return counts


def counts(list_path, background):
    """
    输入待处理帧和背景，计算人数
    :param list_path: 待处理帧图像路径list
    :param background: 背景
    :return: 人数list
    """
    list_person = []
    for i in list_path:
        list_person.append(person_count(background, i))
    return list_person

def cal(res_path:str, list_path_pics:str):
    '''行人检测,人数计数
    Args:
        list_path_pics (str): 截取图片地址
        res_path (str): 结果文件文件夹地址

    Returns:
        tuple: (1-list:人数列表
                2-ndarray:背景图像)
    '''
    # 计算背景
    back = subGetBack(list_path_pics[0], list_path_pics[10],res_path=res_path)
    print('背景合成完成')
    per_nums_list = counts(list_path_pics, back)
    # per_nums_list = [5, 3, 1, 2, 3, 2, 2, 1, 3, 3, 1, 1]
    print("人数计数完成：")
    print(per_nums_list)  # [5, 3, 1, 2, 3, 2, 2, 1, 3, 3, 1, 1]
    return per_nums_list, back

a, l = video_read('A://tkinter//code//pets.mp4',50, 10)
per_nums_list, back = cal(a, l)