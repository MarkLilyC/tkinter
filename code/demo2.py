'''
Author: your name
Date: 2021-09-07 11:43:55
LastEditTime: 2021-09-14 16:50:41
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \tkinter\code\demo1.py
'''
from genericpath import exists
from test import get_time_stamp
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
import fds_write
import numpy
import fds_run
import sub_find_Back

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
string_workcwd_dir = os.getcwd() + '\\work'
string_path_fdshis_arti = os.getcwd() + '\\work\\fdshis.txt' # 获取并创建历史工作文件夹路径
string_path_fdshis_auto = os.getcwd() + '\\work\\fdshis_all.txt' # 获取并创建历史工作文件夹路径
string_path_videohis_arti = os.getcwd() + '\\work\\videohis.txt'
string_path_videohis_auto = os.getcwd() + '\\work\\videohis_all.txt'
string_path_backgroud = '' # 存储背景图像地址
list_string_path_frame = [] # 存储截取的原始图像地址
list_string_path_frame_dst = [] # 存储生成检测结果图像地址


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
    time_stamp = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now/1000))
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
    video_tobeplayed = cv2.VideoCapture(path)
    int_frame_count = int(video_tobeplayed.get(cv2.CAP_PROP_FRAME_COUNT)) # 帧数
    bool_isopened, ndarray_image_1stframe = video_tobeplayed.read() # 获取视频第一帧
    if bool_isopened:
        # 页面改动
        btn_open.place(x=5, y=0)
        btn_file_edit.place(x=5, y=210)
        btn_file_delete.place(x=78, y=210)
        btn_file_save.place(x=151, y=210)
        comb_filenames.place(x=5, y=185)
        text_info_videodetection.place(x=5, y=250)
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
        # ndarray_image_1stframe = cv2.resize(ndarray_image_1stframe, tuple_float_picsize_resize,interpolation=cv2.INTER_NEAREST) # 采用最近邻插值法缩放图片
        image_1st = Image.fromarray(ndarray_image_1stframe).resize(tuple_float_picsize_resize[:2]) 
        tkimage_1stframe = ImageTk.PhotoImage(image=image_1st)
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
        text_insert_changeline(text_info_videodetection, 'Video readed successfully')
        # 添加关于视频检测信息展示的按钮
        btn_video_save.place(x = label_video_x, y = 410)
        btn_videodetection_results.place(x = label_video_x, y = 460)
        
    else:
        print("failed to read video")

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
    string_video_path = list_string_videopath_his[-1]
    string_videodec_results_path = string_video_path.replace(string_video_path.split('.')[-1], '_results')
    # os.mkdir(string_videodec_results_path)
    videoplay_init(string_video_path)

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
    string_video_path = filedialog.askopenfilename() # 打开窗口选择视频，暂时不限制文件类型
    if string_video_path: # 当选中视频后
        videoplay_init(string_video_path)
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
    text_info_videodetection.delete(1.0, 'end')

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
    text_info_videodetection.delete(1.0, 'end')

# 查看是否存在工作目录
# 当此文件不存在也不需要在程序初始化时创建，因为后续函数会再次确认此文件是否存在，当不存在时，彼时再行创建
bool_fdshis_exist,  list_string_filepath= gethis_list_bool(1)
bool_videohis_exist,  list_string_videopath_his= gethis_list_bool(2)


# 窗口初始化
win_main = tk.Tk()
win_main.title('demo1')
win_main.geometry('800x510')
win_main['bg'] = 'white' 
win_main.resizable(False, False)

# 测试按钮图标
tkimage_test = image2tk('A://tkinter//code//icon2//list.png', (36, 36))
btn_test = tk.Button(win_main, image=tkimage_test, cursor='hand2', command=test_func)
btn_test.place(x=600, y=450)
btn_test2 = tk.Button(win_main, image=tkimage_test, cursor='hand2', command=test_func2)
btn_test2.place(x=650, y=450)

# 载入历史记录按钮
btn_fds_his = tk.Button(win_main, image=tkimage_test, cursor='hand2', command=btn_fds_his_f,
                state=(NORMAL if bool_fdshis_exist else DISABLED))
btn_fds_his.place(x=354, y=140)
btn_video_his = tk.Button(win_main, image=tkimage_test, cursor='hand2', command=btn_video_his_f,
                state=DISABLED)
btn_video_his.place(x=418, y=282)

# 播放按钮图标
tkimage_play = image2tk('A://tkinter//code//icon2//run.png', (178, 178)) # 加载播放图标
tkimage_play_f = image2tk('A://tkinter//code//icon2//run_f.png', (178, 178)) # 加载播放图标
btn_play = tk.Button(win_main,image=tkimage_play_f, cursor='hand2', command=btn_play_f) # 创建播放按钮
btn_play.configure(state=DISABLED) # 设置播放按钮初始状态为未激活 不可点击
btn_play.place(x=460, y=140) # 绑定窗口

# 引入FDS模型按钮图标
# 初始图标：未选择FDS文件时的图标
tkimage_open = image2tk('A://tkinter//code//icon2//add.png', (178, 178))
# 选择FDS文件后的图标
tkimage_opened = image2tk('A://tkinter//code//icon2//check.png', (178, 178))
btn_open = tk.Button(win_main,image=tkimage_open, cursor='hand2', command=import_fdsfiles) 
btn_open.place(x=170, y=140) # 居中

# 文件功能按钮
# 编辑
tkimage_edit = image2tk('A://tkinter//code//icon2//edit.png', (32, 32))
btn_file_edit = tk.Button(win_main, image=tkimage_edit, cursor='hand2', command=btn_file_edit_f)
# 删除
tkimage_delete = image2tk('A://tkinter//code//icon2//delete.png', (32, 32))
btn_file_delete = tk.Button(win_main, image=tkimage_delete, cursor='hand2', command=btn_file_delete_f)
# 保存
tkimage_save = image2tk('A://tkinter//code//icon2//save.png', (32, 32))
btn_file_save = tk.Button(win_main, image=tkimage_save, cursor='hand2', command=btn_file_save_f)

# 视频功能按钮
# 保存此视频地址，沿用保存fds文件路径地址的图标
btn_video_save = tk.Button(win_main, image=tkimage_save, cursor='hand2', command=btn_video_save_f)
# 打开视频检测结果文件夹按钮
tkimage_openinfolder = image2tk('A://tkinter/code//icon2//folder.png', (30, 32))
btn_videodetection_results = tk.Button(win_main, image=tkimage_openinfolder, cursor='hand2', command=test_func2)

# 窗口复原按钮图标
tkimage_win_init = image2tk('A://tkinter//code//icon2//previsous.png', (32,32))
btn_win_init = tk.Button(win_main, image=tkimage_win_init, cursor='hand2', command=test_func)

# 创建comb，此comb在选择按钮被点击并存在选择项是才被加载窗口中
tkstringvar_filepath = tkinter.StringVar() # 创建StringVar储存文件名
comb_filenames = ttk.Combobox(win_main, textvariable=tkstringvar_filepath, height=50, width=23) # 创建comb本体
comb_filenames.bind("<<ComboboxSelected>>", comb_getcur) # 将comb与响应事件绑定
string_comb_curitem = comb_filenames.get()

# 创建textbox，此box在选择视频后并视频读取成功后，随着主页面其余图标运动时被加载，用以展示当前视频检测进度
text_info_videodetection = tk.Text(win_main, width=26, height=16, relief=RIDGE, bg='#F5F5F5')
text_info_videodetection.bind("<Key>", lambda a: "break")

# 创建视频label
label_video = tk.Label(win_main, bd=0, bg='#333333')


win_main.mainloop()




