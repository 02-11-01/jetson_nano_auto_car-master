from IPython.display import display
import ipywidgets.widgets as widgets
import cv2
import time

# 线程功能操作库
import threading
import inspect
import ctypes
import matplotlib.pyplot as plt


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)
import YB_Pcb_Car  #导入亚博智能专用的底层库文件

car = YB_Pcb_Car.YB_Pcb_Car()
car.Ctrl_Servo(4, 80)  #控制四号舵机（水平）转到80°
car.Ctrl_Servo(2, 100)  #二号（竖直）100°
def webctrl():
    import socket
    import time
    # 创建socket
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 本地信息
    address = ('', 7788)
    # 绑定
    tcp_server_socket.bind(address)
    # 使用socket创建的套接字默认的属性是主动的，
    # 使用listen将其变为被动的，这样就可以接收别人的链接了
    tcp_server_socket.listen(128)
    # 如果有新的客户端来链接服务器，
    # 那么就产生一个新的套接字专门为这个客户端服务
    # client_socket用来为这个客户端服务
    # tcp_server_socket就可以省下来专门等待其他新客户端的链接
    client_socket, clientAddr = tcp_server_socket.accept()
    # 接收对方发送过来的数据
    while (1):
        recv_data = client_socket.recv(1024)  # 接收1024个字节
        #print('接收到的数据为:', recv_data.decode('gbk'))
        if recv_data.decode('gbk') == 'w':
            car.Car_Run(150, 150)
        if recv_data.decode('gbk') == '-':
            time.sleep(0.07)
            car.Car_Stop()
        if recv_data.decode('gbk') == 's':
            car.Car_Back(150, 150)
            time.sleep(0.07)
            car.Car_Stop()
    client_socket.close()
#转向PID输出值   使用了ipywidgets库中的FloatSlider和HBox组件
TurnZ_PID_slider = widgets.FloatSlider(description='TurnZ_PID', min=-100, max=100.0, step=0.01, orientation='Vertical')
# 创建和显示一个垂直方向的滑动条 用于调整PID控制器中的“转向Z轴”的输出值
slider_container = widgets.HBox([TurnZ_PID_slider])
# 将滑动条在当前的单元格输出中显示出来
display(slider_container)
#bgr8转jpeg格式
import enum
import cv2


def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])
#摄像头组件显示
import cv2
import ipywidgets.widgets as widgets
import threading
import time
import numpy as np
import matplotlib.pyplot as plt
import PID
image_widget = widgets.Image(format='jpg', width=320, height=240)
#white_balance_1(image_widget)
display(image_widget)
#俯视图
image_widget_1 = widgets.Image(format='jpg', width=320, height=240)
display(image_widget_1)
#归一化图+左线（淡绿色） 图像中线（紫色）实际中线（蓝色） 右线（绿色）
image_widget_2 = widgets.Image(format='jpg', width=320, height=240)
display(image_widget_2)
image = cv2.VideoCapture(0)
image.set(3, 640)
image.set(4, 480)
image.set(5, 30)  #设置帧率
# fourcc = cv2.VideoWriter_fourcc(*"MPEG")
image.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
image.set(cv2.CAP_PROP_BRIGHTNESS, 60)  #设置亮度 -64 - 64  0.0  40
image.set(cv2.CAP_PROP_CONTRAST, 50)  #设置对比度 -64 - 64  2.0  50
image.set(cv2.CAP_PROP_EXPOSURE, 156)  #设置曝光值 1.0 - 5000  156.0 156
#ret, frame = image.read()
#image_widget.value = bgr8_to_jpeg(frame)
global Z_axis_pid
Z_axis_pid = PID.PositionalPID(0.5, 0, 1)  #1.2 0 0.1   （0.8 0.0 1.0可以跑有点震荡 0.85 0 2.0）
global prev_left
prev_left = 0
global prev_right
prev_right = 0


