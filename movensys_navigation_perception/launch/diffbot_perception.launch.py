import math

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    lidar_front_left_node = Node(
        package='sick_safetyscanners2',
        executable='sick_safetyscanners2_node',
        name='lidar_front_left_node',
        output='screen',
        emulate_tty=True,
        parameters=[
            {"frame_id": "scan",
             "sensor_ip": "192.168.29.11",
             "host_ip": "192.168.29.44",
             "interface_ip": "0.0.0.0",
             "host_udp_port": 0,
             "channel": 0,
             "channel_enabled": True,
             "skip": 0,
             "angle_start": math.radians(-130),
             "angle_end": math.radians(130),
             "time_offset": 0.0,
             "general_system_state": True,
             "derived_settings": True,
             "measurement_data": True,
             "intrusion_data": True,
             "application_io_data": True,
             "use_persistent_config": False,
             "min_intensities": 0.0,
             "max_distance": 30}
        ],
    )

    lidar_rear_right_node = Node(
        package='sick_safetyscanners2',
        executable='sick_safetyscanners2_node',
        name='lidar_rear_right_node',
        output='screen',
        emulate_tty=True,
        parameters=[
            {"frame_id": "scan",
             "sensor_ip": "192.168.29.12",
             "host_ip": "192.168.29.44",
             "interface_ip": "0.0.0.0",
             "host_udp_port": 0,
             "channel": 0,
             "channel_enabled": True,
             "skip": 0,
             "angle_start": math.radians(-130),
             "angle_end": math.radians(130),
             "time_offset": 0.0,
             "general_system_state": True,
             "derived_settings": True,
             "measurement_data": True,
             "intrusion_data": True,
             "application_io_data": True,
             "use_persistent_config": False,
             "min_intensities": 0.0,
             "max_distance": 30}
        ],
    )

    imu_node = Node(
        package='wheeltec_n100_imu',
        executable='imu_node',
        name='imu_node',
        output='screen',
        parameters=[
            {"serial_port": "/dev/ttyACM0",
             "serial_baud": 921600}
        ],
    )

    return LaunchDescription(
        [lidar_front_left_node, lidar_rear_right_node, imu_node])
