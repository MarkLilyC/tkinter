import os
import datetime
import fds_run
import subprocess
import ana_excel
import cv2
import numpy as np
import sub_find_Back


#  C:\Users\edison\Desktop
#  &EVAC ID='EVAC1', XB=0.00,10.00,0.00,8.00,0.4000,1.60, NUMBER_INITIAL_PERSONS=1, PERS_ID='person1'/

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


def fds_bats_run(fds_run_paths: list):
    """
    运行fds以及smokeview的bat文件
    :param fds_run_paths: fds的运行文件路径list
    :return: 0
    """
    for i in range(len(fds_run_paths)):
        p = subprocess.Popen(
            "cmd.exe /c" + fds_run_paths[i],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        cur_line = p.stdout.readline()
        while cur_line != b'':
            print(cur_line)
            cur_line = p.stdout.readline()
    return 0


def cal(delay, back):
    # 读取视频
    list1 = sub_find_Back.video_read('..//Input//pets.mp4', 50, delay)
    # 计算背景

    if back is None:
        back = sub_find_Back.subGetBack(list1[0], list1[10])
        print('背景合成完成')
        per_nums_list = sub_find_Back.counts(list1, back)
        # per_nums_list = [5, 3, 1, 2, 3, 2, 2, 1, 3, 3, 1, 1]
        print("人数计数完成：")
        print(per_nums_list)  # [5, 3, 1, 2, 3, 2, 2, 1, 3, 3, 1, 1]
    else:
        # 计算人数
        per_nums_list = sub_find_Back.counts(list1, back)
        # per_nums_list = [5, 3, 1, 2, 3, 2, 2, 1, 3, 3, 1, 1]
        print("人数计数完成：")
        print(per_nums_list)  # [5, 3, 1, 2, 3, 2, 2, 1, 3, 3, 1, 1]
    return per_nums_list, back

# 定义（输入）模板文件的路径
list_path = []
path0 = 'C:\\Users\\edison\\Desktop\\test\\base.fds'
list_path.append(path0)
path1 = 'C:\\Users\\edison\\Desktop\\test\\base-l.fds'
list_path.append(path1)
path2 = 'C:\\Users\\edison\\Desktop\\test\\base-l.fds'
list_path.append(path2)
path3 = 'C:\\Users\\edison\\Desktop\\test\\case1-a.fds'
list_path.append(path3)
path4 = 'C:\\Users\\edison\\Desktop\\test\\case1-l.fds'
list_path.append(path4)
path5 = 'C:\\Users\\edison\\Desktop\\test\\case1-r.fds'
list_path.append(path5)
path6 = 'C:\\Users\\edison\\Desktop\\test\\case2-a.fds'
list_path.append(path6)
path7 = 'C:\\Users\\edison\\Desktop\\test\\case2-l.fds'
list_path.append(path7)
path8 = 'C:\\Users\\edison\\Desktop\\test\\case2-r.fds'
list_path.append(path8)
# [5, 3, 1, 2, 3, 2, 2, 1, 3, 3, 1, 1]
per_nums_list = [36,42,57,40,59]
# 根据模板文件的路径创建新的工程的文件夹，由于新工程文件和模板文件是在同一级目录，因此任意选择模板文件的路径传入皆可
new_folders_path_list = creat_folders(path0, 9)

fds_bat_paths_list = []
# 将人数数据传入到四个模板文件中，返回对应生成的fds新文件的文件夹路径list
pathListList = []
for i in range(len(list_path)):
    tmp = fds_duplicate_s(new_folders_path_list[i], list_path[i], per_nums_list)
    # print(tmp)
    fds_bat_paths_list.append(tmp)


# 执行完整的fds文件
for i in fds_bat_paths_list:
    fds_bats_run(i)

csv_time_person_by_num = ana_excel.getParentPathByNum(fds_bat_paths_list, len(per_nums_list))  # 获得所有csv文件路径，通过人数分组，共12组每组八个
time_person_by_num = []
for i in csv_time_person_by_num:  # i即为每个人数各策略下cvs文件的数组
    tmplist = []  # 用于保存当前人数下各策略下的时间
    for j in i:  # j为内部数组下的各csv文件路径
        time = ana_excel.gettimebyperson(j)  # 获取时间
        tmplist.append(time)
    time_person_by_num.append(tmplist)
for i in time_person_by_num:
    for j in i:
        if j == 's':
            i[i.index(j)] = '40'
res_path = csv_time_person_by_num[0][0]
for i in range(3):
    res_path = os.path.dirname(res_path)
res_path += '\\evac'  # 用于存放提取出的人数下的疏散时间文件（txt）与绘制图像
res_path_txt = res_path + '\\Num_time'
res_path_pic = res_path + '\\Pics'
os.makedirs(res_path)
os.makedirs(res_path_txt)
os.makedirs(res_path_pic)
print(time_person_by_num)
for i in range(len(time_person_by_num)):
    pathtmp = res_path_txt + '\\' + str(i) + '.txt'
    file_handle = open(pathtmp, mode='w')
    for j in time_person_by_num[i]:
        file_handle.write(j + ',')
    file_handle.write('\n')
ana_excel.numtimepic(time_person_by_num, per_nums_list, res_path_pic)