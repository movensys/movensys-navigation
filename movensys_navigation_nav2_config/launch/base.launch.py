import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    navigation_model = os.environ.get("NAVIGATION_MODEL", "diffbot")

    description_share = get_package_share_directory('movensys_navigation_description')
    nav2_config_share = get_package_share_directory('movensys_navigation_nav2_config')

    xacro_file = os.path.join(description_share, 'urdf', navigation_model,
                              'movensys_navigation.gazebo.xacro')
    ekf_config_file = os.path.join(nav2_config_share, 'config', navigation_model, 'ekf.yaml')
    rviz_config = os.path.join(nav2_config_share, 'rviz', 'navigation.rviz')

    use_sim_time = ParameterValue(LaunchConfiguration('use_sim_time'), value_type=bool)

    robot_state_publisher = Node(
        package='robot_state_publisher', executable='robot_state_publisher',
        name='robot_state_publisher', output='both',
        parameters=[{
            'use_sim_time': use_sim_time,
            'robot_description': Command(['xacro ', xacro_file, ' robot_name:=amr']),
        }])

    start_robot_localization = Node(
        package='robot_localization', executable='ekf_node',
        name='ekf_filter_node', output='screen',
        parameters=[ekf_config_file, {'use_sim_time': use_sim_time}])

    rviz = Node(
        package='rviz2', executable='rviz2', name='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen')

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true',
        ),
        robot_state_publisher,
        start_robot_localization,
        rviz,
    ])
