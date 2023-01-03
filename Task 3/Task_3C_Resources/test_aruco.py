import cv2 
import numpy as np
from  numpy import interp
task_1b = __import__('task_1b')
vid = cv2.VideoCapture(r"C:\Users\Vasumathi T\Downloads\20230102_113749.mp4")
while(1):
    ret, img = vid.read()
    img=cv2.resize(img, (800, 500))
    #a,b =task_1b.detect_ArUco_details(img)
    try:
        a,b =task_1b.detect_ArUco_details(img)
        img=task_1b.mark_ArUco_image(img,a,b)
    except:
        pass
    cv2.imshow("o",img)
    cv2.waitKey(1)
