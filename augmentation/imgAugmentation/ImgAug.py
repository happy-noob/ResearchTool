#!usr/bin/python
# -*- coding: utf-8 -*-
import cv2
from imgaug import augmenters as iaa
import os
from PIL import Image
from remove_white_edges import remove_white


RemoveW = iaa.Lambda(func_images=remove_white)
# 定义一组变换方法.
seq = iaa.Sequential([
    iaa.Rotate(rotate=(-180, 90), mode='edge'),
    iaa.Fliplr(0.5),  # 对50%的图片进行水平镜像翻转
    iaa.Flipud(0.5),  # 对50%的图片进行垂直镜像翻转
    RemoveW,
    iaa.Resize(500)
])  # apply augmenters in random order

# 图片文件相关路径
path = 'E:/Projects/PythonCode/ResearchTool/testData/Img/pseudo_images/'
savedpath = 'E:/Projects/PythonCode/ResearchTool/testData/Img/out_pseudo_images/'

imglist = []
filelist = os.listdir(path)

if not os.path.exists(savedpath):
    os.mkdir(savedpath)

# 遍历要增强的文件夹，把所有的图片保存在imglist中
# for item in filelist:
#     img = cv2.imread(path + item)
#     # print('item is ',item)
#     # print('img is ',img)
#     # images = load_batch(batch_idx)
#     imglist.append(img)
# print('imglist is ' ,imglist)
file_names = []
def find_image_file(source_path, file_path_list):
    image_ext = ['.jpg', '.JPG', '.PNG', '.png', '.jpeg', '.JPEG', '.bmp']
    for dir_or_file in os.listdir(source_path):
        file_path = os.path.join(source_path, dir_or_file)
        if os.path.isfile(file_path):  # 判断是否为文件
            file_name_ext = os.path.splitext(os.path.basename(file_path))  # 文件名与后缀,元组类型
            file_names.append(str(file_name_ext[0] + file_name_ext[1]))
            if len(file_name_ext) < 2:
                continue
            if file_name_ext[1] in image_ext:  # 后缀在后缀列表中
                file_path_list.append(file_path)
                imglist.append(cv2.imread(file_path))
            else:
                continue

        elif os.path.isdir(file_path):  # 如果是个dir，则再次调用此函数，传入当前目录，递归处理。
            find_image_file(file_path, file_path_list)
        else:
            print('文件夹没有图片' + os.path.basename(file_path))


if __name__ == '__main__':
    find_image_file(path,[])
    print('{} pictures have been appent to imglist'.format(len(imglist)))
    print(type(imglist[0]))
    # print(file_names[0])
# 对文件夹中的图片进行增强操作，循环100次
#     for count in range(10):
#         images_aug = seq.augment_images(imglist)
#         for index in range(len(images_aug)):
#             filename = str(count) + '_' + str(index) + '.jpg'
#             # 保存图片
#             cv2.imwrite(savedpath + filename, images_aug[index])
#             print('image of count%s index%s has been writen' % (count, index))





