import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np

img0 = cv.imread('./photos/red.jpg')
#img0 = img0[0:300,600:1000] #这里截取摄像头拍摄到的路面部分 因为摄像头相对位置固定 所以只需要调整一次
def color_detect(img):
    # 读取图像并转换到HSV空间
    frame = img
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

# 红色线检测
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    lower_red2 = np.array([170, 50, 50])
    upper_red2 = np.array([180, 255, 255])
    red_mask1 = cv.inRange(hsv, lower_red, upper_red)
    red_mask2 = cv.inRange(hsv, lower_red2, upper_red2)
    #red_mask = cv.bitwise_and(frame, frame, mask=red_mask)
    red_mask = cv.bitwise_or(red_mask1, red_mask2)
    #cv.imwrite('./photos/red_mask.jpg', red_mask)
    #img_show(red_mask,"red")
# 白色线检测
    lower_green = np.array([35, 43, 46])
    upper_green = np.array([99, 255, 255])
    green_mask = cv.inRange(hsv,lower_green,upper_green)
    cv.imwrite('black_mask.jpg', green_mask)
    img_show(green_mask, "green")
def find_edge(img):
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5, 5), 0)
    ret, img1 = cv.threshold(blur, 180, 255, cv.THRESH_BINARY)  # 二值化
    img_show(img1,'1')
    histogram = np.sum(img1[img1.shape[0] // 2:, :], axis=0)  #将img1读取行数 取中间行 取全部列 之后压缩为一行 即所有列相加
    print(histogram)
    midpoint = int(histogram.shape[0] / 2)  # 直方图垂直尺寸
    edged = cv.erode(img1, None, iterations=1)
    img_show(img1,'s1s')
    edged = cv.Canny(img1,80, 100)
    contours, h = cv.findContours(edged.copy(), mode=cv.RETR_EXTERNAL, method=cv.CHAIN_APPROX_NONE)   #只储存车道的顶点数据 只检测外轮廓
    largest_contours = sorted(contours, key=cv.contourArea, reverse=True)[0:1]   #找到面积最大的车道
    sec_largest_contours = sorted(contours, key=cv.contourArea, reverse=True)[1:2]   #找到面积第2大的车道
    #这样的方法不合理 如果图像出现比车道面积还大的块就会找错车道
    #pts = largest_contours.reshape(4, 2)
    driving_reference=img0.copy()
    numlg=0 #最大车道的坐标数量
    numse=0 #次大车道的坐标数量
    lg_x=[] #最大车道的x坐标 以下类同
    lg_y=[]
    se_x=[]
    se_y=[]
    for cnt in largest_contours:    #获取最大车道的边缘坐标

        for i in cnt:
          lg_x.append(i[0][0])
          lg_y.append(i[0][1])
          #print(lg_x[numlg],',',lg_y[numlg])
          #print(numlg)
          numlg+=1
          #print(numlg)
    for cnt in sec_largest_contours:   #次大车道的边缘坐标

      for i in cnt:
         se_x.append(i[0][0])
         se_y.append(i[0][1])
         #print(se_x[numse],',',se_y[numse])
         #print(numlg)
         numse+=1
         #print(numse)
    for cnt in range(int(min(numlg,numse)/2)):    #绘制路线
        cv.circle(driving_reference, (int((lg_x[cnt]+se_x[cnt])/2),lg_y[cnt]), 1, (0, 0, 213), 3) #方法是取x平均值 以最大车道的Y坐标为路线的Y坐标 Y坐标取值可能有问题
        #cv.circle(driving_reference, (604,387), 3, (0, 0, 213), 3)
    #print(largest_contours)
    #pts = largest_contours.reshape(4, 2)#将轮廓的点重新整理成一个4x2的矩阵，即四个点，每个点两个坐标。
    #print(pts)
    contour=img0.copy()
    cv.drawContours(contour,largest_contours,-1,(0,0,255),3)
    cv.drawContours(contour,sec_largest_contours,-1,(0,0,255),3)
    img_show(contour,'ss')
    img_show(driving_reference,'ss1')
    #cv.namedWindow('Image', 0)
def img_show(img,name):
    cv.imshow(name, img)
def white_balance_1(img):
    r, g, b = cv.split(img)
    r_avg = cv.mean(r)[0]
    g_avg = cv.mean(g)[0]
    b_avg = cv.mean(b)[0]

    k = (r_avg + g_avg + b_avg) / 3
    kr = k / r_avg
    kg = k / g_avg
    kb = k / b_avg

    r = cv.addWeighted(src1=r, alpha=kr, src2=0, beta=0, gamma=0)
    g = cv.addWeighted(src1=g, alpha=kg, src2=0, beta=0, gamma=0)
    b = cv.addWeighted(src1=b, alpha=kb, src2=0, beta=0, gamma=0)

    balance_img = cv.merge([b, g, r])
    return balance_img

yellow = cv.imread('./photos/green1.jpg')
##yellow=white_balance_1(yellow)
color_detect(yellow)
#yellow_edge=cv.imread('./photos/yellow_mask.jpg')
#img_show(yellow_edge,'yellow')
#find_edge(yellow_edge)

cv.imshow("orgin", yellow)
#cv.imshow("Image", img1)
#cv.imshow("contours", contour)
#cv.imshow("driving_reference", driving_reference)
cv.waitKey(0)
