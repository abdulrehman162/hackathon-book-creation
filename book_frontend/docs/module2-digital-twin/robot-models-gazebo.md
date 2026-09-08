---
title: Setting Up Robot Models in Gazebo
sidebar_label: Robot Models Setup
sidebar_position: 6
description: Comprehensive guide to creating and configuring humanoid robot models in Gazebo simulation environment
tags: [gazebo, robot-models, simulation, robotics, humanoid, sdf, urdf]
---

# Setting Up Robot Models in Gazebo

## Introduction

Creating accurate and stable robot models is fundamental to effective simulation in Gazebo. For humanoid robots, this process involves defining the physical properties, kinematic structure, and dynamic behavior of the robot in a way that closely matches the real-world counterpart. This chapter provides a comprehensive guide to setting up robot models in Gazebo, with a focus on humanoid applications.

## Model Creation Workflow

### Overview of the Process

Setting up a robot model in Gazebo involves several key steps:

1. **Design the kinematic structure**: Define links and joints that represent the robot's physical structure
2. **Specify physical properties**: Configure mass, inertia, and collision properties for each link
3. **Define visual appearance**: Set up visual meshes and materials for rendering
4. **Configure sensors and actuators**: Add simulated sensors and joint controllers
5. **Validate the model**: Test the model in simulation for stability and correctness

### Tools and Formats

Gazebo supports multiple model description formats:

- **SDF (Simulation Description Format)**: Native Gazebo format, most feature-complete
- **URDF (Unified Robot Description Format)**: Commonly used in ROS, automatically converted to SDF
- **MJCF (Multi-Joint Chain Format)**: Used in DeepMind's MuJoCo, supported via converters

## Creating Links and Joints

### Link Definition Structure

A link in Gazebo represents a rigid body with physical properties:

```xml
<link name="link_name">
  <!-- Inertial properties define mass and moment of inertia -->
  <inertial>
    <mass>1.0</mass>
    <pose>0 0 0 0 0 0</pose>
    <inertia>
      <ixx>0.01</ixx>
      <ixy>0.0</ixy>
      <ixz>0.0</ixz>
      <iyy>0.01</iyy>
      <iyz>0.0</iyz>
      <izz>0.01</izz>
    </inertia>
  </inertial>

  <!-- Visual properties define how the link appears -->
  <visual name="visual">
    <geometry>
      <box>
        <size>0.1 0.1 0.1</size>
      </box>
    </geometry>
    <material>
      <ambient>0.5 0.5 0.5 1</ambient>
      <diffuse>0.7 0.7 0.7 1</diffuse>
      <specular>0.1 0.1 0.1 1</specular>
    </material>
  </visual>

  <!-- Collision properties define interaction with physics -->
  <collision name="collision">
    <geometry>
      <box>
        <size>0.1 0.1 0.1</size>
      </box>
    </geometry>
  </collision>
</link>
```

### Joint Definition Structure

Joints connect links and define their relative motion:

```xml
<joint name="joint_name" type="revolute">
  <parent>parent_link</parent>
  <child>child_link</child>
  <pose>0 0 0 0 0 0</pose>
  <axis>
    <xyz>0 0 1</xyz>
    <limit>
      <lower>-1.57</lower>
      <upper>1.57</upper>
      <effort>100</effort>
      <velocity>1</velocity>
    </limit>
    <dynamics>
      <damping>0.1</damping>
      <friction>0.0</friction>
    </dynamics>
  </axis>
</joint>
```

## Physical Property Configuration

### Mass Properties

Accurate mass properties are crucial for realistic simulation:

```xml
<inertial>
  <mass>5.0</mass>
  <inertia>
    <ixx>0.1</ixx>
    <ixy>0.0</ixy>
    <ixz>0.0</ixz>
    <iyy>0.1</iyy>
    <iyz>0.0</iyz>
    <izz>0.1</izz>
  </inertia>
</inertial>
```

For humanoid robots, typical mass distributions:
- **Torso**: 40-50% of total mass
- **Thighs**: 10-15% each
- **Shanks**: 5-8% each
- **Upper arms**: 3-5% each
- **Lower arms**: 2-3% each
- **Head**: 5-7%

### Calculating Inertial Properties

For common geometric shapes, use these formulas:

**Box (width w, depth d, height h):**
```
ixx = 1/12 * mass * (d² + h²)
iyy = 1/12 * mass * (w² + h²)
izz = 1/12 * mass * (w² + d²)
```

**Cylinder (radius r, height h):**
```
ixx = iyy = 1/12 * mass * (3*r² + h²)
izz = 1/2 * mass * r²
```

**Sphere (radius r):**
```
ixx = iyy = izz = 2/5 * mass * r²
```

### Center of Mass Considerations

For humanoid robots:
- **Torso**: Position CoM slightly below geometric center to account for head weight
- **Limbs**: Position CoM toward the heavier end (e.g., upper arms closer to torso)
- **Always**: Verify that CoM is physically reasonable and doesn't cause instability

