import math
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
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
        remappings=[
            ('realsense2_camera/infra1/image_rect_raw', '/image_front_infra1/rgb'),
            ('realsense2_camera/infra1/camera_info', '/image_front_infra1/camera_info'),
            ('realsense2_camera/infra2/image_rect_raw', '/image_front_infra2/rgb'),
            ('realsense2_camera/infra2/camera_info', '/image_front_infra2/camera_info'),
        ],
    )

    lidar_front_left_node = Node(
        package='sick_safetyscanners2',
        executable='sick_safetyscanners2_node',
        name='lidar_front_left_node',
        output='screen',
        emulate_tty=True,
        parameters=[
            {'frame_id': 'scan',
             'sensor_ip': '192.168.29.11',
             'host_ip': '192.168.29.44',
             'interface_ip': '0.0.0.0',
             'host_udp_port': 0,
             'channel': 0,
             'channel_enabled': True,
             'skip': 0,
             'angle_start': math.radians(-130),
             'angle_end': math.radians(130),
             'time_offset': 0.0,
             'general_system_state': True,
             'derived_settings': True,
             'measurement_data': True,
             'intrusion_data': True,
             'application_io_data': True,
             'use_persistent_config': False,
             'min_intensities': 0.0,
             'max_distance': 30}
        ],
    )

    lidar_rear_right_node = Node(
        package='sick_safetyscanners2',
        executable='sick_safetyscanners2_node',
        name='lidar_rear_right_node',
        output='screen',
        emulate_tty=True,
        parameters=[
            {'frame_id': 'scan',
             'sensor_ip': '192.168.29.12',
             'host_ip': '192.168.29.44',
             'interface_ip': '0.0.0.0',
             'host_udp_port': 0,
             'channel': 0,
             'channel_enabled': True,
             'skip': 0,
             'angle_start': math.radians(-130),
             'angle_end': math.radians(130),
             'time_offset': 0.0,
             'general_system_state': True,
             'derived_settings': True,
             'measurement_data': True,
             'intrusion_data': True,
             'application_io_data': True,
             'use_persistent_config': False,
             'min_intensities': 0.0,
             'max_distance': 30}
        ],
    )

    imu_node = Node(
        package='wheeltec_n100_imu',
        executable='imu_node',
        name='imu_node',
        output='screen',
        parameters=[
            {'serial_port': '/dev/ttyACM0',
             'serial_baud': 921600}
        ],
    )

    return LaunchDescription(
        [camera_front_node, lidar_front_left_node, lidar_rear_right_node, imu_node])
