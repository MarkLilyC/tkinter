import os
import sys
import io
import datetime
from tkinter.constants import YES

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

def fds_duplicate(fds_path: str, fds_lines_list: list, tag_line: str):
    '''生成完整的fds文件

    Args:
        fds_path (str): 新生成的完整的fds文件路径
        fds_lines_list (list): 源fds文件中的行list
        tag_line (str): 需要改变的fds语句行

    Returns:
        bool: 写入成功与否
    '''
    
    with open(fds_path, 'a', encoding='UTF-8') as io_new_fds: # 新建文件写入io
    # 循环将源文本中的lines通过io写入新的文件中
        for i in fds_lines_list:
            io_new_fds.writelines(i)
        io_new_fds.write(tag_line)  # 将需要写入的句子写入新的文件中
        io_new_fds.write('&TAIL/')
    io_new_fds.close()
    return YES

def change_line(person_num: int):
    '''传入待写入的人数数据,生成完整的fds疏散语句
    &EVAC ID='EVAC1', XB=0.00,10.00,0.00,8.00,0.4000,1.60, NUMBER_INITIAL_PERSONS= * , PERS_ID='person1'/  \n
    Args:
        person_num (int): 待写入的人数数据

    Returns:
        str': 完整的fds疏散语句
    ''' 
    str_oriline = "&EVAC ID='EVAC', XB=1.60,10.00,0.00,10.00,0.4000,1.60, NUMBER_INITIAL_PERSONS= *, PERS_ID='person'/\n"
    return str_oriline.replace('*', str(person_num))

def fds_duplicate_s(case_folder_path: str, fds_path: str, per_nums_list: list):
    '''批量复制写入新的fds文件

    Args:
        case_folder_path (str): 当前批次的fds文件文件夹路径
        fds_path (str): 当前批次的fds文件源文件(不包含人数line)
        per_nums_list (list): 需要写入的人数list

    Returns:
        list: 返回新生成的fds文件的.bat路径list
    '''
    """
    批量复制写入新的fds文件中
    :param case_folder_path: 当前批次的新fds文件的文件夹路径
    :param fds_path: 当前批次新fds文件的源文件（是最起初的fds文件，不包含人数line，各自之间的区别在于疏散策略）
    :param per_nums_list: 需要写入的人数list
    :return:返回新生成的fds文件的路径list
    """
    list_string_fdsbat_listr = '' # .bat文件路径list
    with open(fds_path, 'r', encoding='UTF-8') as p :
        fds_lines = p.readlines()
    p.close()
    string_headchid = get_headchid
    tmp_int_index = 0
    for i in fds_lines:
        string_newfds_folderpath = case_folder_path + '\\NUM-' + str(tmp_int_index) # 当前fds源文件下(策略下)个人数条件下的fds文件夹
        os.mkdir(string_newfds_folderpath)
        string_new_fds = string_newfds_folderpath + '\\' + 

    '''list_string_fdsbat_path = []  # .bat文件路径list
    new_fds_folder_path_list = []
    fds_io = open(fds_path, 'r')  # fds源文件的io，用于复制
    fds_lines = fds_io.readlines()  # 读取fds源文件中的lines
    for i in range(len(per_nums_list)):  # 根据人数数据建立循环
        new_fds_folder_path = case_folder_path + '\\' + 'NUM-' + str(i)  # 当前策略下、当前人数下，新写成fds文件及其运行生成文件的存储目录
        new_fds_folder_path_list.append(new_fds_folder_path)
        os.makedirs(new_fds_folder_path)  # 创造此文件夹
        new_fds_path = new_fds_folder_path + '\\' + 'case-' + str(i) + '.fds'  # 当前策略、人数下生成的新的fds文件的路径，用于添加到lust中
        fds_duplicate(new_fds_path, fds_lines, change_line(per_nums_list[i]))  # 根据此新路径复制fds文件
        list_string_fdsbat_path.append(create_run_bat(new_fds_path, 1))
    return list_string_fdsbat_path'''


# a = create_folders('A:\\tkinter\\code\\fds\\case0_all.fds', 10)
