'''
Author: your name
Date: 2021-09-07 11:43:55
LastEditTime: 2021-09-16 16:08:12
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \tkinter\code\demo1.py
'''

import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
import tkinter
from PIL import Image, ImageTk
import win32api
import os
import cv2
import time
from tkinter import scrolledtext
import numpy as np
import subprocess
import io
from tkinter.constants import YES

# 声明一些变量
list_string_filepath = [] # 存储选中的FDS路径
list_string_filename = [] # 存储选中的FDS名
string_comb_curitem = '' # 存储comb当前选中的文件名
string_video_path = '' # 存储当前选中的视频地址
string_videodec_results_path = [] # 存储当前视频检测结果图像文件夹
list_string_videopath_his = [] # 存储从历史记录中读取的videos历史记录
bool_fdshis_exist = NO # 是否存在fds的历史使用记录
bool_videohis_exist = NO # 是否存在video的历史使用记录
bool_fdsimported = NO # 是否存在手动选择的fds文件
string_workcwd_dir = os.getcwd() + '/work'
string_path_rc = os.getcwd() + '/work/videtectrc.txt' # 获取并创建历史工作文件夹路径
string_path_fdshis_arti = os.getcwd() + '/work/fdshis.txt' # 获取并创建历史工作文件夹路径
string_path_fdshis_auto = os.getcwd() + '/work/fdshis_all.txt' # 获取并创建历史工作文件夹路径
string_path_videohis_arti = os.getcwd() + '/work/videohis.txt'
string_path_videohis_auto = os.getcwd() + '/work/videohis_all.txt'
string_path_backgroud = '' # 存储背景图像地址
list_string_path_frame = [] # 存储截取的原始图像地址
list_string_path_frame_dst = [] # 存储生成检测结果图像地址
list_int_person_num = []
int_read_delay = 10
int_detect_delay = 30
int_frame_count = 0
tuple_float_picsize_resize = ()
tuple_float_picsize_resize_2 = ()
bool_auto_detect = NO
string_resfolder_path = ''

def import_fdsfiles():
    # 声明为全局变量
    global list_string_filepath 
    global list_string_filename 
    global bool_fdsimported 
    global string_comb_curitem  
    tuple_string_filepath = filedialog.askopenfilenames(filetypes=[('FDS files', ('.fds', '.FDS'))]) # 打开窗口选择fds文件
    list_string_filepath = list(tuple_string_filepath) # 创建list存储选中的fds文件路径
    if tuple_string_filepath: # 当选择文件后
        btn_init()
    else:
        print("未选择任何文件")

def get_time_stamp():
    '''获取时间戳

    Returns
    -------
    str
        时间戳：年月日 时分秒
    '''
    now = int(round(time.time()*1000))
    time_stamp = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(now/1000))
    return time_stamp

def test_func():
    global list_string_filename
    global list_string_filepath
    global bool_fdshis_exist
    global bool_fdsimported
    bool_fdsimported = NO
    btns_change_f([btn_video_save, btn_win_init, text_info_videodetection, label_video, 
    comb_filenames, btn_file_delete, btn_file_save, btn_file_edit], 3)
    # fds文件引入按钮
    btn_open.place(x=170, y=140) 
    btn_open.config(image=tkimage_open) 
    btn_open.config(state=NORMAL)
    # video引入按钮
    btn_play.place(x=460, y=140) 
    btn_play.config(image=tkimage_play_f) 
    btn_play.config(image=tkimage_play, state=DISABLED)
    # 历史引入按钮
    btn_fds_his.place(x=354, y=140)
    bool_fdshis_exist, tmp_list = gethis_list_bool(1)
    btn_fds_his.config(state=(NORMAL if bool_fdshis_exist else DISABLED)) # 设置点击模式
    btn_video_his.place(x=418, y=282)
    btn_video_his.config(state=DISABLED)
    # 清空text控件内容
    text_info_videodetection.delete(0.1, 'end')

def btns_change_f(list_btns: list, mode: int):
    '''作为btn的状态修改函数

    Parameters
    ----------
    list_btns : list[btn1,btn2]
        将待修改状态的btns作为列表元素传入
    mode : int
        修改模式:1-2disabled，2-2normal，3-2forgot
    '''
    if mode == 1 :
        for i in list_btns:
            i.configure(state=DISABLED)
    elif mode == 2:
        for i in list_btns:
            i.configure(state=NORMAL)
    else :
        for i in list_btns:
            i.place_forget()

def comb_getcur(event): 
    '''通过comb选中选项激活文件功能按钮，并声明一个全局变量储存当前所选中的item

    Parameters
    ----------
    event : [type]
        [description]
    '''
    global string_comb_curitem
    string_comb_curitem = comb_filenames.get()
    # 不通过点击某一个comb选项来生成文件功能按钮，但是需要此点击事件来获取最新选中item，以便完成item删除
    '''btn_file_edit.place(x=170, y=350) # 添加文件编辑按钮
    btn_file_delete.place(x=243 , y=350) # 添加文件删除按钮
    btn_file_save.place(x=316, y=350) # 添加fds文件组合保存按钮  '''