## Collision Geometry Optimization

### Choosing Collision Shapes

Select collision geometry based on requirements:

**Simple Geometries (Box, Sphere, Cylinder):**
- Advantages: Fast collision detection, stable simulation
- Use Cases: Initial testing, simple shapes, performance-critical applications

**Capsules:**
- Advantages: Good for limbs, stable contact handling
- Use Cases: Arms, legs, cylindrical components

**Mesh Collisions:**
- Advantages: Accurate representation of complex geometry
- Disadvantages: Computationally expensive, potential instability
- Use Cases: Complex shapes where accuracy is critical

### Collision Mesh Guidelines

When using mesh collision geometry:

1. **Simplify geometry**: Reduce polygon count while maintaining essential features
2. **Convex decomposition**: Break complex meshes into convex parts
3. **Collision groups**: Use multiple collision elements for complex links
4. **Resolution**: Balance accuracy with performance (typically 1000-10000 triangles per link)

```xml
<collision name="complex_collision">
  <!-- Use multiple simple shapes to approximate complex geometry -->
  <geometry>
    <mesh>
      <uri>model://robot/meshes/complex_shape.stl</uri>
    </mesh>
  </geometry>
</collision>
```

## Visual Representation

### Visual vs. Collision Geometry

It's important to distinguish between visual and collision geometry:

- **Visual geometry**: Defines appearance, can be high-resolution
- **Collision geometry**: Defines physical interaction, should be optimized for performance
- **They can be different**: Use detailed visuals with simplified collision shapes

### Material Configuration

Configure materials for realistic rendering:

```xml
<visual name="visual">
  <geometry>
    <mesh>
      <uri>model://robot/meshes/link_visual.dae</uri>
    </mesh>
  </geometry>
  <material>
    <script>
      <uri>file://media/materials/scripts/gazebo.material</uri>
      <name>Gazebo/Blue</name>
    </script>
  </material>
</visual>
```

## URDF to SDF Conversion

### Using xacro for Complex Models

For complex humanoid robots, use xacro (XML Macros) to simplify model definition:

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="humanoid_robot">
  <!-- Define constants -->
  <xacro:property name="M_PI" value="3.1415926535897931" />
  <xacro:property name="torso_mass" value="10.0" />

  <!-- Macro for creating a simple link -->
  <xacro:macro name="simple_link" params="name mass xyz rpy size">
    <link name="${name}">
      <inertial>
        <mass value="${mass}" />
        <origin xyz="${xyz}" rpy="${rpy}" />
        <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.01" />
      </inertial>

      <visual>
        <origin xyz="${xyz}" rpy="${rpy}" />
        <geometry>
          <box size="${size}" />
        </geometry>
      </visual>

      <collision>
        <origin xyz="${xyz}" rpy="${rpy}" />
        <geometry>
          <box size="${size}" />
        </geometry>
      </collision>
    </link>
  </xacro:macro>

  <!-- Use the macro to create links -->
  <xacro:simple_link name="torso" mass="10.0" xyz="0 0 0" rpy="0 0 0" size="0.3 0.2 0.5" />
</robot>
```

### Converting URDF to SDF

Use the following command to convert URDF to SDF:

```bash
gz sdf -p robot.urdf > robot.sdf
```

## Sensor Integration

### Adding Sensors to Models

Common sensors for humanoid robots include:

**IMU (Inertial Measurement Unit):**
```xml
<sensor name="imu_sensor" type="imu">
  <always_on>1</always_on>
  <update_rate>100</update_rate>
  <topic>imu/data</topic>
  <visualize>true</visualize>
</sensor>
```

**Camera:**
```xml
<sensor name="camera" type="camera">
  <camera>
    <horizontal_fov>1.047</horizontal_fov>
    <image>
      <width>640</width>
      <height>480</height>
      <format>R8G8B8</format>
    </image>
    <clip>
      <near>0.1</near>
      <far>10</far>
    </clip>
  </camera>
  <always_on>1</always_on>
  <update_rate>30</update_rate>
  <visualize>true</visualize>
</sensor>
```

**LiDAR:**
```xml
<sensor name="lidar" type="ray">
  <ray>
    <scan>
      <horizontal>
        <samples>720</samples>
        <resolution>1</resolution>
        <min_angle>-1.570796</min_angle>
        <max_angle>1.570796</max_angle>
      </horizontal>
    </scan>
    <range>
      <min>0.1</min>
      <max>10</max>
      <resolution>0.01</resolution>
    </range>
  </ray>
  <always_on>1</always_on>
  <update_rate>10</update_rate>
  <visualize>true</visualize>
</sensor>
```

## Joint Controllers and Actuators

### Joint Control Types

Gazebo supports various joint control methods:

**Position Control:**
```xml
<gazebo reference="joint_name">
  <provideFeedback>true</provideFeedback>
  <joint_properties>
    <damping>0.1</damping>
    <friction>0.0</friction>
  </joint_properties>
