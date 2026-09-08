---
title: Preparing Robot Models for Simulation
sidebar_label: Simulation Readiness
sidebar_position: 2
description: Techniques and best practices for preparing URDF models for physics simulation
tags: [urdf, simulation, gazebo, collision, inertial, physics]
---

# Preparing Robot Models for Simulation

## Overview

This chapter focuses on preparing URDF robot models for physics simulation in environments like Gazebo. Creating simulation-ready models requires careful attention to physical properties, collision geometry, and inertial parameters to ensure stable and realistic simulation behavior.

## Physics Simulation Requirements

### Collision Geometry

Collision geometry defines how the robot interacts with the environment during simulation. Unlike visual geometry, collision geometry should be:

- **Simpler**: Use basic shapes (boxes, cylinders, spheres) when possible
- **Watertight**: Ensure no gaps in mesh geometry
- **Convex**: For complex shapes, use convex decomposition

#### Collision Geometry Types

```xml
<!-- Box collision -->
<collision>
  <geometry>
    <box size="0.5 0.3 0.2"/>
  </geometry>
</collision>

<!-- Cylinder collision -->
<collision>
  <geometry>
    <cylinder radius="0.1" length="0.2"/>
  </geometry>
</collision>

<!-- Sphere collision -->
<collision>
  <geometry>
    <sphere radius="0.1"/>
  </geometry>
</collision>

<!-- Mesh collision -->
<collision>
  <geometry>
    <mesh filename="package://my_robot/meshes/complex_shape.stl"/>
  </geometry>
</collision>
```

### Inertial Properties

Accurate inertial properties are crucial for realistic physics simulation:

```xml
<inertial>
  <mass value="1.0"/>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <!-- Inertia tensor for a box: m/12 * (h²+w², l²+w², l²+h²) -->
  <inertia
    ixx="0.0083"
    ixy="0.0"
    ixz="0.0"
    iyy="0.0167"
    iyz="0.0"
    izz="0.025"/>
</inertial>
```

#### Calculating Inertial Properties

For common shapes:

**Box (length l, width w, height h, mass m):**
- ixx = m/12 * (h² + w²)
- iyy = m/12 * (l² + h²)
- izz = m/12 * (l² + w²)

**Cylinder (radius r, height h, mass m):**
- ixx = iyy = m/12 * (3*r² + h²)
- izz = m/2 * r²

**Sphere (radius r, mass m):**
- ixx = iyy = izz = 2/5 * m * r²

## Gazebo-Specific Integration

### Gazebo Plugins

Integrate Gazebo plugins to enable robot functionality:

```xml
<gazebo>
  <!-- Differential drive plugin -->
  <plugin name="differential_drive" filename="libgazebo_ros_diff_drive.so">
    <ros>
      <namespace>robot</namespace>
      <remapping>cmd_vel:=cmd_vel</remapping>
      <remapping>odom:=odom</remapping>
    </ros>
    <update_rate>30</update_rate>
    <left_joint>left_wheel_joint</left_joint>
    <right_joint>right_wheel_joint</right_joint>
    <wheel_separation>0.3</wheel_separation>
    <wheel_diameter>0.15</wheel_diameter>
    <max_wheel_torque>20</max_wheel_torque>
    <max_wheel_acceleration>1.0</max_wheel_acceleration>
  </plugin>
</gazebo>
```

### Material Definitions

Define materials for Gazebo rendering:

```xml
<gazebo reference="link_name">
  <material>Gazebo/Blue</material>
  <mu1>0.2</mu1>
  <mu2>0.2</mu2>
  <kp>1000000.0</kp>
  <kd>100.0</kd>
</gazebo>
```

### Sensor Integration

Add sensors to your robot model:

```xml
<!-- RGB-D camera -->
<gazebo reference="camera_link">
  <sensor name="camera" type="depth">
    <always_on>true</always_on>
    <visualize>true</visualize>
    <update_rate>30</update_rate>
    <camera>
      <horizontal_fov>1.047</horizontal_fov>
      <image>
        <format>R8G8B8</format>
        <width>640</width>
        <height>480</height>
      </image>
      <clip>
        <near>0.1</near>
        <far>10</far>
      </clip>
    </camera>
    <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
      <ros>
        <namespace>camera</namespace>
        <remapping>image_raw:=image</remapping>
      </ros>
    </plugin>
  </sensor>
</gazebo>
```

## Collision Optimization

### Simplified Collision Models

For complex geometries, create simplified collision models:

```xml
<link name="complex_link">
  <!-- Visual (detailed) -->
  <visual>
    <geometry>
      <mesh filename="package://my_robot/meshes/detailed_model.dae"/>
    </geometry>
  </visual>

  <!-- Collision (simplified) -->
  <collision>
    <geometry>
      <mesh filename="package://my_robot/meshes/simplified_collision.stl"/>
    </geometry>
  </collision>
</link>
```

### Multiple Collision Elements

Use multiple simple shapes to approximate complex geometry:

```xml
<link name="complex_link">
  <collision name="collision_1">
    <origin xyz="0 0 0.1" rpy="0 0 0"/>
    <geometry>
      <box size="0.1 0.1 0.2"/>
    </geometry>
  </collision>

  <collision name="collision_2">
    <origin xyz="0.1 0 0" rpy="0 0 0"/>
    <geometry>
      <cylinder radius="0.05" length="0.2"/>
    </geometry>
  </collision>
</link>
```

