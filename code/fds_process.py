import os
import sys
import io
import datetime

def get_headchid(fds_path: str):
    '''找出fds文件的headchid

    Args:
        fds_path (str): fds文件路径

    Returns:
        str: 指定fds文件的headchid
    '''
    with open(fds_path, 'r', encoding='UTF-8') as p:
        list_string_fdslines = p.readlines()
        for i in list_string_fdslines:
            if i.find('HEAD') == 1:
                return i.split('\'')[1]

def bat_write(p:io.TextIOWrapper, fds_path:str):
    '''用于生成.bat文件

    Args:
        p (io.TextIOWrapper): 待写入的.bat文件io流
        fds_path (str): 需配置.bat文件的fds文件路径

    Returns:
        无返回值,通过io流直接将该bat文件书写完成,需要的io流在调用此函数前就已打开
    '''
    list_str_fdspath_part = fds_path.split('\\', 15) # 将路径分割
    p.write('@echo off \n')
    p.write(list_str_fdspath_part[0] + '\n')
    p.write('cd' + ' ')
    for i in range(len(list_str_fdspath_part) - 2):
        p.write('\\' + list_str_fdspath_part[i + 1])
    p.write('\\' + '\n')
    return 1

def create_run_bat(fds_path:str, mode:str):
    '''为fds与smokeview创建.bat运行文件

    Args:
        fds_path (str): 需要创建运行文件的fds路径
        mode (str): 1-fds,2-smokeview  
    Returns:
        str: 返回生成的.bat文件路径
    '''
    # 找出当前路径fds文件的head chid
    string_fdshead = get_headchid(fds_path=fds_path)
    # 生成.bat文件路径
    string_bat_path = fds_path.replace('.fds', '-fds.bat' if mode == 1 else '-smv.bat')
    with open(string_bat_path, 'w', encoding='UTF-8') as p:
        bat_write(p, fds_path)
        if mode == 1:
            p.write('fds ' + string_fdshead + '.fds\n')
        else:
            p.write(string_fdshead.split('.', 1)[0] + '.smv \n')
        p.write('cd\\ ')
    p.close()
    return string_bat_path

def create_folders(fds_path:str, case_num:int):
    '''在当前选中的fds文件的目录下创建一个含时间戳的文件夹用于存储后续计算结果
    在该文件夹内,含有case_num个子文件夹(名为STR-i),每个文件夹代表一个选中的fds
    文件,在该文件夹内后续会写入新的子文件夹(NUM-i)用于存储该fds文件(策略)下不同
    人数的疏散计算结果

    Args:
        fds_path (str): 源fds文件地址
        case_num (int): 新文件夹内子目录个数,等于疏散案例的个数

    Returns:
        list:string-用于存储各个case的运行结果
    ''' 
    list_fdspath_part = fds_path.split('\\', 15)
    time_stamp = datetime.datetime.now().strftime('%m-%d-%h-%M')
    string_folder_path = fds_path.replace('.fds', time_stamp)
    string_evacres_plot_folderpath = string_folder_path + 'evac_res_plot'
    os.mkdir(string_folder_path)
    os.mkdir(string_evacres_plot_folderpath)
    tmp_str_path = string_folder_path + '\\'
    list_string_path = []
    for i in range(case_num):
        os.mkdir(tmp_str_path + 'STR-' + str(i))
        list_string_path.append(tmp_str_path + 'STR-' + str(i)) 
    return list_string_path

a = create_folders('A:\\tkinter\\code\\fds\\case0_all.fds', 10)