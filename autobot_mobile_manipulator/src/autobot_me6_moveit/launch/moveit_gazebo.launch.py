from launch import LaunchDescription
from launch_ros.actions import Node

from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():

    moveit_config = (
        MoveItConfigsBuilder(
            "me6_robot",
            package_name="autobot_me6_moveit"
        )
        .robot_description(
            file_path="config/me6_robot.urdf.xacro"
        )
        .robot_description_semantic(
            file_path="config/me6_robot.srdf"
        )
        .robot_description_kinematics(
            file_path="config/kinematics.yaml"
        )
        .trajectory_execution(
            file_path="config/moveit_controllers.yaml"
        )
        .to_moveit_configs()
    )

    move_group = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[
            moveit_config.to_dict(),
            {
                "use_sim_time": True,
                "allow_trajectory_execution": True,
            },
        ],
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=[
            "-d",
            str(moveit_config.package_path / "config" / "moveit.rviz"),
        ],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
            {"use_sim_time": True},
        ],
    )

    return LaunchDescription([
        move_group,
        rviz,
    ])
