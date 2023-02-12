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
c_n=None
c_d='n'
p1=['s','r','l','r','l','r','w','s','l']
d=['n','e','s','w']
p2=['rev','s','r']
p3=['l']
p4=['s','l','l']
bot_pack=dict()
bot_pack[1]=[]
bot_pack[3]=[]
bot_pack[2]=[]
drop={"Orange_cone": "E5", "Pink_cone": "E4"}
medicine_package_details=[]
shop_no={'F':5,'E':4,'D':3,'C':2,'B':1}

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

def current_node_update(c_n,i):
	global c_d
	if (i=='s'):
		if(c_d=='w'):
			c_n=(chr(ord(c_n[0])-1))+c_n[1]
		elif(c_d=='e'):
			c_n=(chr(ord(c_n[0])+1))+c_n[1]
		elif(c_d=='s'):
			c_n=c_n[0]+(chr(ord(c_n[1])+1))
		elif(c_d=='n'):
			c_n=c_n[0]+(chr(ord(c_n[1])-1))
	elif(i=='r'):
		if(c_d=='w'):
			c_n=c_n[0]+(chr(ord(c_n[1])-1))
			c_d='n'
		elif(c_d=='e'):
			c_n=c_n[0]+(chr(ord(c_n[1])+1))
			c_d='s'
		elif(c_d=='s'):
			c_n=(chr(ord(c_n[0])-1))+c_n[1]
			c_d='w'
		elif(c_d=='n'):
			c_n=(chr(ord(c_n[0])+1))+c_n[1]
			c_d='e'
	elif(i=='l'):
		if(c_d=='w'):
			c_n=c_n[0]+(chr(ord(c_n[1])+1))
			c_d='s'
		elif(c_d=='e'):
			c_n=c_n[0]+(chr(ord(c_n[1])-1))
			c_d='n'
		elif(c_d=='s'):
			c_n=(chr(ord(c_n[0])+1))+c_n[1]
			c_d='e'
		elif(c_d=='n'):
			c_n=(chr(ord(c_n[0])-1))+c_n[1]
			c_d='w'
	elif(i=='rev'):
		if(c_d=='w'):
			c_n=(chr(ord(c_n[0])+1))+c_n[1]
			c_d='e'
		elif(c_d=='e'):
			c_n=(chr(ord(c_n[0])-1))+c_n[1]
			c_d='w'
		elif(c_d=='s'):
			c_n=c_n[0]+(chr(ord(c_n[1])-1))
			c_d='n'
		elif(c_d=='n'):
			c_n=c_n[0]+(chr(ord(c_n[1])+1))
			c_d='s'
	return c_n

		

def perspective_transform(image):

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

    aruco_handle = sim.getObject('/Alpha_bot')
#################################  ADD YOUR CODE HERE  ###############################
    #pos=sim.getObjectPosition(aruco_handle,sim.handle_parent)
    x=numpy.interp(scene_parameters[0],[0,1],[0.89,-0.89])
    y=numpy.interp(scene_parameters[1],[0,1],[-0.89,0.89])
    y-=0.05

    a=sim.setObjectPosition(aruco_handle,sim.handle_parent,[x,y,0.029])
    #ang=sim.getObjectOrientation(aruco_handle,sim.handle_parent)
    ang=scene_parameters[2]
    l=[1.57,0,1.57]
    if ang>-45 and ang<45 :
        l=[1.57,0,1.57]
    elif ang>45 and ang<135:
        l=[0,1.57,-3.14]
    elif (ang>135 and ang<180) or (ang<-135 and ang>-180):
        l=[1.57,1.57,-1.57]
    elif (ang>-135 and ang<-45):
        l=[0,-1.57,0]
    b=sim.setObjectOrientation(aruco_handle,sim.handle_parent,l)

	#print("Emulated")
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


def pickup(node,connection_2,sim):
	global medicine_package_details,shop_no,bot_pack
	packages=medicine_package_details[int(shop_no[node[0]])]
	
	if (packages!= [] and bot_pack[1]==[]):
		bot_pack[1]=[packages[0],drop[packages[0]]]
		temp=packages[0].split('_')
		temp.append(drop[packages[0]])
		print("PICKED UP: "+temp[0]+"," +temp[1]+","+ temp[2])
		handle='/'+packages[0]
		a=sim.setObjectPosition(sim.getObject(handle),sim.getObject('/Alpha_bot'),[0.03,0,0.04])
		sim.setObjectParent(sim.getObject(handle),sim.getObject('/Alpha_bot'),True)
		i="PICK_"+temp[0]+"_"+'1'
		pb_theme.send_message_via_socket(connection_2,i)
		packages.remove(packages[0])

	if (packages!= [] and bot_pack[2]==[]):
		temp=packages[0].split('_')
		bot_pack[2]=[packages[0],drop[packages[0]]]
		temp.append(drop[packages[0]])
		handle='/'+packages[0]
		a=sim.setObjectPosition(sim.getObject('/'+packages[0]),sim.getObject('/Alpha_bot'),[0.03,0,-0.01])
		sim.setObjectParent(sim.getObject(handle),sim.getObject('/Alpha_bot'),True)
		print("PICKED UP: "+temp[0]+"," +temp[1]+","+ temp[2])
		i="PICK_"+temp[0]+"_"+'1'
		pb_theme.send_message_via_socket(connection_2,i)
		packages.remove(packages[0])

	if (packages!= [] and bot_pack[3]==[]):
		temp=packages[0].split('_')
		bot_pack[3]=[packages[0],drop[packages[0]]]
		temp.append(drop[packages[0]])
		handle='/'+packages[0]
		a=sim.setObjectPosition(sim.getObject('/'+packages[0]),sim.getObject('/Alpha_bot'),[0.03,0,-0.05])
		sim.setObjectParent(sim.getObject(handle),sim.getObject('/Alpha_bot'),True)
		print("PICKED UP: "+temp[0]+"," +temp[1]+","+ temp[2])
		i="PICK_"+temp[0]+"_"+'1'
		pb_theme.send_message_via_socket(connection_2,i)
		packages.remove(packages[0])



