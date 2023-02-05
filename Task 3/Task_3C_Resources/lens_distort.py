import cv2
import numpy as np
'''
mtx=np.array([[882.6062793 ,   0.        , 949.46246768],
       [  0.        , 885.49079501, 570.56205705],
       [  0.        ,   0.        ,   1.        ]])
dist=np.array([[-0.29895604,  0.03340572, -0.00749475, -0.00030157,  0.10321605]])
'''
w=1920
h=1080

def dist_correction(img):
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    mapx,mapy=cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
    dst = cv2.remap(img,mapx,mapy,cv2.INTER_LINEAR)
    return dst

if __name__=="__main__":
    vid = cv2.VideoCapture(1)
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        
    while(1):
        ret, img = vid.read()
        cv2.imshow("o",img)
        cv2.waitKey(1)
        try:
            img=dist_correction(img)
            cv2.imshow("c",img)
            cv2.waitKey(1)
        except:
            pass
