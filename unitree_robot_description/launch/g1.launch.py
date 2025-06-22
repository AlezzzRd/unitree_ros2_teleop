from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import Command, PathJoinSubstitution

def generate_launch_description():
    # 获取包的共享目录路径
    pkg_path = get_package_share_directory('unitree_robot_description')
    
    robot_description = {
        'robot_description': Command([
            'xacro ',
            PathJoinSubstitution([pkg_path, 'urdf', 'g1', 'g1_body29_hand14.urdf.xacro']),
            ' use_sim:=false'  # 传递参数给 xacro
        ])
    }

    return LaunchDescription([
        # 机器人状态发布器
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[robot_description],
        ),
        
        # 关节状态发布器（GUI 版本）
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            output='screen',
        ),
        
        # RViz2 可视化工具
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', PathJoinSubstitution([pkg_path, 'rviz', 'g1.rviz'])]  # 可选：加载默认配置
        ),
    ])