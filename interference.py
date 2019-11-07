import numpy as np
import cv2
import math
font = cv2.FONT_HERSHEY_SIMPLEX

maxSlitDistance=6
maxWavelength=1
maxSlitScreenDistance=6

def interference():    
    slitDistanceRange = [i/10000 for i in range(1,20000)]
    wavelengthRange = [i for i in range(400,650)]
    nuRange = [i/10000 for i in range(10000,30000)]
    slitScreenDistanceRange = [i for i in range(100,170)]
        
    slitDistance = 5
    wavelength  = 700
    slitScreenDistance = 90
    nu  = 0
    while(slitDistance not in slitDistanceRange):
        slitDistance = float(input("Enter distance between slits (in mm)"))
    while(wavelength not in wavelengthRange):
        wavelength = float(input("Enter wavelength (in nm)"))
    while(slitScreenDistance not in slitScreenDistanceRange):
        slitScreenDistance = float(input("Enter distance between slit and screen (in cm)"))
    while(nu not in nuRange):
        nu = float(input("Enter refractive index of the medium")) 
    
    slit_intensity = 1

    flaggg = 1

    #parameters
    t = 2 
    win_height = 700
    win_width = 1600      
    d_factor_in_showing = 50
    leftPadding = 50
    IntensityBarWidth = 70


    #co-ordinates simuulation
    slitDistanceFake = 2
    x_source_1 = leftPadding
    y_source_1 = (win_height//2)-round(d_factor_in_showing*(slitDistanceFake/2))
    x_source_2 = leftPadding
    y_source_2 = (win_height//2)+round(d_factor_in_showing*(slitDistanceFake/2))
    x_screen = win_width-leftPadding*6
    y_screen_1 = 30
    y_screen_2 = win_height - y_screen_1
    y_moving_point = win_height//2


    #co-ordinates graph
    x_axis_1=x_screen+20
    x_axis_2=win_width-20
    x_axis_height=round(0.75*(win_height))
    #############
    flag_for_y_point = 0

    path_difference_to_show = (((win_height//2-y_moving_point) *d_factor_in_showing*(slitDistance/2)) / (win_width-leftPadding))
    thetaFakeMax = math.atan(((win_height//2)-30)/(x_screen-x_source_1)) #in radians

    

    thetaRealMax = 10*(math.pi/180) #in radians (10 degrees)
    RealToFaketheta = thetaRealMax/thetaFakeMax    


    #################      begin Real values
    thetaReal = thetaRealMax #in radians  
    pathDifference = slitDistance*math.sin(thetaReal) # in mm
    phaseDifference = ((2*math.pi)/(wavelength*(10**(-6))))*pathDifference #in radians
    ############################# end Real Values

    while(True):                
        img = np.zeros((win_height,win_width,3), np.uint8)     

        #light_lines 
        img = cv2.line(img,(x_source_1,y_source_1),(x_screen,y_moving_point),(0,0,255),1) 
        img = cv2.line(img,(x_source_2,y_source_2),(x_screen,y_moving_point),(0,0,255),1)   
        #middle_line
        img = cv2.line(img,(x_source_2,win_height//2),(x_screen,y_moving_point),(50,50,50),1)   

        #horizontal line
        img = cv2.line(img,(leftPadding,win_height//2),(x_screen,win_height//2),(100,100,100),1)   

        #perpendicular line  

        #for up        
        if y_moving_point<win_height//2:        
            angle_of_line = ((win_height//2-y_moving_point)+(y_source_2-win_height//2))/(x_screen-x_source_2)
            path_difference_to_show = 5*(((win_height//2-y_moving_point) *d_factor_in_showing*(slitDistanceFake/2)) / (win_width-leftPadding))
            #base
            img = cv2.line(img,(x_source_2,y_source_2),(round(x_source_2+path_difference_to_show*math.cos(angle_of_line)),round(y_source_2-path_difference_to_show*math.sin(angle_of_line))),(255,255,255),2)   
            #perpedicular
            img = cv2.line(img,(x_source_1,y_source_1),(round(x_source_2+path_difference_to_show*math.cos(angle_of_line)),round(y_source_2-path_difference_to_show*math.sin(angle_of_line))),(255,255,255),2)   

        #for down       
        if y_moving_point>win_height//2:        
            angle_of_line = ((y_moving_point-win_height//2)+(win_height//2-y_source_1))/(x_screen-x_source_2)
            path_difference_to_show = 5*(((y_moving_point-win_height//2) *d_factor_in_showing*(slitDistanceFake/2)) / (win_width-leftPadding))
            #base
            img = cv2.line(img,(x_source_1,y_source_1),(round(x_source_1+path_difference_to_show*math.cos(angle_of_line)),round(y_source_1+path_difference_to_show*math.sin(angle_of_line))),(255,255,255),2)   
            #perpedicular
            img = cv2.line(img,(x_source_2,y_source_2),(round(x_source_1+path_difference_to_show*math.cos(angle_of_line)),round(y_source_1+path_difference_to_show*math.sin(angle_of_line))),(255,255,255),2)   

        #Calculations
        thetaFake = math.atan(((win_height//2)-y_moving_point)/(x_screen-x_source_1)) #in radians 
        thetaReal = thetaFake*RealToFaketheta #in radians  
        y_actual = slitScreenDistance*(10)*math.tan(thetaReal) #in mm        
        pathDifference = slitDistance*math.sin(thetaReal) # in mm
        phaseDifference = ((2*math.pi)/(wavelength*(10**(-6))))*pathDifference #in radians
        actual_intensity = math.cos(phaseDifference/2)*math.cos(phaseDifference/2)
        fringe_width = (wavelength*(10**(-6))*slitScreenDistance*(10))/slitDistance #in mm
        #################################Strip and Graph#############################################    
        for s in range(y_screen_1,win_height-y_screen_1):
            y_middle=(win_height)//2
            s_y=abs(y_middle-s)
            theta_here=math.atan(s_y/(x_screen-x_source_1))
            theta_here*=RealToFaketheta
            y_actual2 = slitScreenDistance*(10)*math.tan(theta_here) #in mm        
            pathDifference2 = slitDistance*math.sin(theta_here) # in mm
            phaseDifference2 = ((2*math.pi)/(wavelength*(10**(-6))))*pathDifference2
            intensity=255*(math.cos(phaseDifference2/2)**2)
            x_coordinate=x_screen+30
            img=cv2.line(img, (x_coordinate,s),(x_coordinate+40,s),(intensity,intensity,intensity),1)
            distance=x_coordinate+100-intensity/255*40
            #img=cv2.circle(img,(round(distance),s),(255,255,255),1)
            img = cv2.circle(img,(round(distance),s), 1, (255,255,255), -1) 
                      
        #############################################################################
       
       
       
       
        #screen
        img = cv2.line(img,(x_screen,y_screen_1),(x_screen,y_screen_2),(100,100,100),10)   



        #source_between_line        
        img = cv2.line(img,(x_source_1,y_source_1),(x_source_2,y_source_2),(100,100,100),2)                   
        #source1
        img = cv2.circle(img,(x_source_1,y_source_1), 7, (255,255,255), -1)    
        #source2
        img = cv2.circle(img,(x_source_2,y_source_2), 7, (255,255,255), -1)


        #y_screen_dot      
        img = cv2.circle(img,(x_screen,y_moving_point), 7, (255,255,255), -1)  

        #intensity bar
        #img = cv2.rectangle(img,(leftPadding,actual_intensity),(leftPadding+IntensityBarWidth,win_height-leftPadding),(0,255,0),3)
        img = cv2.rectangle(img, (leftPadding, round(win_height-leftPadding-150*actual_intensity-20)), (leftPadding+IntensityBarWidth, win_height-leftPadding-20), (round(255*actual_intensity), round(255*actual_intensity), round(255*actual_intensity)), cv2.FILLED)          

        
        
        #text    
        cv2.putText(img, "Screen", (x_screen-30,20), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)        
        cv2.putText(img, "Source", (x_source_1//2,y_source_1-x_source_1//2), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)        
        cv2.putText(img, "d", (x_source_1//2,(win_height//2)), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)                
        cv2.putText(img, "Interference of light", (win_width//3,50), font, 1.5, (255, 255, 255), 1, cv2.LINE_AA)        

        cv2.putText(img, "d = "+str(slitDistance)+" (in mm)", (50,100), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)        
        cv2.putText(img, "D = "+str(slitScreenDistance)+" (in cm)", (50,120), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)        
        cv2.putText(img, "r = "+str(nu)+"", (50,140), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)     
        cv2.putText(img, "Angle = "+str(round(thetaReal*(180/math.pi),5))+" (in degrees)", (50,160), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)             
        cv2.putText(img, "Path Difference = "+str(round(pathDifference,5))+" (in mm)", (50,180), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA) 
        cv2.putText(img, "Fringe Width = "+str(round(fringe_width,5))+" (in mm)", (50,220), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA) 
        cv2.putText(img, "Intensity", (leftPadding,win_height-40), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)     
        
        phaseDifferencetoDisplay = (phaseDifference*(180/math.pi))%360
        if phaseDifferencetoDisplay>180:
            phaseDifferencetoDisplay-=360
        cv2.putText(img, "Phase Difference = "+str(round(phaseDifferencetoDisplay,5))+" (in degrees)", (50,200), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)                             
        cv2.imshow("Interference (Fresnel's Biprism Experiment)", img) 


                


        if flag_for_y_point:
            y_moving_point+=1
        else:
            y_moving_point-=1
    
        if y_moving_point>y_screen_2 or y_moving_point<y_screen_1:
            flag_for_y_point^=1
        
        ##############Strip##################
    
        #####################################
                  
        if cv2.waitKey(5) == ord(' '):
            if cv2.waitKey(0) == ord(' '):
                continue

        if cv2.waitKey(5) == 27:
            cv2.destroyAllWindows()    
            break
if __name__ == '__main__':
    interference()