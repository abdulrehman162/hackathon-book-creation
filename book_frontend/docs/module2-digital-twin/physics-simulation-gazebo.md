---
title: Physics Simulation with Gazebo
sidebar_label: Physics Simulation with Gazebo
sidebar_position: 3
description: Comprehensive guide to physics-based simulation for humanoid robots using Gazebo
tags: [gazebo, physics, simulation, robotics, humanoid, dynamics]
---

# Physics Simulation with Gazebo

## Introduction

Gazebo is a powerful open-source robotics simulator that provides accurate physics simulation, high-quality graphics, and convenient programmatic interfaces. For humanoid robotics applications, Gazebo serves as a critical tool for developing, testing, and validating robot behaviors in a safe and controlled environment.

This chapter explores the fundamentals of physics-based simulation in Gazebo, focusing on applications for humanoid robots. We'll cover the physics engine capabilities, model configuration, and best practices for creating realistic simulations.

## Gazebo Architecture and Components

### Core Components

Gazebo's architecture consists of several key components that work together to provide a comprehensive simulation environment:

1. **Physics Engine**: Handles collision detection, dynamics simulation, and constraint solving
2. **Rendering Engine**: Provides realistic visual rendering using OGRE
3. **Sensor Simulation**: Implements various sensor types including cameras, LiDAR, IMU, etc.
4. **Communication Layer**: Uses transport protocols for message passing between components
5. **Model Database**: Hosts pre-built models and environments through Gazebo Fuel

### Supported Physics Engines

Gazebo supports multiple physics engines, each with specific strengths:

- **ODE (Open Dynamics Engine)**: Default engine, good balance of performance and stability
- **Bullet Physics**: Advanced collision detection, suitable for complex scenarios
- **Simbody**: High-accuracy simulation for biomechanical applications
- **DART**: Advanced dynamics and real-time simulation capabilities

## Setting Up Humanoid Robot Models

### Model Description Formats

Gazebo uses SDF (Simulation Description Format) as its native model description language. For ROS integration, URDF (Unified Robot Description Format) models are typically converted to SDF.

#### SDF Structure for Humanoid Robots

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <model name="humanoid_robot">
    <!-- Links define the rigid bodies of the robot -->
    <link name="base_link">
      <!-- Inertial properties -->
      <inertial>
        <mass>10.0</mass>
        <inertia>
          <ixx>0.4</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.4</iyy>
          <iyz>0.0</iyz>
          <izz>0.2</izz>
        </inertia>
      </inertial>

      <!-- Visual representation -->
      <visual name="visual">
        <geometry>
          <box>
            <size>0.3 0.3 0.3</size>
          </box>
        </geometry>
        <material>
          <ambient>0.8 0.8 0.8 1</ambient>
          <diffuse>0.8 0.8 0.8 1</diffuse>
        </material>
      </visual>

      <!-- Collision geometry -->
      <collision name="collision">
        <geometry>
          <box>
            <size>0.3 0.3 0.3</size>
          </box>
        </geometry>
      </collision>
    </link>

    <!-- Additional links for arms, legs, head -->
    <!-- Joints connecting the links -->
  </model>
</sdf>
```

### Inertial Properties Configuration

Proper inertial properties are crucial for realistic physics simulation. Each link should have:

- **Mass**: Realistic mass values based on the physical robot
- **Center of Mass**: Accurate positioning relative to the link frame
- **Inertia Tensor**: Proper 3D inertia values (ixx, ixy, ixz, iyy, iyz, izz)

For humanoid robots, consider the following mass distribution guidelines:
- Torso: 40-50% of total robot mass
- Thighs: 12-15% each
- Shanks: 5-8% each
- Upper arms: 3-5% each
- Lower arms: 2-3% each
- Head: 5-8%

## Physics Configuration Parameters

### Simulation Time Settings

```xml
<physics type="ode">
  <max_step_size>0.001</max_step_size>
  <real_time_factor>1.0</real_time_factor>
  <real_time_update_rate>1000</real_time_update_rate>
</physics>
```

Key parameters:
- **max_step_size**: Simulation time step (smaller = more accurate but slower)
- **real_time_factor**: Target simulation speed relative to real time
- **real_time_update_rate**: Updates per second for the physics engine

### Solver Configuration

```xml
<physics type="ode">
  <ode>
    <solver>
      <type>quick</type>
      <iters>10</iters>
      <sor>1.3</sor>
    </solver>
    <constraints>
      <cfm>0.0</cfm>
      <erp>0.2</erp>
      <contact_max_correcting_vel>100.0</contact_max_correcting_vel>
      <contact_surface_layer>0.001</contact_surface_layer>
    </constraints>
  </ode>
</physics>
```

## Collision Detection and Response

### Collision Geometry Types

Gazebo supports various collision geometry types:

- **Box**: Simple rectangular collision volumes
- **Sphere**: Perfect spherical collisions
- **Cylinder**: Cylindrical collision shapes
- **Capsule**: Rounded cylinders (good for limbs)
- **Mesh**: Complex custom geometry from STL/OBJ files
- **Plane**: Infinite flat surfaces

### Contact Properties

Configure contact behavior between objects:

```xml
<collision name="link_collision">
  <surface>
    <friction>
      <ode>
        <mu>1.0</mu>
        <mu2>1.0</mu2>
        <fdir1>0 0 0</fdir1>
        <slip1>0.0</slip1>
        <slip2>0.0</slip2>
      </ode>
    </friction>
    <bounce>
      <restitution_coefficient>0.1</restitution_coefficient>
      <threshold>100000.0</threshold>
    </bounce>
    <contact>
      <ode>
        <soft_cfm>0.0</soft_cfm>
        <soft_erp>0.2</soft_erp>
        <kp>1000000000000.0</kp>
        <kd>1.0</kd>
        <max_vel>100.0</max_vel>
        <min_depth>0.001</min_depth>
      </ode>
    </contact>
  </surface>
