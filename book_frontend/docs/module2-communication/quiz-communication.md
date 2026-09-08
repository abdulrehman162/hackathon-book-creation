---
title: Quiz - ROS 2 Communication Model
sidebar_label: Quiz - Communication Model
sidebar_position: 4
description: Test your understanding of ROS 2 communication model
tags: [quiz, ros2, communication, nodes, topics, services]
---

# Quiz: ROS 2 Communication Model

## Multiple Choice Questions

### Question 1
What is the primary purpose of a node in ROS 2?
A) To store robot configuration data
B) To serve as a process that performs computation within the ROS 2 environment
C) To manage network connections between robots
D) To store sensor calibration data

<details>
<summary>Answer</summary>
B) To serve as a process that performs computation within the ROS 2 environment
</details>

### Question 2
Which communication pattern is best suited for continuous sensor data like camera images?
A) Services
B) Actions
C) Topics (publish/subscribe)
D) Parameters

<details>
<summary>Answer</summary>
C) Topics (publish/subscribe)
Topics are ideal for continuous data streams like sensor readings.
</details>

### Question 3
What does QoS stand for in the context of ROS 2 communication?
A) Quality of Service
B) Quick Operating System
C) Quantitative Operating System
D) Quality of Software

<details>
<summary>Answer</summary>
A) Quality of Service
</details>

### Question 4
Which QoS policy determines whether late-joining subscribers receive previous messages?
A) Reliability
B) History
C) Durability
D) Deadline

<details>
<summary>Answer</summary>
C) Durability
</details>

### Question 5
What is the main difference between topics and services in ROS 2?
A) Topics are faster than services
B) Topics are asynchronous publish/subscribe, services are synchronous request/response
C) Topics use more bandwidth than services
D) There is no significant difference

<details>
<summary>Answer</summary>
B) Topics are asynchronous publish/subscribe, services are synchronous request/response
</details>

## Short Answer Questions

### Question 6
Explain the publish-subscribe communication pattern in ROS 2 and give two examples of when it would be appropriate to use this pattern in a humanoid robot system.

<details>
<summary>Answer</summary>
In the publish-subscribe pattern:
- Publishers send data to a topic without knowing who will receive it
- Subscribers receive data from topics without knowing who published it
- The middleware handles the routing and delivery

Appropriate use cases in humanoid robots:
1. **Sensor data distribution**: Multiple perception algorithms need access to camera images or IMU data
2. **Robot state broadcasting**: Joint positions, robot pose, or system status need to be available to multiple consumers
</details>

### Question 7
Describe the three main communication patterns in ROS 2 and provide an example of when each would be most appropriate in a humanoid robot application.

<details>
<summary>Answer</summary>
1. **Topics (Publish/Subscribe)**: For continuous data streams
   - Example: Camera images, IMU data, joint states

2. **Services (Request/Response)**: For one-time requests with responses
   - Example: Calibration requests, state queries, configuration changes

3. **Actions**: For long-running tasks with feedback
   - Example: Walking to a location with periodic progress updates, executing complex manipulation tasks
</details>

### Question 8
What are the three main QoS policies related to message delivery in ROS 2, and how do they affect communication?

<details>
<summary>Answer</summary>
1. **Reliability**: Controls whether all messages must be delivered (reliable) or if some loss is acceptable (best effort)
2. **Durability**: Determines if late-joining subscribers receive previous messages (transient) or only new ones (volatile)
3. **History**: Specifies how many messages to keep in the queue for delivery
</details>

## Practical Application Questions

### Question 9
You are designing a communication architecture for a humanoid robot with the following components:
- 2 cameras (head and hand)
- 20 joint encoders
- 4 force/torque sensors (one in each foot, one in each hand)
- 1 IMU in the torso
- 1 microcontroller for each limb

Design an appropriate topic structure for this robot, including QoS considerations for each topic type. Justify your choices.

