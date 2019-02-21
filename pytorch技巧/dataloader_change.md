# Pytorch技巧1：DataLoader的collate_fn参数

[TOC]

本文介绍DataLoader的collate_fn参数，实现自定义的batch输出。

## DataLoader完整的参数表如下：
DataLoader完整的参数表如下：
```python
class torch.utils.data.DataLoader(
    dataset,
    batch_size=1,
    shuffle=False,
    sampler=None,
    batch_sampler=None,
    num_workers=0,
    collate_fn=<function default_collate>,
    pin_memory=False,
    drop_last=False,
    timeout=0,
    worker_init_fn=None)
```
DataLoader在数据集上提供单进程或多进程的迭代器
几个关键的参数意思：
- shuffle：设置为True的时候，每个世代都会打乱数据集
- collate_fn：如何取样本的，我们可以定义自己的函数来准确地实现想要的功能
- drop_last：告诉如何处理数据集长度除于batch_size余下的数据。True就抛弃，否则保留

## 一个测试的例子
```python
import torch
import torch.utils.data as Data
import numpy as np

test = np.array([0,1,2,3,4,5,6,7,8,9,10,11])

inputing = torch.tensor(np.array([test[i:i + 3] for i in range(10)]))
target = torch.tensor(np.array([test[i:i + 1] for i in range(10)]))

torch_dataset = Data.TensorDataset(inputing,target)
batch = 3

loader = Data.DataLoader(
    dataset=torch_dataset,
    batch_size=batch, # 批大小
    # 若dataset中的样本数不能被batch_size整除的话，最后剩余多少就使用多少
    collate_fn=lambda x:(
        torch.cat(
            [x[i][j].unsqueeze(0) for i in range(len(x))], 0
            ).unsqueeze(0) for j in range(len(x[0]))
        )
    )

for (i,j) in loader:
    print(i)
    print(j)
```
输出结果：
```
tensor([[[ 0,  1,  2],
         [ 1,  2,  3],
         [ 2,  3,  4]]], dtype=torch.int32)
tensor([[[ 0],
         [ 1],
         [ 2]]], dtype=torch.int32)
tensor([[[ 3,  4,  5],
         [ 4,  5,  6],
         [ 5,  6,  7]]], dtype=torch.int32)
tensor([[[ 3],
         [ 4],
         [ 5]]], dtype=torch.int32)
tensor([[[  6,   7,   8],
         [  7,   8,   9],
         [  8,   9,  10]]], dtype=torch.int32)
tensor([[[ 6],
         [ 7],
         [ 8]]], dtype=torch.int32)
tensor([[[  9,  10,  11]]], dtype=torch.int32)
tensor([[[ 9]]], dtype=torch.int32)
```

如果不要collate_fn的值，输出变成
```
tensor([[ 0,  1,  2],
        [ 1,  2,  3],
        [ 2,  3,  4]], dtype=torch.int32)
tensor([[ 0],
        [ 1],
        [ 2]], dtype=torch.int32)
tensor([[ 3,  4,  5],
        [ 4,  5,  6],
        [ 5,  6,  7]], dtype=torch.int32)
tensor([[ 3],
        [ 4],
        [ 5]], dtype=torch.int32)
tensor([[  6,   7,   8],
        [  7,   8,   9],
        [  8,   9,  10]], dtype=torch.int32)
tensor([[ 6],
        [ 7],
        [ 8]], dtype=torch.int32)
tensor([[  9,  10,  11]], dtype=torch.int32)
tensor([[ 9]], dtype=torch.int32)
```
所以collate_fn就是使结果多一维。
看看collate_fn的值是什么意思。我们把它改为如下
```python
collate_fn=lambda x:x
```
并输出
```python
for i in loader:
    print(i)
```
得到结果
```
[(tensor([ 0,  1,  2], dtype=torch.int32), tensor([ 0], dtype=torch.int32)), (tensor([ 1,  2,  3], dtype=torch.int32), tensor([ 1], dtype=torch.int32)), (tensor([ 2,  3,  4], dtype=torch.int32), tensor([ 2], dtype=torch.int32))]
[(tensor([ 3,  4,  5], dtype=torch.int32), tensor([ 3], dtype=torch.int32)), (tensor([ 4,  5,  6], dtype=torch.int32), tensor([ 4], dtype=torch.int32)), (tensor([ 5,  6,  7], dtype=torch.int32), tensor([ 5], dtype=torch.int32))]
[(tensor([ 6,  7,  8], dtype=torch.int32), tensor([ 6], dtype=torch.int32)), (tensor([ 7,  8,  9], dtype=torch.int32), tensor([ 7], dtype=torch.int32)), (tensor([  8,   9,  10], dtype=torch.int32), tensor([ 8], dtype=torch.int32))]
[(tensor([  9,  10,  11], dtype=torch.int32), tensor([ 9], dtype=torch.int32))]
```
每个i都是一个列表，每个列表包含batch_size个元组，每个元组包含TensorDataset的单独数据。所以要将重新组合成每个batch包含1\*3\*3的input和1\*3\*1的target，就要重新解包并打包。
看看我们的collate_fn：
```python
collate_fn=lambda x:(
    torch.cat(
        [x[i][j].unsqueeze(0) for i in range(len(x))], 0
        ).unsqueeze(0) for j in range(len(x[0]))
    )
```
j取的是两个变量：input和target。i取的是batch_size。然后通过unsqueeze(0)方法在前面加一维。torch.cat(,0)将其打包起来。然后再通过unsqueeze(0)方法在前面加一维。
完成。
