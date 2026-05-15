import sys

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget


class StatusDisplayWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('ROS2 状态显示器')
        self.resize(420, 140)

        self.status_label = QLabel('等待 /status 消息...')
        self.status_label.setStyleSheet('font-size: 24px; padding: 20px;')

        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        self.setLayout(layout)

    def update_status(self, text: str):
        self.status_label.setText(text)


class StatusDisplayNode(Node):
    def __init__(self, window: StatusDisplayWindow):
        super().__init__('status_display')
        self.window = window

        self.subscription = self.create_subscription(
            String,
            'status',
            self.status_callback,
            10
        )

        self.get_logger().info('status_display 节点已启动，正在订阅 /status')

    def status_callback(self, msg: String):
        self.window.update_status(msg.data)
        self.get_logger().info(f'界面已更新：{msg.data}')


def main():
    rclpy.init()

    app = QApplication(sys.argv)
    window = StatusDisplayWindow()
    window.show()

    node = StatusDisplayNode(window)

    ros_timer = QTimer()
    ros_timer.timeout.connect(lambda: rclpy.spin_once(node, timeout_sec=0))
    ros_timer.start(10)

    exit_code = app.exec()

    node.destroy_node()
    rclpy.shutdown()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()