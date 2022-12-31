import cv2 
import numpy as np
from  numpy import interp
task_1b = __import__('task_1b')
img=cv2.imread(r"C:\Users\Vasumathi T\Downloads\Eyantra\Task 3\Task_3C_Resources\aruco_1.png")

a,b =task_1b.detect_ArUco_details(img)
try:
    img=task_1b.mark_ArUco_image(img,a,b)
except:
    pass
cv2.imshow("o",img)
cv2.waitKey(0)