def btn_init():
    '''激活文件功能按钮
    '''
    global list_string_filepath 
    global list_string_filename 
    global bool_fdsimported 
    global string_comb_curitem  
    global bool_videohis_exist
    btn_open.config(image=tkimage_opened) # 将文件打开图标置为check图标
    btn_file_edit.place(x=170, y=350) # 添加文件编辑按钮
    btn_file_delete.place(x=243 , y=350) # 添加文件删除按钮
    btn_file_save.place(x=316, y=350) # 添加fds文件组合保存按钮  
    btns_change_f([btn_file_delete, btn_file_edit, btn_file_save], 2)
    btn_play.config(image=tkimage_play, state=NORMAL) # 更改播放按钮图标与状态
    btn_video_his.config(state=(NORMAL if gethis_list_bool(2)[1] else DISABLED))
    comb_filenames.place(x=170, y=325) # 将comb绑定到窗口
    # comb设置
    list_string_filename = list(map(lambda x : x.strip().split('/', 10)[-1], list_string_filepath))
    comb_filenames['values'] = tuple(list_string_filename) # 设置comb值
    comb_filenames.current(0) # 设置当前comb选中项为0（index）
    comb_filenames.update() # update
    # 改变一些变量
    string_comb_curitem = comb_filenames.get() # 赋值为当前选中
    bool_fdsimported = YES

def videoplay_init(path): 
    global tuple_float_picsize_resize
    global tuple_float_picsize_resize_2
    global int_frame_count
    video_tobeplayed = cv2.VideoCapture(path)
    int_frame_count = int(video_tobeplayed.get(cv2.CAP_PROP_FRAME_COUNT)) # 帧数
    bool_isopened, ndarray_image_1stframe = video_tobeplayed.read() # 获取视频第一帧
    ndarray_image_1stframe = cv2.cvtColor(ndarray_image_1stframe, cv2.COLOR_BGR2RGBA)
    if bool_isopened:
        # 页面改动
        btn_open.place(x=5, y=0)
        btn_file_edit.place(x=5, y=210)
        btn_file_delete.place(x=78, y=210)
        btn_file_save.place(x=151, y=210)
        comb_filenames.place(x=5, y=185)
        text_info_videodetection.place(x=5, y=250)
        btn_video_save.place(x = 220, y = 410)
        btn_videodetection_results.place(x = 220, y = 462)
        btns_change_f([btn_play, btn_fds_his, btn_video_his],3)
        btns_change_f(list_btns=[btn_open, btn_file_edit, btn_file_delete, btn_file_save], mode=1)
        btn_win_init.place(x=5, y=470)
        # ndarray_image_1stframe = cv2.cvtColor(ndarray_image_1stframe, cv2.COLOR_BGR2BGRA) 
        # 获取视频图像信息
        tuple_image_info = ndarray_image_1stframe.shape
        int_frame_width = tuple_image_info[1]
        int_frame_height = tuple_image_info[0] 
        # 对图像进行缩放
        tuple_float_picsize_resize = tuple(map(int, resizepicandlabel((int_frame_width, int_frame_height), (600, 400)))) 
        tuple_float_picsize_resize_2 = tuple(map(int, resizepicandlabel((int_frame_width, int_frame_height), (123, 82)))) 
    
        # ndarray_image_1stframe = cv2.resize(ndarray_image_1stframe, tuple_float_picsize_resize,interpolation=cv2.INTER_NEAREST) # 采用最近邻插值法缩放图片
        image_1st = Image.fromarray(ndarray_image_1stframe).resize(tuple_float_picsize_resize[:2]) 
        tkimage_1stframe = ImageTk.PhotoImage(image=image_1st)
        image_1st_c = Image.fromarray(ndarray_image_1stframe).resize(tuple_float_picsize_resize_2[:2]) 
        tkimage_1stframe_c = ImageTk.PhotoImage(image=image_1st_c)
        # 创建label
        # label_video = tk.Label(win_main, width=tuple_float_picsize_resize[0], height=tuple_float_picsize_resize[1], bd=0, bg='#333333')
        # 当原图缩放依据为height（即缩放后高满尺寸），此时宽度未达到600，应将图片在图片展示区域设置；当缩放依据为width时 同理
        label_video_x, label_video_y = ((194 if tuple_float_picsize_resize[2] == 0 else (494 - tuple_float_picsize_resize[0]/2)),
                                        (0 if tuple_float_picsize_resize[2] == 1 else (200- tuple_float_picsize_resize[1]/2)))
        label_video.place(x=label_video_x, y=label_video_y)
        # 贴图
        label_video.configure(image=tkimage_1stframe)
        label_video.image = tkimage_1stframe 
        label_video.update() 
        # 文本信息更新
        text_insert_changeline(text_info_videodetection, '视频读取成功')
        # 添加关于视频检测信息展示的按钮
        label_show_back.place(x=266, y=410)
        label_show_back.configure(image=tkimage_1stframe_c)
        label_show_back.image = tkimage_1stframe_c 
        label_show_back.update() 
        int_label_showre_x = 266 + tuple_float_picsize_resize_2[0] + 10
        label_show_res.place(x=int_label_showre_x, y=410)
        tree_info.insert("", 0, text="line1", values=(int_frame_count, int_read_delay, int_detect_delay, '--'))    # #给第0行添加数据，索引值可重复
        tree_info.place(x=int_label_showre_x + tuple_float_picsize_resize_2[0] + 10, y=453)
        tree_info_path.insert("", 0, text="line1", values=(string_video_path))
        tree_info_path.place(x=int_label_showre_x + tuple_float_picsize_resize_2[0] + 10,y=408)
        label_show_res.configure(image=tkimage_1stframe_c)
        label_show_res.image = tkimage_1stframe_c 
        label_show_res.update() 
        # 进行fds文件的准备工作
        return YES
    else:
        text_insert_changeline(text_info_videodetection, "视频读取失败")
        return NO

