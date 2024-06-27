import matplotlib.pyplot as plt
import cv2 as cv2
import numpy as np
frame = cv2.imread('./photos/corner2.png')
frame = cv2.resize(frame, (320, 240))

# 2、透视变换 (查看俯视图)
matSrc = np.float32([[0, 149], [320, 149], [281, 72], [43, 72]])
matDst = np.float32([[0, 240], [320, 240], [320, 0], [0, 0]])
matAffine = cv2.getPerspectiveTransform(matSrc, matDst)  # mat 1 src 2 dst
dst = cv2.warpPerspective(frame, matAffine, (320, 240))
cv2.imshow('trans',dst)

# 画蓝色的矩形框，采集数据的时候采集的就是当前蓝色矩形框中的数据
# src 4->dst 4 (左下角 右下角 右上角 左上角 )
pts = np.array([[0, 149], [320, 149], [281, 72], [43, 72]], np.int32)
# 顶点个数：4，矩阵变成4*1*2维
# OpenCV中需要将多边形的顶点坐标变成顶点数×1×2维的矩阵
# 这里 reshape 的第一个参数为-1, 表示“任意”，意思是这一维的值是根据后面的维度的计算出来的
pts = pts.reshape((-1, 1, 2))
cv2.polylines(frame, [pts], True, (255, 0, 255), 3)  # True表示闭合，（255,0,0）是蓝色，3是线宽
# 3、转化图像二值化(看二值化之后的黑白图像）
cv2.imshow('frame', frame)
dst_gray = cv2.cvtColor(dst, cv2.COLOR_RGB2GRAY)   #转灰度
dst_retval, dst_binaryzation = cv2.threshold(dst_gray, 83, 255, cv2.THRESH_BINARY)   #二值化

dst_binaryzation = cv2.erode(dst_binaryzation, (3,3), iterations=10)  # 腐蚀化操作
cv2.imshow('dst1_', dst_binaryzation)
#dst = cv2.bitwise_not(dst)
edge= cv2.Canny(dst_binaryzation,180,190)
kernel = np.ones((6, 6), dtype=np.uint8)
edge =cv2.bitwise_not(edge)
edge = cv2.erode(edge, kernel, 1)
dege = cv2.cornerHarris(edge, 2, 3, 0.04)



cv2.imshow('edge', edge)

