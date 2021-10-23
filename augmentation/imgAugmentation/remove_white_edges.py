import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageEnhance
import imgaug.augmenters as iaa

# img = cv2.imread(img_path)
# row, col = img.shape[:2]


# top
def top2bottom(img, row, col):
    flag = 0
    i = 0
    j = 0
    for i in range(0, row):
        for j in range(0, col):
            px = img[i, j]
            if px[0] != 255 or px[1] != 255 or px[2] != 255:
                flag = 1
                break
        if flag == 1:
            break
    if flag == 0:
        return -1
    return i


# bottom
def bottom2top(img, row, col):
    flag = 0
    i = 0
    j = 0
    for i in range(row - 1, -1, -1):
        for j in range(0, col):
            px = img[i, j]
            if px[0] != 255 or px[1] != 255 or px[2] != 255:
                flag = 1
                break
        if flag == 1:
            break
    if flag == 0:
        return -1
    return i


# left
def left2right(img, row, col):
    flag = 0
    i = 0
    j = 0
    for j in range(0, col):
        for i in range(0, row):
            px = img[i, j]
            if px[0] != 255 or px[1] != 255 or px[2] != 255:
                # print(j, i)
                flag = 1
                break
        if flag == 1:
            break
    if flag == 0:
        return -1
    return j

# right
def right2left(img, row, col):
    flag = 0
    i = 0
    j = 0
    for j in range(col - 1, -1, -1):
        for i in range(0, row):
            px = img[i, j]
            if px[0] != 255 or px[1] != 255 or px[2] != 255:
                flag = 1
                break
        if flag == 1:
            break
    if flag == 0:
        return -1
    return j

def cropConner(img):
    row, col = img.shape[:2]

    top = top2bottom(img, row, col)
    bottom = bottom2top(img, row, col)
    left = left2right(img, row, col)
    right = right2left(img, row, col)
    h = row - bottom
    w = col - right
    return left,top,right,bottom

# 拉伸处理,save
def stretch500(img, output_img_path):
    # img = cv2.imread(img_path)
    row, col = img.shape[:2]

    top = top2bottom(img, row, col)
    bottom = bottom2top(img, row, col)
    left = left2right(img, row, col)
    right = right2left(img, row, col)
    # print('top', top)
    # print('bottom', bottom)
    # print('left', left)
    # print('right', right)

    crop_max = np.min(np.array([left, top, col - right, row - bottom]))
    # print("crop_max", crop_max)
    cropped1 = img[top:bottom, left:right]
    # 直接拉伸到600*600
    cropped1 = cv2.resize(cropped1, [500, 500])

    # 保存
    cv2.imwrite(output_img_path, cropped1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
#
def remove_white(images,random_state=None, parents=None, hooks=None):
    for i in range(len(images)):
        # img = cv2.imread(img_path)
        img = images[i]
        row, col = img.shape[:2]
        left,top,right,bottom = cropConner(img)
        h = row - bottom
        w = col - right
        # crop_max = np.min(np.array([left,top,h,w]))
        cropped1 = img[top:bottom, left:right]
        images[i] = cropped1
    return  images

