---
title: Exercise - Creating Your First URDF Robot Model
sidebar_label: Exercise - URDF Creation
sidebar_position: 4
description: Practical exercise creating a complete robot model using URDF
tags: [urdf, exercise, robot, modeling, simulation]
---

# Exercise - Creating Your First URDF Robot Model

## Overview
In this exercise, you will create a complete robot model using URDF from scratch. You'll define the robot's structure, specify visual and collision properties, and prepare it for simulation. This hands-on exercise will reinforce your understanding of URDF concepts and best practices.

## Prerequisites
- Understanding of URDF fundamentals (covered in previous chapters)
- Basic XML syntax knowledge
- Access to ROS 2 environment with URDF tools
- Text editor for creating URDF files

## Learning Objectives
- Create a complete robot model using URDF
- Define links with appropriate visual, collision, and inertial properties
- Establish proper joint connections between links
- Validate the URDF model
- Visualize the robot in RViz

## Exercise Steps

### Step 1: Define the Robot Structure
Create a simple differential drive robot with the following specifications:
- Base link (main chassis)
- Two wheel links (left and right)
- Two wheel joints (connecting wheels to base)

Create a new file called `my_robot.urdf`:

```xml
<?xml version="1.0"?>
<robot name="my_robot">
  <!-- Base link definition -->
  <link name="base_link">
    <visual>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <box size="0.5 0.3 0.15"/>
      </geometry>
      <material name="light_grey">
        <color rgba="0.7 0.7 0.7 1.0"/>
      </material>
    </visual>

    <collision>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <box size="0.5 0.3 0.15"/>
      </geometry>
    </collision>

    <inertial>
      <mass value="2.0"/>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <inertia
        ixx="0.02708"
        ixy="0.0"
        ixz="0.0"
        iyy="0.05417"
        iyz="0.0"
        izz="0.075"/>
    </inertial>
  </link>
</robot>
```

### Step 2: Add Wheel Links
Add the left and right wheel links to your URDF file:

```xml
  <!-- Left wheel -->
  <link name="left_wheel">
    <visual>
      <origin xyz="0 0 0" rpy="1.5708 0 0"/>
      <geometry>
        <cylinder radius="0.075" length="0.05"/>
      </geometry>
      <material name="black">
        <color rgba="0.1 0.1 0.1 1.0"/>
      </material>
    </visual>

    <collision>
      <origin xyz="0 0 0" rpy="1.5708 0 0"/>
      <geometry>
        <cylinder radius="0.075" length="0.05"/>
      </geometry>
    </collision>

    <inertial>
      <mass value="0.3"/>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <inertia
        ixx="0.00053"
        ixy="0.0"
        ixz="0.0"
        iyy="0.00053"
        iyz="0.0"
        izz="0.00084"/>
    </inertial>
  </link>

  <!-- Right wheel -->
  <link name="right_wheel">
    <visual>
      <origin xyz="0 0 0" rpy="1.5708 0 0"/>
      <geometry>
        <cylinder radius="0.075" length="0.05"/>
      </geometry>
      <material name="black">
        <color rgba="0.1 0.1 0.1 1.0"/>
      </material>
    </visual>

    <collision>
      <origin xyz="0 0 0" rpy="1.5708 0 0"/>
      <geometry>
        <cylinder radius="0.075" length="0.05"/>
      </geometry>
    </collision>

    <inertial>
      <mass value="0.3"/>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <inertia
        ixx="0.00053"
        ixy="0.0"
        ixz="0.0"
        iyy="0.00053"
        iyz="0.0"
        izz="0.00084"/>
    </inertial>
  </link>
```

### Step 3: Define Joints
Add the joints that connect the wheels to the base:

```xml
  <!-- Left wheel joint -->
  <joint name="left_wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child link="left_wheel"/>
    <origin xyz="0 0.175 -0.075" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <dynamics damping="0.1" friction="0.01"/>
  </joint>

  <!-- Right wheel joint -->
  <joint name="right_wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child link="right_wheel"/>
    <origin xyz="0 -0.175 -0.075" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <dynamics damping="0.1" friction="0.01"/>
  </joint>
```

### Step 4: Add Materials Definition
Add a materials section to your URDF:

```xml
  <!-- Materials -->
  <material name="light_grey">
    <color rgba="0.7 0.7 0.7 1.0"/>
  </material>

  <material name="black">
    <color rgba="0.1 0.1 0.1 1.0"/>
  </material>

  <material name="red">
    <color rgba="0.8 0.2 0.2 1.0"/>
  </material>
```

### Step 5: Complete URDF File
Your complete URDF file should look like this:

