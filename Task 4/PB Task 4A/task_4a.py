'''
*****************************************************************************************
*
*        =================================================
*             Pharma Bot Theme (eYRC 2022-23)
*        =================================================
*
*  This script is intended for implementation of Task 4A
*  of Pharma Bot (PB) Theme (eYRC 2022-23).
*
*  Filename:			task_4a.py
*  Created:
*  Last Modified:		02/01/2023
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
# Filename:			task_4a.py
# Functions:		[ Comma separated list of functions in this file ]
# 					
####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
##############################################################
import numpy as np
import cv2
from zmqRemoteApi import RemoteAPIClient
import zmq
import os
import time
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
    '''
    medicine_packages': [['Shop_1', 'Green', 'Square', [130, 130]], ['Shop_1', 'Orange', 'Square', [130, 170]], ['Shop_1', 'Pink', 'Square', [170, 130]], ['Shop_1', 'Skyblue', 'Square', [170, 170]], ['Shop_2', 'Green', 'Triangle', [270, 130]], ['Shop_2', 'Orange', 'Triangle', [270, 170]], ['Shop_6', 'Green', 'Circle', [630, 170]], ['Shop_6', 'Pink', 'Circle', [670, 170]], ['Shop_6', 'Skyblue', 'Circle', [670, 130]]]
    
    '''

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

if __name__ == "__main__":
    client = RemoteAPIClient()
    sim = client.getObject('sim')

    # path directory of images in test_images folder
    img_dir = os.getcwd() + "\\test_imgs\\"

    i = 0
    config_img = cv2.imread(img_dir + 'maze_' + str(i) + '.png')

    print('\n============================================')
    print('\nFor maze_0.png')

    # object handles of each model that gets imported to the scene can be stored in this list
    # at the end of each test image, all the models will be removed    
    all_models = []

    # import task_1a.py. Make sure that task_1a.py is in same folder as task_4a.py
    task_1 = __import__('task_1a')
    detected_arena_parameters = task_1.detect_arena_parameters(config_img)

    # obtain required arena parameters
    medicine_package_details = detected_arena_parameters["medicine_packages"]
    traffic_signals = detected_arena_parameters['traffic_signals']
    start_node = detected_arena_parameters['start_node']
    end_node = detected_arena_parameters['end_node']
    horizontal_roads_under_construction = detected_arena_parameters['horizontal_roads_under_construction']
    vertical_roads_under_construction = detected_arena_parameters['vertical_roads_under_construction'] 

    print("[1] Setting up the scene in CoppeliaSim")
    all_models = place_packages(medicine_package_details, sim, all_models)
    all_models = place_traffic_signals(traffic_signals, sim, all_models)
    all_models = place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models)
    all_models = place_vertical_barricade(vertical_roads_under_construction, sim, all_models)
    all_models = place_start_end_nodes(start_node, end_node, sim, all_models)
    print("[2] Completed setting up the scene in CoppeliaSim")

    # wait for 10 seconds and then remove models
    time.sleep(10)
    print("[3] Removing models for maze_0.png")

    for i in all_models:
        sim.removeModel(i)

   
    choice = input('\nDo you want to run your script on all test images ? => "y" or "n": ')
    
    if choice == 'y':
        for i in range(1,5):

            print('\n============================================')
            print('\nFor maze_' + str(i) +'.png')
            config_img = cv2.imread(img_dir + 'maze_' + str(i) + '.png')

            # object handles of each model that gets imported to the scene can be stored in this list
            # at the end of each test image, all the models will be removed    
            all_models = []

            # import task_1a.py. Make sure that task_1a.py is in same folder as task_4a.py
            task_1 = __import__('task_1a')
            detected_arena_parameters = task_1.detect_arena_parameters(config_img)

            # obtain required arena parameters
            medicine_package_details = detected_arena_parameters["medicine_packages"]
            traffic_signals = detected_arena_parameters['traffic_signals']
            start_node = detected_arena_parameters['start_node']
            end_node = detected_arena_parameters['end_node']
            horizontal_roads_under_construction = detected_arena_parameters['horizontal_roads_under_construction']
            vertical_roads_under_construction = detected_arena_parameters['vertical_roads_under_construction'] 

            print("[1] Setting up the scene in CoppeliaSim")
            place_packages(medicine_package_details, sim, all_models)
            place_traffic_signals(traffic_signals, sim, all_models)
            place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models)
            place_vertical_barricade(vertical_roads_under_construction, sim, all_models)
            place_start_end_nodes(start_node, end_node, sim, all_models)
            print("[2] Completed setting up the scene in CoppeliaSim")

            # wait for 10 seconds and then remove models
            time.sleep(10)
            print("[3] Removing models for maze_" + str(i) + '.png')
            for i in all_models:
                sim.removeModel(i)
            