import os
import cv2
import uuid
from PIL import Image


# todo: for Images

def find_image_file(source_path, file_path_list):
    """
    递归寻找 文件夹以及子目录的 图片文件。
    :param source_path: 源文件夹路径
    :return file_path_list: 输出 文件路径列表
    """
    image_ext = ['.jpg', '.JPG', '.PNG', '.png', '.jpeg', '.JPEG', '.bmp']
    for dir_or_file in os.listdir(source_path):
        file_path = os.path.join(source_path, dir_or_file)
        if os.path.isfile(file_path):  # 判断是否为文件
            file_name_ext = os.path.splitext(os.path.basename(file_path))  # 文件名与后缀
            if len(file_name_ext) < 2:
                continue
            if file_name_ext[1] in image_ext:  # 后缀在后缀列表中
                file_path_list.append(file_path)
            else:
                continue
        elif os.path.isdir(file_path):  # 如果是个dir，则再次调用此函数，传入当前目录，递归处理。
            find_image_file(file_path, file_path_list)
        else:
            print('文件夹没有图片' + os.path.basename(file_path))

    return file_path_list


def showImages():
    # 1.【输入】
    dir_path = "../testData/Img/pseudo_images"

    # 文件路径 列表 【输出】
    file_path_list = []

    # 2.递归调用
    find_image_file(dir_path, file_path_list)  # 递归查看 文件夹内所有图片

    # 3.显示图片列表
    for item in file_path_list:
        # 打印图片:
        print(item)
        # img_org = cv2.imread(item)
        # cv2.imshow("img", img_org)
        # cv2.waitKey()
    cv2.destroyAllWindows()


def saveImages(images, save_root, names=None):
    if names == None:
        for i in range(len(images)):
            names[i] = uuid.uuid4()
    for id,img in enumerate(images):
        img_name = names[id]
        print(img_name)
        save_path = save_root + "/" + img_name
        cv2.imwrite(save_path, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
