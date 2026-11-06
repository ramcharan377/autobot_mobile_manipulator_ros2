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

    package_name='autobot_description' 

    rviz_config_path = os.path.join(get_package_share_path('autobot_description'), 'rviz', 'urdf_config.rviz')

    set_gazebo_model_path = SetEnvironmentVariable(
    name='GAZEBO_MODEL_PATH',
    value=os.path.dirname(get_package_share_directory(package_name)) + ':' + os.environ.get('GAZEBO_MODEL_PATH', '')
    )

    set_ign_resource_path = SetEnvironmentVariable(
    name='IGN_GAZEBO_RESOURCE_PATH',
    value=os.path.dirname(get_package_share_directory(package_name)) + ':' + os.environ.get('IGN_GAZEBO_RESOURCE_PATH', '')
    )

    set_ign_resource_path = SetEnvironmentVariable(
    name='IGN_GAZEBO_RESOURCE_PATH',
    value=os.path.dirname(get_package_share_directory(package_name)) + ':' +
          os.path.join(get_package_share_directory(package_name), 'models') + ':' +
          os.environ.get('IGN_GAZEBO_RESOURCE_PATH', '')
    )




    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('autobot_description'),'launch','robot_state_publisher.launch.py'
                )]), launch_arguments={'use_sim_time': 'true', 'use_ros2_control': 'true'}.items()
    )

    joystick = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('autobot_joystick_node'),'launch','joystick.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    twist_mux_params = os.path.join(get_package_share_directory('autobot_controller'),'config','twist_mux.yaml')
    twist_mux = Node(
            package="twist_mux",
            executable="twist_mux",
            parameters=[twist_mux_params, {'use_sim_time': True}],
            remappings=[('/cmd_vel_out','/diff_cont/cmd_vel_unstamped')]
        )
    
    


    default_world = os.path.join(
        get_package_share_directory(package_name),
        'worlds',
        # 'empty.world',
        # 'small_warehouse.world',
        'hall1demo.world'
        )    
    
    world = LaunchConfiguration('world')

    world_arg = DeclareLaunchArgument(
        'world',
        default_value=default_world,
        description='World to load'
        )

    # Include the Gazebo launch file, provided by the ros_gz_sim package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]),
                    launch_arguments={'gz_args': ['-r -v4 ', world], 'on_exit_shutdown': 'true'}.items()
             )
    

    # Run the spawner node from the ros_gz_sim package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='ros_gz_sim', executable='create',
                        arguments=['-topic', 'robot_description',
                                   '-name', 'autobot',
                                   '-z', '0.1'],
                        output='screen')


    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_cont"],
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"],
    )


    bridge_params = os.path.join(get_package_share_directory('autobot_controller'),'config','gz_bridge.yaml')
    ros_gz_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            '--ros-args',
            '-p',
            f'config_file:={bridge_params}',
        ]
    )

    ros_gz_image_bridge = Node(
        package="ros_gz_image",
        executable="image_bridge",
        arguments=["/camera/image_raw"]
    )



    # # Code for delaying a node (I haven't tested how effective it is)
    # # 
    # # First add the below lines to imports
    # from launch.actions import RegisterEventHandler
    # from launch.event_handlers import OnProcessExit
    
    # # Then add the following below the current diff_drive_spawner
    # delayed_diff_drive_spawner = RegisterEventHandler(
    #     event_handler=OnProcessExit(
    #         target_action=spawn_entity,
    #         on_exit=[diff_drive_spawner],
    #     )
    # )
    # #
    # # Replace the diff_drive_spawner in the final return with delayed_diff_drive_spawner
    rviz2_node = Node(

        package="rviz2",
        executable="rviz2",
        arguments=['-d', rviz_config_path],
        parameters=[{'use_sim_time': True}]
    )


    # Launch them all!
    return LaunchDescription([
        set_gazebo_model_path,
        set_ign_resource_path,
        rsp,
        joystick,
        twist_mux,
        world_arg,
        gazebo,
        # spawn_entity,
        # diff_drive_spawner,
        # joint_broad_spawner,
        # ros_gz_bridge,
        # ros_gz_image_bridge,
        # rviz2_node
    ])
