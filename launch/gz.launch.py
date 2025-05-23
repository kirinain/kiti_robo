#!/usr/bin/python3

from os.path import join
from xacro import parse, process_doc

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, Command
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory

def get_xacro_to_doc(xacro_file_path, mappings):
    doc = parse(open(xacro_file_path))
    process_doc(doc, mappings=mappings)
    return doc

def generate_launch_description():
    use_sim_time = LaunchConfiguration("use_sim_time", default=True)

    new_bcr_robot_path = get_package_share_directory("new_bcr_robot")
<<<<<<< HEAD
    world_file = LaunchConfiguration("world_file", default = "-r " + join(new_bcr_robot_path, "worlds", "gz", "empty.sdf"))
=======
    world_file = LaunchConfiguration("world_file", default = "-r " + join(new_bcr_robot_path, "worlds", "small_warehouse.sdf"))
>>>>>>> cdb37db (Updated chassis with logo, Imu always on, camera and Lidar as launch param)

    position_x = LaunchConfiguration("position_x")
    position_y = LaunchConfiguration("position_y")
    orientation_yaw = LaunchConfiguration("orientation_yaw")
    camera_enabled = LaunchConfiguration("camera_enabled", default=True)
    two_d_lidar_enabled = LaunchConfiguration("two_d_lidar_enabled", default=True)

<<<<<<< HEAD
    robot_description_content = get_xacro_to_doc(
        join(new_bcr_robot_path, "urdf", "new_bcr_robot.xacro"),
        {"wheel_odom_topic": "odom",
         "sim_gz": "true",
         "two_d_lidar_enabled": "true",
         "conveyor_enabled": "true",
         "camera_enabled": "true"
        }
    ).toxml()
=======
    # robot_description_content = get_xacro_to_doc(
    #     join(new_bcr_robot_path, "urdf", "new_bcr_robot.xacro"),
    #     {"sim_gz": "true",
    #      "two_d_lidar_enabled": "true",
    #      "conveyor_enabled": "false",
    #      "camera_enabled": "true"
    #     }
    # ).toxml()
>>>>>>> cdb37db (Updated chassis with logo, Imu always on, camera and Lidar as launch param)

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        parameters=[{"use_sim_time": use_sim_time},
                    {'robot_description': Command( \
                    ['xacro ', join(new_bcr_robot_path, 'urdf/new_bcr_robot.xacro'),
                    ' camera_enabled:=', camera_enabled,
                    ' two_d_lidar_enabled:=', two_d_lidar_enabled,
                    ' sim_gz:=', "true"
                    ])}]
    )
 
    gz_sim_share = get_package_share_directory("ros_gz_sim")
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(join(gz_sim_share, "launch", "gz_sim.launch.py")),
        launch_arguments={
            "gz_args" : world_file
        }.items()
    )

    gz_spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-topic", "/robot_description",
            "-name", "new_bcr_robot",
            "-allow_renaming", "true",
            "-z", "0.28",
            "-x", position_x,
            "-y", position_y,
            "-Y", orientation_yaw
        ]
    )

    gz_ros2_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            "/cmd_vel@geometry_msgs/msg/Twist@ignition.msgs.Twist",
            "/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock",
            "/odom@nav_msgs/msg/Odometry[ignition.msgs.Odometry",
            "/tf@tf2_msgs/msg/TFMessage[ignition.msgs.Pose_V",
            "/scan@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan",
            "/depth_camera@sensor_msgs/msg/Image[ignition.msgs.Image",
            "/camera_info@sensor_msgs/msg/CameraInfo[ignition.msgs.CameraInfo",
            "/depth_camera/points@sensor_msgs/msg/PointCloud2[ignition.msgs.PointCloudPacked",
            "/imu@sensor_msgs/msg/Imu[ignition.msgs.IMU",
        ],
    )

    return LaunchDescription([
        DeclareLaunchArgument("use_sim_time", default_value=use_sim_time),
        DeclareLaunchArgument("world_file", default_value=world_file),
        DeclareLaunchArgument("camera_enabled", default_value = camera_enabled),
        DeclareLaunchArgument("two_d_lidar_enabled", default_value = two_d_lidar_enabled),
        DeclareLaunchArgument("position_x", default_value="0.0"),
        DeclareLaunchArgument("position_y", default_value="0.0"),
        DeclareLaunchArgument("orientation_yaw", default_value="0.0"),        
        robot_state_publisher,
        gz_sim, gz_spawn_entity, gz_ros2_bridge
    ])