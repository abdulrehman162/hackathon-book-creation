---
title: Exercises and Examples - Digital Twin Simulation
sidebar_label: Exercises and Examples
sidebar_position: 8
description: Practical exercises and examples for digital twin simulation with Gazebo and Unity
tags: [exercises, examples, gazebo, unity, simulation, robotics, humanoid]
---

# Exercises and Examples: Digital Twin Simulation

## Overview

This chapter provides comprehensive exercises and practical examples that integrate the concepts covered in Module 2. These exercises are designed to reinforce your understanding of physics simulation with Gazebo and prepare you for the Unity-based digital twin implementation covered in the next module.

## Exercise 1: Complete Humanoid Robot Model

### Objective
Create a complete humanoid robot model with proper physical properties and validate its behavior in simulation.

### Requirements
- 18+ degrees of freedom (DOF)
- Realistic mass distribution
- Proper inertial properties
- Functional joints with appropriate limits
- Basic sensors (IMU, joint position sensors)

### Implementation Steps

1. **Define the kinematic structure**:
   - Torso with head, neck joint
   - 2-arm structure with shoulder, elbow, wrist joints
   - 2-leg structure with hip, knee, ankle joints
   - Total: 20+ joints for a complete humanoid

2. **Configure physical properties**:
   - Total robot mass: 50-80 kg (adjustable based on application)
   - Realistic mass distribution following humanoid guidelines
   - Proper inertia tensors calculated from geometry
   - Center of mass positioned appropriately

3. **Implement collision and visual geometry**:
   - Use capsules for limbs (stable and efficient)
   - Box geometry for torso and head
   - Proper scaling for realistic proportions

4. **Add sensors**:
   - IMU in torso
   - Joint position/velocity/effort sensors
   - Optional: cameras, force/torque sensors

### Validation Criteria
- Robot maintains stable standing position
- All joints move within specified limits
- No unexpected collisions between links
- Real-time factor remains near 1.0

### Solution Outline

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <model name="complete_humanoid">
    <!-- Torso -->
    <link name="torso">
      <inertial>
        <mass>20.0</mass>
        <inertia>
          <ixx>0.5</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.4</iyy>
          <iyz>0.0</iyz>
          <izz>0.2</izz>
        </inertia>
      </inertial>
      <!-- Visual and collision elements -->
    </link>

    <!-- Head -->
    <link name="head">
      <inertial>
        <mass>3.0</mass>
        <inertia>
          <ixx>0.02</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.02</iyy>
          <iyz>0.0</iyz>
          <izz>0.02</izz>
        </inertia>
      </inertial>
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
          <effort>20</effort>
          <velocity>2</velocity>
        </limit>
      </axis>
    </joint>

    <!-- Left shoulder (3 DOF) -->
    <joint name="left_shoulder_yaw" type="revolute">
      <parent>torso</parent>
      <child>left_upper_arm</child>
      <axis>
        <xyz>0 0 1</xyz>
        <limit>
          <lower>-1.57</lower>
          <upper>1.57</upper>
          <effort>100</effort>
          <velocity>2</velocity>
        </limit>
      </axis>
    </joint>

    <!-- Continue with full kinematic chain... -->
  </model>
