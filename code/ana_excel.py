import csv
import os
import matplotlib.pyplot as plt
import numpy as np
"""with open("1.csv", "rt") as csvfile:
    reader = csv.reader(csvfile)
    column_p = [row[1] for row in reader]
    column_t = [row[0] for row in reader]"""


def getParentPathByNum(listofpaths, numofpersonnums):
    tarlist = []
    for i in range(numofpersonnums):
        tmplist = []
        for j in range(len(listofpaths)):
            parentpath = os.path.dirname(listofpaths[j][i])
            tmpinlist = os.listdir(parentpath)
            for k in tmpinlist:
                if k.endswith('.csv'):
                    if k.find('evac') > 0:
                        tmplist.append(parentpath + '\\' + k)
                        break
        tarlist.append(tmplist)
    return tarlist


def gettimebyperson(path):
    with open(path, "rt") as csvfile:
        reader = csv.reader(csvfile)
        column_t = [row[0] for row in reader]
    with open(path, "rt") as csvfile:
        reader = csv.reader(csvfile)
        column_evacmesh = [row[2] for row in reader]
    index = 0
    for i in column_evacmesh:
        if i == '       0':
            index = column_evacmesh.index(i)
            break
    return column_t[index]


def numtimepic(list1, list2, path):
    """
    绘制疏散人数下的疏散时间图
    :param list2: 人数数据数组
    :param list1: 各人数下的疏散时间数组的数组
    :param path: 存放图片的文件夹名
    :return: none
    """
    for i in range(12):  # i为各人数下的疏散时间数组
        name = ["case1", "case2", "case3"]
        y1 = []
        y2 = []
        y3 = []
        for j in range(3):
            y1.append((round(eval((list1[i][j * 3])), 2)))
            y2.append((round(eval((list1[i][j * 3 + 1])), 2)))
            y3.append((round(eval((list1[i][j * 3 + 2])), 2)))
        print(y3)
        x = np.arange(len(name))
        width = 0.25
        plt.bar(x, y1, width=width, label='ploy1', color='powderblue')
        plt.bar(x + width, y2, width=width, label='ploy2', color='lightcyan', tick_label=name)
        plt.bar(x + 2 * width, y3, width=width, label='ploy3', color='bisque')
        for a, b in zip(x, y1):
            plt.text(a, b, b, ha='center', va='bottom')
        for a, b in zip(x, y2):
            plt.text(a + width, b, b, ha='center', va='bottom')
        for a, b in zip(x, y3):
            plt.text(a + 2 * width, b, b, ha='center', va='bottom')
        plt.xticks()
        plt.legend(loc="upper left")  # 防止label和图像重合显示不出来
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.ylabel('Time')
        xlabeltitle = 'Num=' + str(list2[i])
        plt.xlabel(xlabeltitle)
        plt.rcParams['savefig.dpi'] = 300  # 图片像素
        plt.rcParams['figure.dpi'] = 300  # 分辨率
        plt.rcParams['figure.figsize'] = (15.0, 8.0)  # 尺寸
        plt.title("当前人数下各策略疏散时间")
        plt.savefig(path + '\\' + str(i) + '-' + xlabeltitle + '.jpg')
        plt.close()
