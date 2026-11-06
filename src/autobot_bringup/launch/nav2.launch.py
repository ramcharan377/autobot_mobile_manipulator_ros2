import os

from ament_index_python.packages import get_package_share_directory, get_package_share_path


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command

from launch_ros.actions import Node



def generate_launch_description():


    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    bringup_dir='autobot_bringup' 

    map_path = os.path.join(get_package_share_path('autobot_controller'), 'maps', 'small_warehouse_savee.yaml')
    rviz_config_path = os.path.join(get_package_share_path('autobot_description'), 'rviz', 'nav2_config.rviz')


    launch_sim = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(bringup_dir),'launch','launch_sim.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    localization_nav2 = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(bringup_dir),'launch','localization_launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )


    # Include the Gazebo launch file, provided by the ros_gz_sim package
    navigation_nav2 = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(bringup_dir),'launch','navigation_launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )



    rviz2_node = Node(

        package="rviz2",
        executable="rviz2",
        arguments=['-d', rviz_config_path],
        parameters=[{'use_sim_time': True}]
    )

    
    # Launch them all!
    return LaunchDescription([
        launch_sim,
        localization_nav2,
        navigation_nav2,
        rviz2_node
    ])