</sdf>
```

## Exercise 2: Physics Parameter Optimization

### Objective
Optimize physics parameters for a given humanoid model to achieve stable walking behavior while maintaining performance.

### Scenario
You have a humanoid robot model that exhibits instability during walking. Your task is to identify and fix the physics configuration issues.

### Initial Problem Setup
- Time step: 0.01s (too large)
- Solver iterations: 20 (too low)
- ERP: 0.8 (too high, causing oscillations)
- CFM: 0.01 (too high, causing soft constraints)

### Solution Process

1. **Performance Analysis**:
   ```xml
   <physics type="ode">
     <max_step_size>0.001</max_step_size>  <!-- Reduced from 0.01 -->
     <real_time_update_rate>1000</real_time_update_rate>
     <real_time_factor>1.0</real_time_factor>
   </physics>
   ```

2. **Stability Improvements**:
   ```xml
   <physics type="ode">
     <ode>
       <solver>
         <iters>200</iters>  <!-- Increased from 20 -->
         <sor>1.2</sor>
       </solver>
       <constraints>
         <erp>0.1</erp>  <!-- Reduced from 0.8 -->
         <cfm>0.0001</cfm>  <!-- Reduced from 0.01 -->
       </constraints>
     </ode>
   </physics>
   ```

3. **Contact Parameter Tuning**:
   ```xml
   <collision name="foot_collision">
     <surface>
       <friction>
         <ode>
           <mu>1.0</mu>
           <mu2>1.0</mu2>
         </ode>
       </friction>
       <contact>
         <ode>
           <soft_cfm>0.00001</soft_cfm>
           <soft_erp>0.1</soft_erp>
           <kp>100000000000.0</kp>
           <kd>10.0</kd>
         </ode>
       </contact>
     </surface>
   </collision>
   ```

### Validation
- Real-time factor remains close to 1.0
- Robot can stand stably without oscillation
- Walking gait is smooth and stable
- No foot penetration during walking

## Exercise 3: Sensor Integration and Validation

### Objective
Integrate multiple sensors into a humanoid robot model and validate their data output.

### Sensors to Implement
1. **IMU**: In torso link for orientation and acceleration data
2. **Force/Torque Sensors**: At feet for ground contact force
3. **Joint Position Sensors**: All joints for kinematic feedback
4. **Camera**: Head-mounted for visual perception

### Implementation

```xml
<!-- IMU Sensor -->
<sensor name="imu_sensor" type="imu">
  <always_on>1</always_on>
  <update_rate>100</update_rate>
  <topic>imu/data</topic>
  <visualize>false</visualize>
</sensor>

<!-- Joint Position Sensor -->
<sensor name="left_knee_pos_sensor" type="joint_position">
  <joint>left_knee_joint</joint>
  <always_on>1</always_on>
  <update_rate>100</update_rate>
  <topic>joint_states</topic>
</sensor>

<!-- Camera Sensor -->
<sensor name="head_camera" type="camera">
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

### Validation Process
1. Launch the robot in simulation
2. Subscribe to sensor topics
3. Verify data publication rates
4. Check data ranges and units
5. Validate sensor frame orientations

## Exercise 4: Complex Environment Interaction

### Objective
Create a simulation environment with multiple objects and validate robot interaction capabilities.

### Environment Setup
- Flat ground plane with high friction
- Multiple objects of different shapes and masses
- Inclined plane for testing balance
- Narrow walkway to test navigation

### Implementation

```xml
<sdf version="1.7">
  <world name="complex_environment">
    <physics type="ode">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
    </physics>

    <!-- Ground plane -->
    <include>
      <uri>model://ground_plane</uri>
    </include>

    <!-- Inclined plane -->
    <model name="inclined_plane">
      <pose>2 0 0 0 0.3 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>2 2 0.1</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>2 2 0.1</size>
            </box>
          </geometry>
        </visual>
      </link>
    </model>

    <!-- Objects to interact with -->
    <model name="box_object">
      <pose>1 1 0.5 0 0 0</pose>
      <link name="link">
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
        <collision name="collision">
          <geometry>
            <box>
              <size>0.2 0.2 0.2</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>0.2 0.2 0.2</size>
            </box>
          </geometry>
        </visual>
      </link>
    </model>

    <!-- Include your humanoid robot -->
    <include>
      <uri>model://complete_humanoid</uri>
      <pose>0 0 1.0 0 0 0</pose>
    </include>
  </world>
</sdf>
```

### Validation Tests
1. Robot can walk up the inclined plane
2. Robot can push objects without falling
3. Robot maintains balance when interacting with objects
4. No unexpected physics instabilities in complex scene

## Example 1: Walking Controller Integration

### Objective
Implement a basic walking controller using the physics simulation.

### Control Architecture

