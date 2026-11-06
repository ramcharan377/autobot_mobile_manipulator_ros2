# Validation Notes and Known Issues

## Known issues

- The combined Xacro model may produce a `link 'base_link' is not unique` warning depending on how the description is loaded. Ensure unique link names when expanding the URDF.
- The included combined MoveIt control Xacro uses `mock_components/GenericSystem`; it is a simulation/virtual controller configuration, not a physical arm driver.

## Before using the workspace

1. Build from a clean Ubuntu 22.04 + ROS 2 Humble environment.
2. Verify that the combined Xacro expands to a valid URDF with unique link names.
3. Confirm the transform tree continuously publishes for both the base and six-joint arm.
4. Confirm the Gazebo plugins and `ros2_control` controllers load successfully.
5. Align the Nav2 map with the selected Gazebo world and verify localization/navigation.
6. Treat physical ME6 control as a separate integration task; the included MoveIt fake system will not operate the actual robot.
7. Verify the target robot's physical emergency-stop and downstream safety mechanisms before any hardware motion.
