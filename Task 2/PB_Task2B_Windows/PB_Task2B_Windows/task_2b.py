'''
*****************************************************************************************
*
*        =================================================
*             Pharma Bot Theme (eYRC 2022-23)
*        =================================================
*                                                         
*  This script is intended for implementation of Task 2B   
*  of Pharma Bot (PB) Theme (eYRC 2022-23).
*
*  Filename:			task_2b.py
*  Created:				
*  Last Modified:		8/10/2022
*  Author:				e-Yantra Team
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
# Filename:			task_2b.py
# Functions:		control_logic, read_qr_code
# 					[ Comma separated list of functions in this file ]
# Global variables:	
# 					[ List of global variables defined in this file ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
##############################################################
import  sys
import traceback
import time
import os
import math
from zmqRemoteApi import RemoteAPIClient
import zmq
import numpy as np
import cv2
import random
from pyzbar.pyzbar import decode
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################
def findangle(img):
	def make_points(frame, line):
		height, width, _ = frame.shape
		slope, intercept = line
		y1 = height  # bottom of the frame
		y2 = int(y1 * 1 / 2)  # make points from middle of the frame down

	# bound the coordinates within the frame
		x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
		x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
		return [[x1, y1, x2, y2]]

	def average_slope_intercept(frame, line_segments):   
		lane_lines = []
		if line_segments is None:
			return lane_lines

		height, width, _ = frame.shape
		left_fit = []
		right_fit = []

		boundary = 1/3
		left_region_boundary = width * (1 - boundary)  # left lane line segment should be on left 2/3 of the screen
		right_region_boundary = width * boundary # right lane line segment should be on left 2/3 of the screen

		for line_segment in line_segments:
			for x1, y1, x2, y2 in line_segment:
				if x1 == x2:
					continue
				fit = np.polyfit((x1, x2), (y1, y2), 1)
				slope = fit[0]
				intercept = fit[1]
				if slope < 0:
					if x1 < left_region_boundary and x2 < left_region_boundary:
						left_fit.append((slope, intercept))
				else:
					if x1 > right_region_boundary and x2 > right_region_boundary:
						right_fit.append((slope, intercept))

		left_fit_average = np.average(left_fit, axis=0)
		if len(left_fit) > 0:
			lane_lines.append(make_points(frame, left_fit_average))

		right_fit_average = np.average(right_fit, axis=0)
		if len(right_fit) > 0:
			lane_lines.append(make_points(frame, right_fit_average))

		return lane_lines

	def canny(image):
		blur=cv2.GaussianBlur(image,(5,5),0)
		lower_bound = np.array([76, 76, 76])
		upper_bound = np.array([76,76,76])
		imagemask = cv2.inRange(blur, lower_bound, upper_bound)
		ret,blur = cv2.threshold(imagemask, 48, 255, cv2.THRESH_BINARY)
		canny=cv2.Canny(blur,150,200)
		return canny

	def region_of_interest(image):
		polygons=np.array([[(0,240),(0,120),(320,120),(320,240)]])
		#polygons=np.array([[(0,480),(0,400),(200,0),(440,0),(640,400),(640,480)]])
		mask=np.zeros_like(image)
		cv2.fillPoly(mask,polygons,255)
		masked_image=cv2.bitwise_and(image,mask)
		return masked_image



	
	lane_image=np.copy(img)
	lane_image=cv2.resize(lane_image,(320,240))
	canny_image=canny(lane_image)
	cropped_image=region_of_interest(canny_image)
	lines=cv2.HoughLinesP(cropped_image,1,np.pi/180,10,np.array([]),minLineLength=8,maxLineGap=4)
	lane_lines=average_slope_intercept(lane_image,lines)
	if len(lane_lines)==1:
		x1, _, x2, _ = lane_lines[0][0]
		x_offset = x2 - x1
	else:     
		_, _, left_x2, _ = lane_lines[0][0]
		_, _, right_x2, _ = lane_lines[1][0]
		mid = int(320 / 2)
		x_offset = (left_x2 + right_x2) / 2 - mid
	y_offset = int(240 / 2)
	angle_to_mid_radian = math.atan(x_offset / y_offset)  # angle (in radian) to center vertical line
	angle_to_mid_deg = int(angle_to_mid_radian * 180.0 / math.pi)  # angle (in degrees) to center vertical line
	steering_angle = angle_to_mid_deg + 90  # this is the steering angle needed by picar front wheel
	steering_angle1=180-steering_angle
	return steering_angle1

def isnode(img):
	image=np.copy(img)
	blur=cv2.GaussianBlur(image,(5,5),0)
	lower_bound = np.array([253, 204, 4])
	upper_bound = np.array([253,204,4])
	imagemask = cv2.inRange(blur, lower_bound, upper_bound)
	cnts=cv2.findContours(imagemask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	if cnts[0]:
		return 1
	else:
	    return 0 
		



    



	




##############################################################

def control_logic(sim):
	"""
	Purpose:
	---
	This function should implement the control logic for the given problem statement
	You are required to make the robot follow the line to cover all the checkpoints
	and deliver packages at the correct locations.

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	None

	Example call:
	---
	control_logic(sim)
	"""

	##############  ADD YOUR CODE HERE  ##############
	visionSensorHandle = sim.getObject('/vision_sensor')
	lh=sim.getObject("/left_joint")
	rh=sim.getObject("/right_joint")
	v1=sim.setJointTargetVelocity(lh,0)
	v2=sim.setJointTargetVelocity(rh,0)
	count=0
	while(1):
		img, resX, resY = sim.getVisionSensorCharImage(visionSensorHandle)
		img = np.frombuffer(img, dtype=np.uint8).reshape(resY, resX, 3)
		img = cv2.flip(img, 0)
		angle=90
		cv2.imshow('image', img)
		cv2.waitKey(1)
		try:
			angle=findangle(img)
		except:
			pass  
		#print(angle)
		if isnode(img):
			count+=1
			print(count)
			
			#time.sleep(3)
			if(count==5 or count==9 or count==13):

                #to make visible
				arena_dummy_handle = sim.getObject("/Arena_dummy") 
				childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")
				sim.callScriptFunction("activate_qr_code", childscript_handle, "checkpoint "+chr(64+count))

				v1=sim.setJointTargetVelocity(lh,1)
				v2=sim.setJointTargetVelocity(rh,1)
				time.sleep(0.7)
				v1=sim.setJointTargetVelocity(lh,0)
				v2=sim.setJointTargetVelocity(rh,0)
				time.sleep(5)
				print("reading qr")
				message=read_qr_code(sim)
				

				#v1=sim.setJointTargetVelocity(lh,0)
				#v2=sim.setJointTargetVelocity(rh,0)
				#message=read_qr_code(sim)

                #to make invisible
				arena_dummy_handle = sim.getObject("/Arena_dummy") 
				childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")
				sim.callScriptFunction("deactivate_qr_code", childscript_handle, "checkpoint "+chr(64+count))


				if(message=='Orange Cone'):
					arena_dummy_handle = sim.getObject("/Arena_dummy") 
					childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")
					sim.callScriptFunction("deliver_package", childscript_handle, "package_1", "checkpoint "+chr(64+count))
				elif(message=='Blue Cylinder'):
					arena_dummy_handle = sim.getObject("/Arena_dummy") 
					childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")
					sim.callScriptFunction("deliver_package", childscript_handle, "package_2", "checkpoint "+chr(64+count))
				elif(message=='Pink Cuboid'):
					arena_dummy_handle = sim.getObject("/Arena_dummy") 
					childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")
					sim.callScriptFunction("deliver_package", childscript_handle, "package_3", "checkpoint "+chr(64+count))	
				v1=sim.setJointTargetVelocity(lh,1)
				v2=sim.setJointTargetVelocity(rh,1)
				while (isnode(img)):
					img, resX, resY = sim.getVisionSensorCharImage(visionSensorHandle)
					img = np.frombuffer(img, dtype=np.uint8).reshape(resY, resX, 3)
					img = cv2.flip(img, 0)
				time.sleep(0.25)
				
			else:
				print("no rq")
				v1=sim.setJointTargetVelocity(lh,1)
				v2=sim.setJointTargetVelocity(rh,1)
				while (isnode(img)):
					img, resX, resY = sim.getVisionSensorCharImage(visionSensorHandle)
					img = np.frombuffer(img, dtype=np.uint8).reshape(resY, resX, 3)
					img = cv2.flip(img, 0)
				time.sleep(0.25)
					
				if count==1 or count==3 or count==7 or count==11 or count==15: 
					v1=sim.setJointTargetVelocity(lh,-1)
					v2=sim.setJointTargetVelocity(rh,1)
					time.sleep(1.8)
				elif count==2 or count==4 or count==6 or count==8 or count==10 or count==12 or count==14 or count==16:
					v1=sim.setJointTargetVelocity(lh,1)
					v2=sim.setJointTargetVelocity(rh,-1)
					time.sleep(1.8)
				elif count==5 or count==9 or count==10 or count==13:
					v1=sim.setJointTargetVelocity(lh,1)
					v2=sim.setJointTargetVelocity(rh,1)
					time.sleep(1.8)
				elif count==17:
					break		

		elif(angle==90):
			v1=sim.setJointTargetVelocity(lh,3)
			v2=sim.setJointTargetVelocity(rh,3)
		elif(angle<90):
			v1=sim.setJointTargetVelocity(lh,0.5)
			v2=sim.setJointTargetVelocity(rh,0) 
		elif(angle>90):
			v1=sim.setJointTargetVelocity(lh,0)
			v2=sim.setJointTargetVelocity(rh,0.5)

		cv2.imshow('image', img)
		cv2.waitKey(1)
	
    

	##################################################





def read_qr_code(sim):
	"""
	Purpose:
	---
	This function detects the QR code present in the camera's field of view and
	returns the message encoded into it.

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
	try:
		visionSensorHandle = sim.getObject('/vision_sensor')
		img, resX, resY = sim.getVisionSensorCharImage(visionSensorHandle)
		img = np.frombuffer(img, dtype=np.uint8).reshape(resY, resX, 3)
		img = cv2.flip(img, 0)
		cv2.imshow("qr",img)
		cv2.waitKey(10)
		a=decode(img)
		print(a)
		qr_message=a.data
	except:
		qr_message = None
		
	##################################################
	return qr_message


######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THE MAIN CODE BELOW #########

if __name__ == "__main__":
	client = RemoteAPIClient()
	sim = client.getObject('sim')	

	try:

		## Start the simulation using ZeroMQ RemoteAPI
		try:
			return_code = sim.startSimulation()
			if sim.getSimulationState() != sim.simulation_stopped:
				print('\nSimulation started correctly in CoppeliaSim.')
			else:
				print('\nSimulation could not be started correctly in CoppeliaSim.')
				sys.exit()

		except Exception:
			print('\n[ERROR] Simulation could not be started !!')
			traceback.print_exc(file=sys.stdout)
			sys.exit()

		## Runs the robot navigation logic written by participants
		try:
			control_logic(sim)
			time.sleep(5)
			
			
			

		except Exception:
			print('\n[ERROR] Your control_logic function throwed an Exception, kindly debug your code!')
			print('Stop the CoppeliaSim simulation manually if required.\n')
			traceback.print_exc(file=sys.stdout)
			print()
			sys.exit()

		
		## Stop the simulation using ZeroMQ RemoteAPI
		try:
			return_code = sim.stopSimulation()
			time.sleep(0.5)
			if sim.getSimulationState() == sim.simulation_stopped:
				print('\nSimulation stopped correctly in CoppeliaSim.')
			else:
				print('\nSimulation could not be stopped correctly in CoppeliaSim.')
				sys.exit()

		except Exception:
			print('\n[ERROR] Simulation could not be stopped !!')
			traceback.print_exc(file=sys.stdout)
			sys.exit()

	except KeyboardInterrupt:
		## Stop the simulation using ZeroMQ RemoteAPI
		return_code = sim.stopSimulation()
		time.sleep(0.5)
		if sim.getSimulationState() == sim.simulation_stopped:
			print('\nSimulation interrupted by user in CoppeliaSim.')
		else:
			print('\nSimulation could not be interrupted. Stop the simulation manually .')
			sys.exit()