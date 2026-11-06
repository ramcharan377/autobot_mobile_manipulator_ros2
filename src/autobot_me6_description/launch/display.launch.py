from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    use_gui = LaunchConfiguration("gui")

    pkg_share = get_package_share_directory("autobot_me6_description")

    xacro_file = os.path.join(
        pkg_share,
        "urdf",
        "autobot_me6.urdf.xacro"
    )

    robot_description = {
        "robot_description": Command(
            [
                "xacro ",
                xacro_file,
            ]
        )
    }

    return LaunchDescription([

        DeclareLaunchArgument(
            "gui",
            default_value="true"
        ),

        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[robot_description],
            output="screen"
        ),

        Node(
            package="joint_state_publisher_gui",
            executable="joint_state_publisher_gui",
            condition=None,
            output="screen"
        ),

        Node(
            package="rviz2",
            executable="rviz2",
            output="screen"
        )

    ])