def btn_fds_his_f():
    global list_string_filepath
    global list_string_filename
    global bool_fdsimported
    with open(string_path_fdshis_arti, 'r', encoding='utf-8') as f:
        list_string_filepath = f.readlines() # 修改fds路径列表
        list_string_filepath.pop(0)
        list_string_filepath = list(map(lambda x : x.strip(), list_string_filepath)) # 去除从his文件中读取的filepath后带的'\n'
        list_string_filename = list(map(lambda x : x.split('/', 10)[-1], list_string_filepath))
    if bool_fdsimported:
        # 当存在手动导入的fds文件，则当点击从历史记录读取时，应只修改comb值
        # 读取fdshis内的记录
        comb_filenames['values'] = list_string_filename
        comb_filenames.current(0)
        comb_filenames.update()
    else:
        btn_init()

def btn_video_his_f():
    global string_video_path
    global string_videodec_results_path
    global bool_if_videoopened
    global tuple_float_picsize_resize
    global list_int_person_num
    string_video_path = list_string_videopath_his[-1]
    string_videodec_results_path = string_video_path.replace(string_video_path.split('.')[-1], '_results')
    bool_if_videoopened = videoplay_init(string_video_path)
    tuple_folat_labelsize = tuple_float_picsize_resize[:2]
    if bool_if_videoopened:
        time.sleep(1)
        string_resfolder_path, list_string_pics_path = get_video_frame(string_video_path, label_video, tuple_folat_labelsize)
        # 开始人员计数
        tmp_int_index = int(len(list_string_pics_path)/2)
        ndarray_back = subGetBack(list_string_pics_path[0], list_string_pics_path[tmp_int_index], string_resfolder_path)
        if ndarray_back is not NONE:
            video_play(ndarray_back, label_video, tuple_folat_labelsize)
            text_insert_changeline(text_info_videodetection, "背景合成完成")
            label_show_back.place(x=266, y=410)
            int_label_showre_x = 266 + tuple_float_picsize_resize_2[0] + 10
            label_show_res.place(x=int_label_showre_x, y=410)
            for i in list_string_pics_path:
                int_per_num, ndarray_deection_res = person_count(ndarray_back, i)
                video_play(ndarray_deection_res, label_video, tuple_folat_labelsize[:2])
                video_play(ndarray_deection_res, label_show_res, tuple_float_picsize_resize_2[:2])
                list_int_person_num.append(int_per_num)
                tmp = i.split('_', 5)[-1].replace('.jpg', '')
                text_insert_changeline(text_info_videodetection,'第' + tmp + '帧检测完成')
                tree_info.insert("", 0, text="line1", values=(int_frame_count, int_read_delay, int_detect_delay, tmp))  
            text_insert_changeline(text_info_videodetection, '行人计数完成')
            text_insert_changeline(text_info_videodetection, '开始疏散模拟')
            text_insert_changeline(text_info_videodetection, 'FDS结果文件夹创建..')
            list_string_newfolderpath = create_folders(list_string_filepath)
            text_insert_changeline(text_info_videodetection, '创建完成')
            list_list_string_fdsbatpath = []
            text_insert_changeline(text_info_videodetection, 'FDS文件赋值..')
            for i in range(len(list_string_filepath)):
                tmp =  fds_duplicate_s(list_string_newfolderpath[i], list_string_filepath[i],list_int_person_num)
                list_list_string_fdsbatpath.append(tmp)
            text_insert_changeline(text_info_videodetection, '赋值完成')
            text_insert_changeline(text_info_videodetection, 'FDS开始运行..')
            for i in list_list_string_fdsbatpath:
                fds_bats_run(i)

            # 辅助按钮状态回复
            text_insert_changeline(text_info_videodetection, '全部运行完成')
            btns_change_f([btn_win_init, btn_video_save, btn_videodetection_results], 2)

    else:
        text_insert_changeline(text_info_videodetection, "视频打开失败")

def btn_file_edit_f():
    '''打开记事本查看编辑选中的fds文件
    '''
    string_comb_curitem = comb_filenames.get()
    tmp_path = list_string_filepath[list_string_filename.index(string_comb_curitem)]
    win32api.ShellExecute(0, 'open', 'notepad.exe', tmp_path,'',1)
       
def btn_file_delete_f():
    '''在namelist删除当前comb中选中的item，再将tuple（list）赋值给comb——value，最后update，实现对comb中items的删除
    case
        1.当能删除（删除按钮显示时）
            能进行当前元素的删除
        2.当删除某元素后，列表不为空
            应将comb值设置为列表第一，并将string——comb——curitem设置为第一个元素
        3. 当删除元素后，列表为空
            应将文件编辑等按钮隐藏
    '''
    global bool_fdsimported
    string_comb_curitem = comb_filenames.get() # 获取当前comb选中值
    int_tmp_index = list_string_filename.index(string_comb_curitem)
    list_string_filename.remove(string_comb_curitem) # 在namelist中删除当前item
    list_string_filepath.pop(int_tmp_index) # 在pathlist中删除当前item对应的path
    if list_string_filename: # 当删除元素后，列表不为空
        comb_filenames['values'] = tuple(list_string_filename) # 将更新后的list转换为tuple赋值给comb
        comb_filenames.current(0) # 设置当前comb选中项为0（index）
        string_comb_curitem = list_string_filename[0] # 设置当前string_comb_curitem为第一个元素
        comb_filenames.update() # update
    else: # 当列表为空后
        bool_fdsimported = NO
        btn_file_delete.place_forget()
        btn_file_edit.place_forget()
        btn_file_save.place_forget()
        comb_filenames.place_forget()
        btn_open.config(image=tkimage_open) # 回复打开按钮图标
        btn_play.configure(state=DISABLED, image=tkimage_play_f)
        
