'''
*****************************************************************************************
*
*        =================================================
*             Pharma Bot Theme (eYRC 2022-23)
*        =================================================
*                                                         
*  This script is intended for implementation of Task 2A   
*  of Pharma Bot (PB) Theme (eYRC 2022-23).
*
*  Filename:			task_2a.py
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
# Filename:			task_2a.py
# Functions:		control_logic, detect_distance_sensor_1, detect_distance_sensor_2
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
##############################################################

def control_logic(sim):
	"""
	Purpose:
	---
	This function should implement the control logic for the given problem statement
	You are required to actuate the rotary joints of the robot in this function, such that
	it traverses the points in given order

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
	lh=sim.getObject("/left_joint")
	rh=sim.getObject("/right_joint")
	v1=sim.setJointTargetVelocity(lh,0)
	v2=sim.setJointTargetVelocity(rh,0)
	t=time.time()
	time.sleep(0.1)
	f=2.75+1+1
	while(1):
		dl=detect_distance_sensor_1(sim)
		dr=detect_distance_sensor_2(sim)
		rr=detect_distance_sensor_3(sim)
		#print("l:  ",dl)
		#print("r:  ",dr)	
		#print(dr[4][2])	
		if ((dl[0] and dr[0] and rr[0]) and dl[1]<=0.25 and dr[1]<=0.25 and rr[1]<=0.25 ):
			return 0
		elif (dl[0]==0 and dr[0]):
			#print("s")
			v1=sim.setJointTargetVelocity(lh,f)
			v2=sim.setJointTargetVelocity(rh,f)
			if(dr[1]>0.17531350255012512 or rr[1]<0.17531350255012512):
				v1=sim.setJointTargetVelocity(lh,f+0.16*f)
				v2=sim.setJointTargetVelocity(rh,f)
			if(dr[1]<0.17531350255012512 or rr[1]>0.17531350255012512):
				v1=sim.setJointTargetVelocity(lh,f)
				v2=sim.setJointTargetVelocity(rh,f+0.16*f)	
		elif (dl[0] and dl[1]<=0.18102723360061646+0.12 and dr[0]):
			#print("l")
			v1=sim.setJointTargetVelocity(lh,-2)
			v2=sim.setJointTargetVelocity(rh,2)
			#time.sleep(0.5)
			dr=detect_distance_sensor_2(sim)
			while(dr[4][2]>-0.899):
				#print(dr[4][2])
				dr=detect_distance_sensor_2(sim)
			
			'''
			for i in range(30):
				time.sleep(0.2)
				dr=detect_distance_sensor_2(sim)
				print(dr)				
			'''
		elif (dl[0] and dl[1]<=0.18102723360061646+0.12 and rr[0]):
			#print("r")
			#print(dl[1])
			v1=sim.setJointTargetVelocity(lh,2)
			v2=sim.setJointTargetVelocity(rh,-2)
			#time.sleep(0.5)
			rr=detect_distance_sensor_3(sim)
			while(rr[4][2]>-0.899):
				#print(rr[4][2])
				rr=detect_distance_sensor_3(sim)
			
		else:
			v1=sim.setJointTargetVelocity(lh,f)
			v2=sim.setJointTargetVelocity(rh,f)
			if(dr[1]>0.17531350255012512 or rr[1]<0.17531350255012512):
				v1=sim.setJointTargetVelocity(lh,f+0.16*f)
				v2=sim.setJointTargetVelocity(rh,f)
			if(dr[1]<0.17531350255012512 or rr[1]>0.17531350255012512):
				v1=sim.setJointTargetVelocity(lh,f)
				v2=sim.setJointTargetVelocity(rh,f+0.16*f)			



	##################################################

def detect_distance_sensor_1(sim):
	"""
	Purpose:
	---
	Returns the distance of obstacle detected by proximity sensor named 'distance_sensor_1'

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	distance  :  [ float ]
	    distance of obstacle from sensor

	Example call:
	---
	distance_1 = detect_distance_sensor_1(sim)
	"""
	distance = None
	##############  ADD YOUR CODE HERE  ##############
	sensorHandle=sim.getObject("/distance_sensor_1")
	distance=sim.readProximitySensor(sensorHandle)



	##################################################
	return distance

def detect_distance_sensor_2(sim):
	"""
	Purpose:
	---
	Returns the distance of obstacle detected by proximity sensor named 'distance_sensor_2'

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	distance  :  [ float ]
	    distance of obstacle from sensor

	Example call:
	---
	distance_2 = detect_distance_sensor_2(sim)
	"""
	distance = None
	##############  ADD YOUR CODE HERE  ##############
	sensorHandle=sim.getObject("/distance_sensor_2")
	distance=sim.readProximitySensor(sensorHandle)



	##################################################
	return distance
	

def detect_distance_sensor_3(sim):
	distance = None
	##############  ADD YOUR CODE HERE  ##############
	sensorHandle=sim.getObject("/distance_sensor_3")
	distance=sim.readProximitySensor(sensorHandle)

	return distance 




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