<details>
<summary>Answer</summary>
**Topic Structure:**
- `/sensors/cameras/head/image_raw` - QoS: Best effort, volatile (old images not useful)
- `/sensors/cameras/hand/image_raw` - QoS: Best effort, volatile
- `/sensors/joint_states` - QoS: Reliable, volatile (accuracy important, old data not useful)
- `/sensors/ft/left_foot/force_torque` - QoS: Reliable, volatile (safety-critical, accuracy important)
- `/sensors/ft/right_foot/force_torque` - QoS: Reliable, volatile
- `/sensors/ft/left_hand/force_torque` - QoS: Reliable, volatile
- `/sensors/ft/right_hand/force_torque` - QoS: Reliable, volatile
- `/sensors/imu/torso/data` - QoS: Reliable, volatile (accuracy important for balance)
- `/joint_commands` - QoS: Reliable, transient-local (late-joiners need current state)

**Justification:**
- Camera data uses best effort and volatile since old images have no value
- Joint states use reliable for accuracy in control systems
- Force/torque data uses reliable due to safety implications
- IMU data uses reliable for accurate balance control
- Joint commands use transient-local so late-joining nodes get current state
</details>

### Question 10
Explain the difference between the three node lifecycle states in ROS 2 (unconfigured, inactive, active) and why this is important for humanoid robot applications.

<details>
<summary>Answer</summary>
**Node Lifecycle States:**
1. **Unconfigured**: Node is created but not yet configured; parameters not set
2. **Inactive**: Node is configured with parameters but not yet activated; can't participate in communication
3. **Active**: Node is running and actively participating in communication

**Importance for Humanoid Robots:**
- **Safety**: Allows safe configuration of critical control parameters before activation
- **Synchronization**: Ensures all subsystems are properly configured before starting communication
- **Fault Tolerance**: Enables graceful transitions between states during errors
- **Maintenance**: Allows subsystems to be safely taken offline for maintenance without affecting the entire system
</details>

## Code Analysis Questions

### Question 11
Analyze the following rclpy code snippet and identify the communication patterns being used:

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory

class SimpleController(Node):
    def __init__(self):
        super().__init__('simple_controller')

        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.listener_callback,
            10)

        self.publisher = self.create_publisher(
            JointTrajectory,
            '/joint_trajectory_controller/joint_trajectory',
            10)

        self.timer = self.create_timer(0.01, self.timer_callback)

    def listener_callback(self, msg):
        # Process joint state
        pass

    def timer_callback(self):
        # Publish trajectory command
        msg = JointTrajectory()
        self.publisher.publish(msg)
```

What communication pattern is being implemented? What is the purpose of each component?

<details>
<summary>Answer</summary>
**Communication Pattern:** Publish/Subscribe (topics)

**Components:**
- **Subscription**: Subscribes to `/joint_states` topic to receive current joint positions
- **Publisher**: Publishes to `/joint_trajectory_controller/joint_trajectory` to send control commands
- **Timer**: Creates a control loop that runs at 100Hz (0.01s interval)
- **Callback**: Processes incoming joint state data
- **Timer callback**: Generates and publishes new trajectory commands

This implements a basic control loop where the controller receives sensor data (joint states) and generates control outputs (trajectory commands).
</details>

### Question 12
A humanoid robot needs to execute a complex walking motion that takes 5 seconds. Which communication pattern should be used for commanding this motion, and why?

<details>
<summary>Answer</summary>
**Answer:** Actions

**Reasoning:**
- Walking is a long-running task that takes 5 seconds
- The caller needs feedback on progress during execution
- The caller might need to cancel or modify the motion while it's in progress
- Services are synchronous and would block for 5 seconds
- Topics don't provide acknowledgment of task completion
- Actions provide goal, feedback, and result mechanisms suitable for long-running tasks
</details>

## Learning Objectives Assessment

After completing this quiz, you should be able to:
- Identify and explain the core communication patterns in ROS 2
- Design appropriate topic structures for robot systems
- Apply QoS policies appropriately for different use cases
- Understand the node lifecycle and its importance
- Choose the appropriate communication pattern for specific scenarios
- Implement basic communication patterns using rclpy