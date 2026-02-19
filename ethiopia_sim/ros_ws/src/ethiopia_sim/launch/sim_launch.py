import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    pkg_share = get_package_share_directory("ethiopia_sim")

    # Paths to assets installed with the package
    world_file_path = os.path.join(pkg_share, "worlds", "ethiopia.world")
    urdf_file_path = os.path.join(pkg_share, "urdf", "three_wheel_robot.urdf")

    with open(urdf_file_path, "r") as infp:
        robot_desc = infp.read()

    # Start Gazebo (Gazebo Sim) via ros_gz_sim using our custom world.
    # This assumes `ros-jazzy-ros-gz` is installed.
    #
    # `gz_sim.launch.py` starts both server + GUI; `-r` starts running immediately.
    gz_sim = ExecuteProcess(
        cmd=[
            "ros2",
            "launch",
            "ros_gz_sim",
            "gz_sim.launch.py",
            f"gz_args:={world_file_path} -r",
        ],
        output="screen",
    )

    # Publish the robot description on the parameter for downstream nodes.
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_desc}],
    )

    # Note: Spawning the URDF into Gazebo Sim can be done with
    # `ros_gz_sim create` or a dedicated spawn node, but the exact
    # interface can vary. For now we run the world and state publisher,
    # which is enough for the search/navigator nodes to function.

    return LaunchDescription(
        [
            gz_sim,
            robot_state_publisher,
        ]
    )
