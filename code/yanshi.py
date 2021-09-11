import os
import datetime
import fds_run
import subprocess
import cv2
import numpy as np
import sub_find_Back

img1 = cv2.imread('../new/1.jpg', 0)
img2 = cv2.imread('../new/back.jpg', 0)
# 读取shape
imgInfo = img1.shape
hei = imgInfo[0]
wid = imgInfo[1]
# 正反相减
sub = img2 - img1
sub_back = img1 - img2
cv2.imwrite('C://Users//edison//Desktop//ddesign//pics//p//sub_1.jpg', sub)
cv2.imwrite('C://Users//edison//Desktop//ddesign//pics//p//sub_2.jpg', sub_back)
# 过滤为白色底图
sub_find_Back.subFiltter(sub, 20)
sub_find_Back.subFiltter(sub_back, 20)
cv2.imwrite('C://Users//edison//Desktop//ddesign//pics//p//sub_f1.jpg', sub)
cv2.imwrite('C://Users//edison//Desktop//ddesign//pics//p//sub_f2.jpg', sub_back)
# 二值化
ret_sub, bS = cv2.threshold(sub, 80, 255, cv2.THRESH_BINARY_INV)
ret_sub_2, bB = cv2.threshold(sub_back, 200, 255, cv2.THRESH_BINARY_INV)
cv2.imwrite('C://Users//edison//Desktop//ddesign//pics//p//sub_b1.jpg', bS)
cv2.imwrite('C://Users//edison//Desktop//ddesign//pics//p//sub_b2.jpg', bB)
# 相加
add = cv2.add(bS, bB)
cv2.imwrite('C://Users//edison//Desktop//ddesign//pics//p//add.jpg', add)
# 闭操作
kernel1 = np.ones((5, 5), np.uint8)
close = cv2.morphologyEx(add, cv2.MORPH_CLOSE, kernel1, 1)
cv2.imwrite('C://Users//edison//Desktop//ddesign//pics//p//clos.jpg', close)
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
        cv2.rectangle(close, (x, y), (x + w, y + h), (255, 255, 0), 2)
cv2.imwrite('C://Users//edison//Desktop//ddesign//pics//p//re.jpg', close)
print(counts)