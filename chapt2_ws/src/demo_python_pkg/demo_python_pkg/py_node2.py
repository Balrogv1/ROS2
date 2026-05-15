import rclpy
from rclpy.node import Node

def main():
    rclpy.init()
    node = Node('python_node1')
    node.get_logger().info('你好python 节点！')
    rclpy.spin(node)
    rclpy.shutdown()
