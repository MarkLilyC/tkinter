'''
Author: your name
Date: 2021-09-07 11:43:55
LastEditTime: 2021-09-24 17:00:39
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \tkinter\code\demo1.py
'''
dict_pare_int = {
    'int_read_delay': 10,
    'int_detect_delay': 30,
    'int_binpic_fillter': 20,
    'int_personcount_threhold_1': 80,
    'int_personcount_threhold_2': 300,
    'int_dst_area_min': 400,
    'int_bg_threshold': 127,
    'int_src_index_1': 0,
    'int_src_index_2': 3
}
with open('./work/videtectrc.txt', 'r') as f :
    a = f.readlines()
    tmp_dict  = dict(list(map(lambda x: x.strip().split(':'), a)))
    keys = tmp_dict.keys()
keys2 = dict_pare_int.keys()
c = [x for x in keys2 if x in keys]
for i in c:
    dict_pare_int[i] = tmp_dict[i]
print(dict_pare_int)
