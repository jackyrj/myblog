# -*- coding:utf-8 -*-
'''
* @Author: Jackyrj
* @Date: 2018-06-05 16:22:22
* @Last Modified by:   Jackyrj
* @Last Modified time: 2018-06-05 16:22:22
* @Desc:
'''
import csv_data as cd
import data_processing as dp

filename = 'test.csv'

if 'new' in filename:
    standardize = 0
else:
    standardize = 1

UTCtime = 3
has_list_heander = 1
del_col = 0

input_date_example = '2018.06.04 22:57:00'
interval_min = 20
delta_time_seconds = 60 * 1

new_list_title = ['Time (UTC)', 'Open', 'High', 'Low', 'Close', 'Volume']
missing_list_title = ['Start_Time', 'Stop_Time', 'interval', 'Missing_Count']

#从filename导入数据
data = cd.Csv_data()
data.load_data(filename, has_list_heander)

#原始数据
if standardize == 1:

    #使数据格式标准化
    data.standardize_data(del_col, input_date_example)

    #转换numpy数据为结构数组
    data.str_to_matrixstruct(new_list_title)

    #使时间变成UTC标准时间
    data.set_UTC(UTCtime)

    past_time, near_time = data.date_analyze(interval_min)

    #删除过去的时间
    data.delete_past_data(past_time)

    #删除近期时间的时间
    data.delete_near_data(near_time)

    #数据有效性分析
    missing = dp.data_missing_analyze(delta_time_seconds, missing_list_title, data.data_matrix)

    #数据有效性记录
    data.new_csv('missing', missing_list_title, missing)

    #新数据记录
    data.new_csv('new', new_list_title, data.data_matrix)

#整理后的数据
else:
    data.str_to_matrixstruct(new_list_title)
