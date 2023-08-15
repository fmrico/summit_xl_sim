import launch
import launch_ros
import os

from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

  use_sim_time = launch.substitutions.LaunchConfiguration('use_sim_time')
  world = launch.substitutions.LaunchConfiguration('world')

  ld = launch.LaunchDescription()

  ld.add_action(launch.actions.DeclareLaunchArgument(
    name='use_sim_time',
    description='Use simulation (Gazebo) clock if true',
    choices=['true', 'false'],
    default_value='true',
  ))

  ld.add_action(launch.actions.DeclareLaunchArgument(
    name='world',
    description='World to load',
    default_value=[launch_ros.substitutions.FindPackageShare('turtlebot3_gazebo'), '/worlds/', 'turtlebot3_house.world']
  ))

  
  summit_xl_gazebo = get_package_share_directory('summit_xl_gazebo')

  ld.add_action(launch.actions.IncludeLaunchDescription(
    PythonLaunchDescriptionSource(
      os.path.join(summit_xl_gazebo, 'launch', 'default.launch.py')
    ),
    launch_arguments={
      'verbose': 'false',
      'world': world,
      'use_sim_time': use_sim_time,
    }.items(),
  ))

  # Launch rviz
  start_rviz_cmd = Node(        
        package='rviz2',
        executable='rviz2',
        arguments=['-d', os.path.join(get_package_share_directory('summit_xl_navigation'), 'config_rviz', "nav2.rviz")],
        output='screen')
  ld.add_action(start_rviz_cmd)

  # Doesn't pass parameters properly
  # ld.add_action(launch.actions.IncludeLaunchDescription(
  #   PythonLaunchDescriptionSource(
  #     os.path.join(get_package_share_directory('summit_xl_navigation'), 'launch', 'nav2_bringup_launch.py')
  #   )
  # ))

  return ld