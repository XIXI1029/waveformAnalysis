"""
This code is designed to convert the VOC dataset into a dataset format usable by YOLO.

(Note: VOC refers to the PASCAL Visual Object Classes dataset, a popular computer vision dataset, while YOLO (You Only Look Once) is an object detection model that requires data in a specific format.)
"""

import xml.etree.ElementTree as ET
import os

sets = ['train', 'val']

classes = ['Accumulation Flow', 'Volume', 'Flow', 'Leakage Volume', 'Double_Triggering Flow',
           'Double_Triggering Volume', 'Premature_cycling Flow', 'Premature_cycling Volume',
           'Ineffective_effort Flow', 'Ineffective_effort Volume', 'Normal Flow', 'Normal Volume', 'Normal Pressure']  # class names
# classes = ['Accumulation Flow', 'Accumulation Pressure']
abs_path = os.getcwd()


def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h


def convert_annotation(image_id):
    in_file = open(abs_path + '/datasets/annotations/%s.xml' % (image_id), encoding='UTF-8')
    out_file = open(abs_path + '/datasets/labels/%s.txt' % (image_id), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        # difficult = obj.find('Difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        b1, b2, b3, b4 = b
        # 标注越界修正
        if b2 > w:
            b2 = w
        if b4 > h:
            b4 = h
        b = (b1, b2, b3, b4)
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


for image_set in sets:
    if not os.path.exists(abs_path + '/datasets/labels/'):
        os.makedirs(abs_path + '/datasets/labels/')

    image_ids = open(abs_path + '/datasets/ImageSets/Main/%s.txt' % (image_set)).read().strip().split()
    list_file = open(abs_path + '/datasets/%s.txt' % (image_set), 'w')
    for image_id in image_ids:
        list_file.write(abs_path + '/datasets/images/%s.jpg\n' % (image_id))
        convert_annotation(image_id)
    list_file.close()
