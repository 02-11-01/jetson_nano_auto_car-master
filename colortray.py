import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('./photos/red.jpg', 1)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imshow('src',gray)
dst = cv2.equalizeHist(gray)
# cv2.imshow('dst',dst)
# cv2.waitKey(0)


gray = cv2.cvtColor(gray, cv2.COLOR_BGR2RGB)
dst = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
# plt绘制前后两张图片显示效果
# 源图显示
plt.figure(figsize=(14, 9), dpi=100)  # 设置绘图区域的大小和像素
plt.subplot(121)  # 一行两列第一个
plt.imshow(gray)

# 灰度 直方图均衡化
plt.subplot(122)  # 一行两列第二个
plt.imshow(dst)

#plt.show()

import cv2
import numpy as np
img = cv2.imread('./photos/green.png',1)
imgYUV = cv2.cvtColor(img,cv2.COLOR_BGR2YCrCb)
# cv2.imshow('src',img)
channelYUV = cv2.split(imgYUV)
channelYUV[0] = cv2.equalizeHist(channelYUV[0])
channels = cv2.merge(channelYUV)
result = cv2.cvtColor(channels,cv2.COLOR_YCrCb2BGR)
# cv2.imshow('dst',result)
# cv2.waitKey(0)


imgYUV = cv2.cvtColor(imgYUV, cv2.COLOR_BGR2RGB)
result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
#plt绘制前后两张图片显示效果
plt.figure(figsize=(14, 9), dpi=100)#设置绘图区域的大小和像素
plt.subplot(121)  # 一行两列第一个
plt.imshow(imgYUV)
plt.subplot(122)  # 一行两列第二个
#彩色 直方图均衡化
plt.imshow(result)
plt.show()