</gazebo>
```

**Effort Control:**
```xml
<!-- Use ROS control plugins for more sophisticated control -->
<transmission name="tran1">
  <type>transmission_interface/SimpleTransmission</type>
  <joint name="joint_name">
    <hardwareInterface>EffortJointInterface</hardwareInterface>
  </joint>
  <actuator name="motor1">
    <hardwareInterface>EffortJointInterface</hardwareInterface>
    <mechanicalReduction>1</mechanicalReduction>
  </actuator>
</transmission>
```

### Humanoid-Specific Joint Configurations

For humanoid applications, consider:

- **Compliance**: Add compliance to joints to make robot more robust
- **Safety limits**: Implement software limits to prevent damage
- **Backdrivability**: Configure joints appropriately for human interaction
- **Stiffness control**: Implement variable stiffness where needed

## Model Validation and Testing

### Initial Validation Steps

1. **Load in Gazebo**: Verify the model loads without errors
2. **Check kinematics**: Ensure all joints move as expected
3. **Stability test**: Verify the robot remains stable under gravity
4. **Collision check**: Ensure no unintended collisions occur

### Stability Testing

```bash
# Launch Gazebo with your model
gz sim -v 4 your_model.sdf
```

Monitor for:
- Robot falling through the ground
- Joint oscillations or instabilities
- Unexpected collisions between links
- Physics performance issues

### Performance Validation

- **Simulation speed**: Ensure real-time factor stays near 1.0
- **CPU usage**: Monitor resource consumption
- **Accuracy**: Compare with expected physical behavior
- **Consistency**: Verify reproducible results across runs

## Troubleshooting Common Issues

### Model Not Loading

Common causes:
- **Invalid SDF/URDF syntax**: Validate with `xmllint`
- **Missing mesh files**: Ensure all referenced files exist
- **Path issues**: Check file paths and URIs
- **Dependency issues**: Verify all required models are available

### Instability Problems

- **Mass properties**: Verify realistic mass and inertia values
- **Time step**: Try reducing the simulation time step
- **Solver parameters**: Increase iterations or adjust solver type
- **Joint limits**: Ensure proper limits and dynamics configuration

### Collision Issues

- **Interpenetration**: Check collision geometry and physics parameters
- **Excessive bouncing**: Adjust restitution coefficients
- **No collisions**: Verify collision elements exist and are properly configured

## Advanced Model Features

### Multi-Body Systems

For complex humanoid robots with multiple interacting components:

```xml
<model name="humanoid_with_object">
  <!-- Robot model -->
  <include>
    <uri>model://humanoid_robot</uri>
  </include>

  <!-- Object to manipulate -->
  <include>
    <uri>model://object_to_grasp</uri>
    <pose>0.5 0 1 0 0 0</pose>
  </include>
</model>
```

### Custom Plugins

Add custom functionality with plugins:

```xml
<gazebo>
  <plugin name="custom_controller" filename="libCustomController.so">
    <robotNamespace>/humanoid</robotNamespace>
    <controlRate>100</controlRate>
  </plugin>
</gazebo>
```

## Model Publishing and Sharing

### Gazebo Model Database

Consider contributing your models to the Gazebo Model Database (Fuel) for sharing and reuse:

1. **Organize files**: Follow Gazebo model directory structure
2. **Add metadata**: Include model.config with description and licensing
3. **Test thoroughly**: Ensure model works in various scenarios
4. **Document**: Provide usage instructions and limitations

### Model Directory Structure

```
models/
└── humanoid_robot/
    ├── model.sdf
    ├── model.config
    ├── meshes/
    │   ├── link1.dae
    │   └── link2.stl
    └── materials/
        └── textures/
```

## Best Practices Summary

1. **Start simple**: Begin with basic shapes and add complexity gradually
2. **Validate early**: Test models frequently during development
3. **Use realistic properties**: Base mass and inertia on physical robot
4. **Optimize for performance**: Balance accuracy with simulation speed
5. **Document thoroughly**: Include comments and usage instructions
6. **Test comprehensively**: Verify behavior under various conditions
7. **Version control**: Track model changes with version control systems

## Integration with ROS

For ROS integration, ensure your model includes:

- **Proper joint naming**: Follow ROS naming conventions
- **TF frames**: Define appropriate transformation frames
- **ROS control interfaces**: Include transmission elements
- **URDF compatibility**: Ensure URDF/SDF conversion works correctly

## Conclusion

Setting up robot models in Gazebo is a critical step in creating effective simulations for humanoid robots. By following the guidelines in this chapter, you can create models that are both physically accurate and computationally efficient. Remember to validate your models thoroughly and iterate based on simulation results.

The next chapter will cover physics parameters and configuration to optimize your simulation for specific use cases.

## Exercises

1. Create a simple humanoid model with torso, head, and limbs
2. Configure realistic mass properties for each link
3. Test the model in Gazebo for stability and proper kinematics
4. Add basic sensors to your robot model
5. Validate that joint limits and dynamics are properly configured