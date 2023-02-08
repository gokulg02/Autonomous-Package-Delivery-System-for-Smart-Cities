'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 4B of Pharma Bot (PB) Theme (eYRC 2022-23).
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
# Filename:			task_4b.py
# Functions:		
# 					[ Comma separated list of functions in this file ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv)                    ##
##############################################################
import socket
import time
import os, sys
from zmqRemoteApi import RemoteAPIClient
import traceback
import zmq
import numpy as np
import cv2
from pyzbar.pyzbar import decode
import json
import random
import numpy
import _thread as thread
###############################################################

A=None
B=None
C=None
D=None

## Import PB_theme_functions code
try:
	pb_theme = __import__('PB_theme_functions')
	task_1b = __import__('task_1b')

except ImportError:
	print('\n[ERROR] PB_theme_functions.py file is not present in the current directory.')
	print('Your current directory is: ', os.getcwd())
	print('Make sure PB_theme_functions.py is present in this current directory.\n')
	sys.exit()
	
except Exception as e:
	print('Your PB_theme_functions.py throwed an Exception, kindly debug your code!\n')
	traceback.print_exc(file=sys.stdout)
	sys.exit()


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
        pass
    try:
        B=[b[2][1][0],b[2][1][1]]
    except:
        pass
    try:
        C=[b[1][0][0],b[1][0][1]]
    except:
        pass
    try:
        D=[b[4][3][0],b[4][3][1]]
    except:
        pass
    #print(A,B,C,D)
    AD = numpy.sqrt(((A[0] - D[0]) ** 2) + ((A[1] - D[1]) ** 2))
    BC = numpy.sqrt(((B[0] - C[0]) ** 2) + ((B[1] - C[1]) ** 2))
    maxw = max(int(AD), int(BC))
    AB = numpy.sqrt(((A[0] - B[0]) ** 2) + ((A[1] - B[1]) ** 2))
    CD = numpy.sqrt(((C[0] - D[0]) ** 2) + ((C[1] - D[1]) ** 2))
    maxh = max(int(AB), int(CD))
    i = numpy.float32([A,B,C,D])
    o = numpy.float32([[0, 0], [0, maxh - 1], [maxw - 1, maxh - 1],[maxw - 1, 0]])
    M = cv2.getPerspectiveTransform(i,o)
    out = cv2.warpPerspective(image,M,(maxw, maxh),flags=cv2.INTER_LINEAR)
    out = cv2.resize(out, [out.shape[1], out.shape[1]])
    
    cv2.imshow("p",out)
    cv2.waitKey(1)
    #print("perspective")
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
    #print("5 detected")
    scene_parameters.append(a[5][0][0]/img.shape[0])
    scene_parameters.append(a[5][0][1]/img.shape[1])
    scene_parameters.append(a[5][1])
    #print(scene_parameters)
######################################################################################

    return scene_parameters


def set_values(scene_parameters,sim):
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
    aruco_handle = sim.getObject('/bot')
#################################  ADD YOUR CODE HERE  ###############################
    #pos=sim.getObjectPosition(aruco_handle,sim.handle_parent)
    x=numpy.interp(scene_parameters[0],[0,1],[0.89,-0.89])
    y=numpy.interp(scene_parameters[1],[0,1],[-0.89,0.89])
    y-=0.05

    a=sim.setObjectPosition(aruco_handle,sim.handle_parent,[x,y,0.029])
    #ang=sim.getObjectOrientation(aruco_handle,sim.handle_parent)
    ang=scene_parameters[2]
    if ang<0:
        ang=numpy.interp(ang,[-180,0],[0,180])
    else:
        ang=numpy.interp(ang,[0,180],[-180,0])
    rad=numpy.radians(ang)
    b=sim.setObjectOrientation(aruco_handle,sim.handle_parent,[0,-1.57,0])
    print("Emulated")
