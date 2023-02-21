import time
import brickpi3
import math
import random

BP = brickpi3.BrickPi3() 

WHEEL_RADIUS = 6.88
AXLE_RADIUS = 16.7

NUMBER_OF_PARTICLES = 100
weight = 1 / NUMBER_OF_PARTICLES

BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.NXT_ULTRASONIC)




walls = [["x", 0, 210, 0],["x", 0, 84, 168], ["x", 84, 168, 210], ["x",168, 210, 84], ["y", 0, 168, 0], ["y", 126, 210, 84], ["y", 84, 210, 168], ["y", 0, 84, 210]]

def transform(pos):
    x, y, theta = pos
    return (x * 10 + 100, 500 - y * 10, theta)

def forward(d):
    
    BP.set_motor_position(BP.PORT_A, int(d * 360/(math.pi * WHEEL_RADIUS)))
    BP.set_motor_position(BP.PORT_D, int(d * 360/(math.pi * WHEEL_RADIUS)))
    #Should this be (d * 360/(2 * math.pi * WHEEL_RADIUS)))
    
    BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A))
    BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))
    
    time.sleep(d/6)
    
def rotate(a):
    
    BP.set_motor_position(BP.PORT_A, - int(AXLE_RADIUS * (330 * a * 2 / math.pi)/(math.pi * WHEEL_RADIUS)))
    BP.set_motor_position(BP.PORT_D, int(AXLE_RADIUS * (330 * a * 2 / math.pi)/(math.pi * WHEEL_RADIUS)))
    
    BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A))
    BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))
    
    time.sleep(2)
    
    
def distance(x, y, theta, Ax, Ay, Bx, By):
    m = ((By-Ay)*(Ax-x)-(Bx-Ax)*(Ay-y))/((By-Ay)*math.cos(theta)-(Bx-Ax)*math.sin(theta))
    return (m)

def calculate_likelihood(x, y, theta, z):
    
    mod_theta = (theta % (math.pi * 2))
    temporary_distance = 500
    m = 500
            
    if ((theta % math.pi) == 0) :

        for wall in walls:
            if ((wall[0] == "y") and (wall[1] < y) and (y < wall[2])):
                if (((mod_theta < (math.pi /2)) or ((theta % (math.pi * 2)) > (math.pi * 3/2)))  and wall[3] > x):
                    
                        m = abs(x - wall[3])
                        

                elif ((mod_theta > (math.pi /2)) and ((theta % (math.pi * 2)) < (math.pi * 3/2)) and wall[3] > x):
                    
                         m = abs(x - wall[3])
            if ( m < temporary_distance):
                temporary_distance = m
                                
            
        print(temporary_distance)    
        
    elif (theta % (math.pi/2) == 0):
        print("correct")
        
        for wall in walls:
            if ((wall[0] == "x") and (wall[1] < x) and (x < wall[2])):
                if (mod_theta < math.pi and wall[3] > y):
                
                    print("c2")
                        
                    m = abs(y - wall[3])
                        
                elif (mod_theta > math.pi and wall[3] < y):
                    print("c3")
                    
                    m = abs(y - wall[3])
                
            if ( m < temporary_distance):
                temporary_distance = m   
                
        print(temporary_distance)                
        
    else :
        a = math.sin(theta)/math.cos(theta)
        b = y - a * x
        
        
        for wall in walls:
            if (wall[0] == "x"):
                intersect_x = (wall[3] -b)/a
                if ( wall[1] <= intersect_x <= wall[2]):
                    if (mod_theta < math.pi and wall[3] > y):
                        
                        m = distance(x, y, mod_theta, wall[1], wall[3], wall[2], wall[3])
                        
                    elif (mod_theta > math.pi and wall[3] < y):
                    
                        m = distance(x, y, mod_theta, wall[1], wall[3], wall[2], wall[3])
            else :
                intersect_y = a * wall[3] + b
                
                if ( wall[1] <= intersect_y <= wall[2]):
                    if (((mod_theta < (math.pi /2)) or ((theta % (math.pi * 2)) > (math.pi * 3/2)))  and wall[3] > x):
                    
                        m = distance(x, y, mod_theta, wall[3], wall[1], wall[3], wall[2])

                    elif ((mod_theta > (math.pi /2)) and ((theta % (math.pi * 2)) < (math.pi * 3/2))  and wall[3] > x):
                    
                        m = distance(x, y, mod_theta, wall[3], wall[1], wall[3], wall[2]) 
                        
            if (m < temporary_distance):
                temporary_distance = m
                
                
    #print(math.exp(-((z-temporary_distance)**2)/18))
        
    return(math.exp(-((z-temporary_distance)**2)/18))
    