def Camera_display():
    global peaks_count
    global prev_left, prev_right
    t_start = time.time()
    fps = 0
    global Z_axis_pid
    tag = 0
    while 1:
        # 1、获取图像
        ret, frame = image.read()

        # 帧率显示
        fps = fps + 1
        mfps = fps / (time.time() - t_start)
        cv2.putText(frame, "FPS: " + str(int(mfps)), (80, 80), cv2.FONT_HERSHEY_SIMPLEX, 3.0, (0, 255, 255), 8)

        # 图像resize
        frame = cv2.resize(frame, (320, 240))
        # frame=white_balance_1(frame)

        # 2、透视变换 (查看俯视图)
        matSrc = np.float32([[0, 179], [320, 179], [281, 102], [43, 102]])

        matDst = np.float32([[0, 240], [320, 240], [320, 0], [0, 0]])
        matAffine = cv2.getPerspectiveTransform(matSrc, matDst)  # mat 1 src 2 dst
        dst = cv2.warpPerspective(frame, matAffine, (320, 240))
        # cv2.imshow('trans', dst)

        # 画蓝色的矩形框，采集数据的时候采集的就是当前蓝色矩形框中的数据
        # src 4->dst 4 (左下角 右下角 右上角 左上角 )
        pts = np.array([[0, 179], [320, 179], [281, 102], [43, 102]], np.int32)
        # 顶点个数：4，矩阵变成4*1*2维
        # OpenCV中需要将多边形的顶点坐标变成顶点数×1×2维的矩阵
        # 这里 reshape 的第一个参数为-1, 表示“任意”，意思是这一维的值是根据后面的维度的计算出来的
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(frame, [pts], True, (255, 0, 255), 3)  # True表示闭合，（255,0,0）是蓝色，3是线宽
        # 3、转化图像二值化(看二值化之后的黑白图像）
        # cv2.imshow('frame', frame)
        dst_gray = cv2.cvtColor(dst, cv2.COLOR_RGB2GRAY)  # 转灰度
        dst_retval, dst_binaryzation = cv2.threshold(dst_gray, 60, 255, cv2.THRESH_BINARY)  # 二值化
        # dst_binaryzation = cv2.erode(dst, None, iterations=1)  # 腐蚀化操作
        # dst = cv2.bitwise_not(dst)
        # edge = cv2.Canny(dst_binaryzation, 180, 190)
        # kernel = np.ones((6, 6), dtype=np.uint8)
        # edge = cv2.dilate(edge, kernel, 1)
        # edge = cv2.bitwise_not(edge)

        # cv2.imshow('edge', edge)

        # 当axis为0时,是压缩行,即将每一列的元素相加,将矩阵压缩为一行
        # 当axis为1时,是压缩列,即将每一行的元素相加,将矩阵压缩为一列(这里的一列是为了方便理解说的，实际上，在控制台的输出中，仍然是以一行的形式输出的)
        histogram = np.sum(dst_binaryzation[dst_binaryzation.shape[0] // 2:, :], axis=0)  # 我们这里是一维数组
        # histogram_edge = np.sum(edge[edge.shape[0] // 2:, :], axis=0)  # 我们这里是一维数组
        # midpoint = np.int(histogram.shape[0] / 2)  # 直方图垂直尺寸
        # histogram_image = np.zeros((256, 320), dtype=np.uint8)

        # 归一化直方图
        # histogram = histogram / np.max(histogram) * 256
        # histogram_edge = histogram_edge / np.max(histogram_edge) * 256

        # 在图像上绘制直方图

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
        leftx_base = np.argmin(histogram[:center_r], axis=0)
        rightx_base = np.argmin(histogram[::-1][:center_r], axis=0)  # 反转直方图取最右侧的值
        # print(np.min(histogram[:center_r], axis=0))
        # print(np.min(histogram[::-1][:center_r], axis=0))
        llne = 0
        rlne = 0
        if (leftx_base > 40):
            cv2.putText(dst_binaryzation, "left lane exists", (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        elif (np.min(histogram[:center_r], axis=0) > 255 * 100):
            cv2.putText(dst_binaryzation, "left lane dosnt exist", (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 255), 1)
            llne = 1
            leftx_base = np.argmin(histogram[:rightpoint], axis=0)

        # print(leftx_base, rightx_base)
        if (rightx_base > 40):
            # print(leftx_base, rightx_base)
            cv2.putText(dst_binaryzation, "right lane exists", (10, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255),
                        1)
        elif (np.min(histogram[::-1][:center_r], axis=0) > 255 * 100):
            cv2.putText(dst_binaryzation, "right lane dosnt exist", (10, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 255), 1)
            rlne = 1
            rightx_base = np.argmin(histogram[::-1][:rightpoint], axis=0)
        else:
            cv2.putText(dst_binaryzation, "right lane exists", (10, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255),
                        1)
        if (llne == 1 and rlne == 1):
            cv2.putText(dst_binaryzation, "no lane exists or lane lies in the graph", (10, 85),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        # for i in range(histogram_edge)

        rightx_base = 319 - rightx_base
        # print(leftx_base, rightx_base)
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
        cv2.putText(dst_binaryzation, "Bias: " + str(int(Bias)), (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0),
                    1)
        cv2.putText(dst_binaryzation, "rightx_base: " + str(int(rightx_base)), (10, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (255, 255, 0), 1)
        cv2.putText(dst_binaryzation, "leftx_base: " + str(int(leftx_base)), (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (255, 255, 0), 1)
        # print(Bias)
        Bias_L = leftx_base - center_r
        Bias_R = center_r - rightx_base

        if Bias_L > 0:  # 左车道在右边 往右转
            Bias = Bias_L
            car.Control_Car(40, -50)  # 拐弯时如果出现左侧线在中线右边>10,右拐
            cv2.putText(dst, "turn right Bias_L>0", (10, 205), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
            tag = 0
            # time.sleep(0.001)
            continue
            # car.Control_Car(40, -50)

        if Bias_R > 0:  # 右车道在左边 往左转
            Bias = Bias_R
            car.Control_Car(-50, 40)
            cv2.putText(dst, "turn left Bias_R>0", (10, 205), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
            tag = 1
            # time.sleep(0.001)
            continue
            # car.Control_Car(-50, 40)

        """ if Bias_R <= 10 and Bias_L <= 10:
            Bias = 0"""

        # 图像添加文本
        cv2.putText(dst_binaryzation, "FPS:  " + str(int(mfps)), (10, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255),
                    1)
        cv2.putText(dst_binaryzation, "Bias: " + str(int(Bias)), (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255),
                    1)

        # continue
        # 转向角PID调节
        Z_axis_pid.SystemOutput = Bias
        Z_axis_pid.SetStepSignal(0)
        Z_axis_pid.SetInertiaTime(0.5, 0.2)

        if Z_axis_pid.SystemOutput > 25:  # 20
            Z_axis_pid.SystemOutput = 25
        elif Z_axis_pid.SystemOutput < -25:
            Z_axis_pid.SystemOutput = -25

        TurnZ_PID_slider.value = int(Z_axis_pid.SystemOutput)

        if leftx_base == 0 and rightx_base == 319:
            if prev_left > prev_right:
                # car.Control_Car(0, 0)
                car.Control_Car(-50, 40)
            elif prev_left < prev_right:
                car.Control_Car(50, -50)
            # car.Control_Car(0, 0)

            prev_left = 0
            prev_right = 0

        else:
            if Bias > 10:
                # prev_left = 1
                # prev_right = 0
                if Bias > 140:
                    if tag == 1:
                        car.Control_Car(-45, 35)
                        prev_left = 0
                        prev_right = 0
                        cv2.putText(dst, "tag>0,turn left", (10, 205), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
                    else:
                        car.Control_Car(35, -45)
                        cv2.putText(dst, "tag<0 turn right", (10, 205), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
                        prev_left = 0
                        prev_right = 0
                else:
                    car.Control_Car(45 + int(Z_axis_pid.SystemOutput), 45 - int(Z_axis_pid.SystemOutput))
                    cv2.putText(dst, "PID ctrl", (10, 225), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
                # time.sleep(0.001)
                """ elif Bias < -10:  #黑线在中线的右边，小车右转   （左边速度增大，右边速度减小）
                #prev_right = 1
                #prev_left = 0
                if Bias < -140:
                    car.Control_Car(40, -50)
                    prev_left = 0
                    prev_right = 0
                else:
                    car.Control_Car(45 + int(Z_axis_pid.SystemOutput), 45 - int(Z_axis_pid.SystemOutput))
                time.sleep(0.001)"""

            else:
                car.Car_Run(45, 45)
                cv2.putText(dst, "go straight", (10, 225), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
                # car.Car_Run(0, 0)
                # time.sleep(0.001)

        if left_sum != right_sum:
            if left_sum < right_sum:
                prev_left = prev_left + 1
            elif right_sum < left_sum:
                prev_right = prev_right + 1
        image_widget.value = bgr8_to_jpeg(frame)
        image_widget_1.value = bgr8_to_jpeg(dst)
        image_widget_2.value = bgr8_to_jpeg(dst_binaryzation)


#自动驾驶进程启动
thread3 = threading.Thread(target=Camera_display)
thread3.setDaemon(True)
thread3.start()
#结束自动驾驶进程
car.Car_Stop()
stop_thread(thread3)
image.release()