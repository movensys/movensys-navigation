import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode


def generate_launch_description():
    navigation_model = os.environ.get('NAVIGATION_MODEL', 'diffbot')
    perception_share = get_package_share_directory('movensys_navigation_perception')
    vslam_params = os.path.join(
        perception_share, 'config', navigation_model, 'cuvslam.yaml')

    use_sim_time = LaunchConfiguration('use_sim_time')

    camera_front = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(perception_share, 'launch', 'camera_front.launch.py')),
        launch_arguments={'use_sim_time': use_sim_time}.items(),
    )

    visual_slam_node = ComposableNode(
        name='visual_slam_node',
        package='isaac_ros_visual_slam',
        plugin='nvidia::isaac_ros::visual_slam::VisualSlamNode',
        parameters=[vslam_params, {'use_sim_time': use_sim_time}],
        remappings=[
            ('visual_slam/image_0', '/image_front_infra1/rgb'),
            ('visual_slam/camera_info_0', '/image_front_infra1/camera_info'),
            ('visual_slam/image_1', '/image_front_infra2/rgb'),
            ('visual_slam/camera_info_1', '/image_front_infra2/camera_info'),
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
        camera_front,
        visual_slam_container,
    ])
