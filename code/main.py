import ana_excel
import os

csv_time_person_by_num = [['C:\\Users\\edison\\Desktop\\test\\05-09-16-36\\STR-0\\NUM-0\\base_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-09-16-36\\STR-1\\NUM-0\\base-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-09-16-36\\STR-2\\NUM-0\\case1-a_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-09-16-36\\STR-3\\NUM-0\\case1-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-09-16-36\\STR-4\\NUM-0\\case1-r_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-09-16-36\\STR-5\\NUM-0\\case1-a_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-09-16-36\\STR-6\\NUM-0\\case2-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-09-16-36\\STR-7\\NUM-0\\case2-r_evac.csv'],
                          ['C:\\Users\\edison\\Desktop\\test\\05-09-16-36\\STR-0\\NUM-1\\base_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-09-16-36\\STR-1\\NUM-1\\base-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-09-16-36\\STR-2\\NUM-1\\case1-a_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-09-16-36\\STR-3\\NUM-1\\case1-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-09-16-36\\STR-4\\NUM-1\\case1-r_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-09-16-36\\STR-5\\NUM-1\\case1-a_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-09-16-36\\STR-6\\NUM-1\\case2-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-09-16-36\\STR-7\\NUM-1\\case2-r_evac.csv'],
                          ['C:\\Users\\edison\\Desktop\\test\\05-09-16-36\\STR-0\\NUM-2\\base_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-09-16-36\\STR-1\\NUM-2\\base-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-09-16-36\\STR-2\\NUM-2\\case1-a_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-09-16-36\\STR-3\\NUM-2\\case1-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-09-16-36\\STR-4\\NUM-2\\case1-r_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-09-16-36\\STR-5\\NUM-2\\case1-a_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-09-16-36\\STR-6\\NUM-2\\case2-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-09-16-36\\STR-7\\NUM-2\\case2-r_evac.csv'],
                          ['C:\\Users\\edison\\Desktop\\test\\05-09-16-36\\STR-0\\NUM-3\\base_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-09-16-36\\STR-1\\NUM-3\\base-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-09-16-36\\STR-2\\NUM-3\\case1-a_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-09-16-36\\STR-3\\NUM-3\\case1-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-09-16-36\\STR-4\\NUM-3\\case1-r_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-5\\NUM-3\\case1-a_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-6\\NUM-3\\case2-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-7\\NUM-3\\case2-r_evac.csv'],
                          ['C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-0\\NUM-4\\base_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-1\\NUM-4\\base-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-2\\NUM-4\\case1-a_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-3\\NUM-4\\case1-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-4\\NUM-4\\case1-r_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-5\\NUM-4\\case1-a_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-6\\NUM-4\\case2-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-7\\NUM-4\\case2-r_evac.csv'],
                          ['C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-0\\NUM-5\\base_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-1\\NUM-5\\base-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-2\\NUM-5\\case1-a_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-3\\NUM-5\\case1-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-4\\NUM-5\\case1-r_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-5\\NUM-5\\case1-a_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-6\\NUM-5\\case2-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-7\\NUM-5\\case2-r_evac.csv'],
                          ['C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-0\\NUM-6\\base_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-1\\NUM-6\\base-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-2\\NUM-6\\case1-a_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-3\\NUM-6\\case1-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-4\\NUM-6\\case1-r_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-5\\NUM-6\\case1-a_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-6\\NUM-6\\case2-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-7\\NUM-6\\case2-r_evac.csv'],
                          ['C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-0\\NUM-7\\base_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-1\\NUM-7\\base-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-2\\NUM-7\\case1-a_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-3\\NUM-7\\case1-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-4\\NUM-7\\case1-r_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-5\\NUM-7\\case1-a_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-6\\NUM-7\\case2-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-7\\NUM-7\\case2-r_evac.csv'],
                          ['C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-0\\NUM-8\\base_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-1\\NUM-8\\base-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-2\\NUM-8\\case1-a_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-3\\NUM-8\\case1-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-4\\NUM-8\\case1-r_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-5\\NUM-8\\case1-a_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-6\\NUM-8\\case2-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-7\\NUM-8\\case2-r_evac.csv'],
                          ['C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-0\\NUM-9\\base_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-1\\NUM-9\\base-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-2\\NUM-9\\case1-a_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-3\\NUM-9\\case1-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-4\\NUM-9\\case1-r_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-5\\NUM-9\\case1-a_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-6\\NUM-9\\case2-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-7\\NUM-9\\case2-r_evac.csv'],
                          ['C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-0\\NUM-10\\base_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-1\\NUM-10\\base-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-2\\NUM-10\\case1-a_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-3\\NUM-10\\case1-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-4\\NUM-10\\case1-r_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-5\\NUM-10\\case1-a_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-6\\NUM-10\\case2-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-7\\NUM-10\\case2-r_evac.csv'],
                          ['C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-0\\NUM-11\\base_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-1\\NUM-11\\base-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-2\\NUM-11\\case1-a_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-3\\NUM-11\\case1-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-4\\NUM-11\\case1-r_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-5\\NUM-11\\case1-a_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-6\\NUM-11\\case2-l_evac.csv',
                           'C:\\Users\\edison\\Desktop\\test\\05-08-23-40\\STR-7\\NUM-11\\case2-r_evac.csv']]
tmp = '05-09-16-36'
time_person_by_num = []
for i in csv_time_person_by_num:  # i即为每个人数各策略下cvs文件的数组
    tmplist = []  # 用于保存当前人数下各策略下的时间
    for j in i:  # j为内部数组下的各csv文件路径
        j.replace('05-08-23-40', tmp)
        time = ana_excel.gettimebyperson(j)  # 获取时间
        tmplist.append(time)
    time_person_by_num.append(tmplist)

res_path = csv_time_person_by_num[0][0]
for i in range(3):
    res_path = os.path.dirname(res_path)
res_path += '\\evac'  # 用于存放提取出的人数下的疏散时间文件（txt）与绘制图像
res_path_txt = res_path + '\\Num_time'
res_path_pic = res_path + '\\Pics'
os.makedirs(res_path)
os.makedirs(res_path_txt)
os.makedirs(res_path_pic)

for i in range(len(time_person_by_num)):
    pathtmp = res_path_txt + '\\' + str(i) + '.txt'
    file_handle = open(pathtmp, mode='w')
    for j in time_person_by_num[i]:
        file_handle.write(j + ',')
    file_handle.write('\n')
per_nums_list = [5, 3, 1, 2, 3, 2, 2, 1, 3, 3, 1, 1]
for i in time_person_by_num:
    if len(i) == 8:
        i.append('0')
    for j in i:
        if j == 's':
            i[i.index(j)] = '0'
print(time_person_by_num)
ana_excel.numtimepic(time_person_by_num, per_nums_list, res_path_pic)


