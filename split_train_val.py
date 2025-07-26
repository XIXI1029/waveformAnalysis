"""
分训练集、验证集和测试集，按照 7：3 的比例来分，训练集7，验证集3
"""
import os
import random
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--xml_path', default='datasets/annotations', type=str, help='input xml label path')

parser.add_argument('--txt_path', default='datasets/ImageSets/Main/', type=str, help='output txt label path')
opt = parser.parse_args()

train_percent = 0.7  # 训练集所占比例
val_percent = 0.3  # 验证集所占比例

xmlfilepath = opt.xml_path
txtsavepath = opt.txt_path
total_xml = os.listdir(xmlfilepath)

if not os.path.exists(txtsavepath):
    os.makedirs(txtsavepath)

num = len(total_xml)
list = list(range(num))

t_train = int(num * train_percent)
t_val = int(num * val_percent)

train = random.sample(list, t_train)
num1 = len(train)
for i in range(num1):
    list.remove(train[i])

val_test = [i for i in list if not i in train]
val = random.sample(val_test, t_val)
num2 = len(val)
for i in range(num2):
    list.remove(val[i])

file_train = open(txtsavepath + '/train.txt', 'w')
file_val = open(txtsavepath + '/val.txt', 'w')

for i in train:
    name = total_xml[i][:-4] + '\n'
    file_train.write(name)

for i in val:
    name = total_xml[i][:-4] + '\n'
    file_val.write(name)

file_train.close()
file_val.close()