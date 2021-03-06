import cv2
import numpy as np
import datetime
import os
import time

def subFiltter(img, filtter: int):
    """
    输入图片将其按阈值过滤
    :param img: 源图片（灰度图）
    :param filtter: 阈值
    :return: 无返回值，在原图片基础上修改
    """
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


def subGetBack(img1_path: str, img2_path):
    """
    输入图片得到背景
    :param img1: pic1
    :param img2: pic2
    :return: 背景图片
    """
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
    tmp = img1_path.split('c', 1)
    cv2.imwrite(tmp[0] + 'back.jpg', img2)
    return img2


def video_read(path, frame_rate, delay):
    """
    输入视频相对路径进行读取，读取所得保存到output
    :param path: 视频相对路径
    :param frame_rate: 按帧读取
    :return: 读取图片保存路径
    """
    time_stamp = datetime.datetime.now()
    a = time_stamp.strftime('%m-%d-%H-%M')
    path_out = "..//Output//" + a
    for i in range(6):
        if os.path.exists(path_out):
            time.sleep(10)
        else:
            os.makedirs(path_out)
            break
    path_out += '//'
    list_path_pics = []
    cap = cv2.VideoCapture(path)
    flag = cap.isOpened()
    c = 1
    while flag:
        ret, frame = cap.read()
        if ret:
            if (c-delay) % frame_rate == 0:
                print("开始截取视频第：" + str(c+delay) + " 帧")
                cv2.imwrite(path_out + "capture_image_" + str(c) + '.jpg', frame)
                list_path_pics.append(path_out + "capture_image_" + str(c) + '.jpg')
            c += 1
            cv2.waitKey(0)
        else:
            print("所有帧都已经保存完成")
            break
    cap.release()
    return list_path_pics


def person_count(background, img1_path):
    """
    输入背景，按帧识别人数
    :param background:背景
    :param img1: 待处理帧路径
    :return: 返回人数
    """
    list1 = img1_path.split('.', 1)
    path = list1[0] + '_C' + list1[1]
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
    cv2.imwrite(path, dst2)
    cv2.imwrite(img1_path+'.jpg', dst2)
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







