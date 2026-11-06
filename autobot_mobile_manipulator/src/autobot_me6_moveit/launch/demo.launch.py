from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_demo_launch


def generate_launch_description():

    moveit_config = (
        MoveItConfigsBuilder(
            "me6_robot",
            package_name="autobot_me6_moveit"
        )
        .robot_description_kinematics(
            file_path="config/kinematics.yaml"
        )
        .trajectory_execution(
            file_path="config/moveit_controllers.yaml"
        )
        .to_moveit_configs()
    )

    # Allow small difference between planned start state
    # and current FakeSystem joint state
    moveit_config.trajectory_execution["trajectory_execution.allowed_start_tolerance"] = 0.1

    return generate_demo_launch(moveit_config)
