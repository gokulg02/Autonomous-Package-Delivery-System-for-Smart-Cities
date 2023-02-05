'''
*****************************************************************************************
*
*        		     ===============================================
*           		       Pharma Bot (PB) Theme (eYRC 2022-23)
*        		     ===============================================
*
*  This script contains all the past implemented functions of Pharma Bot (PB) Theme 
*  (eYRC 2022-23).
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			PB_theme_functions.py
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
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################
def get_coord(node):
    x=node[0]
    x=ord(x)-65
    x=-0.89+0.356*x
    y=node[1]
    y=int(y)-1
    y=0.89-0.356*y
    l=[x,y]
    return l


##############################################################


################## ADD SOCKET COMMUNICATION ##################
####################### FUNCTIONS HERE #######################
"""
Add functions written in Task 3D for setting up a Socket
Communication Server in this section
"""

def setup_server(host, port):

	"""
	Purpose:
	---
	This function creates a new socket server and then binds it 
	to a host and port specified by user.

	Input Arguments:
	---
	`host` :	[ string ]
			host name or ip address for the server

	`port` : [ string ]
			integer value specifying port name
	Returns:

	`server` : [ socket object ]
	---

	
	Example call:
	---
	server = setupServer(host, port)
	""" 

	server = None

	##################	ADD YOUR CODE HERE	##################
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Socket created.")
	server.bind((host, port))
	print("Socket bind complete.")
	

	##########################################################

	return server

def setup_connection(server):
	"""
	Purpose:
	---
	This function listens for an incoming socket client and
	accepts the connection request

	Input Arguments:
	---
	`server` :	[ socket object ]
			socket object created by setupServer() function
	Returns:
	---
	`server` : [ socket object ]
	
	Example call:
	---
	connection = setupConnection(server)
	"""
	connection = None
	address = None

	##################	ADD YOUR CODE HERE	##################
	server.listen(3)
	connection, address = server.accept()

	##########################################################

	return connection, address

def receive_message_via_socket(connection):
	"""
	Purpose:
	---
	This function listens for a message from the specified
	socket connection and returns the message when received.

	Input Arguments:
	---
	`connection` :	[ connection object ]
			connection object created by setupConnection() function
	Returns:
	---
	`message` : [ string ]
			message received through socket communication
	
	Example call:
	---
	message = receive_message_via_socket(connection)
	"""

	message = None

	##################	ADD YOUR CODE HERE	##################
	message = connection.recv(50)
	message = str(message, 'UTF-8')

	##########################################################

	return message

def send_message_via_socket(connection, message):
	"""
	Purpose:
	---
	This function sends a message over the specified socket connection

	Input Arguments:
	---
	`connection` :	[ connection object ]
			connection object created by setupConnection() function

	`message` : [ string ]
			message sent through socket communication

	Returns:
	---
	None
	
	Example call:
	---
	send_message_via_socket(connection, message)
	"""

	##################	ADD YOUR CODE HERE	##################
	message= bytes(message, 'utf-8')
	connection.sendall(message)
	##########################################################

##############################################################
##############################################################

######################### ADD TASK 2B ########################
####################### FUNCTIONS HERE #######################
"""
Add functions written in Task 2B for reading QR code from
CoppeliaSim arena in this section
"""

def read_qr_code(sim):
	"""
	Purpose:
	---
	This function detects the QR code present in the CoppeliaSim vision sensor's 
	field of view and returns the message encoded into it.

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	`qr_message`   :    [ string ]
		QR message retrieved from reading QR code

	Example call:
	---
	control_logic(sim)
	"""
	qr_message = None
	
	##############  ADD YOUR CODE HERE  ##############
	visionSensorHandle = sim.getObject('/vision_sensor')
	img, resX, resY = sim.getVisionSensorCharImage(visionSensorHandle)
	img = np.frombuffer(img, dtype=np.uint8).reshape(resY, resX, 3)
	img = cv2.flip(img, 0)

	a=decode(img)
	for x in a:
		qr_message=x.data
		qr_message=str(qr_message)[2:-1]


	##################################################

	return qr_message

##############################################################
##############################################################

############### ADD ARENA PARAMETER DETECTION ################
####################### FUNCTIONS HERE #######################
"""
Add functions written in Task 1A and 3A for detecting arena parameters
from configuration image in this section
"""

def detect_all_nodes(image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list of
	nodes in which traffic signals, start_node and end_node are present in the image

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`traffic_signals, start_node, end_node` : [ list ], str, str
			list containing nodes in which traffic signals are present, start and end node too
	
	Example call:
	---
	traffic_signals, start_node, end_node = detect_all_nodes(maze_image)
	"""    
	traffic_signals = []
	start_node = ""
	end_node = ""

    ##############	ADD YOUR CODE HERE	##############
	for i in range(100,601,100):
		for j in range(100,601,100):
			if ((image[i,j]==np.array([0,0,255])).all()):
				x=int(j/100)
				x=chr(x+64)
				y=str(int(i/100))
				s=x+y
				traffic_signals.append(s)
			elif (((image[i,j]==np.array([0,255,0])).all())):
				x=int(j/100)
				x=chr(x+64)
				y=str(int(i/100))
				s=x+y
				start_node=s
			elif (((image[i,j]==np.array([189,43,105])).all())):
				x=int(j/100)
				x=chr(x+64)
				y=str(int(i/100))
				s=x+y
				end_node=s
	

    ##################################################

	return traffic_signals, start_node, end_node

def detect_horizontal_roads_under_construction(image):	
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list
	containing the missing horizontal links

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`horizontal_roads_under_construction` : [ list ]
			list containing missing horizontal links
	
	Example call:
	---
	horizontal_roads_under_construction = detect_horizontal_roads_under_construction(maze_image)
	"""    
	horizontal_roads_under_construction = []

	##############	ADD YOUR CODE HERE	##############
	for i in range(100,601,100):
		for j in range(150,551,100):
			if ((image[i,j]==np.array([255,255,255])).all()):
				x1=int((j-50)/100)
				x1=chr(x1+64)
				x2=int((j+50)/100)
				x2=chr(x2+64)
				y=str(int(i/100))
				s=x1+y+'-'+x2+y
				horizontal_roads_under_construction.append(s)
	

	##################################################
	
	return horizontal_roads_under_construction	

def detect_vertical_roads_under_construction(image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list
	containing the missing vertical links

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`vertical_roads_under_construction` : [ list ]
			list containing missing vertical links
	
	Example call:
	---
	vertical_roads_under_construction = detect_vertical_roads_under_construction(maze_image)
	"""    
	vertical_roads_under_construction = []

	##############	ADD YOUR CODE HERE	##############
	for i in range(150,551,100):
		for j in range(100,601,100):
			if((image[i,j]==np.array([255,255,255])).all()):
				x=int(j/100)
				x=chr(x+64)
				y1=str(int((i-50)/100))
				y2=str(int((i+50)/100))
				s=x+y1+'-'+x+y2
				vertical_roads_under_construction.append(s)
	
	
	##################################################
	
	return vertical_roads_under_construction

def detect_medicine_packages(image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a nested list of
	details of the medicine packages placed in different shops

	** Please note that the shop packages should be sorted in the ASCENDING order of shop numbers 
	   as well as in the alphabetical order of colors.
	   For example, the list should first have the packages of shop_1 listed. 
	   For the shop_1 packages, the packages should be sorted in the alphabetical order of color ie Green, Orange, Pink and Skyblue.

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`medicine_packages` : [ list ]
			nested list containing details of the medicine packages present.
			Each element of this list will contain 
			- Shop number as Shop_n
			- Color of the package as a string
			- Shape of the package as a string
			- Centroid co-ordinates of the package
	Example call:
	---
	medicine_packages = detect_medicine_packages(maze_image)
	"""    
	medicine_packages = {}

	##############	ADD YOUR CODE HERE	##############
	frame=image[0:200,0:700]
	lower_sb = np.array([255, 255, 0])
	uppper_sb = np.array([255, 255, 0])
	sky_blue= cv2.inRange(frame, lower_sb, uppper_sb)
	lower_pink = np.array([180, 0, 255])
	uppper_pink = np.array([180, 0, 255])
	pink= cv2.inRange(frame, lower_pink, uppper_pink)
	lower_orange = np.array([0, 127, 255])
	uppper_orange = np.array([0,127, 255])
	orange= cv2.inRange(frame, lower_orange, uppper_orange)
	lower_green = np.array([0, 255, 0])
	uppper_green = np.array([0, 255, 0])
	green= cv2.inRange(frame, lower_green, uppper_green)
	mask={'Green':green,'Orange':orange,'Pink':pink,'Skyblue':sky_blue}
	for i in mask:
		cnts = cv2.findContours(mask[i], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		for c in cnts[0]:
			c = cv2.approxPolyDP(c, 0.01 * cv2.arcLength(c, True), True)
			M = cv2.moments(c)
			cX = int(M["m10"] / M["m00"])
			cY = int(M["m01"] / M["m00"])
			x=str(cX)
			x=x[0]
			if len(c)==3:
				medicine_packages.setdefault(int(x), []).append(i+'_cone')
			elif len(c)==4:
				medicine_packages.setdefault(int(x), []).append(i+'_cube')
			else:
				medicine_packages.setdefault(int(x), []).append(i+'_cylinder')   
	

	##################################################

	return medicine_packages

def detect_arena_parameters(maze_image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a dictionary
	containing the details of the different arena parameters in that image

	The arena parameters are of four categories:
	i) traffic_signals : list of nodes having a traffic signal
	ii) start_node : Start node which is mark in light green
	iii) end_node : End node which is mark in Purple
	iv) paths : list containing paths

	These four categories constitute the four keys of the dictionary

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`arena_parameters` : { dictionary }
			dictionary containing details of the arena parameters
	
	Example call:
	---
	arena_parameters = detect_arena_parameters(maze_image)

	Eg. arena_parameters={"traffic_signals":[], 
	                      "start_node": "E4", 
	                      "end_node":"A3", 
	                      "paths": {}}
	"""    
	arena_parameters = {}

    ##############	ADD YOUR CODE HERE	##############
	arena_parameters['traffic_signals'],arena_parameters['start_node'],arena_parameters['end_node']=detect_all_nodes(maze_image)
	arena_parameters['horizontal_roads_under_construction']=detect_horizontal_roads_under_construction(maze_image)
	arena_parameters['vertical_roads_under_construction']=detect_vertical_roads_under_construction(maze_image)
	arena_parameters['medicine_packages']=detect_medicine_packages(maze_image)

    ##################################################

	return arena_parameters

##############################################################
##############################################################

####################### ADD ARENA SETUP ######################
####################### FUNCTIONS HERE #######################
"""
Add functions written in Task 4A for setting up the CoppeliaSim
Arena according to the configuration image in this section
"""

def place_packages(medicine_package_details, sim, all_models):
    """
	Purpose:
	---
	This function takes details (colour, shape and shop) of the packages present in 
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    them on the virtual arena. The packages should be inserted only into the 
    designated areas in each shop as mentioned in the Task document.

    Functions from Regular API References should be used to set the position of the 
    packages.

	Input Arguments:
	---
	`medicine_package_details` :	[ list ]
                                nested list containing details of the medicine packages present.
                                Each element of this list will contain 
                                - Shop number as Shop_n
                                - Color of the package as a string
                                - Shape of the package as a string
                                - Centroid co-ordinates of the package			

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	
	Example call:
	---
	all_models = place_packages(medicine_package_details, sim, all_models)
	"""
    models_directory = os.getcwd()
    packages_models_directory = os.path.join(models_directory, "package_models")
    arena = sim.getObject('/Arena')    

####################### ADD YOUR CODE HERE #########################
    keys=medicine_package_details.keys()
    y=0.684
    for i in keys:
        l=medicine_package_details[i]
        x=-0.89+0.356*(i-1)+0.0445
        for j in l:
            dir=j+".ttm"
            dir=os.path.join(packages_models_directory,dir)
            objectHandle=sim.loadModel(dir)
            sim.setObjectParent(objectHandle,arena,True)
            p=[x,y,0.002]
            sim.setObjectPosition(objectHandle,arena,p)
            all_models.append(objectHandle)
            sim.setObjectAlias(objectHandle,j)
            x=x+0.089




####################################################################

    return all_models

def place_traffic_signals(traffic_signals, sim, all_models):
    """
	Purpose:
	---
	This function takes position of the traffic signals present in 
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    them on the virtual arena. The signal should be inserted at a particular node.

    Functions from Regular API References should be used to set the position of the 
    signals.

	Input Arguments:
	---
	`traffic_signals` : [ list ]
			list containing nodes in which traffic signals are present

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	None
	
	Example call:
	---
	all_models = place_traffic_signals(traffic_signals, sim, all_models)
	"""
    models_directory = os.getcwd()
    traffic_sig_model = os.path.join(models_directory, "signals", "traffic_signal.ttm" )
    arena = sim.getObject('/Arena')

####################### ADD YOUR CODE HERE #########################
    for i in traffic_signals:
        objectHandle=sim.loadModel(traffic_sig_model)
        sim.setObjectParent(objectHandle,arena,True)
        p=get_coord(i)
        p.append(0.15588)
        sim.setObjectPosition(objectHandle,arena,p)
        all_models.append(objectHandle)
        sim.setObjectAlias(objectHandle,'Signal_'+i)


####################################################################

    return all_models

def place_start_end_nodes(start_node, end_node, sim, all_models):
    """
	Purpose:
	---
	This function takes position of start and end nodes present in 
    the arena and places them on the virtual arena. 
    The models should be inserted at a particular node.

    Functions from Regular API References should be used to set the position of the 
    start and end nodes.

	Input Arguments:
	---
	`start_node` : [ string ]
    `end_node` : [ string ]
					

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	---
	None
	
	Example call:
	---
	all_models = place_start_end_nodes(start_node, end_node, sim, all_models)
	"""
    models_directory = os.getcwd()
    start_node_model = os.path.join(models_directory, "signals", "start_node.ttm" )
    end_node_model = os.path.join(models_directory, "signals", "end_node.ttm" )
    arena = sim.getObject('/Arena')   

####################### ADD YOUR CODE HERE #########################
    objectHandle=sim.loadModel(start_node_model)
    sim.setObjectParent(objectHandle,arena,True)
    p=get_coord(start_node)
    p.append(0.15588)
    sim.setObjectPosition(objectHandle,arena,p)
    all_models.append(objectHandle)
    sim.setObjectAlias(objectHandle,'Start_Node')


    objectHandle=sim.loadModel(end_node_model)
    sim.setObjectParent(objectHandle,arena,True)
    p=get_coord(end_node)
    p.append(0.15588)
    sim.setObjectPosition(objectHandle,arena,p)
    all_models.append(objectHandle)
    sim.setObjectAlias(objectHandle,'End_Node')


####################################################################

    return all_models

def place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models):
    """
	Purpose:
	---
	This function takes the list of missing horizontal roads present in 
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    horizontal barricades on virtual arena. The barricade should be inserted 
    between two nodes as shown in Task document.

    Functions from Regular API References should be used to set the position of the 
    horizontal barricades.

	Input Arguments:
	---
	`horizontal_roads_under_construction` : [ list ]
			list containing missing horizontal links		

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	---
	None
	
	Example call:
	---
	all_models = place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models)
	"""
    models_directory = os.getcwd()
    horiz_barricade_model = os.path.join(models_directory, "barricades", "horizontal_barricade.ttm" )
    arena = sim.getObject('/Arena')  

####################### ADD YOUR CODE HERE #########################
    for i in horizontal_roads_under_construction:
        objectHandle=sim.loadModel(horiz_barricade_model)
        sim.setObjectParent(objectHandle,arena,True)
        p1=get_coord(i[:2])
        p2=get_coord(i[-2:])
        p=[]
        p.append((p1[0]+p2[0])/2)
        p.append((p1[1]+p2[1])/2)
        p.append(0.002)
        sim.setObjectPosition(objectHandle,arena,p)
        sim.setObjectAlias(objectHandle,'Horizontal_missing_road_'+i[:2]+'_'+i[-2:])
        all_models.append(objectHandle)


####################################################################

    return all_models


def place_vertical_barricade(vertical_roads_under_construction, sim, all_models):
    """
	Purpose:
	---
	This function takes the list of missing vertical roads present in 
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    vertical barricades on virtual arena. The barricade should be inserted 
    between two nodes as shown in Task document.

    Functions from Regular API References should be used to set the position of the 
    vertical barricades.

	Input Arguments:
	---
	`vertical_roads_under_construction` : [ list ]
			list containing missing vertical links		

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	---
	None
	
	Example call:
	---
	all_models = place_vertical_barricade(vertical_roads_under_construction, sim, all_models)
	"""
    models_directory = os.getcwd()
    vert_barricade_model = os.path.join(models_directory, "barricades", "vertical_barricade.ttm" )
    arena = sim.getObject('/Arena')

####################### ADD YOUR CODE HERE #########################
    for i in vertical_roads_under_construction:
        objectHandle=sim.loadModel(vert_barricade_model)
        sim.setObjectParent(objectHandle,arena,True)
        p1=get_coord(i[:2])
        p2=get_coord(i[-2:])
        p=[]
        p.append((p1[0]+p2[0])/2)
        p.append((p1[1]+p2[1])/2)
        p.append(0.002)
        sim.setObjectPosition(objectHandle,arena,p)
        sim.setObjectAlias(objectHandle,'Vertical_missing_road_'+i[:2]+'_'+i[-2:])
        all_models.append(objectHandle)


####################################################################

    return all_models

##############################################################
##############################################################