import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node

def generate_launch_description():
    ros_distro = os.environ.get('ROS_DISTRO')

    gz_sim_pkg = {'humble': 'ros_ign_gazebo', 'jazzy': 'ros_gz_sim'}[ros_distro]
    gz_bridge_pkg = {'humble': 'ros_ign_bridge', 'jazzy': 'ros_gz_bridge'}[ros_distro]
    gz_sim_launch = {'humble': 'ign_gazebo.launch.py', 'jazzy': 'gz_sim.launch.py'}[ros_distro]
    clock_msg = {'humble': 'ignition.msgs.Clock', 'jazzy': 'gz.msgs.Clock'}[ros_distro]
    imu_msg = {'humble': 'ignition.msgs.IMU', 'jazzy': 'gz.msgs.IMU'}[ros_distro]
    lidar_msg = {'humble': 'ignition.msgs.LaserScan', 'jazzy': 'gz.msgs.LaserScan'}[ros_distro]

    world_file = {'humble': 'arena_ign.world', 'jazzy': 'arena_gz.world'}[ros_distro]

    pkg_share = get_package_share_directory('movensys_navigation_description')
    world_path = os.path.join(pkg_share, 'worlds', world_file)
    rviz_config = os.path.join(
        get_package_share_directory('movensys_navigation_nav2_config'),
        'rviz',
        'navigation.rviz',
    )
    xacro_file = os.path.join(
        pkg_share,
        'urdf',
        os.environ.get('NAVIGATION_MODEL', 'diffbot'),
        'movensys_navigation.gazebo.xacro',
    )

    # Include Gazebo sim launch file with physics optimization
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            get_package_share_directory(gz_sim_pkg),
            f'/launch/{gz_sim_launch}'
        ]),
        launch_arguments={
            'gz_args': f'-r -v 1 {world_path}'
        }.items()
    )

    # Spawn robot from URDF topic
    spawn_entity_robot = Node(
        package=gz_sim_pkg,
        executable='create',
        output='screen',
        arguments=[
            '-name', 'movensys_navigation',
            '-topic', 'robot_description',
            '-z', '0.1'
        ]
    )

    # Bridge for clock and sensors (gz -> ros)
    gz_ros_bridge = Node(
        package=gz_bridge_pkg,
        executable='parameter_bridge',
        arguments=[
            f'/clock@rosgraph_msgs/msg/Clock[{clock_msg}',
            f'/imu@sensor_msgs/msg/Imu[{imu_msg}',
            f'/lidar_front_left_scan@sensor_msgs/msg/LaserScan[{lidar_msg}',
            f'/lidar_rear_right_scan@sensor_msgs/msg/LaserScan[{lidar_msg}',
        ],
        output='screen'
    )

    # RViz with the navigation config from movensys_navigation_nav2_config
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    # Load controllers
    load_joint_state_broadcaster = ExecuteProcess(
        cmd=[
            'ros2', 'control', 'load_controller',
            '--set-state', 'active', 'joint_state_broadcaster',
        ],
        output='screen'
    )

    load_joint_velocity_controller = ExecuteProcess(
        cmd=[
            'ros2', 'control', 'load_controller',
            '--set-state', 'active', 'velocity_controller',
        ],
        output='screen'
    )

    return LaunchDescription([
        gz_sim,
        spawn_entity_robot,
        gz_ros_bridge,
        rviz,
        load_joint_state_broadcaster,
        load_joint_velocity_controller
    ])
