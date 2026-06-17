import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    navigation_model = os.environ.get("NAVIGATION_MODEL", "diffbot")
    nav2_config_share = get_package_share_directory('movensys_navigation_nav2_config')

    # nav2 registers some pluginlib classes differently per distro (e.g. the
    # navfn planner and behaviors use "/" on Humble but "::" on Jazzy), so the
    # params file is selected from the ROS_DISTRO set in the environment
    # (exported in ~/.bashrc / by sourcing /opt/ros/<distro>/setup.bash).
    ros_distro = os.environ.get("ROS_DISTRO", "")
    config_dir = os.path.join(nav2_config_share, 'config', navigation_model)
    params_file = os.path.join(config_dir, f'navigation.{ros_distro}.yaml')
    if not os.path.exists(params_file):
        raise RuntimeError(
            f"No nav2 params file for ROS_DISTRO='{ros_distro}'. "
            f"Expected: {params_file}")
    map_file = os.path.join(nav2_config_share, 'maps', 'my_map.yaml')
    bt_dir = os.path.join(nav2_config_share, 'behavior_trees')
    nav_to_pose_bt = os.path.join(bt_dir, 'navigate_to_pose_w_replanning_and_recovery.xml')
    nav_through_poses_bt = os.path.join(
        bt_dir, 'navigate_through_poses_w_replanning_and_recovery.xml')

    use_sim_time = ParameterValue(LaunchConfiguration('use_sim_time'), value_type=bool)
    remappings = [('/tf', 'tf'), ('/tf_static', 'tf_static')]

    localization_nodes = ['map_server', 'amcl']
    navigation_nodes = ['controller_server', 'smoother_server', 'planner_server',
                        'behavior_server', 'bt_navigator', 'waypoint_follower',
                        'velocity_smoother']

    # robot_state_publisher + EKF + RViz
    start_base = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_config_share, 'launch', 'base.launch.py')),
        launch_arguments={
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'rsp': LaunchConfiguration('rsp'),
        }.items())

    # --- localization (map_server + amcl) ---
    map_server = Node(
        package='nav2_map_server', executable='map_server', name='map_server', output='screen',
        parameters=[params_file, {'use_sim_time': use_sim_time, 'yaml_filename': map_file}],
        remappings=remappings)

    amcl = Node(
        package='nav2_amcl', executable='amcl', name='amcl', output='screen',
        parameters=[params_file, {'use_sim_time': use_sim_time}],
        remappings=remappings)

    lifecycle_localization = Node(
        package='nav2_lifecycle_manager', executable='lifecycle_manager',
        name='lifecycle_manager_localization', output='screen',
        parameters=[{'use_sim_time': use_sim_time, 'autostart': True,
                     'node_names': localization_nodes}])

    # --- navigation servers ---
    nav_servers = GroupAction(actions=[
        Node(package='nav2_controller', executable='controller_server', name='controller_server',
             output='screen', respawn=True, respawn_delay=2.0,
             parameters=[params_file, {'use_sim_time': use_sim_time}],
             remappings=remappings + [('cmd_vel', 'cmd_vel_nav')]),
        Node(package='nav2_smoother', executable='smoother_server', name='smoother_server',
             output='screen', respawn=True, respawn_delay=2.0,
             parameters=[params_file, {'use_sim_time': use_sim_time}], remappings=remappings),
        Node(package='nav2_planner', executable='planner_server', name='planner_server',
             output='screen', respawn=True, respawn_delay=2.0,
             parameters=[params_file, {'use_sim_time': use_sim_time}], remappings=remappings),
        Node(package='nav2_behaviors', executable='behavior_server', name='behavior_server',
             output='screen', respawn=True, respawn_delay=2.0,
             parameters=[params_file, {'use_sim_time': use_sim_time}],
             remappings=remappings + [('cmd_vel', 'cmd_vel_nav')]),
        Node(package='nav2_bt_navigator', executable='bt_navigator', name='bt_navigator',
             output='screen', respawn=True, respawn_delay=2.0,
             parameters=[params_file, {'use_sim_time': use_sim_time,
                                       'default_nav_to_pose_bt_xml': nav_to_pose_bt,
                                       'default_nav_through_poses_bt_xml': nav_through_poses_bt}],
             remappings=remappings),
        Node(package='nav2_waypoint_follower', executable='waypoint_follower',
             name='waypoint_follower', output='screen', respawn=True, respawn_delay=2.0,
             parameters=[params_file, {'use_sim_time': use_sim_time}], remappings=remappings),
        Node(package='nav2_velocity_smoother', executable='velocity_smoother',
             name='velocity_smoother', output='screen', respawn=True, respawn_delay=2.0,
             parameters=[params_file, {'use_sim_time': use_sim_time}],
             remappings=remappings + [('cmd_vel', 'cmd_vel_nav'),
                                      ('cmd_vel_smoothed', 'cmd_vel_safe')]),
    ])

    lifecycle_navigation = Node(
        package='nav2_lifecycle_manager', executable='lifecycle_manager',
        name='lifecycle_manager_navigation', output='screen',
        parameters=[{'use_sim_time': use_sim_time, 'autostart': True,
                     'node_names': navigation_nodes}])

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time', default_value='false',
            description='Use simulation (Gazebo/Isaac) clock if true'),
        DeclareLaunchArgument(
            'rsp', default_value='true',
            description='Publish /robot_description via base.launch.py. Set false when a '
                        'backend launch (Gazebo sim or wmx_ros2_control) already publishes it.'),
        start_base,
        map_server,
        amcl,
        nav_servers,
        lifecycle_localization,
        lifecycle_navigation,
    ])
