---
title: Exercise - DDS Concepts
sidebar_label: Exercise - DDS Concepts
sidebar_position: 5
description: Practical exercise to understand DDS concepts in ROS 2
tags: [exercise, dds, ros2, practical]
---

# Exercise: DDS Concepts in ROS 2

## Objective
This exercise will help you understand how DDS (Data Distribution Service) concepts apply to real-world robotics scenarios by designing a communication architecture for a humanoid robot.

## Scenario: Humanoid Robot Communication Design

You are tasked with designing the communication architecture for a humanoid robot that will be used for research in human-robot interaction. The robot has the following components:

### Hardware Components:
- **Head**: 2 cameras, 1 IMU, 2 microphones, 1 speaker, pan/tilt mechanism
- **Torso**: 1 main computer, 1 battery, 1 IMU, 2 force/torque sensors
- **Arms**: Each arm has 7 joints with encoders, 1 camera in each hand, 1 force/torque sensor at wrist
- **Legs**: Each leg has 6 joints with encoders, 4 force/torque sensors in each foot
- **Control Systems**: Joint controllers, motor drivers, power management

### Communication Requirements:
- Control loops running at 100Hz for joint control
- Perception pipeline processing at 30Hz for cameras
- Safety system monitoring at 1kHz
- Human interaction at 10Hz for audio processing

## Tasks

### Task 1: Topic Design (Individual Work - 15 minutes)
Design the DDS topics for this humanoid robot. Consider:

1. **Create a list of topics** for different types of data
2. **Group related topics** logically
3. **Consider the data flow** between different robot components

<details>
<summary>Example Structure</summary>

**Sensor Topics:**
- `/sensors/cameras/head_left/image_raw`
- `/sensors/cameras/head_right/image_raw`
- `/sensors/imu/head/data`
- `/sensors/imu/torso/data`
- `/sensors/joints/state`
- `/sensors/ft/left_foot/force_torque`
- `/sensors/ft/right_foot/force_torque`

**Control Topics:**
- `/controllers/joints/commands`
- `/controllers/head/pan_tilt`
- `/audio/speaker/output`

**Status Topics:**
- `/system/battery/state`
- `/system/safety/status`
- `/system/robot_state`
</details>

### Task 2: QoS Policy Assignment (Individual Work - 20 minutes)
For each topic you identified, assign appropriate Quality of Service (QoS) policies:

1. **Reliability**: Reliable vs Best Effort
2. **Durability**: Volatile vs Transient Local vs Transient vs Persistent
3. **Deadline**: Maximum time between consecutive samples
4. **Liveliness**: How to monitor publisher availability

Consider the communication requirements and safety aspects of each data type.

<details>
<summary>Guidelines for QoS Selection</summary>

**Joint Commands**: Reliable + Transient-Local (need guaranteed delivery, late-joiners need current state)
**Camera Images**: Best Effort + Volatile (old images not useful, loss acceptable)
**IMU Data**: Reliable + Volatile (accuracy important, old data not useful)
**Force/Torque**: Reliable + Volatile (safety-critical, accuracy important)
**Battery Status**: Reliable + Transient-Local (late-joiners need current battery state)
**Safety Status**: Reliable + Best Available (safety-critical, must be delivered)
</details>

### Task 3: System Architecture (Group Work - 25 minutes)
Sketch a communication architecture diagram showing:

1. **Different nodes** (processes) in the system
2. **Topics** connecting publishers and subscribers
3. **QoS policies** for critical connections
4. **Data flow** patterns

Consider how different computers on the robot might host different nodes.

### Task 4: Analysis Questions (Discussion - 15 minutes)

Answer these questions based on your design:

1. How does your topic design support the distributed nature of the humanoid robot?

2. What trade-offs did you make when selecting QoS policies for different topics?

3. How would your design handle a scenario where a safety-critical node fails?

4. How does DDS data-centricity benefit this robot compared to traditional message-passing?

## Discussion Points

### Scalability Considerations
- How would your design scale if additional sensors were added?
- What happens to network traffic as more topics are created?

### Performance Implications
- How do QoS policies affect real-time performance?
- What are the memory and CPU implications of different durability settings?

### Fault Tolerance
- How does your design handle node failures?
- What mechanisms ensure system safety during communication failures?

## Extension Activities

### Advanced Challenge (Optional)
Research and implement a simple DDS publisher-subscriber pair using the ROS 2 command line tools:
1. Create a simple publisher that sends mock sensor data
2. Create a subscriber that processes this data
3. Experiment with different QoS settings to observe the differences

Commands to research:
- `ros2 topic pub`
- `ros2 topic echo`
- Quality of service settings with `--qos-profile` flag

### Real-world Application
Research how actual humanoid robots (like those in RoboCup, NASA's robots, or commercial platforms) use DDS/ROS 2 and compare their approaches to your design.

## Learning Objectives Achieved

After completing this exercise, you should be able to:
- Design DDS topics for complex robot systems
- Select appropriate QoS policies based on system requirements
- Understand the trade-offs in DDS configuration
- Apply DDS concepts to real-world robotics scenarios
- Analyze the benefits of data-centric communication in robotics

## Evaluation Criteria

- **Completeness**: Did you identify all necessary topics for the robot?
- **Appropriateness**: Are your QoS selections appropriate for the use case?
- **Understanding**: Can you explain the reasoning behind your design choices?
- **Analysis**: Do you understand the implications of your design decisions?