'''
Author: your name
Date: 2021-09-10 16:28:00
LastEditTime: 2021-09-14 13:41:58
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \code\test.py
'''
from cv2 import cv2
import time

def resizepicandlabel(imagesize: tuple, labelsize: tuple):
    '''resize pic and label based on their siezs

    Parameters
    ----------
    image : tuple
        pic_size (int int)
    labelsize : tuple
        label_size (int int)
    '''
    int_frame_width = imagesize[0]
    int_frame_height = imagesize[1]
    int_label_width = labelsize[0]
    int_label_height = labelsize[1]
    float_proportion_width = int_frame_width / int_label_width
    float_proportion_heigth = int_frame_height / int_label_height
    return ([int_frame_width / float_proportion_width, int_frame_height / float_proportion_width, 0] if float_proportion_width > float_proportion_heigth else [int_frame_width / float_proportion_heigth, int_frame_height / float_proportion_heigth, 1])

def get_time_stamp():
    now = int(round(time.time()*1000))
    time_stamp = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now/1000))
    print(time_stamp.__class__)
    stamp = ("".join(time_stamp.split()[0].split("-"))+"".join(time_stamp.split()[1].split(":"))).replace('.', '')
    print(stamp)

if __name__ == '__main__':
    get_time_stamp()