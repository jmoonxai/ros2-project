import rclpy as rp
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import termios
import tty



class TurtleTeleop(Node):
    def __init__(self):
        super().__init__('TurtleTeleop')
        self.publisher = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.timer_callback)


        self.speed = 2.0

    def get_key(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            tty.setraw(sys.stdin.fileno())
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        return key
    
    def timer_callback(self):
        key = self.get_key()

        if key == 'q':
            self.get_logger().info("Shutting down node...")
            self.destroy_node()
            rp.shutdown()
            return

        msg = Twist()

        if key == 'w':
            msg.linear.x = self.speed

        elif key == 's':
            msg.linear.x = -self.speed

        elif key == 'a':
            msg.angular.z = 2.0

        elif key == 'd':
            msg.angular.z = -2.0
        
        elif key == "+": # 스피드
            self.speed +=0.5
        
        elif key == "-":
            self.speed +=0.5
        

        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
        
        
        self.publisher.publish(msg)



def main():
    rp.init()

    turtlesim_publisher = TurtleTeleop()
    rp.spin(turtlesim_publisher)
    
    turtlesim_publisher.destroy_node()
    rp.shutdown()




if __name__ == "__main__" :
 
    main()

