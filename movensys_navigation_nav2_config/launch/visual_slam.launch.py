import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import ComposableNodeContainer, Node
from launch_ros.descriptions import ComposableNode


def generate_launch_description():
    navigation_model = os.environ.get('NAVIGATION_MODEL', 'diffbot')
    nav2_config_share = get_package_share_directory('movensys_navigation_nav2_config')
    vslam_params = os.path.join(
        nav2_config_share, 'config', navigation_model, 'visual_slam.yaml')

    use_sim_time = LaunchConfiguration('use_sim_time')
    launch_realsense = LaunchConfiguration('launch_realsense')

    realsense_node = Node(
        package='realsense2_camera',
        executable='realsense2_camera_node',
        namespace='camera',
        name='camera',
        output='screen',
        condition=IfCondition(launch_realsense),
        parameters=[{
            'enable_infra1': True,
            'enable_infra2': True,
            'enable_color': False,
            'enable_depth': False,
            'depth_module.emitter_enabled': 0,
            'depth_module.profile': '640x360x90',
            'enable_gyro': True,
            'enable_accel': True,
            'gyro_fps': 200,
            'accel_fps': 200,
            'unite_imu_method': 2,      # 2 = linear interpolation -> /camera/imu
            'enable_sync': True,
        }],
    )

    # --- cuVSLAM (Isaac ROS Visual SLAM) ---
    visual_slam_node = ComposableNode(
        name='visual_slam_node',
        package='isaac_ros_visual_slam',
        plugin='nvidia::isaac_ros::visual_slam::VisualSlamNode',
        parameters=[vslam_params, {'use_sim_time': use_sim_time}],
        remappings=[
            ('visual_slam/image_0', '/camera/infra1/image_rect_raw'),
            ('visual_slam/camera_info_0', '/camera/infra1/camera_info'),
            ('visual_slam/image_1', '/camera/infra2/image_rect_raw'),
            ('visual_slam/camera_info_1', '/camera/infra2/camera_info'),
            ('visual_slam/imu', '/camera/imu'),
        ],
    )

    visual_slam_container = ComposableNodeContainer(
        name='visual_slam_container',
        namespace='',
        package='rclcpp_components',
        executable='component_container_mt',
        composable_node_descriptions=[visual_slam_node],
        output='screen',
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo/Isaac) clock if true',
        ),
        DeclareLaunchArgument(
            'launch_realsense',
            default_value='true',
            description='Start the realsense2_camera driver here. Set false to feed '
                        'cuVSLAM from another stereo source (e.g. Isaac Sim).',
        ),
        realsense_node,
        visual_slam_container,
    ])
