#-*- coding:UTF-8 -*-
import numpy as np
import cv2

cap = cv2.VideoCapture(0)
ret = cap.set(3, 640)  # 设置帧宽
ret = cap.set(4, 480)  # 设置帧高
font = cv2.FONT_HERSHEY_SIMPLEX  # 设置字体样式
kernel = np.ones((5, 5), np.uint8)  # 卷积核

if cap.isOpened() is True:  # 检查摄像头是否正常启动
    while (True):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 转换为灰色通道
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # 转换为HSV空间

        lower_green = np.array([35, 50, 100])  # 设定绿色的阈值下限
        upper_green = np.array([77, 255, 255])  # 设定绿色的阈值上限
        #  消除噪声
        mask = cv2.inRange(hsv, lower_green, upper_green)  # 设定掩膜取值范围
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # 形态学开运算
        bila = cv2.bilateralFilter(mask, 10, 200, 200)  # 双边滤波消除噪声
        edges = cv2.Canny(opening, 50, 100)  # 边缘识别
        # 识别圆形
        circles = cv2.HoughCircles(
            edges, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=40, minRadius=10, maxRadius=500)
        if circles is not None:  # 如果识别出圆
            for circle in circles[0]:
                #  获取圆的坐标与半径
                x = int(circle[0])
                y = int(circle[1])
                r = int(circle[2])
                cv2.circle(frame, (x, y), r, (0, 0, 255), 3)  # 标记圆
                cv2.circle(frame, (x, y), 3, (255, 255, 0), -1)  # 标记圆心
                text = 'x:  ' + str(x) + ' y:  ' + str(y)
                print(text+"  r: " + str(r))
                cv2.putText(frame, text, (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA, 0)  # 显示圆心位置
        else:
            # 如果识别不出，显示圆心不存在
            cv2.putText(frame, 'x: None y: None', (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA, 0)
        cv2.imshow('frame', frame)
        cv2.imshow('mask', mask)
        cv2.imshow('edges', edges)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
else:
    print('cap is not opened!')