```xml
<?xml version="1.0"?>
<robot name="my_robot">
  <!-- Materials -->
  <material name="light_grey">
    <color rgba="0.7 0.7 0.7 1.0"/>
  </material>

  <material name="black">
    <color rgba="0.1 0.1 0.1 1.0"/>
  </material>

  <material name="red">
    <color rgba="0.8 0.2 0.2 1.0"/>
  </material>

  <!-- Base link definition -->
  <link name="base_link">
    <visual>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <box size="0.5 0.3 0.15"/>
      </geometry>
      <material name="light_grey">
        <color rgba="0.7 0.7 0.7 1.0"/>
      </material>
    </visual>

    <collision>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <box size="0.5 0.3 0.15"/>
      </geometry>
    </collision>

    <inertial>
      <mass value="2.0"/>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <inertia
        ixx="0.02708"
        ixy="0.0"
        ixz="0.0"
        iyy="0.05417"
        iyz="0.0"
        izz="0.075"/>
    </inertial>
  </link>

  <!-- Left wheel -->
  <link name="left_wheel">
    <visual>
      <origin xyz="0 0 0" rpy="1.5708 0 0"/>
      <geometry>
        <cylinder radius="0.075" length="0.05"/>
      </geometry>
      <material name="black">
        <color rgba="0.1 0.1 0.1 1.0"/>
      </material>
    </visual>

    <collision>
      <origin xyz="0 0 0" rpy="1.5708 0 0"/>
      <geometry>
        <cylinder radius="0.075" length="0.05"/>
      </geometry>
    </collision>

    <inertial>
      <mass value="0.3"/>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <inertia
        ixx="0.00053"
        ixy="0.0"
        ixz="0.0"
        iyy="0.00053"
        iyz="0.0"
        izz="0.00084"/>
    </inertial>
  </link>

  <!-- Right wheel -->
  <link name="right_wheel">
    <visual>
      <origin xyz="0 0 0" rpy="1.5708 0 0"/>
      <geometry>
        <cylinder radius="0.075" length="0.05"/>
      </geometry>
      <material name="black">
        <color rgba="0.1 0.1 0.1 1.0"/>
      </material>
    </visual>

    <collision>
      <origin xyz="0 0 0" rpy="1.5708 0 0"/>
      <geometry>
        <cylinder radius="0.075" length="0.05"/>
      </geometry>
    </collision>

    <inertial>
      <mass value="0.3"/>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <inertia
        ixx="0.00053"
        ixy="0.0"
        ixz="0.0"
        iyy="0.00053"
        iyz="0.0"
        izz="0.00084"/>
    </inertial>
  </link>

  <!-- Left wheel joint -->
  <joint name="left_wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child link="left_wheel"/>
    <origin xyz="0 0.175 -0.075" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <dynamics damping="0.1" friction="0.01"/>
  </joint>

  <!-- Right wheel joint -->
  <joint name="right_wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child link="right_wheel"/>
    <origin xyz="0 -0.175 -0.075" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <dynamics damping="0.1" friction="0.01"/>
  </joint>
</robot>
```

### Step 6: Validate Your URDF
Save your URDF file and validate it using the command line:

```bash
# Assuming your file is saved as my_robot.urdf
check_urdf my_robot.urdf
```

This command will check for syntax errors and structural issues in your URDF.

### Step 7: Visualize the Robot
Visualize your robot in RViz to verify its structure:

1. Launch RViz:
```bash
ros2 run rviz2 rviz2
```

2. In RViz, add a RobotModel display:
   - Click "Add" in the Displays panel
   - Select "RobotModel" under "Robot Models"
   - Set the "Robot Description" parameter to point to your URDF file

Alternatively, you can use a simple launch file to visualize:

```xml
<!-- robot_state_publisher_launch.py -->
import launch
from launch.substitutions import Command, LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Get the URDF file path
    urdf_file = os.path.join(
        get_package_share_directory('your_package_name'),
        'urdf',
        'my_robot.urdf'
    )

    # Launch the robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[
            {'robot_description': Command(['xacro ', urdf_file])}
        ]
    )

    # Launch RViz
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen'
    )

    return launch.LaunchDescription([
        robot_state_publisher,
        rviz
    ])
```

### Step 8: Add Gazebo Integration (Optional)
To make your robot ready for simulation in Gazebo, add the following Gazebo-specific elements to your URDF:

```xml
  <!-- Gazebo plugin for differential drive -->
  <gazebo>
    <plugin name="diff_drive" filename="libgazebo_ros_diff_drive.so">
      <ros>
        <namespace>my_robot</namespace>
        <remapping>cmd_vel:=cmd_vel</remapping>
        <remapping>odom:=odom</remapping>
      </ros>
      <update_rate>30</update_rate>
      <left_joint>left_wheel_joint</left_joint>
      <right_joint>right_wheel_joint</right_joint>
      <wheel_separation>0.35</wheel_separation>
      <wheel_diameter>0.15</wheel_diameter>
      <max_wheel_torque>20</max_wheel_torque>
      <max_wheel_acceleration>1.0</max_wheel_acceleration>
      <command_topic>cmd_vel</command_topic>
      <odometry_topic>odom</odometry_topic>
      <odometry_frame>odom</odometry_frame>
      <robot_base_frame>base_link</robot_base_frame>
    </plugin>
  </gazebo>

  <!-- Gazebo materials -->
  <gazebo reference="base_link">
    <material>Gazebo/Grey</material>
  </gazebo>

  <gazebo reference="left_wheel">
    <material>Gazebo/Black</material>
  </gazebo>

  <gazebo reference="right_wheel">
    <material>Gazebo/Black</material>
  </gazebo>
```

## Expected Outcomes
- Successful validation of your URDF file with `check_urdf`
- Proper visualization of your robot model in RViz
- Understanding of how to structure a complete robot model
- Knowledge of best practices for URDF creation

## Troubleshooting Tips
- If validation fails, check for missing closing tags or incorrect attribute values
- If visualization doesn't work, ensure all links are properly connected through joints
- If physics simulation is unstable, verify inertial properties are realistic
- Use simple geometric shapes initially, then add complexity

## Extensions
1. Add a caster wheel for better stability
2. Include a simple sensor (e.g., IMU or camera) in your model
3. Create a more complex robot with multiple degrees of freedom
4. Use Xacro to parameterize your URDF for easier modification

## Resources
- [ROS URDF Tutorials](http://wiki.ros.org/urdf/Tutorials)
- [Gazebo Robot Simulation](http://gazebosim.org/tutorials?tut=ros2_robot_spawn)
- [URDF Best Practices](http://wiki.ros.org/urdf/XML)