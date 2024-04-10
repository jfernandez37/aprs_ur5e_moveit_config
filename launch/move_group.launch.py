from launch import LaunchDescription
from launch.actions import OpaqueFunction

from launch_ros.actions import Node

from moveit_configs_utils import MoveItConfigsBuilder

def launch_setup(context, *args, **kwargs):
    moveit_config = (
        MoveItConfigsBuilder("ur5e", package_name="aprs_ur5e_moveit_config")
        .robot_description(file_path="config/ur5e.urdf")
        .robot_description_semantic(file_path="config/ur5e.srdf")
        .trajectory_execution(file_path="config/controllers.yaml")
        .planning_pipelines(pipelines=["ompl"])
        .to_moveit_configs()
    )
    
    # Move group node
    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[
            moveit_config.to_dict()
        ],
    )   

    nodes_to_start = [
        move_group_node
    ]

    return nodes_to_start


def generate_launch_description():
    declared_arguments = []

    return LaunchDescription(declared_arguments + [OpaqueFunction(function=launch_setup)])