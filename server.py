#import YB_Pcb_Car  # 导入亚博智能专用的底层库文件

#car = YB_Pcb_Car.YB_Pcb_Car()
#car.Ctrl_Servo(4, 80)
#car.Ctrl_Servo(2, 110)
import socket
# import YB_Pcb_Car as car
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
    print('接收到的数据为:', recv_data.decode('gbk'))
    if recv_data.decode('gbk') == 'w':
        time.sleep(0.07)
        print("w")
 #       car.Car_Run(150, 150)
    if recv_data.decode('gbk') == 'm':
        time.sleep(0.07)
        print("wawd")
        #car.Car_Stop()
    if recv_data.decode('gbk') == 's':
 #       car.Car_Back(150, 150)
        time.sleep(0.07)
 #       car.Car_Stop()

client_socket.close()