# 当axis为0时,是压缩行,即将每一列的元素相加,将矩阵压缩为一行
# 当axis为1时,是压缩列,即将每一行的元素相加,将矩阵压缩为一列(这里的一列是为了方便理解说的，实际上，在控制台的输出中，仍然是以一行的形式输出的)
histogram = np.sum(dst_binaryzation[dst_binaryzation.shape[0] // 2:, :], axis=0)  # 我们这里是一维数组
histogram1 = np.sum(dst_binaryzation[:dst_binaryzation.shape[0] // 2, :], axis=0)  # 上半部分，检测弯道
frame1 = np.array(frame[:frame.shape[0] // 2, :])  # 上半部分，检测弯道
histogram1 = np.float32(histogram1)
histogram1 = cv2.cornerHarris(src=histogram1, blockSize=9, ksize=21, k=0.04)
# 变量a的阈值为0.01 * dst.max()，如果dst的图像值大于阈值，那么该图像的像素点设为True，否则为False
# 将图片每个像素点根据变量a的True和False进行赋值处理，赋值处理是将图像角点勾画出来
a = dst > 0.01 * dst.max()
print('a=',np.sum(a))
frame1[a] = [0, 0, 255]
histogram_edge = np.sum(edge[edge.shape[0] // 2:, :], axis=0)  # 我们这里是一维数组
#midpoint = np.int(histogram.shape[0] / 2)  # 直方图垂直尺寸
histogram_image = np.zeros((256, 320), dtype=np.uint8)

# 归一化直方图
#histogram = histogram / np.max(histogram) * 256
histogram_edge = histogram_edge / np.max(histogram_edge) * 256

# 在图像上绘制直方图
for i in range(256):
    cv2.line(histogram_image, (i * 2, 256), (i * 2, 256 - int(histogram[i])), 255, 1)
    #cv2.line(histogram_image, (i * 2, 256), (i * 2, 256 - int(histogram_edge[i])), 128, 1)

# 显示直方图图像
cv2.imshow('Histogram', histogram_image)

left_sum = np.sum(histogram[:20], axis=0)  # 计算左边像素点之和
right_sum = np.sum(histogram[300:], axis=0)  # 计算右边像素点之和

# print("left_sum =%d "%left_sum)
# print("right_sum = %d"%right_sum)


rightpoint = 320
center_r = 159
# print (histogram)
# print(histogram[::-1])
# plt.plot(histogram)
# plt.plot(histogram[::-1])
# plt.show()

# 4、获取黑线左右边线并绘制线条
# 获取左右线的位置
for i in range(0,len(histogram1)):
    if histogram1[i]>=0:
        cv2.circle(frame,(i,30),2,(0,0,255), -1)
leftx_base = np.argmin(histogram[:center_r], axis=0)
rightx_base = np.argmin(histogram[::-1][:center_r], axis=0)  # 反转直方图取最右侧的值
print(np.min(histogram[:center_r],axis=0))
print(np.min(histogram[::-1][:center_r],axis=0))
llne=0
rlne=0
if(leftx_base>40):
    print("left lane exists")
elif(np.min(histogram[:center_r],axis=0)>255*100):
    print("left lane dosnt exist")
    llne=1
    leftx_base = np.argmin(histogram[:rightpoint], axis=0)

print(leftx_base, rightx_base)
if(rightx_base>40):
    #print(leftx_base, rightx_base)
    print("right lane exists")
elif(np.min(histogram[::-1][:center_r],axis=0)>255*100):
    print("right lane dosnt exist")
    rlne=1
    rightx_base = np.argmin(histogram[::-1][:rightpoint], axis=0)
else:
    print("right lane exists")
if(llne==1 and rlne==1):
    print("no lane exists or lane lies in the graph")
#for i in range(histogram_edge)

rightx_base = 319 - rightx_base
print(leftx_base, rightx_base)
dst_binaryzation = cv2.cvtColor(dst_binaryzation, cv2.COLOR_GRAY2RGB)
cv2.line(dst_binaryzation, (159, 0), (159, 240), (255, 0, 255), 2)  # 图像中线 紫色 # fix liusen 200321  149->159
lane_center = int((leftx_base + rightx_base) / 2)  # 左右线中间位置
# print("lane_center")
# print(lane_center)
cv2.line(dst_binaryzation, (leftx_base, 0), (leftx_base, 240), (0, 255, 0), 2)  # 赛道左侧位置
cv2.line(dst_binaryzation, (rightx_base, 0), (rightx_base, 240), (0, 255, 0), 2)  # 赛道右侧位置
cv2.line(dst_binaryzation, (lane_center, 0), (lane_center, 240), (255, 0, 0), 2)  # 实际中线位置

left_sum_value = int(np.sum(histogram[:center_r], axis=0)) / 159
right_sum_value = int(np.sum(histogram[center_r:], axis=0)) / 159
# print("left_sum_value = %d", left_sum_value)
# print("right_sum_value = %d", right_sum_value)
# 5、计算偏差
Bias = 159 - lane_center
cv2.putText(dst_binaryzation, "Bias: " + str(int(Bias)), (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
cv2.putText(dst_binaryzation, "rightx_base: " + str(int(rightx_base)), (10, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
cv2.putText(dst_binaryzation, "leftx_base: " + str(int(leftx_base)), (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
# print(Bias)

cv2.imshow("dst", dst)
cv2.imshow('dst_', dst_binaryzation)
cv2.waitKey()