```python
#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState
from tf.transformations import euler_from_quaternion
import numpy as np

class SimpleWalker:
    def __init__(self):
        rospy.init_node('simple_walker')

        # Joint command publishers
        self.joint_pubs = {}
        joints = [
            'left_hip_yaw', 'left_hip_roll', 'left_hip_pitch',
            'left_knee', 'left_ankle_pitch', 'left_ankle_roll',
            'right_hip_yaw', 'right_hip_roll', 'right_hip_pitch',
            'right_knee', 'right_ankle_pitch', 'right_ankle_roll'
        ]

        for joint in joints:
            self.joint_pubs[joint] = rospy.Publisher(
                f'/{joint}_position_controller/command',
                Float64,
                queue_size=1
            )

        # Joint state subscriber
        rospy.Subscriber('/joint_states', JointState, self.joint_state_callback)

        self.joint_positions = {}
        self.rate = rospy.Rate(100)  # 100 Hz control loop

    def joint_state_callback(self, msg):
        for i, name in enumerate(msg.name):
            if name in self.joint_positions:
                self.joint_positions[name] = msg.position[i]

    def walking_pattern(self, t):
        """Generate walking pattern based on time"""
        # Simple oscillating pattern for walking
        step_freq = 1.0  # 1 Hz walking
        left_swing = np.sin(2 * np.pi * step_freq * t)
        right_swing = np.sin(2 * np.pi * step_freq * t + np.pi)

        return {
            'left_knee': 0.5 * left_swing,
            'right_knee': 0.5 * right_swing,
            'left_ankle_pitch': 0.2 * left_swing,
            'right_ankle_pitch': 0.2 * right_swing
        }

    def run(self):
        start_time = rospy.Time.now().to_sec()

        while not rospy.is_shutdown():
            current_time = rospy.Time.now().to_sec() - start_time

            # Generate walking pattern
            target_joints = self.walking_pattern(current_time)

            # Publish commands
            for joint, target_pos in target_joints.items():
                if joint in self.joint_pubs:
                    self.joint_pubs[joint].publish(Float64(target_pos))

            self.rate.sleep()

if __name__ == '__main__':
    walker = SimpleWalker()
    walker.run()
```

## Example 2: Balance Controller

### Objective
Implement a simple balance controller to maintain upright posture.

### Implementation

```python
#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Vector3
import numpy as np

class BalanceController:
    def __init__(self):
        rospy.init_node('balance_controller')

        # Publishers for ankle joints
        self.left_ankle_pub = rospy.Publisher(
            '/left_ankle_pitch_position_controller/command',
            Float64, queue_size=1
        )
        self.right_ankle_pub = rospy.Publisher(
            '/right_ankle_pitch_position_controller/command',
            Float64, queue_size=1
        )

        # IMU subscriber
        rospy.Subscriber('/imu/data', Imu, self.imu_callback)

        self.roll = 0.0
        self.pitch = 0.0
        self.rate = rospy.Rate(100)

        # PID parameters
        self.kp = 10.0
        self.ki = 1.0
        self.kd = 5.0
        self.error_integral = 0.0
        self.prev_error = 0.0

    def imu_callback(self, msg):
        # Convert quaternion to roll/pitch
        orientation_q = msg.orientation
        orientation_list = [
            orientation_q.x,
            orientation_q.y,
            orientation_q.z,
            orientation_q.w
        ]
        (roll, pitch, yaw) = euler_from_quaternion(orientation_list)

        self.roll = roll
        self.pitch = pitch

    def balance_control(self):
        # Use pitch angle for balance control
        target_pitch = 0.0  # Desired upright position
        error = target_pitch - self.pitch

        # PID control
        self.error_integral += error * 0.01  # dt = 0.01
        derivative = (error - self.prev_error) / 0.01

        output = self.kp * error + self.ki * self.error_integral + self.kd * derivative

        # Apply limits to prevent excessive movement
        output = max(min(output, 0.3), -0.3)

        self.left_ankle_pub.publish(Float64(output))
        self.right_ankle_pub.publish(Float64(output))

        self.prev_error = error

    def run(self):
        while not rospy.is_shutdown():
            self.balance_control()
            self.rate.sleep()

if __name__ == '__main__':
    controller = BalanceController()
    controller.run()
```

