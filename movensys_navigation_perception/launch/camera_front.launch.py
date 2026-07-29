import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    use_sim_time_arg = DeclareLaunchArgument(
        "use_sim_time", default_value="false",
        description="Use simulation clock (/clock)"
    )

    pkg_share = get_package_share_directory('movensys_navigation_perception')
    navigation_model = os.environ.get('NAVIGATION_MODEL', 'diffbot')
    realsense_config = os.path.join(pkg_share, 'config', navigation_model,
                                    'realsense_front.yaml')

    camera_front_node = Node(
        package='realsense2_camera',
        executable='realsense2_camera_node',
        name='realsense2_camera',
        namespace='camera_front',
        parameters=[realsense_config],
        output='screen',
        condition=UnlessCondition(LaunchConfiguration('use_sim_time')),
        remappings=[
            ('realsense2_camera/infra1/image_rect_raw', '/image_front_infra1/rgb'),
            ('realsense2_camera/infra1/camera_info', '/image_front_infra1/camera_info'),
            ('realsense2_camera/infra2/image_rect_raw', '/image_front_infra2/rgb'),
            ('realsense2_camera/infra2/camera_info', '/image_front_infra2/camera_info'),
        ],
    )

    # Both run at once under sim, so each needs its own node name.
    start_camera_front_left_transform_simulation = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="camera_front_infra1_tf",
        output="log",
        condition=IfCondition(LaunchConfiguration("use_sim_time")),
        parameters=[{"use_sim_time": True}],
        arguments=[
            "--frame-id", "base_link",
            "--child-frame-id", "camera_front_infra1_optical_frame",
            "--x", "0.4",
            "--y", "0.0",
            "--z", "0.17",
            "--roll", "-1.5707963",
            "--pitch", "0.0",
            "--yaw", "-1.5707963",
        ],
    )

    start_camera_front_right_transform_simulation = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="camera_front_infra2_tf",
        output="log",
        condition=IfCondition(LaunchConfiguration("use_sim_time")),
        parameters=[{"use_sim_time": True}],
        arguments=[
            "--frame-id", "base_link",
            "--child-frame-id", "camera_front_infra2_optical_frame",
            "--x", "0.4",
            "--y", "-0.095",     
            "--z", "0.17",
            "--roll", "-1.5707963",
            "--pitch", "0.0",
            "--yaw", "-1.5707963",
        ],
    )

    return LaunchDescription([
        use_sim_time_arg,
        camera_front_node,
        start_camera_front_left_transform_simulation,
        start_camera_front_right_transform_simulation,
    ])
