import rclpy
from rclpy.node import Node
from demo_python_pkg.person_node import PersonNode

class WriterNode(PersonNode):
    def __init__(self, node_name:str,name:str, age:int,book:str) -> None:
        print('WriterNode __init__ 方法被调用了')
        super().__init__(node_name,name,age)
        self.book = book



def main():
    rclpy.init()
    node = WriterNode('lisi','法外狂徒李四',18,'论快速入狱')
    node.eat('鱼香肉丝')
    rclpy.spin(node)
    rclpy.shutdown()