'''
Author: your name
Date: 2021-09-07 11:43:55
LastEditTime: 2021-09-09 17:32:03
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
    global tuple_string_filepath # 声明存储filepath的全局变量tuple
    global list_string_filename # 声明存储filepath的全局变量list
    tuple_string_filepath = filedialog.askopenfilenames(filetypes=[('FDS files', ('.fds', '.FDS'))]) # 打开窗口选择fds文件
    if tuple_string_filepath: # 当选择文件后
        btn_open.config(image=tkimage_opened) # 将文件打开图标置为check图标
        comb_filenames.place(x=170, y=325) # 将comb绑定到窗口
        list_string_filename = list(map(lambda x : x.split('/', 10)[-1], tuple_string_filepath))
        # tuple_string_filename= tuple(map(lambda x : x.split('/', 10)[-1], tuple_string_filepath)) 
        comb_filenames['values'] = tuple(list_string_filename) # 设置comb值
        comb_filenames.current(0) # 设置当前comb选中项为0（index）
        comb_filenames.update() # update
        global string_comb_curitem
        string_comb_curitem = comb_filenames.get()
        btn_file_edit.place(x=170, y=350) # 添加文件编辑按钮
        btn_file_delete.place(x=243 , y=350) # 添加文件删除按钮
        btn_file_save.place(x=316, y=350) # 添加fds文件组合保存按钮  
        btn_play.config(image=tkimage_play)
        return tuple_string_filepath # 返回所选文件路径列表
    else:
        print("未选择任何文件")
        return None
    
def test_func():
    cwd_ini = os.getcwd() + '\\work' # 获得当前工作目录，组成工作文件存储路径
    work_his = cwd_ini + '\\workhis.txt' # 创建历史fds路径存储文件
    if os.path.exists(cwd_ini): # 如果工作文件路径存在
        with open(work_his,'w', encoding='utf-8') as f: # 打开文件并以覆盖形式写入      
            for i in list_string_filename:
                f.writelines(i + '\n')
    else: # 若工作文件路径不存在
        os.mkdir(cwd_ini) # 创建工作文件存储文件啊及
        with open(work_his,'w', encoding='utf-8') as f: # 打开文件并以覆盖形式写入      
            for i in list_string_filename:
                f.writelines(i + '\n')

def init_file_btns(event): 
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
    
def btn_file_edit_f():
    '''打开记事本查看编辑选中的fds文件
    '''
    tmp_path = list_string_filename[list_string_filename.index(string_comb_curitem)]
    win32api.ShellExecute(0, 'open', 'notepad.exe', tmp_path,'',1)
       
def btn_file_delete_f():
    '''在namelist删除当前comb中选中的item，再将tuple（list）赋值给comb——value，最后update，实现对comb中items的删除
    '''
    list_string_filename.remove(string_comb_curitem) # 在namelist中删除当前item
    comb_filenames['values'] = tuple(list_string_filename) # 将更新后的list转换为tuple赋值给comb
    comb_filenames.current(0) # 设置当前comb选中项为0（index）
    comb_filenames.update() # update
    
def btn_file_save_f():
    '''存储当前选中fds文件路径
    '''
    if os.path.exists():
        print('exist')
    else:
        cwd_ini = os.getcwd() + '\\work' # 获得当前工作目录
        os.mkdir(cwd_ini)

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
win_main.resizable(False, False)
# 测试按钮图标
tkimage_test = image2tk('A://tkinter//code//icon2//list.png', (36, 36))
btn_test = tk.Button(win_main, image=tkimage_test, cursor='hand2', command=test_func)
btn_test.place(x=0, y=0)
# 播放按钮图标
tkimage_play = image2tk('A://tkinter//code//icon2//run.png', (178, 178)) # 加载播放图标
tkimage_play_f = image2tk('A://tkinter//code//icon2//run_f.png', (178, 178)) # 加载播放图标
btn_play = tk.Button(win_main,image=tkimage_play_f, cursor='hand2', command=test_func) # 创建播放按钮
btn_play.place(x=460, y=140) # 绑定窗口
# 引入FDS模型按钮图标
# 初始图标：未选择FDS文件时的图标
tkimage_open = image2tk('A://tkinter//code//icon2//add.png', (178, 178))
# 选择FDS文件后的图标
tkimage_opened = image2tk('A://tkinter//code//icon2//check.png', (178, 178))
btn_open = tk.Button(win_main,image=tkimage_open, cursor='hand2', command=import_fdsfiles) 
btn_open.place(x=170, y=140) # 居中
# 功能图标
# 编辑
tkimage_edit = image2tk('A://tkinter//code//icon2//edit.png', (32, 32))
btn_file_edit = tk.Button(win_main, image=tkimage_edit, cursor='hand2', command=btn_file_edit_f)
# 删除
tkimage_delete = image2tk('A://tkinter//code//icon2//delete.png', (32, 32))
btn_file_delete = tk.Button(win_main, image=tkimage_delete, cursor='hand2', command=btn_file_delete_f)
# 保存
tkimage_save = image2tk('A://tkinter//code//icon2//save.png', (32, 32))
btn_file_save = tk.Button(win_main, image=tkimage_save, cursor='hand2', command=btn_file_save_f)
# 创建comb，此comb在选择按钮被点击并存在选择项是才被加载窗口中
tkstringvar_filepath = tkinter.StringVar() # 创建StringVar储存文件名
comb_filenames = ttk.Combobox(win_main, textvariable=tkstringvar_filepath, height=50, width=23) # 创建comb本体
comb_filenames.bind("<<ComboboxSelected>>", init_file_btns) # 将comb与响应事件绑定
string_comb_curitem = comb_filenames.get()

win_main.mainloop()




