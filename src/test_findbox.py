# import imutils
import scipy.spatial
import matplotlib.pyplot as plt
import os
import cv2
import numpy as np


def read_path(image_path):
    images_name = os.listdir(image_path)
    images_path = [os.path.join(image_path, image_name) for image_name in images_name]
    print(images_path)
    # print('./output_data' + images_path[0].split('/')[2].replace(' ', '') + '.jpg')
    return images_path


def output_path(output_path, image_path, img):
    cv2.imwrite(output_path + '/' + image_path.split('/')[2].replace(' ', ''), img)


def black_white(image_path):
    img = cv2.imread(image_path)
    # img = cv2.resize(img, (64, 32), interpolation=cv2.INTER_CUBIC)
    height, width, depth = np.array(img).shape
    white = [255, 255, 255]
    black = [0, 0, 0]
    # 将非白区域变白
    for i in range(height):
        for j in range(width):
            if white in img[i, j, :]:
                pass
            else:
                img[i, j, :] = black
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    cnts = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # print(len(cnts))
    # cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    # # 将轮廓按面积大小降序排序
    # c = sorted(cnts, key=cv2.contourArea, reverse=True)
    # # 将小的区域填充成黑色
    print(len(cnts))
    for i in range(len(cnts) - 1):
        x, y, w, h = cv2.boundingRect(cnts[i + 1])
        img[y:(y + h), x:(x + w), :] = black
    # cv2.rectangle(imgsize, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imwrite(r'C:\my_repo\BizDoc-Ocr\test_1_white.jpg', img)
    # output_path(output_path, image_path, img)


if __name__ == '__main__':
    black_white(r'C:\my_repo\BizDoc-Ocr\test_1.jpg')