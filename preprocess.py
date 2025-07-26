"""
This code implements image tilt correction based on Hough line detection.
"""
import cv2 as cv
from scipy.stats import *

# 倾斜校正
def correct_skew(image):
    # cv.imshow("original",image)
    img1 = image.copy()
    img2 = image.copy()
    img3 = image.copy()
    # canny边缘检测
    gray = cv.cvtColor(img1,cv.COLOR_BGR2GRAY)
    mg_blur = cv.GaussianBlur(gray, (1, 1), 0)
    edges = cv.Canny(mg_blur,50,150,apertureSize=3)
    # cv.imshow("edges",edges)
    # 霍夫曼直线检测
    lines = cv.HoughLines(edges,1,np.pi/180,200)
    ks = []
    flag1 = 0
    if lines is None:
        return image
    elif not len(lines):
        return image
    for line in lines:
        rho,theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*a)
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*a)
        cv.line(img2,(x1,y1),(x2,y2),(0,0,255),1)
        if x1 - x2 == 0:
            continue
        else:
            k = (y2-y1)/(x2-x1)
            ks.append(k)
            if k > 0 :
                flag1 = flag1 + 1
            elif k < 0:
                flag1 = flag1 - 1
    ks_array = np.round(ks,5)
    mode_k = mode(ks_array,keepdims=True)
    # 图像旋转
    rows, cols = img3.shape[:2]
    angle = np.degrees(np.arctan(mode_k[0]))
    if abs(angle) >= 45:
        angle = 0
    M = cv.getRotationMatrix2D((cols/2, rows/2), float(angle), 1.0)
    result = cv.warpAffine(img3, M, (cols, rows))
    return result