## Exercise 5: Simulation Validation and Comparison

### Objective
Validate simulation results against expected physical behavior.

### Validation Tests

1. **Free Fall Test**:
   - Place robot in air with no contacts
   - Verify acceleration matches gravitational constant (9.81 m/s²)
   - Check that position follows expected parabolic trajectory

2. **Pendulum Test**:
   - Create a simple pendulum from one of the robot's limbs
   - Verify oscillation frequency matches theoretical calculation
   - Formula: f = 1/(2π) * √(g/L) where L is pendulum length

3. **Collision Response Test**:
   - Drop robot from known height
   - Measure impact force and verify conservation of momentum
   - Check that robot bounces with appropriate coefficient of restitution

### Implementation for Validation

```python
#!/usr/bin/env python3
import rospy
from gazebo_msgs.msg import ModelStates
from std_msgs.msg import Float64
import numpy as np

class SimulationValidator:
    def __init__(self):
        rospy.init_node('simulation_validator')

        # Subscribe to model states to get position/velocity
        rospy.Subscriber('/gazebo/model_states', ModelStates, self.model_states_callback)

        self.robot_position = None
        self.robot_velocity = None
        self.start_time = None
        self.test_active = False

        self.rate = rospy.Rate(100)

    def model_states_callback(self, msg):
        try:
            robot_idx = msg.name.index('complete_humanoid')
            self.robot_position = msg.pose[robot_idx].position
            self.robot_velocity = msg.twist[robot_idx].linear
        except ValueError:
            pass  # Robot not found in model states

    def free_fall_test(self):
        """Test free fall acceleration"""
        if self.robot_position and self.test_active:
            # Calculate acceleration from velocity changes
            # Compare with expected gravitational acceleration (9.81 m/s²)
            pass

    def run(self):
        rospy.sleep(1)  # Wait for simulation to initialize

        # Start validation tests
        self.test_active = True
        self.start_time = rospy.Time.now().to_sec()

        while not rospy.is_shutdown():
            if self.test_active:
                self.free_fall_test()
            self.rate.sleep()

if __name__ == '__main__':
    validator = SimulationValidator()
    validator.run()
```

## Troubleshooting Common Issues

### Physics Instability
- **Symptoms**: Robot oscillates, falls through ground, explodes
- **Solutions**: Reduce time step, increase solver iterations, check mass properties

### Performance Issues
- **Symptoms**: Low real-time factor, lag, dropped frames
- **Solutions**: Simplify collision geometry, reduce solver iterations, increase time step (carefully)

### Control Issues
- **Symptoms**: Robot doesn't respond to commands, unstable behavior
- **Solutions**: Check joint limits, verify controller parameters, validate sensor data

## Best Practices Summary

1. **Start Simple**: Begin with basic models and gradually add complexity
2. **Validate Incrementally**: Test each component separately before integration
3. **Monitor Performance**: Keep track of real-time factor and CPU usage
4. **Document Parameters**: Keep records of working parameter sets
5. **Test Edge Cases**: Verify behavior under extreme conditions
6. **Compare with Reality**: When possible, validate against physical robot data

## Conclusion

These exercises and examples provide practical applications of the physics simulation concepts covered in Module 2. By working through these implementations, you'll gain hands-on experience with creating, configuring, and validating humanoid robot simulations in Gazebo.

The skills developed through these exercises will be essential as you move on to the Unity-based digital twin implementation in the next module, where you'll focus on high-fidelity visualization and human-robot interaction.

## Next Steps

After completing these exercises, you should be able to:
- Create complete humanoid robot models with proper physics properties
- Configure physics parameters for stable and performant simulation
- Integrate sensors and validate their functionality
- Implement basic control algorithms for walking and balance
- Validate simulation results against expected behavior

Proceed to the next module to learn about digital twins and HRI implementation in Unity.