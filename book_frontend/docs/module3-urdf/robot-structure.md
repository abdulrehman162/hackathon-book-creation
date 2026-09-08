---
title: Robot Structure Definition with URDF
sidebar_label: Robot Structure
sidebar_position: 1
description: Understanding the fundamental components of robot structure definition using URDF
tags: [urdf, robot, structure, links, joints, modeling]
---

# Robot Structure Definition with URDF

## Overview

This chapter covers the fundamental concepts of defining robot structures using the Unified Robot Description Format (URDF). URDF is an XML-based format that describes robot models, including their physical and visual properties, kinematic structure, and other characteristics necessary for simulation and control.

## URDF Basics

### What is URDF?

URDF (Unified Robot Description Format) is an XML format used in ROS to describe robot models. It defines the physical structure of a robot, including:

- **Links**: Rigid parts of the robot (e.g., chassis, arms, wheels)
- **Joints**: Connections between links that allow relative motion
- **Visual properties**: How the robot appears in visualization tools
- **Collision properties**: How the robot interacts with the environment in simulation
- **Inertial properties**: Mass, center of mass, and inertia for physics simulation

### Basic URDF Structure

A basic URDF file has the following structure:

```xml
<?xml version="1.0"?>
<robot name="my_robot">
  <!-- Links definition -->
  <link name="base_link">
    <visual>
      <geometry>
        <cylinder length="0.6" radius="0.2"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.6" radius="0.2"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="10"/>
      <inertia ixx="1.0" ixy="0.0" ixz="0.0" iyy="1.0" iyz="0.0" izz="1.0"/>
    </inertial>
  </link>

  <!-- Joints definition -->
  <joint name="base_to_wheel" type="continuous">
    <parent link="base_link"/>
    <child link="wheel_link"/>
    <origin xyz="0 0.25 0" rpy="0 0 0"/>
  </joint>

  <link name="wheel_link">
    <visual>
      <geometry>
        <cylinder length="0.1" radius="0.1"/>
      </geometry>
    </visual>
  </link>
</robot>
```

## Links in URDF

### Link Components

A link in URDF represents a rigid body and can contain several sub-elements:

#### Visual Element
Describes how the link appears in visualization tools:

```xml
<visual>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <geometry>
    <!-- Geometry type: box, cylinder, sphere, or mesh -->
    <box size="1.0 0.5 0.3"/>
  </geometry>
  <material name="blue">
    <color rgba="0 0 1 1"/>
  </material>
</visual>
```

#### Collision Element
Defines the collision properties for physics simulation:

```xml
<collision>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <geometry>
    <box size="1.0 0.5 0.3"/>
  </geometry>
</collision>
```

#### Inertial Element
Specifies the physical properties for dynamics simulation:

```xml
<inertial>
  <mass value="1.0"/>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <inertia ixx="1.0" ixy="0.0" ixz="0.0" iyy="1.0" iyz="0.0" izz="1.0"/>
</inertial>
```

## Joints in URDF

Joints define the connection between links and specify the allowed motion:

### Joint Types

1. **revolute**: Rotational joint with limited range
2. **continuous**: Rotational joint without limits
3. **prismatic**: Linear sliding joint with limits
4. **fixed**: No relative motion between links
5. **floating**: 6 DOF motion (rarely used)
6. **planar**: Motion in a plane

### Joint Definition Example

```xml
<joint name="joint_name" type="revolute">
  <parent link="parent_link_name"/>
  <child link="child_link_name"/>
  <origin xyz="1.0 0 0" rpy="0 0 0"/>
  <axis xyz="0 0 1"/>
  <limit lower="-1.57" upper="1.57" effort="10.0" velocity="1.0"/>
  <dynamics damping="0.5" friction="0.1"/>
</joint>
```

## Advanced URDF Features

### Materials

Define reusable materials for visual elements:

```xml
<material name="red">
  <color rgba="1 0 0 1"/>
</material>

<material name="blue">
  <color rgba="0 0 1 1"/>
</material>
```

### Transmission Elements

Define how joints are controlled by actuators:

```xml
<transmission name="tran1">
  <type>transmission_interface/SimpleTransmission</type>
  <joint name="joint1">
    <hardwareInterface>hardware_interface/EffortJointInterface</hardwareInterface>
  </joint>
  <actuator name="motor1">
    <hardwareInterface>hardware_interface/EffortJointInterface</hardwareInterface>
    <mechanicalReduction>1</mechanicalReduction>
  </actuator>
</transmission>
```

### Gazebo-Specific Elements

Include Gazebo-specific properties:

```xml
<gazebo reference="link_name">
  <material>Gazebo/Blue</material>
  <mu1>0.2</mu1>
  <mu2>0.2</mu2>
</gazebo>
```

## Best Practices

### 1. Use Descriptive Names
Use clear, consistent naming conventions for links and joints to make the URDF more maintainable.

### 2. Organize Complex Models
For complex robots, break the URDF into multiple files and use xacro for parameterization.

### 3. Validate URDF
Always validate your URDF files using tools like `check_urdf`:

```bash
check_urdf /path/to/robot.urdf
```

### 4. Start Simple
Begin with a simple model and gradually add complexity to avoid debugging complex issues.

## Common URDF Issues and Solutions

### 1. Floating Point Precision
Use appropriate precision for numerical values to avoid simulation instabilities.

### 2. Inertial Properties
Ensure inertial properties are physically realistic to prevent simulation problems.

### 3. Joint Limits
Define appropriate joint limits to prevent kinematic issues.

### 4. Parent-Child Relationships
Ensure all joints have properly defined parent and child links.

## Example: Simple Mobile Robot

Here's a complete example of a simple mobile robot URDF:

```xml
<?xml version="1.0"?>
<robot name="simple_robot">
  <!-- Base link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.5 0.3 0.1"/>
      </geometry>
      <material name="white">
        <color rgba="1 1 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.5 0.3 0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.01"/>
    </inertial>
  </link>

  <!-- Wheels -->
  <link name="left_wheel">
    <visual>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
      <material name="black">
        <color rgba="0 0 0 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.2"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <!-- Joints -->
  <joint name="left_wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child link="left_wheel"/>
    <origin xyz="0 0.2 -0.05" rpy="1.5708 0 0"/>
    <axis xyz="0 0 1"/>
  </joint>

  <link name="right_wheel">
    <visual>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
      <material name="black">
        <color rgba="0 0 0 1"/>
      </material>
    </visual>
  </link>

  <joint name="right_wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child link="right_wheel"/>
    <origin xyz="0 -0.2 -0.05" rpy="1.5708 0 0"/>
    <axis xyz="0 0 1"/>
  </joint>
</robot>
```

## Tools for Working with URDF

### 1. check_urdf
Command-line tool to validate URDF files.

### 2. urdf_to_graphiz
Generate visual representations of the robot's kinematic structure.

### 3. RViz
Visualize URDF models in 3D.

### 4. Gazebo
Simulate URDF models in physics environment.

## Next Steps

Now that you understand the fundamentals of robot structure definition with URDF, continue to the next chapter to learn about preparing your robot models for simulation:

[→ Simulation Readiness](./simulation-readiness.md)