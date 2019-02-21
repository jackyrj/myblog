# -*- coding:utf-8 -*-
'''
* @Author: Jackyrj
* @Date: 2018-06-05 15:39:11
* @Last Modified by:   Jackyrj
* @Last Modified time: 2018-06-05 15:39:11
* @Desc:
'''

import csv
import os
#import datetime
import time
#import re
import numpy as np
import pandas as pd

def exeTime(func):
    '''
    * runtime
    '''
    def newFunc(*args, **args2):
        '''
        * runtime
        '''
        t0 = time.time()
        print("@%s, {%s} start" % (time.strftime("%X", time.localtime()), func.__name__))
        back = func(*args, **args2)
        print("@%s, {%s} end" % (time.strftime("%X", time.localtime()), func.__name__))
        print("@time=%.3fs taken for {%s} \n" % (time.time() - t0, func.__name__))
        return back
    return newFunc

def number_index_list(data_array):
    '''
    * index list
    '''
    n = []
    for index, k in enumerate(data_array):
        if ord(k) >= 48 and ord(k) <= 57:
            n.append(index)
    return n

@exeTime
def split_str(array, col):
    '''
    * cut off str by letter
    '''
    return np.array(np.char.split(np.char.join('%', array[:, col]), '%').tolist())

@exeTime
def datetime_str_add(date_standard_matrix, time_standard_matrix):
    '''
    * concatenate string
    '''
    data_matrix_len = len(date_standard_matrix)
    datetime_standard_matrix_join = [[] for i in range(data_matrix_len)]
    for i in range(data_matrix_len):
        datetime_standard_matrix_join[i] =''.join([''.join(date_standard_matrix[i, :]), ' ', ''.join(time_standard_matrix[i, :])])
    return datetime_standard_matrix_join

