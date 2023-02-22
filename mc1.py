import time     
import brickpi3 
import math 

import time     
import brickpi3 
import math 
import random

BP = brickpi3.BrickPi3() 

WHEEL_RADIUS = 6.88
AXLE_RADIUS = 16.7

NUMBER_OF_PARTICLES = 100
weight = 1 / NUMBER_OF_PARTICLES

BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.NXT_ULTRASONIC)




walls = [["x", 0, 210, 0],["x", 0, 84, 168], ["x", 84, 168, 210], ["x",168, 210, 84], ["y", 0, 168, 0], ["y", 126, 210, 84], ["y", 84, 210, 168], ["y", 0, 84, 210]]

def transform(pos):
    x, y, theta = pos
    return (x * 10 + 100, 500 - y * 10, theta)

def forward(d):
    
    BP.set_motor_position(BP.PORT_A, int(d * 370/(math.pi * WHEEL_RADIUS)))
    BP.set_motor_position(BP.PORT_D, int(d * 370/(math.pi * WHEEL_RADIUS)))
    
    BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A))
    BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))
    
    time.sleep(d/8)
    
def rotate(a):
    
    BP.set_motor_position(BP.PORT_A, - int(AXLE_RADIUS * (290 * a * 2 / math.pi)/(math.pi * WHEEL_RADIUS)))
    BP.set_motor_position(BP.PORT_D, int(AXLE_RADIUS * (290 * a * 2 / math.pi)/(math.pi * WHEEL_RADIUS)))
    
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
    #print(x)
            
    if ((theta % math.pi) == 0) :

        for wall in walls:
            if ((wall[0] == "y") and (wall[1] < y) and (y < wall[2])):
                if (((mod_theta < (math.pi /2)) or ((theta % (math.pi * 2)) > (math.pi * 3/2)))  and wall[3] > x):
                    
                        m = abs(x - wall[3])
                        

                elif ((mod_theta > (math.pi /2)) and ((theta % (math.pi * 2)) < (math.pi * 3/2)) and wall[3] > x):
                    
                         m = abs(x - wall[3])
            if ( m < temporary_distance):
                temporary_distance = m
                                
            
        #print(temporary_distance)    
        
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
                
        #print(temporary_distance)                
        
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
                    if (((mod_theta < (math.pi /2)) or ((mod_theta % (math.pi * 2)) > (math.pi * 3/2)))  and wall[3] > x):
                    
                        m = distance(x, y, mod_theta, wall[3], wall[1], wall[3], wall[2])

                    elif ((mod_theta > (math.pi /2)) and ((mod_theta % (math.pi * 2)) < (math.pi * 3/2))  and wall[3] < x):
                    
                        m = distance(x, y, mod_theta, wall[3], wall[1], wall[3], wall[2]) 
                        
            if (m < temporary_distance):
                temporary_distance = m
                
        #print(temporary_distance)        
                
                
    #print(math.exp(-((z-temporary_distance)**2)/18))
        
    #print("theoretical distance =", temporary_distance)    
    #return(math.exp(-((z-temporary_distance)**2)/18))
    return(math.exp(- math.pow(z-temporary_distance,2))/18 + 0.001)
    #return(math.exp(-((temporary_distance-temporary_distance)**2)/18) + 0.2)
    

def move_step(distance, angle_change, particles):
    
    rotate(angle_change )
    forward(distance)
        
    sonar_measurement = 0
        
    for i in range (10):
        try:
            value = BP.get_sensor(BP.PORT_2)
            print(value)   
            if (i > 2):
                sonar_measurement += value
                
        except brickpi3.SensorError as error:
            i -= 1
            print(error)


    sonar_measurement = sonar_measurement / 7 

    print("sonar = ", sonar_measurement)

    #sonar_measurement = BP.get_sensor(BP.PORT_3) + 2
    #sonar_measurement = 30

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
        temp_particles.append([particles[j][0], particles[j][1], particles[j][2], weight])

    if (angle_change != 0):
        for temp_particle in temp_particles:
            g = random.gauss(0, 0.005)
            temp_particle[2] += (angle_change + g)  

    for i in range(NUMBER_OF_PARTICLES):
        e = random.gauss(0, 1)
        f = random.gauss(0, 0.005)

        particles[i][0] = temp_particles[i][0] + (distance + e) * math.cos(temp_particles[i][2])
        particles[i][1] = temp_particles[i][1] + (distance + e) * math.sin(temp_particles[i][2])
        particles[i][2] = temp_particles[i][2] + (f) + curr_angle  # use updated curr_angle
        particles[i][3] = calculate_likelihood(particles[i][0], particles[i][1], particles[i][2], sonar_measurement) * weight



        #print("prev_weight =", temp_particles[i][3])
        #print("weight = ", particles[i][3])    
        #particles2.append((particles[i][0], particles[i][1], particles[i][2]))


    sum_weights = 0

    for i in range(NUMBER_OF_PARTICLES):
        sum_weights += particles[i][3]
        
    print("sum weights =", sum_weights)    

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

    print("curr x = ", curr_x_coord)

    print("curr y = ", curr_y_coord)

    print("curr angle = ", curr_angle * 180 / math.pi)
    
    return(particles, curr_x_coord, curr_y_coord, curr_angle)
            
    
    
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
        
        print(total_distance)
        
        final_angle = math.atan2(y_distance, x_distance)
        angle_change = final_angle - curr_angle

        if (angle_change < - math.pi):
            angle_change += 2 * math.pi

        if (angle_change > math.pi):
            angle_change += - (2 * math.pi)

        while(total_distance >= 20):
            (particles, curr_x_coord, curr_y_coord, curr_angle) = move_step(20, angle_change, particles)
            x_distance = (x_coord - curr_x_coord)
            y_distance = (y_coord - curr_y_coord)
            total_distance = math.sqrt(pow(x_distance, 2) + pow(y_distance, 2))
            final_angle = math.atan2(y_distance, x_distance)
            angle_change = final_angle - curr_angle

            if (angle_change < - math.pi):
                angle_change += 2 * math.pi

            if (angle_change > math.pi):
                angle_change += - (2 * math.pi)

            curr_angle += angle_change  # update the current orientation
            
            print("angle change:", angle_change *180/math.pi)


        (particles, curr_x_coord, curr_y_coord, curr_angle) = move_step(total_distance, angle_change, particles)
        

    

            
        #draw correctly    
            
        #print ("drawParticles:" + str(particles2))             

        
except KeyboardInterrupt:
    BP.reset_all()          
        
    
#calculate_likelihood(20, 20 , math.pi/4 ,209)    
    

    
    
    
