'''
Author: your name
Date: 2021-09-07 11:43:55
LastEditTime: 2021-09-12 17:19:28
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \tkinter\code\demo1.py
'''
from genericpath import exists
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
import tkinter
from PIL import Image, ImageTk
import win32api
import os
import cv2
import numpy
# 声明一些变量
list_string_filepath = [] # 存储选中的FDS路径
list_string_filename = [] # 存储选中的FDS名
string_comb_curitem = '' # 存储comb当前选中的文件名
string_video_path = '' # 存储当前选中的视频地址
list_string_videopath_his = [] # 存储从历史记录中读取的videos历史记录
bool_fdshis_exist = NO # 是否存在fds的历史使用记录
bool_videohis_exist = NO # 是否存在video的历史使用记录
bool_fdsimported = NO # 是否存在手动选择的fds文件

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
    
def test_func():
    string_video_path = filedialog.askopenfilename() # 打开窗口选择视频，暂时不限制文件类型
    if string_video_path: # 当选中视频后
        # 读取视频
        video_tobeplayed = cv2.VideoCapture(string_video_path)
        int_frame_count = int(video_tobeplayed.get(cv2.CAP_PROP_FRAME_COUNT)) # 帧数
        bool_isopened, ndarray_image_1stframe = video_tobeplayed.read() # 获取视频第一帧
        if bool_isopened:
            # 页面改动
            btn_open.place(x=5, y=0)
            text_info_videodetection.place(x=5, y=280)
            text_insert_changeline(text_info_videodetection, 'Video readed successfully')
            btns_change_f(list_btns=[btn_open], mode=1)
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
            label_video = tk.Label(win_main, width=tuple_float_picsize_resize[0], height=tuple_float_picsize_resize[1], bd=0, bg='#333333')
            # 当原图缩放依据为height（即缩放后高满尺寸），此时宽度未达到600，应将图片在图片展示区域设置；当缩放依据为width时 同理
            label_video.place(x = (194 if tuple_float_picsize_resize[2] == 0 else (494 - tuple_float_picsize_resize[0]/2)),
                              y = (0 if tuple_float_picsize_resize[2] == 1 else (200- tuple_float_picsize_resize[1]/2)))
            # 贴图
            label_video.configure(image=tkimage_1stframe)
            label_video.image = tkimage_1stframe 
            label_video.update() 
        else :
            print('视频加载失败')
    else: # 当未选中视频
        string_video_path = '' # 将此变量置空

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
    btn_play.config(image=tkimage_play, state=NORMAL) # 更改播放按钮图标与状态
    btn_video_his.config(state=(NORMAL if bool_videohis_exist else DISABLED))
    comb_filenames.place(x=170, y=325) # 将comb绑定到窗口
    # comb设置
    list_string_filename = list(map(lambda x : x.split('/', 10)[-1], list_string_filepath))
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
        comb_filenames.place(x=5, y=185)
        btn_file_edit.place(x=5, y=210)
        btn_file_delete.place(x=78, y=210)
        btn_file_save.place(x=151, y=210)
        btns_change_f([btn_play, btn_fds_his, btn_video_his],3)
        text_info_videodetection.place(x=5, y=280)
        text_insert_changeline(text_info_videodetection, 'Video readed successfully')
        btns_change_f(list_btns=[btn_open, btn_file_edit, btn_file_delete, btn_file_save], mode=1)
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
        label_video = tk.Label(win_main, width=tuple_float_picsize_resize[0], height=tuple_float_picsize_resize[1], bd=0, bg='#333333')
        # 当原图缩放依据为height（即缩放后高满尺寸），此时宽度未达到600，应将图片在图片展示区域设置；当缩放依据为width时 同理
        label_video_x, label_video_y = ((194 if tuple_float_picsize_resize[2] == 0 else (494 - tuple_float_picsize_resize[0]/2)),
                                        (0 if tuple_float_picsize_resize[2] == 1 else (200- tuple_float_picsize_resize[1]/2)))
        label_video.place(x=label_video_x, y=label_video_y)
        # 贴图
        label_video.configure(image=tkimage_1stframe)
        label_video.image = tkimage_1stframe 
        label_video.update() 
        # 添加关于视频检测信息展示的按钮
        btn_video_save.place(x = label_video_x, y = 410)
    else:
        print("failed to read video")

def btn_fds_his_f():
    global list_string_filepath
    global list_string_filename
    with open(string_workcwd_file, 'r', encoding='utf-8') as f:
        list_string_filepath = f.readlines() # 修改fds路径列表
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
    videoplay_init(list_string_videopath_his[-1])

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
    if os.path.exists(string_workcwd_dir): # 当此路径存在 
        with open(string_workcwd_file, 'w') as f:
            for i in list_string_filepath:
                f.writelines(i + '\n')
    else: # 当此路径不存在则创建对应文件夹与文件
        os.mkdir(string_workcwd_dir)
        with open(string_workcwd_file, 'w') as f:
            for i in list_string_filepath:
                f.writelines(i + '\n')
    btn_fds_his.config(state=NORMAL)

