# Python数据练习之数据查缺（一）

本文展示待处理的cvs数据、主程序流程图和主程序。

## cvs数据
保存为csv格式

```
Time (UTC),Open,High,Low,Close,Volume
2018.06.04 00:00:00,1.1667,1.1668,1.1667,1.1668,214.25
2018.06.04 00:01:00,1.1668,1.16696,1.16672,1.16696,225.6
2018.06.04 00:02:00,1.16697,1.16725,1.16696,1.16725,182.16
2018.06.04 00:03:00,1.16725,1.16732,1.16715,1.16732,236.51
2018.06.04 00:04:00,1.16732,1.16735,1.16721,1.16721,249.98
2018.06.04 00:17:00,1.16779,1.16782,1.16772,1.16776,203.45
2018.06.04 00:18:00,1.16776,1.1679,1.16772,1.16773,186.9
2018.06.04 00:19:00,1.16772,1.16775,1.16762,1.16762,133.35
2018.06.04 00:20:00,1.16763,1.16766,1.16753,1.16753,112.91
2018.06.04 00:21:00,1.16754,1.1676,1.1675,1.16755,142.59
```


## 主程序流程图
```flow
st=>start: 开始
e=>end: 结束
op_read_name=>operation: 输入文件名
cond_new=>condition: 文件是否处理过
op_load=>operation: 导入数据

st->op_read_name->cond_new
cond_new(no,left)->e

```

## 主程序函数
```python
# -*- coding:utf-8 -*-
'''
* @Author: Jackyrj
* @Date: 2018-06-05 16:22:22
* @Last Modified by:   Jackyrj
* @Last Modified time: 2018-06-05 16:22:22
* @Desc:
'''
import time

# 编写的库
import csv_data as cd

start = time.clock()

# 文件路径
filename = 'test.csv'

# 处理过的文件跳过处理
if 'new' in filename:
    standardize = 0
else:
    standardize = 1

# 时区
UTCtime = 0
# 是否有表头，处理过程中不保留表头
has_list_heander = 1

# 从第一列数起有多少列需要删除
del_col = 0

# 时间格式
input_date_example = '2018.06.04 01:38:00'

# 需要截取的时间区域
past_time = '2010-01-01 00:00:00'
near_time = '2018-06-04 01:38:00'

# 需要分析的时间间隔，以秒为单位
delta_time_seconds = 60 * 1

# 新表的表头
new_list_title = ['Time (UTC)', 'Open', 'High', 'Low', 'Close', 'Volume']

# 分析列表的表头
missing_list_title = ['Start_Time', 'Stop_Time', 'interval', 'Missing_Count']

#从filename导入数据
data = cd.Csv_data()
data.load_data(filename, has_list_heander)

#原始数据
if standardize == 1:
    #使数据格式标准化
    data.standardize_data(del_col, input_date_example)

    #转换numpy数据为list
    data.str_to_matrixstruct(new_list_title)

    #使时间变成UTC标准时间
    data.set_UTC(UTCtime)

    #删除过去的时间
    data.delete_past_data(past_time)

    #删除近期时间的时间
    data.delete_near_data(near_time)

    #数据有效性分析
    data.data_missing_analyze(delta_time_seconds, missing_list_title)

    #数据有效性记录
    data.new_csv('missing', missing_list_title, data.missing)

    #新数据记录
    data.new_csv('new', new_list_title, data.data_matrix)

#整理后的数据
else:
    data.str_to_matrixstruct(new_list_title)

end = time.clock()
print('runtime = ', str(end-start))
```
