import rclpy
from rclpy.node import Node
from chapt4_interface.srv import FaceDetector
from sensor_msgs.msg import Image
import cv2
from ament_index_python.packages import get_package_share_directory # 获取功能包share目录的绝对路径
import os
from cv_bridge import CvBridge
import time
import face_recognition
from rcl_interfaces.srv import SetParameters
from rcl_interfaces.msg import Parameter,ParameterValue,ParameterType


class FaceDetectClientNode(Node):
    def __init__(self):
        super().__init__('face_detect_client_node')
        self.bridge = CvBridge()
        self.default_image_path = os.path.join(get_package_share_directory('demo_python_service'), 'resource', 'bus.jpg')
        self.get_logger().info('人脸检测客户端节点初始化完成')
        self.client = self.create_client(FaceDetector, 'face_detect')
        self.image = cv2.imread(self.default_image_path)
        if self.image is None:
            raise RuntimeError(f'图片读取失败：{self.default_image_path}')

    def call_set_parameters(self, parameters):
        #1 创建客户端，等待
        update_param = self.create_client(SetParameters, 'face_detect_node/set_parameters')
        while update_param.wait_for_service(timeout_sec=1.0) is False:
            self.get_logger().info('等待服务端...')
        request = SetParameters.Request()
        request.parameters = parameters
        future = update_param.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        response = future.result()
        return response
    
    def update_detect_model(self, model='hog'):
        param = Parameter()
        param.name = 'model'
        #创建 parameter value
        param_value = ParameterValue()
        param_value.type = ParameterType.PARAMETER_STRING
        param_value.string_value = model
        param.value = param_value
        #请求更新参数
        response = self.call_set_parameters([param])
        for result in response.results:
            self.get_logger().info(f'设置参数结果：{result.successful} {result.reason}')

    def send_request(self):
        # 1.判断服务端是否在线
        while self.client.wait_for_service(timeout_sec=1.0) is False:
            self.get_logger().info('等待服务端...')
        # 2.创建请求对象
        request = FaceDetector.Request()
        request.image = self.bridge.cv2_to_imgmsg(self.image)
        # 3.发送请求并等待处理完成
        future = self.client.call_async(request) # 现在future 并没有包含响应结果，需要等待服务
        rclpy.spin_until_future_complete(self, future) # 等待future完成，直到服务端返回响应
        response = future.result()
        self.get_logger().info(f'识别到的人脸个数：{response.number},耗时{response.use_time}秒')
        self.show_response(response)
        
    def show_response(self,response):
        for i in range(response.number):
            top = response.top[i]
            right = response.right[i]
            bottom = response.bottom[i]
            left = response.left[i]
            cv2.rectangle(self.image, (left, top), (right, bottom), (0, 0, 255), 2)
        # cv2.imshow('image', self.image)
        # cv2.waitKey(0) # 阻塞式
    

def main():
    rclpy.init()
    node = FaceDetectClientNode()
    node.get_logger().info("--- 第一次识别：使用服务端默认/Launch配置 ---")
    node.send_request()
    time.sleep(1) 

    node.get_logger().info("--- 第二次识别：手动切模型为 cnn ---")
    node.update_detect_model('hog')
    node.send_request()

    node.destroy_node()
    rclpy.shutdown()