def btn_play_f():
    global string_video_path
    string_video_path = filedialog.askopenfilename() # 打开窗口选择视频，暂时不限制文件类型
    if string_video_path: # 当选中视频后
        videoplay_init(string_video_path)
        '''
        # 读取视频
        video_tobeplayed = cv2.VideoCapture(string_video_path)
        int_frame_count = int(video_tobeplayed.get(cv2.CAP_PROP_FRAME_COUNT)) # 帧数
        bool_isopened, ndarray_image_1stframe = video_tobeplayed.read() # 获取视频第一帧
        if bool_isopened:
            # 页面改动
            btn_open.place(x=5, y=0)
            comb_filenames.place(x=5, y=185)
            btn_file_edit.place(x=5, y=210)
            btn_file_delete.place(x=78, y=210)
            btn_file_save.place(x=151, y=210)
            btns_change_f([btn_play, btn_fds_his, btn_video_his],3)
            text_info_videodetection.place(x=5, y=280)
            text_insert_changeline(text_info_videodetection, 'Video readed successfully')
            btns_change_f(list_btns=[btn_open, btn_file_edit, btn_file_delete, btn_file_save], mode=1)
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
            label_video = tk.Label(win_main, width=tuple_float_picsize_resize[0], height=tuple_float_picsize_resize[1], bd=0, bg='#333333')
            # 当原图缩放依据为height（即缩放后高满尺寸），此时宽度未达到600，应将图片在图片展示区域设置；当缩放依据为width时 同理
            label_video_x, label_video_y = ((194 if tuple_float_picsize_resize[2] == 0 else (494 - tuple_float_picsize_resize[0]/2)),
                                            (0 if tuple_float_picsize_resize[2] == 1 else (200- tuple_float_picsize_resize[1]/2)))
            label_video.place(x=label_video_x, y=label_video_y)
            # 贴图
            label_video.configure(image=tkimage_1stframe)
            label_video.image = tkimage_1stframe 
            label_video.update() 
            # 添加关于视频检测信息展示的按钮
            btn_video_save.place(x = label_video_x, y = 410)
        else :
            print('视频加载失败')
        '''
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
    if os.path.exists(string_workcwd_video) : # 当该his文件存在时
        with open(string_workcwd_video, 'a') as f: 
            f.writelines(string_video_path + '\n') # 直接写入
    else: # 当该文件不存在时
        if os.path.exists(string_workcwd_dir) : # 若work文件夹存在 
            with open(string_workcwd_video, 'w') as f: # 则直接创建该文件 并写入
                f.writelines(string_video_path + '\n')
        else :
            os.mkdir(string_workcwd_dir)
            with open(string_workcwd_video, 'w') as f: 
                f.writelines(string_video_path + '\n')

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

# 查看是否存在工作目录
string_workcwd_dir = os.getcwd() + '\\work'
print(string_workcwd_dir)
string_workcwd_file = os.getcwd() + '\\work\\fdshis.txt' # 获取并创建历史工作文件夹路径
string_workcwd_video = os.getcwd() + '\\work\\videohis.txt'
# 当此文件不存在也不需要在程序初始化时创建，因为后续函数会再次确认此文件是否存在，当不存在时，彼时再行创建
if os.path.exists(string_workcwd_file) :
    with open(string_workcwd_file, 'r') as f:
        list_string_filepath = f.readlines()
if os.path.exists(string_workcwd_video) :
    with open(string_workcwd_video, 'r') as f:
        list_string_videopath_his = f.readlines() 
bool_fdshis_exist = (YES if len(list_string_filepath) > 0 else NO)
bool_videohis_exist = (YES if len(list_string_videopath_his) else NO)

# 窗口初始化
win_main = tk.Tk()
win_main.title('demo1')
win_main.geometry('800x500')
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
btn_video_save = tk.Button(win_main, image=tkimage_save, cursor='hand2', command=test_func2)
# 打开视频检测结果文件夹按钮
tkimage_openinfolder = image2tk('A://tkinter/code//icon2//folder.png', (32, 32))
btn_video_results = tk.Button(win_main, image=tkimage_openinfolder, cursor='hand2', command=test_func2)

# 创建comb，此comb在选择按钮被点击并存在选择项是才被加载窗口中
tkstringvar_filepath = tkinter.StringVar() # 创建StringVar储存文件名
comb_filenames = ttk.Combobox(win_main, textvariable=tkstringvar_filepath, height=50, width=23) # 创建comb本体
comb_filenames.bind("<<ComboboxSelected>>", comb_getcur) # 将comb与响应事件绑定
string_comb_curitem = comb_filenames.get()

# 创建textbox，此box在选择视频后并视频读取成功后，随着主页面其余图标运动时被加载，用以展示当前视频检测进度
text_info_videodetection = tk.Text(win_main, width=26, height=16, relief=RIDGE, bg='#F5F5F5')
text_info_videodetection.bind("<Key>", lambda a: "break")




win_main.mainloop()