def btn_file_save_f():
    '''存储当前选中fds文件路径
    '''
    time_stamp_tmp = get_time_stamp()
    save_videohis_auto(time_stamp_tmp, 1, list_string_filepath)
    if os.path.exists(string_workcwd_dir): # 当此路径存在 
        with open(string_path_fdshis_arti, 'w') as f:
            f.writelines(time_stamp_tmp + '\n')
            for i in list_string_filepath:
                f.writelines(i + '\n')
    else: # 当此路径不存在则创建对应文件夹与文件
        os.mkdir(string_workcwd_dir)
        with open(string_path_fdshis_arti, 'w') as f:
            f.writelines(time_stamp_tmp + '\n')
            for i in list_string_filepath:
                f.writelines(i + '\n')
    btn_fds_his.config(state=NORMAL)

def btn_video_save_f():
    time_stamp_tmp = get_time_stamp()
    save_videohis_auto(time_stamp_tmp, 2, [string_video_path])
    if os.path.exists(string_workcwd_dir): # 当此路径存在 
        with open(string_path_videohis_arti, 'w') as f:
            f.writelines(time_stamp_tmp + '\n')
            f.writelines(string_video_path)
    else: # 当此路径不存在则创建对应文件夹与文件
        os.mkdir(string_workcwd_dir)
        with open(string_path_videohis_arti, 'w') as f:
            f.writelines(time_stamp_tmp + '\n')
            f.writelines(string_video_path)

def btn_videodetection_results_f():
    os.system("start explorer " + string_resfolder_path.replace('/', '/'))

def save_videohis_auto(timestamp:str, mode:int, pathlist:list):
    '''自动存储用户选择的fds或者video文件

    Parameters
    ----------
    timestamp : str
        传入时间戳
    mode : int
        1-fds
        2-video
    pathlist : list
        待写入文件路径集合
    '''
    str_path_tmp = string_path_fdshis_auto if mode==1 else string_path_videohis_auto
    if os.path.exists(string_workcwd_dir): # 当此路径存在 
        with open(str_path_tmp, 'a') as f:
            f.writelines(timestamp + '\n')
            for i in pathlist:
                f.writelines(i + '\n')
    else: # 当此路径不存在则创建对应文件夹与文件
        os.mkdir(string_workcwd_dir)
        with open(str_path_tmp, 'a') as f:
            f.writelines(timestamp + '\n')
            for i in pathlist:
                f.writelines(i + '\n')
            
