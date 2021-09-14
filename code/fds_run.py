import os
import sys
import io


def bat_write(p: io.TextIOWrapper, fds_path: str):
    """
    书写fds、smokeview的运行bat文件
    :param p: 需要写入的bat文件的io
    :param fds_path: 需要配置运行文件的fds文件夹的路径
    :return: 返回生成运行文件的路径
    """
    list_of_fdspath = fds_path.split('\\', 10)
    p.write('@echo off \n')
    p.write(list_of_fdspath[0] + '\n')
    p.write('cd' + ' ')
    for i in range(len(list_of_fdspath) - 2):
        p.write('\\' + list_of_fdspath[i + 1])
    p.write('\\' + '\n')


def create_run_bat(path: str, mode: str):
    """
    新创建一个运行文件
    :param path:需要配置运行文件的fds路径
    :param mode:需要的是fds、smokeview
    :return:生成bat文件的路径
    """
    # 找出当前路径fds文件的head chid
    fds_head = get_headchid(path)
    # 找出当前要书写的例子的case id，用以生成运行文件的路径
    list1 = path.split('\\', 10)  # 将路径分隔
    target_path = ''  # 定义运行文件路径为空字符串
    for i in range(len(list1) - 1):  # 循环将fds路径分隔的结果加到运行文件路径，但是最后的命名不在此
        target_path += list1[i] + '\\'
    if mode == 'fds':
        # 根据fds文件的路径中的fds文件名‘name.fds’，将fds运行文件的文件名写为‘name-run.bat"
        target_path += list1[len(list1) - 1].split('.', 1)[0] + '-run.bat'
    else:
        target_path += list1[len(list1) - 1].split('.', 1)[0] + '-smv-' + 'run.bat'
    p = open(target_path, 'a', encoding='UTF-8')
    bat_write(p, path)
    if mode == 'fds':
        p.write('fds ' + list1[len(list1) - 1] + '\n')
    else:

        p.write(list1[len(list1) - 1].split('.', 1)[0] + '.smv \n')
    p.write('cd\\ ')
    p.close()
    return target_path


'''
获得指定路径的fds程序中的head chid，用于smokeview的runbat
path：fds文件的相对路径
'''


def get_headchid(path: str):
    p = open(path, 'r', encoding='UTF-8')
    fds_lines = p.readlines()
    fds_head = 'does not find head'
    for i in range(fds_lines.__len__()):
        if fds_lines[i].find('HEAD') == 1:
            fds_head = fds_lines[i]
            i = len(fds_head)
        else:
            pass
    list1 = fds_head.split('\'', 2)
    return list1[1]
