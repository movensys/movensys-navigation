import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import Command, LaunchConfiguration

xacro_file = get_package_share_directory('amr_description') + '/urdf/amr.xacro'
diff_drive_config = os.path.join(get_package_share_directory('navigation_package'),
    'config', 'differential_drive.yaml')
ekf_config_file = os.path.join(get_package_share_directory('navigation_package'),
    'config', 'ekf.yaml')
safe_motion_config = os.path.join(get_package_share_directory('navigation_package'),
    'config', 'safe_motion.yaml')

robot_state_publisher = Node(package='robot_state_publisher',
        executable='robot_state_publisher', name='robot_state_publisher', output='both',
        parameters=[{'use_sim_time': True,
            'robot_description': Command(['xacro ', xacro_file, ' robot_name:=amr'])}])

start_motor_controller = Node(package='navigation_package', executable='differential_drive',
    name='differential_drive', output='screen',
    parameters=[diff_drive_config, {'use_sim_time': True}])

start_robot_localization = Node(package='robot_localization', executable='ekf_node',
    name='ekf_filter_node', output='screen',
	parameters=[ekf_config_file, {'use_sim_time': True}],
    remappings=[('/cmd_vel', '/cmd_vel_safe'),
                ('odometry/filtered', '/odom')])


    
start_safe_motion = Node(
    package='navigation_package',
    executable='safe_motion',
    name='safe_motion',
    output='screen',
    parameters=[safe_motion_config])

start_grpc_bridge = Node(
    package='navigation_package',
    executable='grpc_bridge',
    name='grpc_bridge',
    output='screen',
)

def generate_launch_description():
    return LaunchDescription([
        robot_state_publisher,
        start_motor_controller,
        start_safe_motion,
        start_robot_localization,
        start_grpc_bridge,
    ])