def btn_play_f():
    global string_video_path
    global list_string_filepath
    global list_int_person_num
    global string_resfolder_path
    string_video_path = filedialog.askopenfilename() # 打开窗口选择视频，暂时不限制文件类型
    if string_video_path: # 当选中视频后
        bool_if_videoopened = videoplay_init(string_video_path)
        label_show_back.place(x=266, y=410)
        int_label_showre_x = 266 + tuple_float_picsize_resize_2[0] + 10
        label_show_res.place(x=int_label_showre_x, y=410)
        time.sleep(1)
        tuple_folat_labelsize = tuple_float_picsize_resize[:2]
        if bool_if_videoopened:
            string_resfolder_path, list_string_pics_path = get_video_frame(string_video_path, label_video, tuple_folat_labelsize)
            text_insert_changeline(text_info_videodetection, "开始背景合成..")
            # 开始人员计数
            tmp_int_index = int(len(list_string_pics_path)/2)
            ndarray_back = subGetBack(list_string_pics_path[0], list_string_pics_path[tmp_int_index], string_resfolder_path)
            if ndarray_back is not NONE:
                video_play(ndarray_back, label_video, tuple_folat_labelsize)
                # 创建label
                # label_video = tk.Label(win_main, width=tuple_float_picsize_resize[0], height=tuple_float_picsize_resize[1], bd=0, bg='#333333')
                # 当原图缩放依据为height（即缩放后高满尺寸），此时宽度未达到600，应将图片在图片展示区域设置；当缩放依据为width时 同理
                '''label_show_x, label_show_y = ((255 if tuple_float_picsize_resize_2[2] == 0 else (316 - tuple_float_picsize_resize_2[0]/2)),
                                                (410 if tuple_float_picsize_resize_2[2] == 1 else (492- tuple_float_picsize_resize_2[1]/2)))
                label_show_x = label_show_x if label_show_x-242 < 6 else 255
                label_show_2_x, label_show_2_y = ((383 if tuple_float_picsize_resize_2[2] == 0 else (444 - tuple_float_picsize_resize_2[0]/2)),
                                                (410 if tuple_float_picsize_resize_2[2] == 1 else (492- tuple_float_picsize_resize_2[1]/2)))
                label_show_2_x = label_show_2_x if label_show_2_x-(label_show_x+tuple_float_picsize_resize_2[0]) < 6 else label_show_x+tuple_float_picsize_resize_2[0] + 5'''
                # 贴图
                video_play(ndarray_back, label_show_back, tuple_float_picsize_resize_2[:2])
                text_insert_changeline(text_info_videodetection, "背景合成完成")
                text_insert_changeline(text_info_videodetection, "开始行人计数..")
                for i in list_string_pics_path:
                    int_per_num, ndarray_deection_res = person_count(ndarray_back, i)
                    video_play(ndarray_deection_res, label_video, tuple_folat_labelsize[:2])
                    video_play(ndarray_deection_res, label_show_res, tuple_float_picsize_resize_2[:2])
                    list_int_person_num.append(int_per_num)
                    tmp = i.split('_', 5)[-1].replace('.jpg', '')
                    text_insert_changeline(text_info_videodetection,'第' + tmp + '帧检测完成')
                    tree_info.insert("", 0, text="line1", values=(int_frame_count, int_read_delay, int_detect_delay, tmp)) 
                text_insert_changeline(text_info_videodetection, '行人计数完成')
                time.sleep(3)
                text_insert_changeline(text_info_videodetection, '开始疏散模拟..')
                text_insert_changeline(text_info_videodetection, 'FDS结果文件夹创建..')
                list_string_newfolderpath = create_folders(list_string_filepath)
                text_insert_changeline(text_info_videodetection, '创建完成')
                list_list_string_fdsbatpath = []
                text_insert_changeline(text_info_videodetection, 'FDS文件赋值..')
                for i in range(len(list_string_filepath)):
                    tmp =  fds_duplicate_s(list_string_newfolderpath[i], list_string_filepath[i],list_int_person_num)
                    list_list_string_fdsbatpath.append(tmp)
                text_insert_changeline(text_info_videodetection, '赋值完成')
                text_insert_changeline(text_info_videodetection, 'FDS开始运行..')
                for i in list_list_string_fdsbatpath:
                    fds_bats_run(i)
                # 辅助按钮状态回复
                text_insert_changeline(text_info_videodetection, '全部运行完成')
                btns_change_f([btn_win_init, btn_video_save, btn_videodetection_results], 2)
        else:
            text_insert_changeline(text_info_videodetection, '视频打开失败')
    else: # 当未选中视频
        string_video_path = '' # 将此变量置空

def image2tk(iamgepath, target_size):
    '''[summary]Image方式读取图片，返回转换为tkimage

    Parameters
    ----------
    iamgepath : [string]
        文件路径
    size : [tuple]
        图片resize后的大小
    Returns
    -------
    tkimage
        tkimage用于btn展示
    '''
    return ImageTk.PhotoImage(image=Image.open(iamgepath).resize(target_size))

def resizepicandlabel(imagesize: list, labelsize: list):
    '''使pic尺寸缩放适合label尺寸

    Parameters
    ----------
    imageshape : list
        图片尺寸[width, height]
    labelsize : list
        label尺寸[width, height]

    Returns
    -------
    list
        [resize后宽度， resize后高度， resize所依照的proportion]
    '''
    int_frame_width = imagesize[0]
    int_frame_height = imagesize[1]
    int_label_width = labelsize[0]
    int_label_height = labelsize[1]
    float_proportion_width = int_frame_width / int_label_width
    float_proportion_heigth = int_frame_height / int_label_height
    return ((int_frame_width / float_proportion_width, int_frame_height / float_proportion_width, 0) if float_proportion_width > float_proportion_heigth else (int_frame_width / float_proportion_heigth, int_frame_height / float_proportion_heigth, 1))
       
def test_func2():
    os.system("start explorer " + string_resfolder_path.replace('/', '/'))

def text_insert_changeline(text:tkinter.Text, line:str):
    '''输入文字到Text控件并换行

    Parameters
    ----------
    text : tkinter.Text
        待输入文字的text控件
    line : str
        待输入的文字
    ''' 
    text.insert(tk.INSERT, line)
    text.insert(tk.INSERT, '\n')
    text.see(END)

def gethis_list_bool(mode:int):
    '''判断是否存在历史值

    Parameters
    ----------
    mdoe : int
        1-fds
        2-video
    '''
    tmp_list = []
    tmp_string_his_path = string_path_fdshis_arti if mode == 1 else string_path_videohis_arti
    if os.path.exists(tmp_string_his_path) :
        with open(tmp_string_his_path, 'r') as f:
            tmp_list = f.readlines()
        return YES if len(tmp_list) > 0 else NO, tmp_list
    else:
        return NO, []

def btn_win_init_f():
    global list_string_filename
    global list_string_filepath
    global bool_fdshis_exist
    global bool_fdsimported
    bool_fdsimported = NO
    btns_change_f([btn_video_save, btn_win_init, text_info_videodetection, label_video, 
    comb_filenames, btn_file_delete, btn_file_save, btn_file_edit,btn_videodetection_results,
    label_show_back, label_show_res, btn_videodetection_results, tree_info, tree_info_path], 3)
    # fds文件引入按钮
    btn_open.place(x=170, y=140) 
    btn_open.config(image=tkimage_open) 
    btn_open.config(state=NORMAL)
    # video引入按钮
    btn_play.place(x=460, y=140) 
    btn_play.config(image=tkimage_play_f) 
    btn_play.config(image=tkimage_play, state=DISABLED)
    # 历史引入按钮
    btn_fds_his.place(x=354, y=140)
    bool_fdshis_exist, tmp_list = gethis_list_bool(1)
    btn_fds_his.config(state=(NORMAL if bool_fdshis_exist else DISABLED)) # 设置点击模式
    btn_video_his.place(x=418, y=282)
    btn_video_his.config(state=DISABLED)
    # 清空text控件内容
    text_info_videodetection.delete(1.0, 'end')

