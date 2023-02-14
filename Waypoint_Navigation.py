import time     
import brickpi3 
import math 

BP = brickpi3.BrickPi3() 

WHEEL_RADIUS = 6.88
AXLE_RADIUS = 16.7

def forward(d):
    
    BP.set_motor_position(BP.PORT_A, int(d * 360/(math.pi * WHEEL_RADIUS)))
    BP.set_motor_position(BP.PORT_D, int(d * 360/(math.pi * WHEEL_RADIUS)))
    
    BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A))
    BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))
    
    time.sleep(d/6)
    
def rotate(a):
    
    BP.set_motor_position(BP.PORT_A, - int(AXLE_RADIUS * (280*a/90)/(math.pi * WHEEL_RADIUS)))
    BP.set_motor_position(BP.PORT_D, int(AXLE_RADIUS * (280*a/90)/(math.pi * WHEEL_RADIUS)))
    
    BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A))
    BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))
    
    time.sleep(2)
    

try:
    
    curr_x_coord = 0
    curr_y_coord = 0
    curr_angle = 0
    
    BP.set_motor_limits(BP.PORT_A, 50, 200)
    BP.set_motor_limits(BP.PORT_D, 50, 200)
    
    while True:
        print("add a waypoint y/n ")
        cont = input()
        
        if (cont == "n"):
            break;
            
        print("enter x coord of destination(meters)")
        x_coord = int(input())
        print("enter y coord of destination (meters)")
        y_coord = int(input())

        x_distance = (x_coord * 100 - curr_x_coord)
        
        y_distance = (y_coord * 100 - curr_y_coord)
        
        total_distance = math.sqrt(pow(x_distance,2) + pow(y_distance,2))
        
        final_angle = math.atan2(y_distance, x_distance)*180/math.pi
        
        angle_change = final_angle - curr_angle

        curr_x_coord = x_coord
        curr_y_coord = y_coord
        curr_angle = final_angle

        rotate(angle_change)
        forward(total_distance)

        print("Done!")
        

except KeyboardInterrupt:
    BP.reset_all()        
