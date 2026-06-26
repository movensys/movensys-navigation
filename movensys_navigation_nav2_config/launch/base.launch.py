import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    navigation_model = os.environ.get('NAVIGATION_MODEL', 'diffbot')

    description_share = get_package_share_directory('movensys_navigation_description')
    nav2_config_share = get_package_share_directory('movensys_navigation_nav2_config')
    perception_share = get_package_share_directory('movensys_navigation_perception')

    xacro_file = os.path.join(description_share, 'urdf', navigation_model,
                              'movensys_navigation.xacro')
    ekf_config_file = os.path.join(nav2_config_share, 'config', navigation_model, 'ekf.yaml')
    rviz_config = os.path.join(nav2_config_share, 'rviz', 'navigation.rviz')

    use_sim_time = ParameterValue(LaunchConfiguration('use_sim_time'), value_type=bool)

    robot_state_publisher = Node(
        package='robot_state_publisher', executable='robot_state_publisher',
        name='robot_state_publisher', output='both',
        condition=IfCondition(LaunchConfiguration('rsp')),
        parameters=[{
            'use_sim_time': use_sim_time,
            'robot_description': Command(['xacro ', xacro_file, ' robot_name:=amr']),
        }])

    start_robot_localization = Node(
        package='robot_localization', executable='ekf_node',
        name='ekf_filter_node', output='screen',
        parameters=[ekf_config_file, {'use_sim_time': use_sim_time}],
        remappings=[('odometry/filtered', 'odom'), ('cmd_vel', 'cmd_vel_safe')])

    rviz = Node(
        package='rviz2', executable='rviz2', name='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen')

    start_perception = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(perception_share, 'launch', f'{navigation_model}_perception.launch.py')),
        condition=UnlessCondition(LaunchConfiguration('use_sim_time')))

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true',
        ),
        DeclareLaunchArgument(
            'rsp',
            default_value='true',
            description='Publish /robot_description here. Set false when a backend '
                        'launch (Gazebo sim or wmx_ros2_control) already publishes it.',
        ),
        robot_state_publisher,
        start_robot_localization,
        rviz,
        start_perception,
    ])
