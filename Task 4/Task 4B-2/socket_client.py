'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 3D of Pharma Bot (PB) Theme (eYRC 2022-23).
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
# Filename:			socket_server_pt1.py
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
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################





##############################################################

def setup_client(host, port):

	"""
	Purpose:
	---
	This function creates a new socket client and then tries
    to connect to a socket server.

	Input Arguments:
	---
	`host` :	[ string ]
			host name or ip address for the server

	`port` : [ string ]
			integer value specifying port name
	Returns:

	`client` : [ socket object ]
	           a new client socket object
	---

	
	Example call:
	---
	client = setup_client(host, port)
	""" 

	client = None

	##################	ADD YOUR CODE HERE	##################
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((host,port))

	##########################################################

	return client

def receive_message_via_socket(client):
	"""
	Purpose:
	---
	This function listens for a message from the specified
	socket client and returns the message when received.

	Input Arguments:
	---
	`client` :	[ socket object ]
			socket client object created by setup_client() function
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
	message = client.recv(100)
	message = str(message, 'UTF-8')

	##########################################################

	return message

def send_message_via_socket(client, message):
	"""
	Purpose:
	---
	This function sends a message over the specified socket client

	Input Arguments:
	---
	`client` :	[ socket object ]
			client socket object created by setup_client() function

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

	message=res = bytes(message, 'utf-8')
	client.sendall(message)

	##########################################################


def straight():
	time.sleep(1)
	send_message_via_socket(client,"STRAIGHT")

def left():
	time.sleep(1)
	send_message_via_socket(client,"LEFT")

def right():
	time.sleep(1)
	send_message_via_socket(client,"RIGHT")

def wait_5():
	time.sleep(1)
	send_message_via_socket(client,"WAIT_5")

def rev():
	time.sleep(1)
	send_message_via_socket(client,"REVERSE")

def scan_qr():
	time.sleep(1)
	send_message_via_socket('SCAN_QR_POS')

def pick(color,led):
	print(color,led)




######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THE MAIN SECTION #########
#########      APART FROM THE REQUIRED AREAS (host, port etc)     #########

if __name__ == "__main__":

		host = "172.20.10.5"
		port = 5050


		## Set up new socket client and connect to a socket server
		try:
			client = setup_client(host, port)

			# print(type(client))

		except socket.error as error:
			print("Error in setting up client")
			print(error)
			sys.exit()
		while(1):
			msg=receive_message_via_socket(client)
			if msg=="START":
				print("emulation started")
				while(1):
					msg=receive_message_via_socket(client)
					print(msg)
					if msg=='s':
						straight()
					elif msg=='r':
						right()
					elif msg=='l':
						left()
					elif msg=='w':
						wait_5()
					elif msg=='rev':
						rev()
					elif msg=='SCAN_QR':
						scan_qr()
					elif msg[:4]=="PICK":
						temp=msg.split('_')
						pick(temp[1],temp[2])
					elif msg=='STOP':
						break
			else:
				pass
			break	

					
		