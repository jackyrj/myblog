# -*- coding:utf-8 -*-
'''
* @Author: Jackyrj
* @Date: 2018-06-29 09:13:44
* @Last Modified by:   Jackyrj
* @Last Modified time: 2018-06-29 09:13:44
* @Desc:
'''
__author__ = 'Jackyrj'

import time
import numpy as np

def exeTime(func):
    """runtime
    """
    def newFunc(*args, **args2):
        """[summary]
        """
        t0 = time.time()
        print("@%s, {%s} start" % (time.strftime("%X", time.localtime()), func.__name__))
        back = func(*args, **args2)
        print("@%s, {%s} end" % (time.strftime("%X", time.localtime()), func.__name__))
        print("@time=%.3fs taken for {%s} \n" % (time.time() - t0, func.__name__))
        return back
    return newFunc

@exeTime
def data_missing_analyze(dtime, list_title, data_matrix):
    """analyze csv file，and save a data_missing csv file
    """
    dtime = np.timedelta64(dtime, 's')

    list_formats = ['datetime64[s]', 'datetime64[s]', 'timedelta64[s]', 'int16']

    current_time_array = data_matrix[1:][data_matrix.dtype.names[0]]
    front_time_array = data_matrix[0:-1][data_matrix.dtype.names[0]]

    missing_array = current_time_array - front_time_array
    is_missing_array = missing_array != dtime
    missing_count = missing_array / dtime -1
    missing = []

    if np.any(is_missing_array):
        missing_matrix_struct = np.zeros(sum(is_missing_array), dtype={'names':list_title, 'formats':list_formats})

        missing_matrix_struct[:][list_title[0]] = np.array(current_time_array[is_missing_array], dtype='datetime64[s]').T
        missing_matrix_struct[:][list_title[1]] = np.array(front_time_array[is_missing_array], dtype='datetime64[s]').T
        missing_matrix_struct[:][list_title[2]] = np.array(missing_array[is_missing_array], dtype='timedelta64[s]').T
        missing_matrix_struct[:][list_title[3]] = np.array(missing_count[is_missing_array], dtype='int16').T

        missing = missing_matrix_struct
    return missing
