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

from numpy import disp
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
	
	'''
	for i in range(10):
		d1=detect_distance_sensor_1(sim)
		d2=detect_distance_sensor_2(sim)
		print(i)
		print(d1)
		print(d2)
		time.sleep(5)
	
	for i in range(100):
		v1=sim.setJointTargetVelocity(lh,0)
		v2=sim.setJointTargetVelocity(rh,0.5)
		print(i)
		print(v1,v2)
	'''
	'''
	#Left turn
	v1=sim.setJointTargetVelocity(lh,-0.5)
	v2=sim.setJointTargetVelocity(rh,0.5)
	time.sleep(4.2)	
	v1=sim.setJointTargetVelocity(lh,0)
	v2=sim.setJointTargetVelocity(rh,0)
	'''
	'''
	#Right turn
	v1=sim.setJointTargetVelocity(lh,0.5)
	v2=sim.setJointTargetVelocity(rh,-0.5)
	time.sleep(4.2)	
	v1=sim.setJointTargetVelocity(lh,0)
	v2=sim.setJointTargetVelocity(rh,0)
	'''
	t=time.time()
	while(1):
		dl=detect_distance_sensor_1(sim)
		dr=detect_distance_sensor_2(sim)
		if (dl[0] and dr[0]):
			v1=sim.setJointTargetVelocity(lh,0.5)
			v2=sim.setJointTargetVelocity(rh,0.5)
			print("s")
		elif (dl[0]==0 and dr[0]):
			print("l")
			v1=sim.setJointTargetVelocity(lh,0.5)
			v2=sim.setJointTargetVelocity(rh,0.5)
			time.sleep(4.4)
			v1=sim.setJointTargetVelocity(lh,-0.5)
			v2=sim.setJointTargetVelocity(rh,0.5)
			time.sleep(4.6)
			v1=sim.setJointTargetVelocity(lh,0.5)
			v2=sim.setJointTargetVelocity(rh,0.5)
			time.sleep(4.4)
		elif (dl[0] and dr[0]==0):
			print("r")
			v1=sim.setJointTargetVelocity(lh,0.5)
			v2=sim.setJointTargetVelocity(rh,0.5)
			time.sleep(4.4)
			v1=sim.setJointTargetVelocity(lh,0.5)
			v2=sim.setJointTargetVelocity(rh,-0.5)
			time.sleep(4.6)
			v1=sim.setJointTargetVelocity(lh,0.5)
			v2=sim.setJointTargetVelocity(rh,0.5)
			time.sleep(4.4)
		
			



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
	sensorHandle=sim.getObject("/distance_sensor_1")
	#x=sim.handleProximitySensor(sensorHandle)
	distance=sim.readProximitySensor(sensorHandle)
	#distance=distance[1]
	##############  ADD YOUR CODE HERE  ##############




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
	#distance=distance[1]



	##################################################
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