def deliver():
	global c_n,bot_pack,c_d
	pos=sim.getObjectPosition(sim.getObject('/Alpha_bot'),sim.handle_parent)
	print(pos)
	if (bot_pack[1]!=[] and c_n==bot_pack[1][1]):
		pack=bot_pack[1][0]
		sim.setObjectPosition(sim.getObject('/'+pack),sim.handle_parent,[pos[0]+0.1,pos[1]+0.1,0.029])
		sim.setObjectParent(sim.getObject('/'+pack),sim.getObject('/Arena'),True)
		print(sim.getObjectPosition(sim.getObject('/'+pack),sim.handle_parent))
		bot_pack[1]=[]

	if (bot_pack[2]!=[] and c_n==bot_pack[2][1]):
		pack=bot_pack[2][0]
		sim.setObjectPosition(sim.getObject('/'+pack),sim.handle_parent,[pos[0]+0.1,pos[1]+0.1,pos[2]])
		sim.setObjectParent(sim.getObject('/'+pack),sim.getObject('/Arena'),True)
		print(sim.getObjectPosition(sim.getObject('/'+pack),sim.handle_parent))
		bot_pack[2]=[]
	
	if (bot_pack[3]!=[] and c_n==bot_pack[3][1]):
		pack=bot_pack[3][0]
		sim.setObjectPosition(sim.getObject('/'+pack),sim.handle_parent,[pos[0]+0.1,pos[1]+0.1,pos[2]])
		sim.setObjectParent(sim.getObject('/'+pack),sim.getObject('/Arena'),True)
		bot_pack[3]=[]



		


def task_4b_implementation(sim,detected_arena_parameters):
	##################	ADD YOUR CODE HERE	##################
	global A,B,C,D,c_n,c_d
	c_n=detected_arena_parameters['start_node']
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
		#print(A,B,C,D)
	
	thread.start_new_thread(emulation_thread,(sim,))
	pb_theme.send_message_via_socket(connection_2, "START")
	for i in p1:
		pb_theme.send_message_via_socket(connection_2,i)
		msg = pb_theme.receive_message_via_socket(connection_2)
		c_n=current_node_update(c_n,i)
		if (msg=="WAIT_5"):
			print("WAIT_5")
		else:
			print("ARRIVED AT NODE "+c_n)
	
	#package pickup
	pickup(c_n,connection_2,sim)

	for i in p2:
		pb_theme.send_message_via_socket(connection_2,i)
		msg = pb_theme.receive_message_via_socket(connection_2)
		c_n=current_node_update(c_n,i)
		if (msg=="WAIT_5"):
			print("WAIT_5")
		else:
			print("ARRIVED AT NODE "+c_n)
	#package 1 delivery
	deliver()
	for i in p3:
		pb_theme.send_message_via_socket(connection_2,i)
		msg = pb_theme.receive_message_via_socket(connection_2)
		c_n=current_node_update(c_n,i)
		if (msg=="WAIT_5"):
			print("WAIT_5")
		else:
			print("ARRIVED AT NODE "+c_n)
	#package 2 delivery
	deliver()
	for i in p4:
		pb_theme.send_message_via_socket(connection_2,i)
		msg = pb_theme.receive_message_via_socket(connection_2)
		c_n=current_node_update(c_n,i)
		if (msg=="WAIT_5"):
			print("WAIT_5")
		else:
			print("ARRIVED AT NODE "+c_n)
	pb_theme.send_message_via_socket(connection_2,'STOP')
	exit()
	'''
	while(1):
		ret, img = vid.read()
		try:
			set_values(transform_values(img),sim)
		except:
			pass
		img = cv2.resize(img, [640, 360])
		#cv2.imshow("g",img)
		#cv2.waitKey(1)
	'''
	##########################################################


if __name__ == "__main__":
	
	host = ''
	port = 5050
	coppelia_client = RemoteAPIClient()
	sim = coppelia_client.getObject('sim')
	print("234")
	
	## Set up new socket server
	try:
		server = pb_theme.setup_server(host, port)
		print("Socket Server successfully created")

		# print(type(server))

	except socket.error as error:
		print("Error in setting up server")
		print(error)
		sys.exit()

	
	## Set up new connection with a socket client (PB_task3d_socket.exe)
	try:
		print("\nPlease run PB_socket.exe program to connect to PB_socket client")
		connection_1, address_1 = pb_theme.setup_connection(server)
		print("Connected to: " + address_1[0] + ":" + str(address_1[1]))

	except KeyboardInterrupt:
		sys.exit()
	
	# ## Set up new connection with Raspberry Pi
	try:
		print("\nPlease connect to Raspberry pi client")
		connection_2, address_2 = pb_theme.setup_connection(server)
		print("Connected to: " + address_2[0] + ":" + str(address_2[1]))

	except KeyboardInterrupt:
		sys.exit()

	
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

		
		print("Medicine Packages: ", medicine_package_details)
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
	print(message)
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
	

	task_4b_implementation(sim,detected_arena_parameters)
	
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
	