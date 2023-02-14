import time     
import brickpi3 
import math 
import random

BP = brickpi3.BrickPi3() 

WHEEL_RADIUS = 6.88
AXLE_RADIUS = 16.7

NUMBER_OF_PARTICLES = 100
weight = 1 / NUMBER_OF_PARTICLES

def forward(d):
    
    BP.set_motor_position(BP.PORT_A, int(d * 360/(math.pi * WHEEL_RADIUS)))
    BP.set_motor_position(BP.PORT_D, int(d * 360/(math.pi * WHEEL_RADIUS)))
    
    BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A))
    BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))
        
def rotate():
    
    BP.set_motor_position(BP.PORT_A, - int(AXLE_RADIUS * 280/(math.pi * WHEEL_RADIUS)))
    BP.set_motor_position(BP.PORT_D, int(AXLE_RADIUS * 280/(math.pi * WHEEL_RADIUS)))
    
    BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A))
    BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))
    
    time.sleep(10)
    

try:
    BP.set_motor_limits(BP.PORT_A, 80, 200)
    BP.set_motor_limits(BP.PORT_D, 80, 200)
    
    particles = []
    
    for i in range(NUMBER_OF_PARTICLES):
        particles.append([0,0,0,weight])
    
    x0,y0 = 0,0
    x1,y1 = 0,0
    flag = 0
    
    for i in range(4):
        for i in range(4):
            forward(10)
            
            if flag == 0:
                x1 += 10
                print ("drawLine:" + str((10 * (x0 + 50),10 * (y0 + 50),10 * (x1 + 50),10 * (y1 + 50))))
                x0 += 10
                
            elif flag == 1:
                y1 -= 10
                print ("drawLine:" + str((10 * (x0 + 50),10 * (y0 + 50),10 * (x1 + 50),10 * (y1 + 50))))             
                y0 -= 10
            
            elif flag == 2:
                x1 -= 10 
                print ("drawLine:" + str((10 * (x0 + 50),10 * (y0 + 50),10 * (x1 + 50),10 * (y1 + 50))))                
                x0 -= 10
                
            elif flag == 3:
                y1 += 10
                print ("drawLine:" + str((10 * (x0 + 50),10 * (y0 + 50),10 * (x1 + 50),10 * (y1 + 50)))) 
                y0 += 10
                

            for particle in particles:
                e = random.gauss(0, 5)
                f = random.gauss(0, 1)
                particle[0] += (10 + e) * math.cos(particle[2]) 
                particle[1] += (10 + e) * math.sin(particle[2]) 
                particle[2] += f
                
                print ("drawParticles:" + str((particle[0],particle[1],particle[2])))
                
            time.sleep(5)
            print("Forward")
        rotate()
        flag += 1
        for particle in particles:
            g = random.gauss(0, 1)
            particle[2] += math.pi / 2 + g
            print ("drawParticles:" + str((particle[0],particle[1],particle[2])))
            
        print("Rotate")
        
    print("Done!")
        

except KeyboardInterrupt:
    BP.reset_all()   
