'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 1A of Pharma Bot (PB) Theme (eYRC 2022-23).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:		    2503
# Author List:	    Naveen,Gokul,Jashwin,vinisha
# Filename:			task_1a.py
# Functions:		detect_traffic_signals, detect_horizontal_roads_under_construction, detect_vertical_roads_under_construction,
#					detect_medicine_packages, detect_arena_parameters
# 					[ Comma separated list of functions in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv)                    ##
##############################################################
import cv2
import numpy as np
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################





##############################################################

def detect_traffic_signals(maze_image):

	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list of
	nodes in which traffic signals are present in the image

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`traffic_signals` : [ list ]
			list containing nodes in which traffic signals are present
	
	Example call:
	---
	traffic_signals = detect_traffic_signals(maze_image)
	"""    
	traffic_signals = []

	##############	ADD YOUR CODE HERE	##############
	for i in range(100,601,100):
		for j in range(100,601,100):
			if ((maze_image[i,j]==np.array([0,0,255])).all()):
				x=int(j/100)
				x=chr(x+64)
				y=str(int(i/100))
				s=x+y
				traffic_signals.append(s)
	

	##################################################
	
	return traffic_signals
	

def detect_horizontal_roads_under_construction(maze_image):
	
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
			if ((maze_image[i,j]==np.array([0,0,0])).all()):
				x1=int((j-50)/100)
				x1=chr(x1+64)
				x2=int((j+50)/100)
				x2=chr(x2+64)
				y=str(int(i/100))
				s=x1+y+'-'+x2+y
				horizontal_roads_under_construction.append(s)
				
	##################################################
	
	return horizontal_roads_under_construction	

def detect_vertical_roads_under_construction(maze_image):

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
	for i in range(150,651,100):
		for j in range(100,751,100):
			b,g,r=maze_image[i,j]
			if(b==255 and g==255 and r==255):
				y1=i-50
				y1=str(y1)
				y1=y1[0]
				y2=i+50
				y2=str(y2)
				y2=y2[0]
				x=j
				x=str(x)
				x=int(x[0])+64
				x=chr(x)
				vertical_roads_under_construction .append(x+y1+'-'+x+y2)
	vertical_roads_under_construction .sort()
	##################################################
	
	return vertical_roads_under_construction


def detect_medicine_packages(maze_image):

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
	medicine_packages_present = []

	##############	ADD YOUR CODE HERE	##############
	frame=maze_image[0:200,0:800]
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
				medicine_packages_present.append(['Shop_'+x,i,'Triangle',[cX,cY]])
			elif len(c)==4:
				medicine_packages_present.append(['Shop_'+x,i,'Square',[cX,cY]])
			else:
				medicine_packages_present.append(['Shop_'+x,i,'Circle',[cX,cY]])    
	medicine_packages_present.sort()
	##################################################

	return medicine_packages_present

def detect_start_node(maze_img):

	start=None

	
	return start

def detect_arena_parameters(maze_image):

	"""
	Purpose:
	---
	This function takes the image as an argument and returns a dictionary
	containing the details of the different arena parameters in that image

	The arena parameters are of four categories:
	i) traffic_signals : list of nodes having a traffic signal
	ii) horizontal_roads_under_construction : list of missing horizontal links
	iii) vertical_roads_under_construction : list of missing vertical links
	iv) medicine_packages : list containing details of medicine packages

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
	"""    
	arena_parameters = {}

	##############	ADD YOUR CODE HERE	##############
	arena_parameters['traffic_signals']=detect_traffic_signals(maze_image)
	arena_parameters['horizontal_roads_under_construction']=detect_horizontal_roads_under_construction(maze_image)
	arena_parameters['vertical_roads_under_construction']=detect_vertical_roads_under_construction(maze_image)
	arena_parameters['medicine_packages']=detect_medicine_packages(maze_image)
	##################################################
	
	return arena_parameters


######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS FUNCTION #########	

if __name__ == "__main__":

    # path directory of images in test_images folder
	img_dir_path = "public_test_images/"

    # path to 'maze_0.png' image file
	file_num = 0
	img_file_path = img_dir_path + 'maze_' + str(file_num) + '.png'
	
	# read image using opencv
	maze_image = cv2.imread(img_file_path)
	
	print('\n============================================')
	print('\nFor maze_' + str(file_num) + '.png')

	# detect and print the arena parameters from the image
	arena_parameters = detect_arena_parameters(maze_image)

	print("Arena Prameters: " , arena_parameters)

	# display the maze image
	cv2.imshow("image", maze_image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	choice = input('\nDo you want to run your script on all test images ? => "y" or "n": ')
	
	if choice == 'y':

		for file_num in range(1, 15):
			
			# path to maze image file
			img_file_path = img_dir_path + 'maze_' + str(file_num) + '.png'
			
			# read image using opencv
			maze_image = cv2.imread(img_file_path)
	
			print('\n============================================')
			print('\nFor maze_' + str(file_num) + '.png')
			
			# detect and print the arena parameters from the image
			arena_parameters = detect_arena_parameters(maze_image)

			print("Arena Parameter: ", arena_parameters)
				
			# display the test image
			cv2.imshow("image", maze_image)
			cv2.waitKey(2000)
			cv2.destroyAllWindows()