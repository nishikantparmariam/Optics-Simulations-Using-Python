import numpy as np
import cv2
import math
font = cv2.FONT_HERSHEY_SIMPLEX

maxSlitDistance=6
maxWavelength=1
maxSlitScreenDistance=6

def interference():
    slitDistance = maxSlitDistance+1
    while(slitDistance>maxSlitDistance):
        slitDistance = int(input("Enter distance between slits (in mm)"))
    wavelength = int(input("Enter wavelength (in nm)"))
    slitScreenDistance = int(input("Enter distance between slits (in cm)"))
    nu = int(input("Enter refractive index of the medium"))
    

    #parameters
    t = 2 
    win_height = 700
    win_width = 1600      
    d_factor_in_showing = 50
    leftPadding = 30


    #co-ordinates simuulation
    x_source_1 = leftPadding
    y_source_1 = (win_height//2)-round(d_factor_in_showing*(slitDistance/2))
    x_source_2 = leftPadding
    y_source_2 = (win_height//2)+round(d_factor_in_showing*(slitDistance/2))
    x_screen = win_width//2
    y_screen_1 = 30
    y_screen_2 = win_height - 20
    y_moving_point = win_height//2


    #co-ordinates graph
    x_axis_1=x_screen+20
    x_axis_2=win_width-20
    x_axis_height=
    #############
    flag_for_y_point = 0

    path_difference_to_show = (((win_height//2-y_moving_point) *d_factor_in_showing*(slitDistance/2)) / (win_width-leftPadding))

    while(True):                
        img = np.zeros((win_height,win_width,3), np.uint8)     

        #light_lines 
        img = cv2.line(img,(x_source_1,y_source_1),(x_screen,y_moving_point),(0,0,255),1) 
        img = cv2.line(img,(x_source_2,y_source_2),(x_screen,y_moving_point),(0,0,255),1)   

        #perpendicular line  
        #for up
        angle_of_line = ((win_height//2-y_moving_point)+(y_source_2-win_height//2))/(x_screen-x_source_2)
        if y_moving_point<win_height//2:
            img = cv2.line(img,(x_source_2,y_source_2),(round(x_source_2+path_difference_to_show*math.cos(angle_of_line)),round(y_source_2-path_difference_to_show*math.sin(angle_of_line))),(255,255,255),2)   

        #screen
        img = cv2.line(img,(x_screen,y_screen_1),(x_screen,y_screen_2),(100,100,100),4)   



        #source_between_line        
        img = cv2.line(img,(x_source_1,y_source_1),(x_source_2,y_source_2),(100,100,100),2)                   
        #source1
        img = cv2.circle(img,(x_source_1,y_source_1), 7, (255,255,255), -1)    
        #source2
        img = cv2.circle(img,(x_source_2,y_source_2), 7, (255,255,255), -1)      
                     
        
        #text    
        cv2.putText(img, "Screen", (win_width//2-30,20), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)        
        cv2.putText(img, "Source", (x_source_1//2,y_source_1-x_source_1//2), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)        
        cv2.putText(img, "d", (x_source_1//2,(win_height//2)), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)        
        cv2.imshow("Interference (Fresnel's Biprism Experiment)", img) 


        #update all variables
        path_difference_to_show = 6*(((win_height//2-y_moving_point) *d_factor_in_showing*(slitDistance/2)) / (win_width-leftPadding))


        if flag_for_y_point:
            y_moving_point+=1
        else:
            y_moving_point-=1
    
        if y_moving_point>y_screen_2 or y_moving_point<y_screen_1:
            flag_for_y_point^=1
        

        #img=cv2.line(img,())

        if cv2.waitKey(5) == 27:
            cv2.destroyAllWindows()    
            break

        if cv2.waitKey(5) == ord(' '):
            if cv2.waitKey(0) == ord(' '):
                continue
if __name__ == '__main__':
    interference()