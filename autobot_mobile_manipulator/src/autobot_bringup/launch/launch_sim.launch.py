import os

from ament_index_python.packages import get_package_share_directory, get_package_share_path


from launch import LaunchDescription
from launch.actions import (
    IncludeLaunchDescription,
    DeclareLaunchArgument,
    SetEnvironmentVariable,
    RegisterEventHandler,
)

from launch.event_handlers import OnProcessExit
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

    # set_ign_resource_path = SetEnvironmentVariable(
    # name='IGN_GAZEBO_RESOURCE_PATH',
    # value=os.path.dirname(get_package_share_directory(package_name)) + ':' + os.environ.get('IGN_GAZEBO_RESOURCE_PATH', '')
    # )

    # set_ign_resource_path = SetEnvironmentVariable(
    # name='IGN_GAZEBO_RESOURCE_PATH',
    #       os.environ.get('IGN_GAZEBO_RESOURCE_PATH', '')
    # )     
    set_ign_resource_path = SetEnvironmentVariable(
        name='IGN_GAZEBO_RESOURCE_PATH',
        value=os.path.dirname(get_package_share_directory('autobot_description')) + ':' +
              os.path.dirname(get_package_share_directory('cra_description')) + ':' +
              os.path.join(get_package_share_directory('autobot_description'), 'models') + ':' +
              os.environ.get('IGN_GAZEBO_RESOURCE_PATH', '')
    )

    # Build a list of paths you want to include:
    # paths = [
    #     os.path.dirname(get_package_share_directory(package_name)),
    # ]

    # # Append any existing value for IGN_GAZEBO_RESOURCE_PATH (if present)
    # existing = os.environ.get('IGN_GAZEBO_RESOURCE_PATH', '')
    # if existing:
    #     paths.append(existing)

    # # Join all paths with colons
    # combined_paths = ':'.join(paths)

    # set_ign_resource_path = SetEnvironmentVariable(
    #     name='IGN_GAZEBO_RESOURCE_PATH',
    #     value=combined_paths
    # )


    # # Get the share directory for the package.
    # # For example, this might be:
    # package_share = get_package_share_directory(package_name)

    # # Option 1: Use the parent directory of package_share.
    # parent_dir = os.path.dirname(package_share)
    # # Option 2: Use the package_share itself.
    # # Uncomment the following line if you prefer to use package_share directly.
    # # parent_dir = package_share

    # # Define the models directory path.
    # models_dir = os.path.join(package_share, 'models')

    # # Get any existing value for IGN_GAZEBO_RESOURCE_PATH.
    # existing = os.environ.get('IGN_GAZEBO_RESOURCE_PATH', '')

    # # Combine the paths, separated by colons.
    # combined_paths = parent_dir + ':' + models_dir
    # if existing:
    #     combined_paths += ':' + existing

    # # (Optional) Print the combined paths to debug.
    # print("Combined IGN_GAZEBO_RESOURCE_PATH =", combined_paths)

    # set_ign_resource_path = SetEnvironmentVariable(
    #     name='IGN_GAZEBO_RESOURCE_PATH',
    #     value=combined_paths
    # )






    # Complete Edubot + ME6 robot description
    combined_xacro = os.path.join(
        get_package_share_directory('autobot_me6_description'),
        'urdf',
        'autobot_me6_sim.urdf.xacro'
    )

    robot_description = Command([
        'xacro ',
        combined_xacro
    ])

    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True
        }]
    )

# DISABLED_JOYSTICK:     joystick = IncludeLaunchDescription(
# DISABLED_JOYSTICK:                 PythonLaunchDescriptionSource([os.path.join(
# DISABLED_JOYSTICK:                     get_package_share_directory('autobot_joystick_node'),'launch','joystick.launch.py'
# DISABLED_JOYSTICK:                 )]), launch_arguments={'use_sim_time': 'true'}.items()
# DISABLED_JOYSTICK:     )

    twist_mux_params = os.path.join(get_package_share_directory('autobot_controller'),'config','twist_mux.yaml')
    twist_mux = Node(
            package="twist_mux",
            executable="twist_mux",
            parameters=[twist_mux_params, {'use_sim_time': True}],
            remappings=[('/cmd_vel_out','/diff_cont/cmd_vel_unstamped')]
        )
    
    


    default_world = os.path.join(
        get_package_share_directory('autobot_description'),
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
                                #    '-x', '-1.2',  # x in meters
                                #    '-y', '-0.85', # y in meters
                                #    '-z', '0.1',   # z in meters
                                #    '-R', '0.0',   # R(Roll) in rad
                                #    '-P', '0.0',   # P(Pitch) in rad
                                #    '-Y', '0.0',  # Y(Yaw) in rad  
                                    '-x', '1.8',  # x in meters
                                    '-y', '7.0', # y in meters
                                    '-z', '0.01',   # z in meters
                                    '-R', '0.0',   # R(Roll) in rad
                                    '-P', '0.0',   # P(Pitch) in rad
                                    '-Y', '-1.57',  # Y(Yaw) in rad
                                   ],
                        output='screen')


    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"],
    )

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_cont"],
    )

    me6_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["me6_group_controller"],
    )

    delayed_joint_broad_spawner = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_entity,
            on_exit=[joint_broad_spawner],
        )
    )

    delayed_diff_drive_spawner = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=joint_broad_spawner,
            on_exit=[diff_drive_spawner],
        )
    )


    delayed_me6_controller_spawner = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=diff_drive_spawner,
            on_exit=[me6_controller_spawner],
        )
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
        # set_gazebo_model_path,
        set_ign_resource_path,
        rsp,
# DISABLED_JOYSTICK: joystick,
        twist_mux,
        world_arg,
        gazebo,
        spawn_entity,
        delayed_diff_drive_spawner,
        delayed_joint_broad_spawner,
        delayed_me6_controller_spawner,
        ros_gz_bridge,
        ros_gz_image_bridge,
        # rviz2_node
    ])