try:
    
    curr_x_coord = 84
    curr_y_coord = 30
    curr_angle = 0
    
    BP.set_motor_limits(BP.PORT_A, 50, 200)
    BP.set_motor_limits(BP.PORT_D, 50, 200)
    
    particles = []    
    
    for i in range(NUMBER_OF_PARTICLES):
        particles.append([84,30,0,weight])
        
    
    
    while True:
        print("add a waypoint y/n ")
        cont = input()
        
        if (cont == "n"):
            break;
            
        print("enter x coord of destination(cm)")
        x_coord = float(input())
        print("enter y coord of destination (cm)")
        y_coord = float(input())

        x_distance = (x_coord  - curr_x_coord)
        print("distance is: ", x_distance)
        
        y_distance = (y_coord - curr_y_coord)
        
        total_distance = math.sqrt(pow(x_distance,2) + pow(y_distance,2))
        
        final_angle = math.atan2(y_distance, x_distance)
        
        angle_change = final_angle - curr_angle
        print("angle change is: ", angle_change)

        rotate(angle_change)
        forward(total_distance)
        
        print("got here")
        
        #sonar_measurement = BP.get_sensor(BP.PORT_3) + 2
        sonar_measurement = 30
        
        print("not here")
        
        cumulative_weights = []
        
        cumulative_weights.append(particles[0][3])
        
        temp_particles = []
        
        for i in range(NUMBER_OF_PARTICLES - 1):
            cumulative_weights.append((cumulative_weights[i] + particles[i + 1][3]))
            
        
        for i in range(NUMBER_OF_PARTICLES):
            rand_num = random.uniform(0, 1)
            j = 0
            while(cumulative_weights[j] < rand_num):
                j += 1
            temp_particles.append([particles[j][0], particles[j][1], particles[j][2], weight)
            
        for i in range(NUMBER_OF_PARTICLES):
            e = random.gauss(0, 0.8)
            f = random.gauss(0, 1)
            
            particles[i][0] = temp_particles[i][0] + (total_distance + e) * math.cos(temp_particles[i][2])
    
            particles[i][1] = temp_particles[i][1] + (total_distance + e) * math.sin(temp_particles[i][2])
        
            particles[i][2] = temp_particles[i][2] - (f * math.pi / 180)
            
            particles[i][3] = calculate_likelihood(temp_particles[i][0], temp_particles[i][1], temp_particles[i][2], sonar_measurement) * temp_particles[i][3]

                
            #particles2.append((particles[i][0], particles[i][1], particles[i][2]))
        
        
        sum_weights = 0
        
        for i in range(NUMBER_OF_PARTICLES):
            sum_weights += particles[i][3]
            
        for i in range(NUMBER_OF_PARTICLES):
            particles[i][3] = particles[i][3]/sum_weights
        
        
        #update curr x y theta
        
        sum_x = 0
        sum_y = 0
        sum_theta = 0
        
        for i in range(NUMBER_OF_PARTICLES):
            sum_x += particles[i][0] * particles[i][3] 
            sum_y += particles[i][1] * particles[i][3]
            sum_theta += particles[i][2] * particles[i][3]
            
        curr_x_coord = sum_x
        curr_y_coord = sum_y
        curr_angle = sum_theta    
            
            
        #draw correctly    
            
        #print ("drawParticles:" + str(particles2))        
        

        
except KeyboardInterrupt:
    BP.reset_all()          
        
    
#calculate_likelihood(20, 20 , math.pi/4 ,209)    
    

    
    
    
