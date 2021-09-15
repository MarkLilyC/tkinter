'''
Author: your name
Date: 2021-09-10 16:28:00
LastEditTime: 2021-09-14 13:41:58
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \code\test.py
'''
from cv2 import cv2
import time
import datetime
import os

def resizepicandlabel(imagesize: tuple, labelsize: tuple):
    '''resize pic and label based on their siezs

    Parameters
    ----------
    image : tuple
        pic_size (int int)
    labelsize : tuple
        label_size (int int)
    '''
    int_frame_width = imagesize[0]
    int_frame_height = imagesize[1]
    int_label_width = labelsize[0]
    int_label_height = labelsize[1]
    float_proportion_width = int_frame_width / int_label_width
    float_proportion_heigth = int_frame_height / int_label_height
    return ([int_frame_width / float_proportion_width, int_frame_height / float_proportion_width, 0] if float_proportion_width > float_proportion_heigth else [int_frame_width / float_proportion_heigth, int_frame_height / float_proportion_heigth, 1])

def get_time_stamp():
    now = int(round(time.time()*1000))
    time_stamp = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now/1000))
    print(time_stamp.__class__)
    stamp = ("".join(time_stamp.split()[0].split("-"))+"".join(time_stamp.split()[1].split(":"))).replace('.', '')
    print(stamp)

def get_headchid(path: str):
    with open(path, 'r', encoding='UTF-8') as p:
        fds_lines = p.readlines()
        for i in fds_lines :
            if i.find('HEAD') == 1:
                return i.split('\'')[1]

def creat_folders(fds_path: str, case_num: int):
    """
    建立新的cases的文件夹，将fds源文本的路径传入，合成时间作为新的文件夹位置
    :param fds_path: fds源文本的路径
    :param case_num: 新文件夹内的子目录个数，等于疏散案例的个数
    :return:新生成文件夹的路径
    """
    fds_path_list = fds_path.split('\\', 10)
    target_path = ''
    for i in range(len(fds_path_list) - 1):
        target_path += fds_path_list[i] + '\\'
    time_stamp = datetime.datetime.now()
    target_path += time_stamp.strftime('%m-%d-%H-%M')
    evac_res_path = target_path + '\\evacres'
    os.makedirs(target_path)
    os.makedirs(evac_res_path)
    target_path += '\\'
    target_path_list = []
    for i in range(case_num):
        os.makedirs(target_path + 'STR-' + str(i))
        target_path_list.append(target_path + 'STR-' + str(i))
    return target_path_list


def fds_duplicate(fds_path: str, fds_lines_list: list, tag_line: str):
    """
    :将新fds文件的路径、fds源文本的lines作为list、需要改写的line传入，生成完整的新的fds文件
    :param fds_path:新生成的fds文件路径
    :param fds_lines_list:源文本的fds的lines作为list
    :param tag_line:需要写入的line
    :return:0代表失败、1代表成成功
    """
    fds_io = open(fds_path, 'a', encoding='UTF-8')  # 新建文件写入io
    # 循环将源文本中的lines通过io写入新的文件中
    for i in range(len(fds_lines_list)):
        fds_io.write(fds_lines_list[i])
    fds_io.write(tag_line)  # 将需要写入的句子写入新的文件中
    fds_io.write('&TAIL/')
    fds_io.close()
    return 1


def change_line(person_num: int):
    """
    传入新的人数数据（单个），嵌入需要写入的句子
    &EVAC ID='EVAC1', XB=0.00,10.00,0.00,8.00,0.4000,1.60, NUMBER_INITIAL_PERSONS= * , PERS_ID='person1'/  \n
    :param person_num: 需要写入的人数数字
    :return: 返回新生成的line
    """
    org = "&EVAC ID='EVAC', XB=1.60,10.00,0.00,10.00,0.4000,1.60, NUMBER_INITIAL_PERSONS= *, PERS_ID='person'/\n"
    org_list = org.split('*', 2)
    tag_line = org_list[0] + str(person_num) + org_list[1]
    return tag_line


def fds_duplicate_s(case_folder_path: str, fds_path: str, per_nums_list: list):
    """
    批量复制写入新的fds文件中
    :param case_folder_path: 当前批次的新fds文件的文件夹路径
    :param fds_path: 当前批次新fds文件的源文件（是最起初的fds文件，不包含人数line，各自之间的区别在于疏散策略）
    :param per_nums_list: 需要写入的人数list
    :return:返回新生成的fds文件的路径list
    """
    fds_run_paths = []  # 新写的fds文件的路径list，用于返回
    new_fds_folder_path_list = []
    fds_io = open(fds_path, 'r')  # fds源文件的io，用于复制
    fds_lines = fds_io.readlines()  # 读取fds源文件中的lines
    for i in range(len(per_nums_list)):  # 根据人数数据建立循环
        new_fds_folder_path = case_folder_path + '\\' + 'NUM-' + str(i)  # 当前策略下、当前人数下，新写成fds文件及其运行生成文件的存储目录
        new_fds_folder_path_list.append(new_fds_folder_path)
        os.makedirs(new_fds_folder_path)  # 创造此文件夹
        new_fds_path = new_fds_folder_path + '\\' + 'case-' + str(i) + '.fds'  # 当前策略、人数下生成的新的fds文件的路径，用于添加到lust中
        fds_duplicate(new_fds_path, fds_lines, change_line(per_nums_list[i]))  # 根据此新路径复制fds文件
        fds_run_paths.append(fds_run.create_run_bat(new_fds_path, 'fds'))
    return fds_run_paths     

if __name__ == '__main__':
    a = []
    for i in range(4):
        a.append(i)
    print(a)