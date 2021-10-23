import os
# import IO_Form
# import remove_white_edges
from multiprocessing import Process
import cv2
import imgaug.augmenters as iaa
from PIL import Image
import argparse
from augmentation.imgAugmentation.remove_white_edges import remove_white

#多线程
parser = argparse.ArgumentParser(description="Implementation of Augmentation")
parser.add_argument("--data_path", type=str, default="./datasets",
                    help="path to dataset repository")
parser.add_argument("--output_path", type=str, default="./out",
                    help="path to augmentation dataset repository")
parser.add_argument("--num_workers",type=int,default=0)

global args
args =parser.parse_args()
data_path = args.data_path
output_path = args.output_path
num = args.num_workers
if not os.path.exists(output_path):
    os.mkdir(output_path)

imglist = []
file_names =[]
# 遍历要增强的文件夹，把所有的图片保存在imglist中
def find_image_file(source_path,file_path_list):
    image_ext = ['.jpg', '.JPG', '.PNG', '.png', '.jpeg', '.JPEG', '.bmp']
    for dir_or_file in os.listdir(source_path):
        file_path = os.path.join(source_path, dir_or_file)
        if os.path.isfile(file_path):  # 判断是否为文件
            file_name_ext = os.path.splitext(os.path.basename(file_path))  # 文件名与后缀,元组类型
            if len(file_name_ext) < 2:
                continue
            if file_name_ext[1] in image_ext:  # 后缀在后缀列表中
                file_path_list.append(file_path)
                imglist.append(cv2.imread(file_path))
                file_names.append(str(file_name_ext[0] + file_name_ext[1]))
            else:
                continue

        elif os.path.isdir(file_path):  # 如果是个dir，则再次调用此函数，传入当前目录，递归处理。
            find_image_file(file_path, file_path_list)
        else:
            print('文件夹没有图片' + os.path.basename(file_path))
    # print(type(imglist[0]))
    # print(file_names[0])
    return imglist,file_names


def imgAug(imglist,file_names,images_folder=None):
    if not images_folder == None:
        for i, name in enumerate(file_names):
            file_names[i] = images_folder + '/' + name

    RemoveW = iaa.Lambda(func_images=remove_white)
    # 定义一组变换方法.
    seq = iaa.Sequential([
        iaa.Rotate(rotate=(-180, 90), mode='edge'),
        iaa.Fliplr(0.5),  # 对50%的图片进行水平镜像翻转
        iaa.Flipud(0.5),  # 对50%的图片进行垂直镜像翻转
        RemoveW,
        iaa.Resize(500)
    ])
    for index,img in enumerate(imglist):
        img = seq.augment_image(img)
        cv2.imwrite(file_names[index],img)
        print('{} has been written'.format(file_names[index]))

# python main_swav_aug.py  --data_path ./data  --output_path ./flip_rotate_data --num_workers 5
if __name__ == '__main__':
    imglist, file_names = find_image_file(data_path, [])
    print('{} pictures have been appent to imglist'.format(len(imglist)))
    # 单进程
    if num == 0:
        for i, name in enumerate(file_names):
            file_names[i] = output_path + '/' + name
        # imgAug(imglist, file_names)
    # 多进程
    else:
        process = []
        for id in range(num):
            images_folder = output_path + '/data{}'.format(id)
            if not os.path.exists(images_folder):
                os.mkdir(images_folder)
            p = Process(target=imgAug,args=(imglist,file_names,images_folder))
            p.start()
            print("*********Process{} Start**********".format(id))
            process.append(p)

        for item in process:
            item.join()
    print("***********All Process End*******************")

#deletewhite
# if __name__ == '__main__':
#     data_path = r"E:\\DataSets\\images"
#     save_path = r"E:\\DataSets\\augmentation\\outAug"
#     if not os.path.exists(save_path):
#         os.makedirs(save_path)
#     # imgAug(origin_path,img_path)
#     origin_path = []
#     origin_path = find_image_file(data_path, origin_path)  # 递归寻找图片，当前origin_path是所有图片的绝对路径
#     images = []
#     for path in origin_path:
#         image = cv2.imread(path)
#         images.append(image)
#     count = 0
#     for img in images:
#         img_name = origin_path[count].split("\\")[-1]
#         output_path = save_path +"\\" + img_name
#         stretch(img, output_path)  # 去白边处理
#         count += 1
