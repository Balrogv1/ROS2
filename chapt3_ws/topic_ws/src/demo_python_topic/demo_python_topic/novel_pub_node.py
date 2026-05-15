import rclpy
from rclpy.node import Node
import requests
from example_interfaces.msg import String
from queue import Queue

class NovelPubNode(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.get_logger().info(f'{node_name}，启动！')
        self.novels_queue_ = Queue() # 创建队列
        self.nobel_pubblisher = self.create_publisher(String, 'novel', 10) # 创建发布者
        self.create_timer(3.0, self.timer_callback) # 创建定时器
    
    def timer_callback(self):
        # self.novel_pubblisher.publish() # 发布消息
        if self.novels_queue_.qsize() > 0:
            line = self.novels_queue_.get() # 取出队列中的元素
            msg = String()
            msg.data = line
            self.nobel_pubblisher.publish(msg) # 发布消息
            self.novels_queue_.put(line) 
            self.get_logger().info(f'发布了：{msg}')

    def download(self, url):
        response = requests.get(url)
        response.encoding = 'utf-8'
        text = response.text
        self.get_logger().info(f'下载{url},{len(text)}')
        for line in text.splitlines():
            self.novels_queue_.put(line) # 加入队列
        

def main():
    rclpy.init()
    node = NovelPubNode('novel_pub')
    node.download('http://localhost:8000/novel1.txt')
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()