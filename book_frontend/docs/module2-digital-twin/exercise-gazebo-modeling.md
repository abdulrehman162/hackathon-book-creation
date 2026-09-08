---
title: Exercise - Gazebo Robot Modeling
sidebar_label: Exercise - Robot Modeling
sidebar_position: 5
description: Practical exercise for creating and configuring humanoid robot models in Gazebo simulation
tags: [exercise, gazebo, robot-modeling, simulation, robotics]
---

# Exercise: Gazebo Robot Modeling

## Objective
Create a simple humanoid robot model in Gazebo using SDF/URDF and configure its physical properties for realistic simulation.

## Prerequisites
- Basic understanding of SDF/URDF robot description formats
- Gazebo simulation environment installed
- Text editor for creating model files

## Exercise Steps

### Step 1: Create a Basic Humanoid Robot SDF Model

Create a simple humanoid robot model with the following specifications:
- Single main body (torso) link
- Two arm links (upper and lower) with joints
- Two leg links (upper and lower) with joints
- Head link attached to torso

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <model name="simple_humanoid">
    <!-- Torso (main body) -->
    <link name="torso">
      <pose>0 0 1.0 0 0 0</pose>
      <inertial>
        <mass>10.0</mass>
        <inertia>
          <ixx>0.5</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.5</iyy>
          <iyz>0.0</iyz>
          <izz>0.5</izz>
        </inertia>
      </inertial>
      <visual name="torso_visual">
        <geometry>
          <box>
            <size>0.3 0.2 0.5</size>
          </box>
        </geometry>
      </visual>
      <collision name="torso_collision">
        <geometry>
          <box>
            <size>0.3 0.2 0.5</size>
          </box>
        </geometry>
      </collision>
    </link>

    <!-- Head -->
    <link name="head">
      <pose>0 0 0.3 0 0 0</pose>
      <inertial>
        <mass>2.0</mass>
        <inertia>
          <ixx>0.1</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.1</iyy>
          <iyz>0.0</iyz>
          <izz>0.1</izz>
        </inertia>
      </inertial>
      <visual name="head_visual">
        <geometry>
          <sphere>
            <radius>0.1</radius>
          </sphere>
        </geometry>
      </visual>
      <collision name="head_collision">
        <geometry>
          <sphere>
            <radius>0.1</radius>
          </sphere>
        </geometry>
      </collision>
    </link>

    <!-- Neck joint -->
    <joint name="neck_joint" type="revolute">
      <parent>torso</parent>
      <child>head</child>
      <axis>
        <xyz>0 0 1</xyz>
        <limit>
          <lower>-0.5</lower>
          <upper>0.5</upper>
          <effort>100</effort>
          <velocity>1</velocity>
        </limit>
      </axis>
    </joint>

    <!-- Left upper arm -->
    <link name="left_upper_arm">
      <pose>0.2 0 0.3 0 0 0</pose>
      <inertial>
        <mass>1.0</mass>
        <inertia>
          <ixx>0.05</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.05</iyy>
          <iyz>0.0</iyz>
          <izz>0.05</izz>
        </inertia>
      </inertial>
      <visual name="left_upper_arm_visual">
        <geometry>
          <cylinder>
            <radius>0.05</radius>
            <length>0.3</length>
          </cylinder>
        </geometry>
      </visual>
      <collision name="left_upper_arm_collision">
        <geometry>
          <cylinder>
            <radius>0.05</radius>
            <length>0.3</length>
          </cylinder>
        </geometry>
      </collision>
    </link>

    <!-- Left shoulder joint -->
    <joint name="left_shoulder_joint" type="revolute">
      <parent>torso</parent>
      <child>left_upper_arm</child>
      <axis>
        <xyz>0 1 0</xyz>
        <limit>
          <lower>-1.57</lower>
          <upper>1.57</upper>
          <effort>50</effort>
          <velocity>1</velocity>
        </limit>
      </axis>
    </joint>
  </model>
</sdf>
```

### Step 2: Save and Test the Model

1. Save the above code as `simple_humanoid.sdf` in your Gazebo models directory
2. Launch Gazebo and insert your model from the model database
3. Observe how the robot behaves in the simulation environment

### Step 3: Configure Physical Properties

Adjust the following physical properties to improve the simulation:

1. **Mass properties**: Ensure each link has appropriate mass values
2. **Inertial tensors**: Calculate realistic values based on geometry
3. **Joint limits**: Set appropriate angle limits for realistic movement
4. **Damping and friction**: Add these parameters to joints for realistic behavior

```xml
<!-- Add to each joint -->
<physics>
  <ode>
    <damping_factor>0.01</damping_factor>
    <friction>0.0</friction>
    <spring_reference>0</spring_reference>
    <spring_stiffness>0</spring_stiffness>
  </ode>
</physics>
```

### Step 4: Add Sensors to Your Robot

Add a simple IMU sensor to the torso link:

```xml
<!-- Add inside the torso link definition -->
<sensor name="imu_sensor" type="imu">
  <always_on>1</always_on>
  <update_rate>50</update_rate>
  <visualize>true</visualize>
  <topic>imu_data</topic>
</sensor>
```

### Step 5: Test in Simulation

1. Launch Gazebo with your robot model
2. Apply forces to test the physics simulation
3. Verify that the robot responds appropriately to gravity and collisions
4. Check that sensor data is being published correctly

### Step 6: Advanced Configuration

For a more realistic humanoid model:

1. Add additional links for lower arms and legs
2. Implement joint controllers for actuation
3. Add realistic joint limits based on human anatomy
4. Configure collision properties appropriately

## Deliverables

Upon completion of this exercise, you should have:

1. A complete SDF file for a simple humanoid robot
2. Understanding of proper inertial and collision configuration
3. Knowledge of how to add sensors to your robot model
4. Experience testing your model in Gazebo simulation

## Validation Checklist

- [ ] Robot model loads successfully in Gazebo
- [ ] Robot maintains stable posture under gravity
- [ ] Joints have appropriate limits and behave realistically
- [ ] Sensors publish data correctly
- [ ] Robot responds appropriately to external forces

## Learning Outcomes

After completing this exercise, you should understand:
- How to structure a robot model in SDF format
- The importance of proper inertial properties for stable simulation
- How to configure joints with appropriate limits and dynamics
- How to add sensors to enhance robot capabilities in simulation
- Best practices for robot modeling in Gazebo for humanoid robots