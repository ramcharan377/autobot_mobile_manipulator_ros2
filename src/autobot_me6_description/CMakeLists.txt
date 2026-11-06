cmake_minimum_required(VERSION 3.8)
project(autobot_me6_description)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY
    launch
    urdf
    rviz
    config
    scripts
  DESTINATION
    share/${PROJECT_NAME}
)

ament_package()