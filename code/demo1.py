'''
Author: your name
Date: 2021-09-07 11:43:55
LastEditTime: 2021-09-24 17:00:39
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \tkinter\code\demo1.py
'''
from sys import prefix
import yaml
import os

with open('./work/videtectrc.yml', 'r', encoding='utf-8') as f:
    lines = f.read()

print(lines, lines.__class__)
f_load = yaml.load(lines)
print(f_load, f_load.__class__)


