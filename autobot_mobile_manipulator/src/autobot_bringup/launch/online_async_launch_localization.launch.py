import os
import yaml

from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    config_dir = get_package_share_directory('autobot_controller')

    # Workspace root is 4 levels up from the installed package share directory:
    # <ws>/install/<pkg>/share/<pkg>  →  up 4  →  <ws>
    ws_root = os.path.normpath(os.path.join(config_dir, '..', '..', '..', '..'))
    ws_config_path = os.path.join(ws_root, 'config.yaml')

    with open(ws_config_path, 'r') as f:
        ws_config = yaml.safe_load(f)

    map_name = ws_config.get('map_name', 'hall1demo_serial')
    map_file_path = os.path.join(config_dir, 'maps', map_name)

    slam_toolbox_node = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        parameters=[
            os.path.join(config_dir, 'config', 'mapper_params_online_async_localization.yaml'),
            {'use_sim_time': True, 'map_file_name': map_file_path}
        ]
    )

    return LaunchDescription([slam_toolbox_node])