## Inertial Optimization

### Center of Mass Considerations

Ensure the center of mass is correctly positioned:

```xml
<inertial>
  <mass value="2.5"/>
  <origin xyz="0.01 0 -0.02" rpy="0 0 0"/>
  <inertia ixx="0.01" ixy="0.0" ixz="0.001" iyy="0.02" iyz="0.0" izz="0.025"/>
</inertial>
```

### Composite Inertial Calculation

For assemblies, calculate combined inertial properties using the parallel axis theorem:

```xml
<!-- Combined link representing multiple parts -->
<inertial>
  <mass value="5.0"/>  <!-- Sum of component masses -->
  <origin xyz="0.02 0.01 -0.01"/>  <!-- Combined center of mass -->
  <inertia
    ixx="0.08"  <!-- Combined inertia tensor -->
    ixy="0.001"
    ixz="0.002"
    iyy="0.09"
    iyz="0.001"
    izz="0.07"/>
</inertial>
```

## Simulation Stability Tips

### 1. Appropriate Time Steps

Configure Gazebo with appropriate physics parameters:

```xml
<gazebo>
  <physics type="ode">
    <max_step_size>0.001</max_step_size>
    <real_time_factor>1.0</real_time_factor>
    <real_time_update_rate>1000</real_time_update_rate>
  </physics>
</gazebo>
```

### 2. Joint Damping and Friction

Add appropriate damping to prevent oscillations:

```xml
<joint name="joint_name" type="revolute">
  <dynamics damping="0.1" friction="0.01"/>
  <!-- Other joint properties -->
</joint>
```

### 3. Proper Mass Distribution

Ensure realistic mass distribution:

```xml
<!-- Base should be heavier than appendages -->
<link name="base_link">
  <inertial>
    <mass value="5.0"/>  <!-- Heavier base for stability -->
    <!-- ... -->
  </inertial>
</link>

<link name="end_effector">
  <inertial>
    <mass value="0.1"/>  <!-- Light end effector -->
    <!-- ... -->
  </inertial>
</link>
```

## Validation and Testing

### URDF Validation

Validate your URDF before simulation:

```bash
# Check URDF syntax and structure
check_urdf my_robot.urdf

# Visualize the kinematic tree
urdf_to_graphiz my_robot.urdf
```

### Simulation Testing Checklist

1. **Kinematic Structure**: Verify joint connections and limits
2. **Physical Properties**: Check masses, inertias, and dimensions
3. **Collision Models**: Ensure no self-collisions in default pose
4. **Stability**: Test for oscillations or unstable behavior
5. **Performance**: Monitor simulation update rate and CPU usage

### Common Issues and Solutions

**Issue**: Robot falls through the ground
- **Solution**: Check collision geometry and inertial properties

**Issue**: Joints oscillate wildly
- **Solution**: Add damping, reduce time step, or adjust physics parameters

**Issue**: Robot is too slow or fast
- **Solution**: Adjust mass and inertia values

**Issue**: Robot tips over easily
- **Solution**: Lower center of mass, increase base mass, widen stance

## Advanced Simulation Features

### Transmission Elements

Define how joints connect to controllers:

```xml
<transmission name="left_wheel_trans">
  <type>transmission_interface/SimpleTransmission</type>
  <joint name="left_wheel_joint">
    <hardwareInterface>velocity_interface</hardwareInterface>
  </joint>
  <actuator name="left_wheel_motor">
    <hardwareInterface>velocity_interface</hardwareInterface>
    <mechanicalReduction>1</mechanicalReduction>
  </actuator>
</transmission>
```

### Gazebo Control Interface

Integrate with ROS control:

```xml
<gazebo>
  <plugin name="ros_control" filename="libgazebo_ros_control.so">
    <robotNamespace>/my_robot</robotNamespace>
    <robotSimType>gazebo_ros_control/DefaultRobotHWSim</robotSimType>
  </plugin>
</gazebo>
```

## Performance Optimization

### 1. Level of Detail

Use different levels of detail for different purposes:
- **Visual**: High-resolution meshes for rendering
- **Collision**: Simplified meshes for physics
- **Planning**: Even simpler models for path planning

### 2. Fixed Joints Optimization

Combine links connected by fixed joints when possible:

```xml
<!-- Instead of separate links with fixed joint -->
<link name="base"/>
<link name="sensor_mount"/>
<joint name="fixed_joint" type="fixed">
  <parent link="base"/>
  <child link="sensor_mount"/>
</joint>

<!-- Combine into single link if they don't move relative to each other -->
<link name="base_with_sensor_mount">
  <!-- Combined geometry -->
</link>
```

## Resources

- [Gazebo Model Tutorial](http://gazebosim.org/tutorials/?tut=ros_urdf)
- [URDF Best Practices](http://wiki.ros.org/urdf/XML)
- [Physics Simulation Guidelines](https://physics-simulation.example.com)
- [Collision Geometry Optimization](https://collision-optimization.example.com)

## Next Steps

With your robot model properly prepared for simulation, continue to the next section to learn about validation and testing:

[→ URDF Quiz](./quiz-urdf.md)