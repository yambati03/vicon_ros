import rclpy
from rclpy.node import Node
import socket
from struct import unpack

from vicon_msgs.msg import ViconObject


class ViconPublisher(Node):
    def __init__(self):
        super().__init__('vicon_publisher')
        self.vicon_publisher = self.create_publisher(ViconObject, 'vicon', 10)

        IP = "0.0.0.0"
        PORT = 51001

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((IP, PORT))

        while rclpy.ok():
            self.publish_vicon_update()

    def __del__(self):
        self.sock.close()

    def publish_vicon_update(self):
        data, _ = self.sock.recvfrom(256)
        frame_number = unpack('i', data[0:4])[0]

        # Raw data in mm, convert to m
        x = unpack('d', data[32:40])[0]/1000
        y = unpack('d', data[40:48])[0]/1000
        z = unpack('d', data[48:56])[0]/1000

        # Euler angles in radians, rotation order: (rx,ry,rz) using intermediate frame
        rx = unpack('d', data[56:64])[0]
        ry = unpack('d', data[64:72])[0]
        rz = unpack('d', data[72:80])[0]

        msg = ViconObject()

        msg.header.frame_id = "vicon"
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.frame_number = frame_number

        msg.position.x = x
        msg.position.y = y
        msg.position.z = z
        msg.rotation.x = rx
        msg.rotation.y = ry
        msg.rotation.z = rz

        self.vicon_publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    vicon_publisher = ViconPublisher()

    rclpy.spin(vicon_publisher)

    vicon_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
