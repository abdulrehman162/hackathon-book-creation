---
title: Quiz - ROS 2 Fundamentals
sidebar_label: Quiz - Fundamentals
sidebar_position: 4
description: Test your understanding of ROS 2 fundamentals
tags: [quiz, ros2, fundamentals, test]
---

# Quiz: ROS 2 Fundamentals

## Multiple Choice Questions

### Question 1
What does DDS stand for in the context of ROS 2?
A) Distributed Data System
B) Data Distribution Service
C) Dynamic Data Sharing
D) Distributed Data Storage

<details>
<summary>Answer</summary>
B) Data Distribution Service
</details>

### Question 2
Which of the following is NOT a core characteristic of ROS 2?
A) Middleware for robot software
B) Language agnostic
C) Operating system replacement
D) Real-time capable

<details>
<summary>Answer</summary>
C) Operating system replacement
ROS 2 is a middleware framework, not an operating system replacement.
</details>

### Question 3
What makes DDS data-centric rather than message-centric?
A) It focuses on sending messages between specific endpoints
B) The middleware understands the data and manages distribution based on content
C) It only works with specific data types
D) It requires a central server for all communications

<details>
<summary>Answer</summary>
B) The middleware understands the data and manages distribution based on content
</details>

### Question 4
Which QoS policy controls how data is retained for late-joining subscribers?
A) Reliability
B) Deadline
C) Liveliness
D) Durability

<details>
<summary>Answer</summary>
D) Durability
</details>

### Question 5
Why is ROS 2 particularly well-suited for humanoid robots?
A) Because it's designed specifically for bipedal locomotion
B) Due to its ability to handle complex distributed systems with multiple domains
C) Because it only works with humanoid robot hardware
D) It's required by all humanoid robot manufacturers

<details>
<summary>Answer</summary>
B) Due to its ability to handle complex distributed systems with multiple domains
</details>

## Short Answer Questions

### Question 6
Explain the publish-subscribe pattern in ROS 2 and why it's beneficial for humanoid robots.

<details>
<summary>Answer</summary>
In the publish-subscribe pattern:
- Publishers create data without knowing who will consume it
- Subscribers express interest in specific types of data without knowing who produces it
- The DDS middleware handles routing and delivery

This is beneficial for humanoid robots because:
- It decouples different subsystems
- Enables multiple publishers and subscribers for the same data
- Allows new components to join without disrupting existing ones
- Supports the distributed nature of humanoid robot architectures
</details>

### Question 7
List three specific advantages of ROS 2 for humanoid robot development.

<details>
<summary>Answer</summary>
Three advantages of ROS 2 for humanoid robot development:
1. Real-time capabilities with configurable Quality of Service (QoS) policies
2. Proven ecosystem with tools, libraries, and community support
3. Scalability from single robots to multi-robot systems
</details>

### Question 8
Describe how DDS Quality of Service (QoS) policies can be used to meet different requirements in a humanoid robot system.

<details>
<summary>Answer</summary>
DDS QoS policies can be configured differently for various data types in a humanoid robot:
- **Control data**: High reliability and low latency for safety-critical commands
- **Sensor data**: Different durability settings (transient for maps, volatile for images)
- **Status information**: Deadline policies to ensure updates occur regularly
- **Debugging data**: Best-effort delivery to avoid impacting critical systems
</details>

## Practical Application Question

### Question 9
Imagine a humanoid robot with 2 cameras, 3 IMUs, 20 joint encoders, and 4 force/torque sensors. Design a topic organization for this robot using ROS 2 concepts. Consider what QoS policies you would use for each type of sensor data and justify your choices.

<details>
<summary>Answer</summary>
Topic organization:

**Camera data**:
- `/camera/head/image_raw` (volatile durability, best-effort reliability)
- `/camera/body/image_raw` (volatile durability, best-effort reliability)

**IMU data**:
- `/imu/head/data` (volatile durability, reliable reliability)
- `/imu/torso/data` (volatile durability, reliable reliability)
- `/imu/foot_left/data` (volatile durability, reliable reliability)

**Joint data**:
- `/joint_states` (transient-local durability, reliable reliability)

**Force/torque data**:
- `/ft_sensor/left_foot` (volatile durability, reliable reliability)
- `/ft_sensor/right_foot` (volatile durability, reliable reliability)
- `/ft_sensor/left_hand` (volatile durability, reliable reliability)
- `/ft_sensor/right_hand` (volatile durability, reliable reliability)

Justification:
- Camera data uses volatile durability since old images are not useful
- IMU and joint data use reliable reliability for accuracy
- Joint states use transient-local durability so late-joining nodes can get current state
- Force/torque data uses reliable reliability for safety-critical applications
</details>

## Learning Objectives Assessment

After completing this quiz, you should be able to:
- Define key ROS 2 and DDS concepts
- Explain the benefits of ROS 2 for humanoid robotics
- Apply QoS policies appropriately for different use cases
- Design topic organizations for complex robot systems