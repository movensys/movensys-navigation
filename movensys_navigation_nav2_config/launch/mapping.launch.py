import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    navigation_model = os.environ.get('NAVIGATION_MODEL', 'diffbot')
    nav2_config_share = get_package_share_directory('movensys_navigation_nav2_config')
    slam_toolbox_file = os.path.join(nav2_config_share, 'config', navigation_model,
                                     'slam_toolbox.yaml')

    use_sim_time = LaunchConfiguration('use_sim_time')

    start_base = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_config_share, 'launch', 'base.launch.py')),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'rsp': LaunchConfiguration('rsp'),
        }.items())

    start_slam_toolbox = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('slam_toolbox'),
                         'launch', 'online_async_launch.py')),
        launch_arguments={
            'slam_params_file': slam_toolbox_file,
            'use_sim_time': use_sim_time,
        }.items())

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo/Isaac) clock if true',
        ),
        DeclareLaunchArgument(
            'rsp', default_value='true',
            description='Publish /robot_description via base.launch.py. Set false when a '
                        'backend launch (Gazebo sim or wmx_r2_control) already publishes it.',
        ),
        start_base,
        start_slam_toolbox,
    ])
