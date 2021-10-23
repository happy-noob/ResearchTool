import os
import cv2
import imgaug.augmenters as iaa
from imgAugmentation.remove_white_edges import remove_white
import torchvision.transforms as transform
from PIL import Image
from torchvision.datasets import ImageFolder
from logging import getLogger
from utils.fileProcess import find_image_file,saveImages

def imgAug(data_path,save_root):
    origin_pathes = []
    origin_pathes,filenames = find_image_file(data_path,origin_pathes) #递归寻找图片，当前origin_path是所有图片的绝对路径
    images = []
    for path in origin_pathes:
        image = cv2.imread(path)
        images.append(image)
    sometimes = lambda aug: iaa.Sometimes(0.5, aug)
    RemoveW = iaa.Lambda(func_images=remove_white)
    # SaveImg = iaa.Lambda(func_images=saveImages)

    # pipeline
    seq = iaa.Sequential([

        iaa.Rotate(rotate=(-180, 90), mode='edge'),
        iaa.Fliplr(0.5),  # 对50%的图片进行水平镜像翻转
        iaa.Flipud(0.5),  # 对50%的图片进行垂直镜像翻转
        RemoveW,
        # iaa.Resize(500),

        # iaa.SomeOf( (2, 5),
        #            [
        #                iaa.Fliplr(0.5),  # 对50%的图片进行水平镜像翻转
        #                iaa.Flipud(0.5),  # 对50%的图片进行垂直镜像翻转
        #                iaa.Rotate(rotate=(-180, 180), seed=0.8),
        #                # sometimes(
        #                #     iaa.Superpixels(
        #                #         p_replace=(0, 1.0),
        #                #         n_segments=(20, 200)
        #                #     )
        #                # ),
        #                # iaa.OneOf([
        #                #     # 高斯扰动
        #                #     iaa.GaussianBlur((0, 3.0)),
        #                #     # 从最邻近像素中取均值来扰动。
        #                #     iaa.AverageBlur(k=(2, 7)),
        #                #     # 通过最近邻中位数来扰动。
        #                #     iaa.MedianBlur(k=(3, 11)),
        #                # ]),
        #
        #                # 锐化
        #                # iaa.Sharpen(alpha=(0, 1.0), lightness=(0.75, 1.5)),
        #                # 浮雕效果
        #                # iaa.Emboss(alpha=(0, 1.0), strength=(0, 2.0)),
        #                # iaa.Invert(0.05, per_channel=True),  # invert color channels
        #                # Add a value of -10 to 10 to each pixel.
        #                # iaa.Add((-10, 10), per_channel=0.5),
        #                # 按像素加。
        #                # iaa.AddElementwise((-40, 40)),
        #                # Change brightness of images (50-150% of original value).
        #                # iaa.Multiply((0.5, 1.5)),
        #                # Multiply each pixel with a random value between 0.5 and 1.5.
        #                # 按像素值乘。
        #                # iaa.MultiplyElementwise((0.5, 1.5)),
        #                # Improve or worsen the contrast of images.
        #                # 改变图像的对比度
        #                # iaa.ContrastNormalization((0.5, 2.0)),
        #            ],
        #            # do all of the above augmentations in random order 定义随机数
        #            random_order=True
        #            ),
    ])
    images_aug = seq(images=images) #处理图片，images_aug是增强后的图片集合
    # print(images_aug[0])
    # save
    saveImages(images_aug,save_root,filenames)
    print("*************Done***************")

# if __name__ == '__main__':
#     saveImages()