def get_video_frame(video_path:str, label:tk.Label, re_size:tuple):
    '''从视频中截取图片，加载到label上

    Args:
        video_path (str): 视频路径
        label (tk.Label): 放置图片的label
        re_size (tuple): label的尺寸(width, height)
    '''
    time_stamp = get_time_stamp()
    str_resfolder = video_path.replace(video_path.split('.')[1], 'res-')
    str_resfolder += time_stamp # 结果文件文件夹
    os.mkdir(str_resfolder)
    str_resfolder_oripics = str_resfolder + '/results' # 结果图片文件夹
    os.mkdir(str_resfolder_oripics)
    list_path_pics = []
    cap = cv2.VideoCapture(video_path)
    flag = cap.isOpened()
    c = 1
    while flag:
        ret, ndarray_pic = cap.read()
        if ret:
            if (c-int_read_delay) % int_detect_delay == 0:
                ndarray_pic = cv2.cvtColor(ndarray_pic, cv2.COLOR_BGR2RGBA)
                tmp_pic_path = str_resfolder_oripics + "/capture_image_" + str(c) + '.jpg'
                text_insert_changeline(text_info_videodetection, "截取视频第：" + str(c) + " 帧..")
                ndarray_pic_res = video_play(ndarray_pic, label, re_size)
                cv2.imwrite(tmp_pic_path, ndarray_pic_res)
                list_path_pics.append(tmp_pic_path)
            c += 1
        else:
            text_insert_changeline(text_info_videodetection, "所有帧都已经保存完成..")
            text_insert_changeline(text_info_videodetection, "视频截取成功..")
            text_insert_changeline(text_info_videodetection, "开始行人检测计数..")
            break
    cap.release()
    # string_res_folderpath, list_video_frames_path = video_detection.video_read(string_video_path, 50, 10)
    return str_resfolder, list_path_pics

def video_play(pic:np.ndarray, label:tk.Label,re_size:tuple):
    '''将图片加载到label上，达到播放视频的效果

    Args:
        pic (np.ndarray): [利用cv2从视频中获得的图片]
        label (tk.Label): 加载图片的label
        re_size (tuple) : label的尺寸(width,height)
    Returns:
        [np.ndarray]: [resize并转换颜色空间后的图片]
    ''' 
    image_tobeplayed = Image.fromarray(pic).resize(re_size) # 将cv2读取的图像转换为Image,并修改大小
    imageTk_tobeplayed = ImageTk.PhotoImage(image=image_tobeplayed) # 转换为imagetk
    label.configure(image=imageTk_tobeplayed) # 使用configure方法将label更新为最新待播放图像
    label.image = imageTk_tobeplayed # 更新
    label.update() # 更新
    return pic

# 视频检测方法

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
    if img1 is not NONE and img2 is not NONE:
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
        tmp = res_path + '/background.jpg'
        cv2.imwrite(tmp, img2)
        return img2
    else:
        text_insert_changeline(text_info_videodetection, "背景合成失败：截取图片打开失败")

