import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def launch_setup(context, *args, **kwargs):
    use_sim_time = LaunchConfiguration('use_sim_time')
    navigation_model = os.environ.get('NAVIGATION_MODEL', 'diffbot')

    bridge_params = os.path.join(
        get_package_share_directory('movensys_navigation_nav2_config'),
        'config', navigation_model, 'sim_bridge.yaml')

    bridge_node = Node(
        package='movensys_navigation_nav2_config',
        executable='sim_bridge',
        name='sim_bridge',
        output='screen',
        parameters=[bridge_params, {'use_sim_time': use_sim_time}],
    )

    return [bridge_node]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation time',
        ),
        OpaqueFunction(function=launch_setup),
    ])
