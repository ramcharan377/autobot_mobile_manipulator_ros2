# Package Inventory

| Package | Role in this repository | License |
|---|---|---|
| `autobot_description` | Mobile-base URDF/Xacro, meshes, Gazebo world/assets and RViz configurations | MIT |
| `autobot_controller` | Drive/controller, Gazebo bridge, SLAM Toolbox and Nav2 parameters; selected map pair | MIT |
| `autobot_bringup` | Simulation, base, camera, mapping, localization and Nav2 launch files | MIT |
| `autobot_me6_description` | Combined base + ME6 robot description, mount, simulation control Xacro | MIT |
| `autobot_me6_moveit` | Combined robot ME6 MoveIt planning and controller configuration | BSD |

## Dependencies kept external

`cra_description`, `dobot_rviz` and the related vendor packages are fetched from the official DOBOT ROS 2 V4 repository using `dobot-dependencies.repos`. `dobot_moveit`, `dobot_msgs_v4` and standalone `me6_moveit` are not duplicated in this project repository; they are available through the upstream dependency import if needed by that stack.
