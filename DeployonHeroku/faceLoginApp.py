# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 14:12:04 2020

@author: Aruna


"""

import psutil
import face_recognition
import cv2
import csv
import numpy as np
import pandas as pd

############### FACE CAPTURE FOR LOGIN #################
# define a video capture object 

class UserLogin:
    def captureAndCompare(name):
        vid = cv2.VideoCapture(0) 
          
        while(True): 
              
            # Capture the video frame by frame 
            ret, frame = vid.read() 
            # Display the resulting frame 
            cv2.imshow('frame', frame) 
              
            #'q' button is set as the quitting button----can be replaced by capture button on UI
            if cv2.waitKey(1) & 0xFF == ord('q'): 
                break
       
        vid.release() 
        # Destroy all the windows 
        cv2.destroyAllWindows()  
        
        
        ###############USING FACE ENCODINGS#########################
        ##checks if user matches to any database existing and gives true of false
    
    
       
        users=[]
        unknown=[]
        
        face_encoding_to_check=face_recognition.face_encodings(frame)[0]
        df1 = pd.DataFrame(face_encoding_to_check, columns=["colummn"])
        df1.to_csv('login'+'.csv', index=False)

        
        sizeOfUserDatabase=9######dynamic and received from app database
        for i in range(1,sizeOfUserDatabase+1):
            user='./user'+str(i)+'.csv'
            users.append(user)
            #print("users",user
        #print("users",users)
        count=0
        result=[]
        
        
        #######user database size will be updated automatically as registraion happens on app
        
        
        for user in users:
            count=count+1
           
            ##################READ CSV FILE FOR REGISTERED USER ENCODINGS##########################
            col_list = ["colummn"]
            usercsv=pd.read_csv(user, usecols=col_list)
            userEncodings = usercsv.colummn.tolist()
        
            logincsv=pd.read_csv('login.csv', usecols=col_list)
            unknown.append(userEncodings)
            loginEncodings = logincsv.colummn.tolist()
   
            decision=face_recognition.compare_faces([userEncodings], face_encoding_to_check,tolerance=0.4)
            result.append(decision)
                
            print("Same?",decision)
            
 
        # ###for 2 or more faces detected and matched in database, check which has closer match to its resp.matching face
        ct=0
        set=0
        
        for i in result:
            if i==[True]:
                eucli_dist=face_recognition.api.face_distance(face_encoding_to_check,unknown)
                print(eucli_dist)
                allow_user = min(eucli_dist) 
                index = [i for i, j in enumerate(eucli_dist) if j == allow_user] 
                #print("The list of duplicate elements is :  " + str(oc_set))
                set=1
                value=1
            elif i==[False] and set!=1:
                value=0
        if value==1:
                print("index :",index)
                print("Allow user"+str(index[0])+" with "+str(allow_user) +" eucli_dist")
                ##return to login page
        else:
            print("denied")
               
                ###display welcome
                
                #value=0
                ######app will request for credentials
            ct=ct+1
        #print(value)

        return value

# val=UserLogin.captureAndCompare('Aru')
# print(val)
        
        ###if 2 or more matched, check for eucli_dist
        
        
