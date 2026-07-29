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
    config_dir = os.path.join(nav2_config_share, 'config', navigation_model)
    ekf_config_file = os.path.join(config_dir, 'ekf.yaml')
    ekf_cuvslam_config_file = os.path.join(config_dir, 'ekf_cuvslam.yaml')
    rviz_config = os.path.join(nav2_config_share, 'rviz', 'navigation.rviz')

    use_sim_time = ParameterValue(LaunchConfiguration('use_sim_time'), value_type=bool)
    use_cuvslam = LaunchConfiguration('use_cuvslam')

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
        condition=UnlessCondition(use_cuvslam),
        parameters=[ekf_config_file, {'use_sim_time': use_sim_time}],
        remappings=[('odometry/filtered', 'odom'), ('cmd_vel', 'cmd_vel_safe')])

    start_robot_localization_cuvslam = Node(
        package='robot_localization', executable='ekf_node',
        name='ekf_filter_node', output='screen',
        condition=IfCondition(use_cuvslam),
        parameters=[ekf_cuvslam_config_file, {'use_sim_time': use_sim_time}],
        remappings=[('odometry/filtered', 'odom'), ('cmd_vel', 'cmd_vel_safe')])

    # cuVSLAM (Isaac ROS Visual SLAM) + RealSense driver.
    start_visual_slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(perception_share, 'launch', 'visual_slam.launch.py')),
        condition=IfCondition(use_cuvslam),
        launch_arguments={'use_sim_time': LaunchConfiguration('use_sim_time')}.items())

    rviz = Node(
        package='rviz2', executable='rviz2', name='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen')

    perception_launch = os.path.join(
        perception_share, 'launch', f'{navigation_model}_perception.launch.py')

    start_perception = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(perception_launch),
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
                        'launch (Gazebo sim or wmx_r2_control) already publishes it.',
        ),
        DeclareLaunchArgument(
            'use_cuvslam',
            default_value='false',
            description='Fuse Isaac ROS Visual SLAM (cuVSLAM) into the EKF. When true, '
                        'the EKF uses ekf_cuvslam.yaml and the RealSense + cuVSLAM stack '
                        'is launched (requires an isaac-ros_* image).',
        ),
        robot_state_publisher,
        start_robot_localization,
        start_robot_localization_cuvslam,
        start_visual_slam,
        rviz,
        start_perception,
    ])
