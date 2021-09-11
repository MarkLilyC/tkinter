import cv2
import sub_find_Back
import numpy as np
import copy
img1 = cv2.imread('../new/back.jpg', 0)
img2 = cv2.imread('capture_image_155.jpg', 0)
img2_copy = copy.deepcopy(img2)
imgInfo = img1.shape
hei = imgInfo[0]
wid = imgInfo[1]
sub = img1 - img2
sub_back = img2 - img1
sub_find_Back.subFiltter(sub, 20)
sub_find_Back.subFiltter(sub_back, 20)
# 二值化
ret_sub, bS = cv2.threshold(sub, 80, 255, cv2.THRESH_BINARY_INV)
ret_sub_2, bB = cv2.threshold(sub_back, 200, 255, cv2.THRESH_BINARY_INV)
add = cv2.add(bS, bB)

kernel1 = np.ones((5, 5), np.uint8)
close = cv2.erode(add, kernel1, 1)
# close = cv2.morphologyEx(add, cv2.MORPH_CLOSE, kernel1, 4)
dst2 = np.zeros((hei, wid, 1), np.uint8)
for i in range(hei):
    for j in range(wid):
        dst2[i, j] = 255
counts = 0
contours_back, hierarchy_back = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
list_rea = []
for i in contours_back:
    # 当当前检测的面积小于阈值
    rea = cv2.contourArea(i)
    if rea > 400:
        list_rea.append(rea)
        (x, y, w, h) = cv2.boundingRect(i)
        counts += 1
        cv2.rectangle(close, (x, y), (x + w, y + h), (255, 255, 255), 2)
        cv2.rectangle(img2, (x, y), (x + w, y + h), (255, 255, 255), 2)
        print(rea)
cv2.imwrite('da3.jpg', close)
print(counts)
cv2.waitKey(0)

