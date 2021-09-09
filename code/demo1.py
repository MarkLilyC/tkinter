'''
Author: your name
Date: 2021-09-07 11:43:55
LastEditTime: 2021-09-09 15:33:25
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
from cv2 import cv2




"""def playfunc():
    '''[隐藏播放图标] 当点击播放图标时， 隐藏播放图标与按钮
    '''
    # label实现视频容器
    image_cover = Image.open('A://tkinter//code/bg.png')
    image_playcover= ImageTk.PhotoImage(image=image_cover)
    label_video = tk.Label(win_main, width=600, height=400, bd=1, bg='white')
    label_video.place(x=0,y=0)
    string_filepath = filedialog.askopenfilename() # 打开窗口选择目标视频
    btn_play.place_forget() # 隐藏播放按钮
    video_tobeplayed = cv2.VideoCapture(string_filepath) # 打开目标视频
    int_waittime = int(1000/video_tobeplayed.get(5))
    int_movietime = int((video_tobeplayed.get(7)/video_tobeplayed.get(5))/60)
    bar_playscale = tk.Scale(win_main, from_=0, to=int_movietime, length=1000, orient=tk.HORIZONTAL, resolution=0.1, 
        showvalue=1, bd=0, cursor='hand2', tickinterval=int_movietime/20) 
    bar_playscale.place(x=0, y=540)
    while video_tobeplayed.isOpened(): # 当视频正常打开时
        ret, image_frame = video_tobeplayed.read() # 读取视频帧
        if ret == True: # 当成功读取时
            image_frame = cv2.cvtColor(image_frame, cv2.COLOR_BGR2RGBA) # 修改颜色空间 
            image_tobeplayed = Image.fromarray(image_frame).resize((540,360)) # 将cv2读取的图像转换为Image,并修改大小
            imageTk_tobeplayed = ImageTk.PhotoImage(image=image_tobeplayed) # 转换为imagetk
            label_video.configure(image=imageTk_tobeplayed) # 使用configure方法将label更新为最新待播放图像
            label_video.image = imageTk_tobeplayed # 更新
            label_video.update() # 更新
            cv2.waitKey(int_waittime)
        else:
            break
"""
        
        
def import_fdsfiles():
    '''[选择FDS文件]
        
    Returns
    -------
    [list]
        [选择的FDS文件路径列表]]
    '''
    global list_string_filepath # 将此列表声明为全局变量以便后续访问
    list_string_filepath = filedialog.askopenfilenames(filetypes=[('FDS files', ('.fds', '.FDS'))]) # 打开窗口选择fds文件
    int_files = len(list_string_filepath) # 所选文件个数
    if list_string_filepath: # 当选择文件后
        btn_open.config(image=tkimage_opened) # 将文件打开图标置为check图标
        # 创建comb
        tkstringvar_filepath = tkinter.StringVar() # 创建StringVar储存文件名
        comb_filenames = ttk.Combobox(win_main, textvariable=tkstringvar_filepath) # 创建comb本体
        comb_filenames.place(x=286, y=305, width=134) # 绑定到窗口
        comb_filenames['values'] = tuple(map(lambda x : x.split('/', 10)[-1], list_string_filepath)) # 设置comb值
        a = 0
        def xFunc(event): 
            a = (comb_filenames.index(comb_filenames.get())) 
            return a           
        comb_filenames.bind("<<ComboboxSelected>>", xFunc)
        # 创建文件功能按钮
        btn_file_edit = tk.Button(win_main,image=tkimage_edit, cursor='hand2', command=btn_file_edit_f(list_string_filepath[a])) 
        btn_file_edit.place(x=286, y=350)
        return list_string_filepath # 返回所选文件路径列表
    else:
        print("未选择任何文件")
        return None
    
def getaa():
    print(list_string_filepath)

def btn_file_edit_f(path):
    '''编辑所选中fds文件

    Parameters
    ----------
    path : string
        所选fds文件的路径
    '''
    print(path)

def image2tk(iamgepath, size):
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
    return ImageTk.PhotoImage(image=Image.open(iamgepath).resize(size))
# 窗口初始化
win_main = tk.Tk()
win_main.title('demo1')
win_main.geometry('800x500')
win_main['bg'] = 'white'

# 播放按钮图标
tkimage_play = image2tk('A://tkinter//code//icon2//run.png', (128, 128))
# 引入FDS模型按钮图标
# 初始图标：未选择FDS文件时的图标
tkimage_open = image2tk('A://tkinter//code//icon2//add.png', (128, 128))
# 选择FDS文件后的图标
tkimage_opened = image2tk('A://tkinter//code//icon2//check.png', (128, 128))

# 功能图标
# 编辑
tkimage_edit = image2tk('A://tkinter//code//icon2//edit.png', (32, 32))
# 删除
tkimage_delete = image2tk('A://tkinter//code//icon2//delete.png', (32, 32))
# 保存
tkimage_save = image2tk('A://tkinter//code//icon2//save.png', (32, 32))
# 新建btn，添加到主窗口， 添加图标 ，添加鼠标动作, 绑定事件
btn_open = tk.Button(win_main,image=tkimage_open, cursor='hand2', command=import_fdsfiles) 
btn_play = tk.Button(win_main,image=tkimage_play, cursor='hand2', command=getaa) 
btn_open.place(x=286, y=170) # 居中
btn_play.place(x=450, y=170) # 居中
print(btn_open.__class__)


win_main.mainloop()
