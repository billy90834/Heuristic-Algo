#import module
import numpy as np
import random
import matplotlib.pyplot as plt
import configparser as config

#read and create dataset
file_empty = 0
#capacity
with open('p07_c.txt', mode="r") as file:
    capacity = np.loadtxt(file)
    if capacity.size == 0:
        file_empty = 1

#weights
with open('p07_w.txt', mode="r") as file:
    weights = np.loadtxt(file)
    weights = weights.astype(np.int32)
    if weights.size == 0:
        file_empty = 1

#profits
with open('p07_p.txt', mode="r") as file:
    profits = np.loadtxt(file)
    profits = profits.astype(np.int32)
    if profits.size == 0:
        file_empty = 1

#selections
with open('p07_s.txt', mode="r") as file:
    selects = np.loadtxt(file)
    selects = selects.astype(np.int32)
    if selects.size == 0:
        file_empty = 1

if file_empty == 1:
    print('file is empty')
    exit()

# 計算string代表的value, weight
def count_values(keys):
    res_v = 0
    res_w = 0
    for idx, key in enumerate(keys):
        if int(key)==1:
            res_v += profits[int(idx)]
            res_w += weights[int(idx)]
    return res_v,res_w

# random 01 bitstring
def rand_key(count):
    while True:
        init_key = ""
        for i in range(count):
            temp = str(random.randint(0, 1))
            init_key += temp
        res_v, res_w = count_values(init_key)
        # 不能超過限重
        if res_w <= capacity: 
            break
    return res_v, init_key

# change a bit
def change_a_bit(key, position, bit):
    temp = list(key)
    temp[position] = str(bit)
    key = "".join(temp)
    return key

# opposite
def opposite(key, position):
    temp = list(key)
    if(key[position] == '1'):
        temp[position] = '0'
    else:
        temp[position] = '1'
    key = "".join(temp)
    return key

# 迭代次數500次
round = 500

# 折線圖list
list_plot = [0 for x in range(0, round)]

# 最大值
max_v = 0

# 物品數量
items = np.size(weights)

# 溫度設定
t_init = 1000
t_min = 1
eta = 0.999
k = 1
t = t_init

# 折線圖list
list_plot = []
iter = 0

# 溫度還沒到設定值以前
while t > t_min:
    # 生成random bit string
    res_v, init_key = rand_key(items)
    take_step_key = init_key

    list_plot.append(max_v)
    iter += 1

    # 隨機選一個物品改變狀態 0->1 or 1->0
    take_step_key_new = opposite(take_step_key, random.randint(0, items-1))
    
    # 計算改變前後的value, weight
    value_old, weight_old = count_values(take_step_key)
    value_new, weight_new = count_values(take_step_key_new)
    if weight_new <= capacity:
        res = value_new - value_old

        # 新價值較高 or 有機率允許改變
        if res > 0 or np.exp(-res/k*t) > np.random.rand():
            take_step_key = take_step_key_new

    # 紀錄最大值&最大值之string
    if max_v < res_v:
        max_v = res_v
        max_v_key = take_step_key

    t = t*eta

print('result max value: ' + str(max_v))
print('result knapsack: ' + str(max_v_key))
print('expected max value: ', end='')
expected_v = 0
for idx, select in enumerate(selects):
    if select == 1:
        expected_v += profits[int(idx)]
print(expected_v)
print('expected knapsack: ', end='')
s = [str(i) for i in selects]
res = int(''.join(s))
print(res)

# 折線收斂圖
x = np.linspace(1, 500, iter)
y = np.linspace(1, capacity)
plt.plot(x, list_plot, 'b')
plt.show()
