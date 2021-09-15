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

import tkinter
from tkinter import ttk
 
 
win = tkinter.Tk()
win.title("Kahn Software v1")    # #窗口标题
win.geometry("600x500+200+20")   # #窗口位置500后面是字母x
'''
表格
'''
tree = ttk.Treeview(win, show='headings', height=1)      # #创建表格对象
tree["columns"] = ("帧数", "延迟", "间隔", "当前")     # #定义列
tree.column("帧数", width=60, anchor=CENTER)          # #设置列
tree.column("延迟", width=60, anchor=CENTER) 
tree.column("间隔", width=60, anchor=CENTER) 
tree.column("当前", width=60, anchor=CENTER) 
tree.heading("帧数", text="视频帧数")     # #设置显示的表头名
tree.heading("延迟", text="起始延迟")
tree.heading("间隔", text="识别间隔")
tree.heading("当前", text="当前帧数")
tree.insert("", 0, text="line1", values=("1", "18", "180", "65"))    # #给第0行添加数据，索引值可重复
tree.insert("", 0, text="当前帧数", values=(1000))    # #给第0行添加数据，索引值可重复
tree.place(x=10, y=10)
win.mainloop()   # #窗口持久化