class Csv_data():
    '''
    * control csv data
    '''
    def __init__(self):
        self.filename = ''
        self.data_matrix = []

    @exeTime
    def load_data(self, csvname, has_list_heander):
        '''
        * load csv file
        '''
        self.data_matrix = pd.read_csv(csvname, sep=',', header=None, skiprows=list(range(has_list_heander)), dtype='S20').values.astype(str, copy=False)
        self.filename = csvname

    @exeTime
    def standardize_data(self, del_col, input_date_example):
        '''
        * standardize csv file，and save a new csc file
        '''
        date_format_list = '0000-00-00 00:00:00'.split(' ')

        #计算有数据前有多少列
        col = input_date_example.count(',') + 1

        data_matrix_len = len(self.data_matrix)

        time_standard = np.array(list(date_format_list[1]))
        time_standard_n = number_index_list(date_format_list[1])
        time_standard_matrix = np.full((data_matrix_len, len(time_standard)), time_standard)

        date_standard = np.array(list(date_format_list[0]))
        date_standard_n = number_index_list(date_format_list[0])
        date_standard_matrix = np.full((data_matrix_len, len(date_standard)), date_standard)

        #如果日期和时间分开为两列
        if col - 2 == del_col:

            time_temp_n = number_index_list(self.data_matrix[0][col - 1])
            time_n_min = min(len(time_standard_n), len(time_temp_n))

            data_matrix_time = split_str(self.data_matrix, col - 1)

            time_standard_matrix[:, time_standard_n[:time_n_min]] = data_matrix_time[:, time_temp_n[:time_n_min]]

            date_temp_n = number_index_list(self.data_matrix[0][col - 2])
            date_n_min = min(len(date_standard_n), len(date_temp_n))

            data_matrix_date = split_str(self.data_matrix, col - 2)

            date_standard_matrix[:, date_standard_n[:date_n_min]] = data_matrix_date[:, date_temp_n[:date_n_min]]

            self.data_matrix[:, del_col] = datetime_str_add(date_standard_matrix, time_standard_matrix)

            #删除时间列和需要删除的无用列
            self.data_matrix = np.delete(self.data_matrix, del_col + 1, axis=1)
            self.data_matrix = np.delete(self.data_matrix, range(del_col), axis=1)

        else:
            row_datetime_list_temp = self.data_matrix[0][col - 1].split(' ')
            time_temp_n = number_index_list(row_datetime_list_temp[1])
            date_temp_n = number_index_list(row_datetime_list_temp[0])

            time_n_min = min(len(time_standard_n), len(time_temp_n))
            date_n_min = min(len(date_standard_n), len(date_temp_n))
            data_matrix_split = np.array(np.char.split(self.data_matrix[:, col - 1], ' ').tolist())


            data_matrix_date = split_str(data_matrix_split, 0)
            data_matrix_time = split_str(data_matrix_split, 1)


            date_standard_matrix[:, date_standard_n[:date_n_min]] = data_matrix_date[:, date_temp_n[:date_n_min]]
            time_standard_matrix[:, time_standard_n[:time_n_min]] = data_matrix_time[:, time_temp_n[:time_n_min]]

            self.data_matrix[:, del_col] = datetime_str_add(date_standard_matrix, time_standard_matrix)

            #删除需要删除的无用列
            self.data_matrix = np.delete(self.data_matrix, range(del_col), axis=1)

    @exeTime
    def str_to_matrixstruct(self, list_title):
        '''
        * set numpy array to list
        '''
        list_formats = [x if index != 0  else 'datetime64[s]'  for index, x in enumerate(['float'] *len(list_title))]
        data_matrix_struct = np.zeros(len(self.data_matrix), dtype={'names':list_title, 'formats':list_formats})

        for index in range(1, len(list_title)):
            data_matrix_struct[:][list_title[index]] = np.array(self.data_matrix[:, index], dtype='float').T
        data_matrix_struct[:][list_title[0]] = np.array(self.data_matrix[:, 0], dtype='datetime64[s]').T

        self.data_matrix = data_matrix_struct

    @exeTime
    def set_UTC(self, timezone):
        '''
        * set time to UTC
        '''
        self.data_matrix[:][self.data_matrix.dtype.names[0]] += np.timedelta64(timezone, 'h')

    @exeTime
    def delete_past_data(self, past_time):
        '''
        * delete the past data
        * past_time eg.:'1999.01.01 00:00:00'
        '''
        past_time = np.datetime64(past_time, 's')
        past_time_list_len = len(self.data_matrix[self.data_matrix[self.data_matrix.dtype.names[0]] < past_time])
        self.data_matrix = np.delete(self.data_matrix, range(past_time_list_len), axis=0)

    @exeTime
    def delete_near_data(self, near_time):
        '''
        * delete the near data
        * near_time eg.:'2018.06.01 00:00:00'
        '''
        near_time = np.datetime64(near_time, 's')
        near_time_list_len = len(self.data_matrix[self.data_matrix[self.data_matrix.dtype.names[0]] > near_time])
        data_matrix_len = len(self.data_matrix)
        self.data_matrix = np.delete(self.data_matrix, range(data_matrix_len - near_time_list_len, data_matrix_len), axis=0)

    @exeTime
    def date_analyze(self, interval_min):
        '''
        * analyze data's date
        * interval_min means input's interval(in minutes)
        '''
        data_len = 2 + 1 * 60 // interval_min
        print('data_len',data_len)
        # 取前面的时间点
        print(self.data_matrix)
        date_past = self.data_matrix[:data_len][self.data_matrix.dtype.names[0]].astype('datetime64[m]')
        datetime_first = date_past[0].astype('datetime64[s]')
        print(date_past)
        # 判断第一个时间点是否符合
        if self.data_matrix[0][0] == datetime_first:
            past_time = self.data_matrix[0][0]
        else:
            datedelta_past = date_past[1:] - date_past[0:-1]
            index = np.where(datedelta_past == np.timedelta64(1, 'h'))[0][0]
            past_time = self.data_matrix[index + 1][0]

        # 取后面的时间点
        date_near = self.data_matrix[-data_len:][self.data_matrix.dtype.names[0]].astype('datetime64[m]')
        datetime_last = ((date_near[-1] + np.timedelta64(1, 'h')).astype('datetime64[m]') - np.timedelta64(1, 'm')).astype('datetime64[s]')
        print(date_near)
        # 判断最后一个时间点是否符合
        if self.data_matrix[-1][0] - np.timedelta64(1, 'm') == datetime_last:
            near_time = self.data_matrix[-1][0]
        else:
            datedelta_near = date_near[1:] - date_near[0:-1]
            index = np.where(datedelta_near == np.timedelta64(1, 'h'))[0][-1]
            near_time = self.data_matrix[index - data_len][0]

        return past_time, near_time

    @exeTime
    def new_csv(self, suffix, list_title, data_matrix):
        '''
        * create a new fili with a underlined suffix name(下划线后缀)
        '''
        filename_new = os.path.splitext(self.filename)[0] + '_' + suffix + os.path.splitext(self.filename)[1]

        if not isinstance(data_matrix, list):
            data_matrix = data_matrix.tolist()
            with open(filename_new, 'w', newline='') as f:
                writer = csv.writer(f)
                #写入新的csv文件中
                writer.writerow(list_title)
                writer.writerows(data_matrix)

        else:
            with open(filename_new, 'w', newline='') as f:
                writer = csv.writer(f)
                #写入新的csv文件中
                writer.writerow(['Empty'])

        return filename_new
