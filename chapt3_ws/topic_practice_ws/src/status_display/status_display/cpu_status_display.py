import sys

import rclpy
from rclpy.node import Node
from status_interfaces.msg import SystemStatus

from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)


class CpuStatusWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('ROS2 系统状态监控')
        self.resize(920, 520)

        self.setStyleSheet("""
            QWidget {
                font-size: 24px;
            }
            QLabel {
                padding: 8px;
            }
            QProgressBar {
                min-height: 36px;
                text-align: center;
                font-size: 22px;
            }
        """)

        self.host_label = QLabel('主机名：等待数据...')
        self.cpu_label = QLabel('CPU：等待数据...')
        self.memory_label = QLabel('内存：等待数据...')
        self.net_label = QLabel('网络：等待数据...')

        self.cpu_bar = QProgressBar()
        self.cpu_bar.setRange(0, 100)
        self.cpu_bar.setValue(0)

        self.memory_bar = QProgressBar()
        self.memory_bar.setRange(0, 100)
        self.memory_bar.setValue(0)

        layout = QVBoxLayout()
        layout.addWidget(self.host_label)
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.cpu_bar)
        layout.addWidget(self.memory_label)
        layout.addWidget(self.memory_bar)
        layout.addWidget(self.net_label)
        self.setLayout(layout)

    def update_status(self, msg: SystemStatus):
        self.host_label.setText(f'主机名：{msg.host_name}')

        cpu_value = max(0, min(100, int(msg.cpu_percent)))
        memory_value = max(0, min(100, int(msg.memory_percent)))

        self.cpu_label.setText(f'CPU 使用率：{msg.cpu_percent:.1f}%')
        self.cpu_bar.setValue(cpu_value)

        memory_total_gb = msg.memory_total / 1024
        memory_available_gb = msg.memory_available / 1024
        self.memory_label.setText(
            f'内存使用率：{msg.memory_percent:.1f}% '
            f'可用：{memory_available_gb:.2f} GB / 总量：{memory_total_gb:.2f} GB'
        )
        self.memory_bar.setValue(memory_value)

        self.net_label.setText(
            f'网络：发送 {msg.net_sent:.2f} MB，接收 {msg.net_recv:.2f} MB'
        )


class CpuStatusDisplayNode(Node):
    def __init__(self, window: CpuStatusWindow):
        super().__init__('cpu_status_display')
        self.window = window

        self.subscription = self.create_subscription(
            SystemStatus,
            'system_status',
            self.status_callback,
            10
        )

        self.get_logger().info('CPU 状态显示节点已启动，正在订阅 /system_status')

    def status_callback(self, msg: SystemStatus):
        self.window.update_status(msg)
        self.get_logger().info(
            f'收到系统状态：CPU {msg.cpu_percent:.1f}%, '
            f'内存 {msg.memory_percent:.1f}%'
        )


def main():
    rclpy.init()

    app = QApplication(sys.argv)
    app.setFont(QFont('Noto Sans CJK SC', 18))

    window = CpuStatusWindow()
    window.show()

    node = CpuStatusDisplayNode(window)

    ros_timer = QTimer()
    
    def spin_ros_once():
        if rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0)

    ros_timer.timeout.connect(spin_ros_once)
    ros_timer.start(10)

    exit_code = app.exec()

    ros_timer.stop()
    node.destroy_node()
    if rclpy.ok():
        rclpy.shutdown()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()