def person_count(background:np.ndarray, img1_path:str):
    '''1-输入待识别图像与背景图像识别以识别人数
       2-将
    Args:
        background (ndarray): 背景图像
        img1_path (ndarray): 待识别图像

    Returns:
        int: 识别人数
        ndarray: 识别结果图像
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
    return counts, img1

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

# fds文件功能

def get_headchid(fds_lines: list):
    '''找出fds文件的headchid

    Args:
        fds_lines (list): fds文件行内容

    Returns:
        str: 指定fds文件的headchid
    '''
    for i in fds_lines:
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
    list_str_fdspath_part = fds_path.split('/', 15) # 将路径分割
    p.write('@echo off \n')
    p.write(list_str_fdspath_part[0] + '\n')
    p.write('cd' + ' ')
    for i in range(len(list_str_fdspath_part) - 2):
        p.write('/' + list_str_fdspath_part[i + 1])
    p.write('/' + '\n')
    return 1

def create_run_bat(fds_path:str, mode:str, string_fdshead:str):
    '''为fds与smokeview创建.bat运行文件

    Args:
        fds_path (str): 需要创建运行文件的fds路径
        mode (str): 1-fds,2-smokeview  '
        string_fdshead (str) : 当前fds文件的headchid
    Returns:
        str: 返回生成的.bat文件路径
    '''
    # 生成.bat文件路径
    string_bat_path = fds_path.replace('.fds', '-fds.bat' if mode == 1 else '-smv.bat')
    with open(string_bat_path, 'w', encoding='UTF-8') as p:
        bat_write(p, fds_path)
        if mode == 1:
            p.write('fds ' + string_fdshead + '.fds\n')
        else:
            p.write(string_fdshead.split('.', 1)[0] + '.smv \n')
        p.write('cd/ ')
    p.close()
    return string_bat_path

def create_folders(list_fds_path:list):
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
    fds_path = list_fds_path[0] # A:/tkinter/code/fds/case0_all.fds 形如这样的fds文件路径
    now = int(round(time.time()*1000))
    time_stamp = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(now/1000)) # 获得时间戳
    string_folder_path = fds_path.replace(fds_path.split('/',10)[-1], time_stamp) # A:\tkinter\code\fds\2021-09-16-21-02-48 和fds_path处于同一路径下的根据时间戳创建的结果文件夹
    string_evacres_plot_folderpath = string_folder_path + '/evac_res_plot'
    os.mkdir(string_folder_path) 
    os.mkdir(string_evacres_plot_folderpath)
    tmp_str_path = string_folder_path + '/' # A:\tkinter\code\fds\2021-09-16-21-02-48/在结果文文件夹中创建新的文件夹
    list_string_path = []
    for i in range(len(list_fds_path)):
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
    list_string_fdsbat_list = [] # .bat文件路径list
    with open(fds_path, 'r', encoding='UTF-8') as p :
        fds_lines = p.readlines()
    p.close()
    string_headchid = get_headchid(fds_lines) # 找出headchid
    for i in range(len(per_nums_list)):
        string_newfds_folderpath = case_folder_path + '/NUM-' + str(i) # 当前fds源文件下(策略下)个人数条件下的fds文件夹
        os.mkdir(string_newfds_folderpath)
        string_new_fds_path = string_newfds_folderpath + '/' + string_headchid + '.fds'
        fds_duplicate(string_new_fds_path, fds_lines, change_line(per_nums_list[i]))
        list_string_fdsbat_list.append(create_run_bat(string_new_fds_path, 1, string_headchid))
    return list_string_fdsbat_list
    '''list_string_fdsbat_path = []  # .bat文件路径list
    new_fds_folder_path_list = []
    fds_io = open(fds_path, 'r')  # fds源文件的io，用于复制
    fds_lines = fds_io.readlines()  # 读取fds源文件中的lines
    for i in range(len(per_nums_list)):  # 根据人数数据建立循环
        new_fds_folder_path = case_folder_path + '/' + 'NUM-' + str(i)  # 当前策略下、当前人数下，新写成fds文件及其运行生成文件的存储目录
        new_fds_folder_path_list.append(new_fds_folder_path)
        os.makedirs(new_fds_folder_path)  # 创造此文件夹
        new_fds_path = new_fds_folder_path + '/' + 'case-' + str(i) + '.fds'  # 当前策略、人数下生成的新的fds文件的路径，用于添加到lust中
        fds_duplicate(new_fds_path, fds_lines, change_line(per_nums_list[i]))  # 根据此新路径复制fds文件
        list_string_fdsbat_path.append(create_run_bat(new_fds_path, 1))
    return list_string_fdsbat_path'''

def fds_bats_run(fds_run_paths: list):
    """
    运行fds以及smokeview的bat文件
    :param fds_run_paths: fds的运行文件路径list
    :return: 0
    """

    for i in fds_run_paths:
        text_insert_changeline(text_info_videodetection, i + '正在运行..')
        p = subprocess.Popen(
            "cmd.exe /c" + i,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        cur_line = p.stdout.readline()
        while cur_line != b'':
            cur_line = p.stdout.readline()
        text_insert_changeline(text_info_videodetection, i + '运行完成')
    return 0

if __name__ == "__main__" :
    # 查看是否存在工作目录
    list_string_rc = []
    if os.path.exists(string_path_rc) :
        with open(string_path_rc, 'r') as f:
                list_string_rc = f.readlines()
        int_read_delay, int_detect_delay = list(map(lambda i: int(i.strip().split(':',1)[-1]), list_string_rc))
    else:
        if os.path.exists(string_workcwd_dir):
            with open(string_path_rc, 'w') as f:
                f.writelines("int_read_delay:10\n")
                f.writelines("int_detect_delay:30\n")
        else:
            os.mkdir(string_workcwd_dir)
            with open(string_path_rc, 'w') as f:
                f.writelines("int_read_delay:10\n")
                f.writelines("int_detect_delay:30\n")
    # 当此文件不存在也不需要在程序初始化时创建，因为后续函数会再次确认此文件是否存在，当不存在时，彼时再行创建
    bool_fdshis_exist,  list_string_filepath= gethis_list_bool(1)
    bool_videohis_exist,  list_string_videopath_his= gethis_list_bool(2)

    # 窗口初始化
    win_main = tk.Tk()
    win_main.title('CJ_V1.0')
    win_main.geometry('800x510')
    win_main['bg'] = 'white' 
    win_main.resizable(False, False)

    # 测试按钮图标
    tkimage_test = image2tk('A:/tkinter/code/icon2/list.png', (36, 36))
    btn_test = tk.Button(win_main, image=tkimage_test, cursor='hand2', command=test_func)
    # btn_test.place(x=600, y=450)
    btn_test2 = tk.Button(win_main, image=tkimage_test, cursor='hand2', command=test_func2)
    btn_test2.place(x=650, y=450)

    # 创建初始设置按钮
    text_frame_init = tk.Button(win_main)

    # 载入历史记录按钮
    btn_fds_his = tk.Button(win_main, image=tkimage_test, cursor='hand2', command=btn_fds_his_f,
                    state=(NORMAL if bool_fdshis_exist else DISABLED))
    btn_fds_his.place(x=354, y=140)
    btn_video_his = tk.Button(win_main, image=tkimage_test, cursor='hand2', command=btn_video_his_f,
                    state=DISABLED)
    btn_video_his.place(x=418, y=282)

    # 播放按钮图标
    # tkimage_play = image2tk('A:/tkinter/code/icon2/run.png', (178, 178)) # 加载播放图标
    tkimage_play = image2tk('A:/tkinter/code/icon2/run.png', (178, 178)) # 加载播放图标
    tkimage_play_f = image2tk('A:/tkinter/code/icon2/run_f.png', (178, 178)) # 加载播放图标
    btn_play = tk.Button(win_main,image=tkimage_play_f, cursor='hand2', command=btn_play_f) # 创建播放按钮
    btn_play.configure(state=DISABLED) # 设置播放按钮初始状态为未激活 不可点击
    btn_play.place(x=460, y=140) # 绑定窗口

    # 引入FDS模型按钮图标
    # 初始图标：未选择FDS文件时的图标
    tkimage_open = image2tk('A:/tkinter/code/icon2/add.png', (178, 178))
    # 选择FDS文件后的图标
    tkimage_opened = image2tk('A:/tkinter/code/icon2/check.png', (178, 178))
    btn_open = tk.Button(win_main,image=tkimage_open, cursor='hand2', command=import_fdsfiles) 
    btn_open.place(x=170, y=140) # 居中

    # 文件功能按钮
    # 编辑
    tkimage_edit = image2tk('A:/tkinter/code/icon2/edit.png', (32, 32))
    btn_file_edit = tk.Button(win_main, image=tkimage_edit, cursor='hand2', command=btn_file_edit_f)
    # 删除
    tkimage_delete = image2tk('A:/tkinter/code/icon2/delete.png', (32, 32))
    btn_file_delete = tk.Button(win_main, image=tkimage_delete, cursor='hand2', command=btn_file_delete_f)
    # 保存
    tkimage_save = image2tk('A:/tkinter/code/icon2/save.png', (32, 32))
    btn_file_save = tk.Button(win_main, image=tkimage_save, cursor='hand2', command=btn_file_save_f)

    # 视频功能按钮
    # 保存此视频地址，沿用保存fds文件路径地址的图标
    btn_video_save = tk.Button(win_main, image=tkimage_save, cursor='hand2', command=btn_video_save_f, state=DISABLED)
    # 打开视频检测结果文件夹按钮
    tkimage_openinfolder = image2tk('A:/tkinter/code/icon2/folder.png', (30, 32))
    btn_videodetection_results = tk.Button(win_main, image=tkimage_openinfolder, cursor='hand2', command=btn_videodetection_results_f, state=DISABLED)

    # 窗口复原按钮图标
    tkimage_win_init = image2tk('A:/tkinter/code/icon2/previsous.png', (32,32))
    btn_win_init = tk.Button(win_main, image=tkimage_win_init, cursor='hand2', command=btn_win_init_f, state=DISABLED)

    # 创建comb，此comb在选择按钮被点击并存在选择项是才被加载窗口中
    tkstringvar_filepath = tkinter.StringVar() # 创建StringVar储存文件名
    comb_filenames = ttk.Combobox(win_main, textvariable=tkstringvar_filepath, height=50, width=23) # 创建comb本体
    comb_filenames.bind("<<ComboboxSelected>>", comb_getcur) # 将comb与响应事件绑定
    string_comb_curitem = comb_filenames.get()

    # 创建textbox，此box在选择视频后并视频读取成功后，随着主页面其余图标运动时被加载，用以展示当前视频检测进度
    text_info_videodetection = scrolledtext.ScrolledText(win_main, width=26, height=16, relief=RIDGE, bg='#F5F5F5')
    # text_info_videodetection = tk.Text(win_main, width=26, height=16, relief=RIDGE, bg='#F5F5F5')
    text_info_videodetection.bind("<Key>", lambda a: "break")

    # 创建视频label
    label_video = tk.Label(win_main, bd=0, bg='#333333')

    # 小图展示label
    label_show_back = tk.Label(win_main, bd=0)
    label_show_res = tk.Label(win_main, bd=0, bg='#333333')

    # 创建treeview
    tree_info = ttk.Treeview(win_main, show='headings', height=1)
    tree_info["columns"] = ("帧数", "延迟", "间隔", "当前")     # #定义列
    tree_info.column("帧数", width=60, anchor=CENTER)          # #设置列
    tree_info.column("延迟", width=60, anchor=CENTER) 
    tree_info.column("间隔", width=60, anchor=CENTER) 
    tree_info.column("当前", width=60, anchor=CENTER) 
    tree_info.heading("帧数", text="视频帧数")     # #设置显示的表头名
    tree_info.heading("延迟", text="起始延迟")
    tree_info.heading("间隔", text="识别间隔")
    tree_info.heading("当前", text="当前帧数")
    tree_info_path = ttk.Treeview(win_main, show='headings', height=1)
    tree_info_path["columns"] = ("视频地址")     # #定义列
    tree_info_path.column("视频地址", width=240, anchor=CENTER) 
    tree_info_path.heading("视频地址", text="视频地址")     # #设置显示的表头名

    win_main.mainloop()