</collision>
```

## Joint Configuration for Humanoid Robots

### Joint Types and Limits

Humanoid robots typically use:

- **Revolute joints**: Single-axis rotation (elbows, knees)
- **Prismatic joints**: Linear motion (prismatic actuators)
- **Fixed joints**: Rigid connections
- **Continuous joints**: Unlimited rotation (wheels)
- **Ball joints**: Multi-axis rotation (hips, shoulders)

```xml
<joint name="knee_joint" type="revolute">
  <parent>thigh</parent>
  <child>shank</child>
  <axis>
    <xyz>0 1 0</xyz>
    <limit>
      <lower>-2.5</lower>
      <upper>0.5</upper>
      <effort>200</effort>
      <velocity>5</velocity>
    </limit>
    <dynamics>
      <damping>1.0</damping>
      <friction>0.1</friction>
    </dynamics>
  </axis>
</joint>
```

### Humanoid-Specific Joint Considerations

For realistic humanoid simulation, consider:

- **Range of Motion**: Limit joints to biologically plausible ranges
- **Joint Stiffness**: Configure appropriate stiffness for stability
- **Damping**: Add damping to prevent oscillations
- **Actuator Dynamics**: Model motor characteristics accurately

## Environment Setup and World Configuration

### Creating Simulation Worlds

Gazebo worlds are defined in SDF format and include:

- Models and their initial positions
- Physics engine configuration
- Lighting and rendering settings
- Plugins for additional functionality

```xml
<sdf version="1.7">
  <world name="humanoid_world">
    <!-- Physics configuration -->
    <physics type="ode">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
    </physics>

    <!-- Include ground plane -->
    <include>
      <uri>model://ground_plane</uri>
    </include>

    <!-- Include sky -->
    <include>
      <uri>model://sun</uri>
    </include>

    <!-- Your robot model -->
    <include>
      <uri>model://humanoid_robot</uri>
      <pose>0 0 1 0 0 0</pose>
    </include>

    <!-- Additional environment models -->
    <include>
      <uri>model://simple_room</uri>
    </include>
  </world>
</sdf>
```

## Best Practices for Stable Simulation

### Model Design Guidelines

1. **Use realistic masses**: Ensure mass properties match the physical robot
2. **Proper inertial tensors**: Calculate accurate 3D inertia values
3. **Appropriate collision geometry**: Balance accuracy with performance
4. **Joint limits**: Constrain to realistic ranges to prevent damage
5. **Damping and friction**: Add realistic dynamic properties

### Simulation Tuning

1. **Start with default parameters**: Use Gazebo's recommended defaults
2. **Adjust step size**: Smaller steps for more stability, larger for performance
3. **Increase solver iterations**: For more stable constraint solving
4. **Tune contact parameters**: Balance between stability and accuracy
5. **Validate against reality**: Compare simulation results with physical tests

## Troubleshooting Common Issues

### Robot Falling Through Ground

Common causes and solutions:
- **Insufficient collision geometry**: Ensure all links have proper collision shapes
- **Incorrect mass/inertia**: Verify realistic values for all links
- **Physics parameters**: Increase solver iterations or reduce time step
- **Ground plane properties**: Check friction and contact parameters

### Joint Instability

- **High joint stiffness**: Reduce stiffness values gradually
- **Insufficient damping**: Add appropriate damping to joints
- **Mass distribution**: Ensure realistic mass ratios between connected links
- **Joint limits**: Verify proper limit configuration

### Performance Issues

- **Complex collision meshes**: Simplify collision geometry
- **Small time steps**: Increase time step within stability limits
- **Solver iterations**: Reduce iterations if accuracy allows
- **Number of contacts**: Optimize model geometry to reduce contact points

## Integration with Control Systems

### ROS Integration

Gazebo integrates seamlessly with ROS through:

- **Gazebo ROS packages**: Standard interfaces for sensors and actuators
- **Controller plugins**: Joint position, velocity, and effort controllers
- **TF publishing**: Automatic transformation publishing for robot state
- **Sensor plugins**: Camera, IMU, LiDAR, and other sensor simulation

### Control Architecture

For humanoid robots, implement:
- **Low-level joint controllers**: Position, velocity, or effort control
- **High-level motion planners**: Trajectory generation and inverse kinematics
- **State estimation**: Robot state feedback and sensor fusion
- **Safety systems**: Collision avoidance and emergency stops

## Advanced Topics

### Multi-Body Dynamics

For complex humanoid robots with many degrees of freedom:
- **Articulated body algorithm**: Efficient computation of dynamics
- **Constraint handling**: Managing closed-loop kinematic chains
- **Contact modeling**: Handling multiple simultaneous contacts

### Real-time Simulation

For hardware-in-the-loop applications:
- **Real-time kernels**: Ensure deterministic timing
- **Communication latency**: Minimize delays in control loops
- **Synchronization**: Coordinate simulation with hardware

## Summary

Physics simulation with Gazebo provides a powerful foundation for developing and testing humanoid robots. By understanding the physics engine capabilities, proper model configuration, and simulation tuning techniques, you can create realistic and stable simulations that accurately represent real-world robot behavior.

The next chapter will explore how Unity can complement Gazebo by providing high-fidelity visualization and human-robot interaction capabilities.

## Further Reading

- Gazebo Documentation: http://gazebosim.org/tutorials
- Physics-based Simulation in Robotics: Academic papers and research
- Humanoid Robot Simulation Best Practices: Industry guidelines