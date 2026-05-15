import launch
import launch_ros
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # [1] 申明 Launch 参数：model_type
    # 作用：允许用户在命令行通过 model_type:=xxx 动态传参
    action_declare_arg_model_type = DeclareLaunchArgument(
        'model_type', 
        default_value='hog',
        description='人脸识别模型选择：hog 或 cnn'
    )

    # [2] 获取 Launch 参数的值 (此时它是一个代号，待启动时填充)
    model_type_config = LaunchConfiguration('model_type')

    # [3] 定义【服务端】节点
    action_node_face_service_node = launch_ros.actions.Node(
        package='demo_python_service',
        executable='face_detect_node',
        name='face_detect_node', 
        output='screen',
        # 核心：将 Launch 参数传递给节点的内部参数 'model'
        parameters=[{
            'model': model_type_config,
            'number_of_times_to_upsample': 1
        }]
    )

    # [4] 定义【客户端】节点
    action_node_face_client_node = launch_ros.actions.Node(
        package='demo_python_service',
        executable='face_detect_client_node',
        name='face_detect_client_node',
        output='screen'
    )

    # [5] 将所有动作打包返回
    return launch.LaunchDescription([
        action_declare_arg_model_type, # 必须放入列表
        action_node_face_service_node,
        action_node_face_client_node
    ])