######################################################################################
    #print(pos)
    #print(ang)
    return None

def emulation_thread(sim):
    global A,B,C,D
    vid = cv2.VideoCapture(r"C:\Users\Vasumathi T\Downloads\wetransfer_track_2023-02-06_1445\Final.mp4")
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    while(1):
        ret, img = vid.read()
        try:
            set_values(transform_values(img),sim)
        except:
            pass
        img = cv2.resize(img, [640, 360])
        #cv2.imshow("g",img)
        #cv2.waitKey(1)



def task_4b_implementation(sim):
	"""
	Purpose:
	---
	This function contains the implementation logic for task 4B 

	Input Arguments:
	---
    `sim` : [ object ]
            ZeroMQ RemoteAPI object

	You are free to define additional input arguments for this function.

	Returns:
	---
	You are free to define output parameters for this function.
	
	Example call:
	---
	task_4b_implementation(sim)
	"""

	##################	ADD YOUR CODE HERE	##################
	global A,B,C,D
	#print("emu stsrted")
	vid = cv2.VideoCapture(r"C:\Users\Vasumathi T\Downloads\wetransfer_track_2023-02-06_1445\Final.mp4")
	vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
	vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
	width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
	height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
	while(A==None or B==None or C==None or D==None):
		ret, img = vid.read()
		a,b =task_1b.detect_ArUco_details(img)
		try:
			A=[b[3][2][0],b[3][2][1]]
		except:
			pass
		try:
			B=[b[2][1][0],b[2][1][1]]
		except:
			pass
		try:
			C=[b[1][0][0],b[1][0][1]]
		except:
			pass
		try:
			D=[b[4][3][0],b[4][3][1]]
		except:
			pass 
		print(A,B,C,D)

	#pb_theme.send_message_via_socket(connection_2, "START_RUN")
	thread.start_new_thread(emulation_thread,(sim,))
	while(1):
		print(time.time())
		time.sleep(5)
	while(1):
		ret, img = vid.read()
		try:
			set_values(transform_values(img),sim)
		except:
			pass
		img = cv2.resize(img, [640, 360])
		#cv2.imshow("g",img)
		#cv2.waitKey(1)

	##########################################################


