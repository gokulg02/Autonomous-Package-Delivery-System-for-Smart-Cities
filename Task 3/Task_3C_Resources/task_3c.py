'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 3C of Pharma Bot (PB) Theme (eYRC 2022-23).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_3c.py
# Functions:		[ perspective_transform, transform_values, set_values ]
# 					


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the five available  ##
## modules for this task                                    ##
##############################################################
import cv2 
import numpy
from zmqRemoteApi import RemoteAPIClient
import zmq
import requests
##############################################################

#################################  ADD UTILITY FUNCTIONS HERE  #######################


#####################################################################################

def perspective_transform(image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns the image after 
    applying perspective transform on it. Using this function, you should
    crop out the arena from the full frame you are receiving from the 
    overhead camera feed.

    HINT:
    Use the ArUco markers placed on four corner points of the arena in order
    to crop out the required portion of the image.

    Input Arguments:
    ---
    `image` :	[ numpy array ]
            numpy array of image returned by cv2 library 

    Returns:
    ---
    `warped_image` : [ numpy array ]
            return cropped arena image as a numpy array
    
    Example call:
    ---
    warped_image = perspective_transform(image)
    """   
    
#################################  ADD YOUR CODE HERE  ###############################
    a,b =task_1b.detect_ArUco_details(image)
    try:
        A=[b[3][2][0],b[3][2][1]]
    except:
        A=None
    try:
        B=[b[2][1][0],b[2][1][1]]
    except:
        B=None
    try:
        C=[b[1][0][0],b[1][0][1]]
    except:
        C=None
    try:
        D=[b[4][3][0],b[4][3][1]]
    except:
        D=None
    #print(A,B,C,D)
    if (A==None and B!=None and C!=None and D!=None):
        A=[B[1],D[0]]
    AD = numpy.sqrt(((A[0] - D[0]) ** 2) + ((A[1] - D[1]) ** 2))
    BC = numpy.sqrt(((B[0] - C[0]) ** 2) + ((B[1] - C[1]) ** 2))
    maxw = max(int(AD), int(BC))
    AB = numpy.sqrt(((A[0] - B[0]) ** 2) + ((A[1] - B[1]) ** 2))
    CD = numpy.sqrt(((C[0] - D[0]) ** 2) + ((C[1] - D[1]) ** 2))
    maxh = max(int(AB), int(CD))
    i = numpy.float32([A,B,C,D])
    o = numpy.float32([[0, 0], [0, maxh - 1], [maxw - 1, maxh - 1],[maxw - 1, 0]])
    M = cv2.getPerspectiveTransform(i,o)
    out = cv2.warpPerspective(img,M,(maxw, maxh),flags=cv2.INTER_LINEAR)
    cv2.imshow("O",out)
    cv2.waitKey(1)
    print("perspective")
######################################################################################

    return out

def transform_values(image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns the 
    position and orientation of the ArUco marker (with id 5), in the 
    CoppeliaSim scene.

    Input Arguments:
    ---
    `image` :	[ numpy array ]
            numpy array of image returned by camera

    Returns:
    ---
    `scene_parameters` : [ list ]
            a list containing the position and orientation of ArUco 5
            scene_parameters = [c_x, c_y, c_angle] where
            c_x is the transformed x co-ordinate [float]
            c_y is the transformed y co-ordinate [float]
            c_angle is the transformed angle [angle]
    
    HINT:
        Initially the image should be cropped using perspective transform 
        and then values of ArUco (5) should be transformed to CoppeliaSim
        scale.
    
    Example call:
    ---
    scene_parameters = transform_values(image)
    """   
    scene_parameters = []
#################################  ADD YOUR CODE HERE  ###############################
    img=perspective_transform(image)
    a,_ =task_1b.detect_ArUco_details(img)
    print("5 detected")
    scene_parameters.append(a[5][0][0]/img.shape[0])
    scene_parameters.append(a[5][0][1]/img.shape[1])
    scene_parameters.append(a[5][1])
    #print(scene_parameters)
######################################################################################

    return scene_parameters


def set_values(scene_parameters):
    """
    Purpose:
    ---
    This function takes the scene_parameters, i.e. the transformed values for
    position and orientation of the ArUco marker, and sets the position and 
    orientation in the CoppeliaSim scene.

    Input Arguments:
    ---
    `scene_parameters` :	[ list ]
            list of co-ordinates and orientation obtained from transform_values()
            function

    Returns:
    ---
    None

    HINT:
        Refer Regular API References of CoppeliaSim to find out functions that can
        set the position and orientation of an object.
    
    Example call:
    ---
    set_values(scene_parameters)
    """   
    aruco_handle = sim.getObject('/aruco_5')
#################################  ADD YOUR CODE HERE  ###############################
    #pos=sim.getObjectPosition(aruco_handle,sim.handle_parent)
    x=numpy.interp(scene_parameters[0],[0,1],[0.955,-0.955])
    y=numpy.interp(scene_parameters[1],[0,1],[-0.955,0.955])
    a=sim.setObjectPosition(aruco_handle,sim.handle_parent,[x,y,0.029])
    #ang=sim.getObjectOrientation(aruco_handle,sim.handle_parent)
    ang=scene_parameters[2]
    if ang<0:
        ang=numpy.interp(ang,[-180,0],[0,180])
    else:
        ang=numpy.interp(ang,[0,180],[-180,0])
    rad=numpy.radians(ang)
    b=sim.setObjectOrientation(aruco_handle,sim.handle_parent,[0,0,rad])
    print("Emulated")
######################################################################################
    #print(pos)
    #print(ang)
    return None

if __name__ == "__main__":
    url="http://192.168.152.71:8080/shot.jpg"
    client = RemoteAPIClient()
    sim = client.getObject('sim')
    task_1b = __import__('task_1b')
    vid = cv2.VideoCapture(r"C:\Users\Vasumathi T\Downloads\20230102_113749.mp4")

    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    while(1):
        ret, img = vid.read()
        img=cv2.resize(img, (800, 500))
        #img=cv2.imread(r"C:\Users\Vasumathi T\Downloads\Eyantra\Task 3\Task_3C_Resources\aruco_1.png")
        cv2.imshow("g",img)
        cv2.waitKey(1)
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        try:
            set_values(transform_values(img))
        except:
            pass

#################################  ADD YOUR CODE HERE  ################################

#######################################################################################



    
