'''
Author: your name
Date: 2021-09-10 16:28:00
LastEditTime: 2021-09-11 17:25:53
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \code\test.py
'''
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
    if float_proportion_width == float_proportion_heigth: # 当二者尺寸比例相同
        return [int_frame_width / float_proportion_width, int_frame_height/ float_proportion_width] 
    elif float_proportion_width < 1 and float_proportion_heigth < 1: # 当pic全小于label，则对pic进行放大
        return [int_frame_width / float_proportion_heigth, int_label_height] if float_proportion_width < float_proportion_heigth else [int_frame_height / float_proportion_width, int_label_width]
    else: # 当pic单边小于pic时
        return [] if float_proportion_width < float_proportion_heigth else []


print(resizepicandlabel((300, 300), (600, 400)))