if __name__ == "__main__":
	
	host = ''
	port = 5050
	coppelia_client = RemoteAPIClient()
	sim = coppelia_client.getObject('sim')

	
	## Set up new socket server
	try:
		server = pb_theme.setup_server(host, port)
		print("Socket Server successfully created")

		# print(type(server))

	except socket.error as error:
		print("Error in setting up server")
		print(error)
		sys.exit()

	'''
	## Set up new connection with a socket client (PB_task3d_socket.exe)
	try:
		print("\nPlease run PB_socket.exe program to connect to PB_socket client")
		connection_1, address_1 = pb_theme.setup_connection(server)
		print("Connected to: " + address_1[0] + ":" + str(address_1[1]))

	except KeyboardInterrupt:
		sys.exit()
	'''
	# ## Set up new connection with Raspberry Pi
	try:
		print("\nPlease connect to Raspberry pi client")
		connection_2, address_2 = pb_theme.setup_connection(server)
		print("Connected to: " + address_2[0] + ":" + str(address_2[1]))

	except KeyboardInterrupt:
		sys.exit()

	'''
	## Send setup message to PB_socket
	pb_theme.send_message_via_socket(connection_1, "SETUP")

	message = pb_theme.receive_message_via_socket(connection_1)
	## Loop infinitely until SETUP_DONE message is received
	while True:
		if message == "SETUP_DONE":
			break
		else:
			print("Cannot proceed further until SETUP command is received")
			message = pb_theme.receive_message_via_socket(connection_1)

	try:
		# obtain required arena parameters
		config_img = cv2.imread("config_image.png")
		detected_arena_parameters = pb_theme.detect_arena_parameters(config_img)			
		medicine_package_details = detected_arena_parameters["medicine_packages"]
		traffic_signals = detected_arena_parameters['traffic_signals']
		start_node = detected_arena_parameters['start_node']
		end_node = detected_arena_parameters['end_node']
		horizontal_roads_under_construction = detected_arena_parameters['horizontal_roads_under_construction']
		vertical_roads_under_construction = detected_arena_parameters['vertical_roads_under_construction']

		# print("Medicine Packages: ", medicine_package_details)
		# print("Traffic Signals: ", traffic_signals)
		# print("Start Node: ", start_node)
		# print("End Node: ", end_node)
		# print("Horizontal Roads under Construction: ", horizontal_roads_under_construction)
		# print("Vertical Roads under Construction: ", vertical_roads_under_construction)
		# print("\n\n")

	except Exception as e:
		print('Your task_1a.py throwed an Exception, kindly debug your code!\n')
		traceback.print_exc(file=sys.stdout)
		sys.exit()
	
	try:

		## Connect to CoppeliaSim arena
		coppelia_client = RemoteAPIClient()
		sim = coppelia_client.getObject('sim')

		## Define all models
		all_models = []

		## Setting up coppeliasim scene
		print("[1] Setting up the scene in CoppeliaSim")
		all_models = pb_theme.place_packages(medicine_package_details, sim, all_models)
		all_models = pb_theme.place_traffic_signals(traffic_signals, sim, all_models)
		all_models = pb_theme.place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models)
		all_models = pb_theme.place_vertical_barricade(vertical_roads_under_construction, sim, all_models)
		all_models = pb_theme.place_start_end_nodes(start_node, end_node, sim, all_models)
		print("[2] Completed setting up the scene in CoppeliaSim")
		print("[3] Checking arena configuration in CoppeliaSim")

	except Exception as e:
		print('Your task_4a.py throwed an Exception, kindly debug your code!\n')
		traceback.print_exc(file=sys.stdout)
		sys.exit()

	pb_theme.send_message_via_socket(connection_1, "CHECK_ARENA")

	## Check if arena setup is ok or not
	message = pb_theme.receive_message_via_socket(connection_1)
	while True:
	
		if message == "ARENA_SETUP_OK":
			print("[4] Arena was properly setup in CoppeliaSim")
			break
		elif message == "ARENA_SETUP_NOT_OK":
			print("[4] Arena was not properly setup in CoppeliaSim")
			connection_1.close()
			# connection_2.close()
			server.close()
			sys.exit()
		else:
			pass

	## Send Start Simulation Command to PB_Socket
	pb_theme.send_message_via_socket(connection_1, "SIMULATION_START")
	
	## Check if simulation started correctly
	message = pb_theme.receive_message_via_socket(connection_1)
	while True:
		# message = pb_theme.receive_message_via_socket(connection_1)
		
		if message == "SIMULATION_STARTED_CORRECTLY":
			print("[5] Simulation was started in CoppeliaSim")
			break

		if message == "SIMULATION_NOT_STARTED_CORRECTLY":
			print("[5] Simulation was not started in CoppeliaSim")
			sys.exit()

	## Send Start Command to Raspberry Pi to start execution
	pb_theme.send_message_via_socket(connection_2, "START")
	'''

	task_4b_implementation(sim)
	'''
	## Send Stop Simulation Command to PB_Socket
	pb_theme.send_message_via_socket(connection_1, "SIMULATION_STOP")

	## Check if simulation started correctly
	message = pb_theme.receive_message_via_socket(connection_1)
	while True:
		# message = pb_theme.receive_message_via_socket(connection_1)

		if message == "SIMULATION_STOPPED_CORRECTLY":
			print("[6] Simulation was stopped in CoppeliaSim")
			break

		if message == "SIMULATION_NOT_STOPPED_CORRECTLY":
			print("[6] Simulation was not stopped in CoppeliaSim")
			sys.exit()
	'''