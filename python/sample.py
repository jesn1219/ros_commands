#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
PI = 3.1415926535897

class Burger :
    vel_msg = None
    velocity_publisher = None
    rate = None
    time_start = None
    time_now = None
    velocity_publisher = None

    def __init__(self) :
        rospy.init_node('robot_cleaner', anonymous=True)
        self.vel_msg = Twist()
        self.velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.time_start = rospy.Time.now().to_sec()
        self.rate = rospy.Rate(120)
        self.init_vel()

    def init_vel(self) :
        self.vel_msg.linear.x = 0
        self.vel_msg.linear.y = 0
        self.vel_msg.linear.z = 0
        self.vel_msg.angular.x = 0
        self.vel_msg.angular.y = 0
        self.vel_msg.angular.z = 0
        self.velocity_publisher.publish(self.vel_msg)

    def time_uptime(self) :
        return time_start - rospy.Time.now().to_sec()

    def front_back(self) :
        print("draw_rectangle")
        while not rospy.is_shutdown():
            #Setting the current time for distance calculus
            #Loop to move the turtle in an specified distance

            time_checkpoint = rospy.Time.now().to_sec()

            while (rospy.Time.now().to_sec() - time_checkpoint) < 3 :
                self.vel_msg.linear.x = 1
                self.velocity_publisher.publish(self.vel_msg)
                self.rate.sleep()

            time_checkpoint = rospy.Time.now().to_sec()
            while (rospy.Time.now().to_sec() - time_checkpoint) < 3 :
                self.vel_msg.linear.x = -1
                self.velocity_publisher.publish(self.vel_msg)
                self.rate.sleep()

            print("Finished")
            break
        self.init_vel()

    def forward_sec(self, speed, sec) :
        print("forward_sec")
        while not rospy.is_shutdown():
            #Setting the current time for distance calculus
            #Loop to move the turtle in an specified distance

            time_checkpoint = rospy.Time.now().to_sec()

            while (rospy.Time.now().to_sec() - time_checkpoint) < sec :
                self.vel_msg.linear.x = speed
                self.velocity_publisher.publish(self.vel_msg)
                self.rate.sleep()


            print("Finished")
            break
        self.init_vel()


    def turn_angle(self, degree, speed) :
        print("Let's rotate your robot")
        #speed = input("Input your speed (degrees/sec):")
        #angle = input("Type your distance (degrees):")
        #clockwise = input("Clockwise?: ") #True or false
        if (degree > 0) :
            clockwise = True
        else :
            clockwise = False
            degree = abs(degree)

        #Converting from angles to radians
        angular_speed = speed*2*PI/360
        relative_angle = degree*2*PI/360

        #We wont use linear components
        self.vel_msg.linear.x=0
        self.vel_msg.linear.y=0
        self.vel_msg.linear.z=0
        self.vel_msg.angular.x = 0
        self.vel_msg.angular.y = 0

        # Checking if our movement is CW or CCW
        if clockwise:
            self.vel_msg.angular.z = -abs(angular_speed)
        else:
            self.vel_msg.angular.z = abs(angular_speed)
        # Setting the current time for distance calculus
        t0 = rospy.Time.now().to_sec()
        current_angle = 0

        while(current_angle <= relative_angle):
            self.velocity_publisher.publish(self.vel_msg)
            t1 = rospy.Time.now().to_sec()
            current_angle = angular_speed*(t1-t0)
            print(self.vel_msg)
            self.rate.sleep()


        #Forcing our robot to stop
        self.vel_msg.angular.z = 0
        self.velocity_publisher.publish(self.vel_msg)




    # starts a new node

if __name__ == '__main__':
    try:
        # 200 120 160
        #Testing our function
        test = Burger()
        test.forward_sec(speed = 0.2, sec = 7)
        test.turn_angle(-90,15)
        test.forward_sec(speed = 0.2, sec = 6)
        test.turn_angle(90,15)
        test.forward_sec(speed = 0.2, sec = 8)
        test.turn_angle(180,10)
        test.forward_sec(speed = 0.2, sec = 8)
        test.turn_angle(-90,15)
        test.forward_sec(speed = 0.2, sec = 6)
        test.turn_angle(90,15)
        test.forward_sec(speed = 0.2, sec = 7)
        test.turn_angle(180,10)



        #test.turn_angle(90,30)
        test.init_vel()
    except rospy.ROSInterruptException: pass
