import rclpy

from sensor_msgs.msg import Joy
import numpy as np
import socket
import json

dado = np.zeros(17)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 5555))


def joy_callback(msg):
    try:
        s.recv(1024)
        dado_j = [msg.axes[0],msg.axes[1]]
        dado_b = [msg.buttons[0], msg.buttons[13], msg.buttons[14], msg.buttons[15], msg.buttons[16]]
        s.send(json.dumps({"bots": dado_b, "joys": dado_j}).encode())
    except:
        s.close()

def main():
    rclpy.init()

    # Create a node that subscribes to the /joy topic and publishes to the /skidbot/cmd_vel topic.
    node = rclpy.create_node('joy_controller')
    subscription = node.create_subscription(Joy, '/joy', lambda msg: joy_callback(msg), 10)

    # Spin the node to receive messages and call the joy_callback function for each message.
    rclpy.spin(node)

    # Clean up before exiting.
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
        main()