import cv2
import numpy as np



#基于轮廓提取和透射变换————失败
def contour_to_rect(contour):#定义轮廓
    pts = contour.reshape(4, 2)#将轮廓的点重新整理成一个4x2的矩阵，即四个点，每个点两个坐标。
    print(pts)
    rect = np.zeros((4, 2), dtype = "float32")#创建一个同样大小的矩阵，用于存放矩形的四个顶点坐标。
    s = pts.sum(axis = 1)#计算每个点的坐标和。
#     print(s)
    rect[0] = pts[np.argmin(s)]#坐标和最小的点，矩形的左上角。
#     print(pts[np.argmin(s)])
    rect[2] = pts[np.argmax(s)]#坐标和最大的点，矩形的右下角。
    diff = np.diff(pts, axis = 1)#计算每个点的坐标差。
    rect[1] = pts[np.argmin(diff)]#坐标差最小的点，矩形的右上角。
    rect[3] = pts[np.argmax(diff)]#坐标差最大的点，矩形的左下角。
    return rect#轮廓转为矩形




def approximate_contour(contour):#近似轮廓形状
    peri = cv2.arcLength(contour, True)#计算周长，为真闭合
    return cv2.approxPolyDP(contour, 0.032 * peri, True)#cv2.approxPolyDP函数近似轮廓。这个函数的第二个参数是近似的精度，周长的3.2%作为精度值。

# 获取顶点坐标
def get_receipt_contour(contours):
    # 遍历所有轮廓
    for c in contours:
        # 使用approximate_contour函数来近似轮廓
        approx = approximate_contour(c)
        # 如果近似后的轮廓有四个点，我们可以假设它是收据的矩形
        if len(approx) == 4:
            return approx


def wrap_perspective(img, rect):
    # 解包矩形的四个点：左上角、右上角、右下角、左下角
    (tl, tr, br, bl) = rect
    # 计算新图像的宽度
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    # 计算新图像的高度
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    # 取宽度和高度的最大值作为最终尺寸
    maxWidth = max(int(widthA), int(widthB))
    maxHeight = max(int(heightA), int(heightB))
    # 目标点，用于将屏幕映射到“扫描”视图
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")
    # 计算透视变换矩阵
    M = cv2.getPerspectiveTransform(rect, dst)
    # 执行透视变换以获取屏幕
    return cv2.warpPerspective(img, M, (maxWidth, maxHeight))

if __name__ == "__main__":
    # 读取图像文件
    img = cv2.imread("./d91c1cd0a9c3464886c246431a302737.png")
    # 将图像转换为灰度
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 使用高斯滤波降噪
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # 使用Canny算法检测边缘
    edged = cv2.Canny(blur, 50, 150)
    # 寻找边缘的轮廓
    contours, h = cv2.findContours(edged.copy(), mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
    #cv2.imshow("Original Image", contours)
    # 对找到的轮廓按面积大小排序，并取最大的五个
    largest_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
    # 获取收据的轮廓
    receipt_contour = get_receipt_contour(largest_contours)
    # 复制原始图像
    ori_img = img.copy()
    # 在收据轮廓的每个顶点画圆
    for color in contour_to_rect(receipt_contour):
        cv2.circle(ori_img, (int(color[0]), int(color[1])), 1, (0, 0, 255), 4)
    # 对收据轮廓进行透视变换
    scanned = wrap_perspective(img.copy(), contour_to_rect(receipt_contour))


    # 使用cv2.imshow展示原始图像和处理后的图像
    cv2.imshow("Original Image", ori_img)
    cv2.imshow("Scanned Image", scanned)
    # 等待关闭窗口
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("没有找到合适的轮廓")

