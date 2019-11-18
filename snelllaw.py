import numpy as np
import cv2
import math
def snelllaw():
    u_slab=0
    u_env=float(input("Enter refractive index of environment: \n "))
    u_slab=float(input("Enter refractive index of glass slab: \n"))
    incidence_angle=float(input("Enter angle of incidence to slab: \n")) #in degres
    incidence_angle=(math.pi/180)*incidence_angle    
    refraction_angle = math.asin((u_env/u_slab)*math.sin(incidence_angle))

    
    win_height = 700
    win_width = 700
    slab_height = 400
    slab_width = 200
    t = 2 #thickness of border    
    incident_point_y = (win_width-slab_width)//2
    incident_point_x = (win_height-slab_height)//2+75    
    flag = 1    
    while(True):        
        refraction_angle = math.asin((u_env/u_slab)*math.sin(incidence_angle))
        lateral_shift = (slab_width)*(math.sin(incidence_angle-refraction_angle)/math.cos(refraction_angle))
        #img = cv2.line(img,(0,0),(511,511),(255,0,0),5)  
        img = np.zeros((win_height,win_width,3), np.uint8)
        #normal to incidence
        img = cv2.line(img,(incident_point_x,incident_point_y-50),(incident_point_x,incident_point_y+50),(0,0,255),t)            
        #slab
        img = cv2.rectangle(img, ((win_height-slab_height)//2,(win_width-slab_width)//2), ((win_height+slab_height)//2,(win_width+slab_width)//2), (98,81,53),t)
        #incident line
        len_incident_line=700  
        img =cv2.line(img,(incident_point_x,incident_point_y),(round(incident_point_x-len_incident_line*math.sin(incidence_angle)),round(incident_point_y-len_incident_line*math.cos(incidence_angle))),(0,255,0),t) 
        #line inside slab    
        img = cv2.line(img,(incident_point_x,incident_point_y),(incident_point_x+round(slab_width*math.tan(refraction_angle)),(win_width+slab_width)//2),(255,0,0),t)   
        #normal to refracted
        img = cv2.line(img,(incident_point_x+round(slab_width*math.tan(refraction_angle)),(win_width+slab_width)//2-50),(incident_point_x+round(slab_width*math.tan(refraction_angle)),(win_width+slab_width)//2+50),(0,0,255),t)            
        #refracted line
        img =cv2.line(img,(incident_point_x+round(slab_width*math.tan(refraction_angle)),(win_width+slab_width)//2),(incident_point_x+round(slab_width*math.tan(refraction_angle)+len_incident_line*math.sin(incidence_angle)),((win_width+slab_width)//2+round(len_incident_line*math.cos(incidence_angle)))),(0,255,0),t) 
        #put text
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, "Refractive Index 1 : "+str(u_env), (win_width-220,25), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(img, "Refractive Index 2 : "+str(u_slab), (win_width-220,45), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(img, "Incident Angle : "+str(round((incidence_angle*180)/(math.pi))), (win_width-220,65), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(img, "Refraction Angle : "+str(round((refraction_angle*180)/(math.pi))), (win_width-220,85), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(img, "Lateral Shift : "+str(round(lateral_shift))+" pixels", (win_width-220,105), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)        
        cv2.putText(img, "Snell's Law", (25,win_height-25), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
        if flag:
            incidence_angle+=0.005 
        else:
             incidence_angle-=0.005
        refraction_angle = math.asin((u_env/u_slab)*math.sin(incidence_angle))
        if incidence_angle>1.48353 or incidence_angle<0 or incident_point_x+round(slab_width*math.tan(refraction_angle)) + 75> (win_height+slab_height)//2:
            flag^=1          
        cv2.imshow("Snell's Law", img)                
        if cv2.waitKey(10) == 27:
            cv2.destroyAllWindows()    
            break
if __name__ == '__main__':
    snelllaw()