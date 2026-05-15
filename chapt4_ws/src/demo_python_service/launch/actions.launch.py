from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
import launch_ros
import launch

def generate_launch_description():
    # [1] 声明一个开关参数 (注意拼写：Declare)
    action_declare_arg_run_turtle = DeclareLaunchArgument(
        'run_turtlesim', 
        default_value='true',
        description='是否启动小乌龟节点'
    )

    # [2] 获取参数值代号
    run_turtlesim_config = LaunchConfiguration('run_turtlesim')

    # [3] 动作：带有条件的启动
    # IfCondition: 只有当参数为 'true' 时执行
    action_node_turtle = launch_ros.actions.Node(
        package='turtlesim',
        executable='turtlesim_node',
        condition=IfCondition(run_turtlesim_config) 
    )

    # UnlessCondition: 除非参数为 'true' 否则执行（即 false 时运行）
    action_log_skip = launch.actions.LogInfo(
        msg="检测到 run_turtlesim 为 false，跳过小乌龟启动。",
        condition=UnlessCondition(run_turtlesim_config)
    )

    return launch.LaunchDescription([
        action_declare_arg_run_turtle,
        action_node_turtle,
        action_log_skip
    ])