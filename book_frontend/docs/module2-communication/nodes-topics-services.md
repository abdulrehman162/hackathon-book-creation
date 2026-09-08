---
title: Nodes, Topics, and Services
sidebar_label: Nodes, Topics, and Services
sidebar_position: 2
description: Understanding the core communication primitives in ROS 2
tags: [ros2, nodes, topics, services, communication]
---

# Nodes, Topics, and Services

## Nodes: The Building Blocks

A **node** in ROS 2 is an executable process that works within the ROS 2 environment. It's the basic unit of computation in a ROS 2 system. In humanoid robotics, nodes might represent:

- Individual sensor drivers
- Control algorithms for different limbs
- Perception systems (vision, localization)
- High-level behavior planners
- Human-robot interaction interfaces

### Creating a Node

In ROS 2, nodes are typically created by inheriting from the `Node` class in your chosen client library (rclpy for Python, rclcpp for C++):

```python
import rclpy
from rclpy.node import Node

class MyRobotNode(Node):
    def __init__(self):
        super().__init__('my_robot_node')
        # Node initialization code here
```

### Node Lifecycle

Nodes in ROS 2 have a well-defined lifecycle:
1. **Unconfigured**: Node created but not yet configured
2. **Inactive**: Node configured but not yet activated
3. **Active**: Node running and participating in communication
4. **Finalized**: Node shut down and cleaned up

## Topics: Publish-Subscribe Communication

**Topics** implement a publish-subscribe communication pattern where publishers send data to a topic and subscribers receive data from that topic. This is ideal for continuous data streams like:

- Sensor readings (camera images, IMU data, joint states)
- Robot state information
- Control commands
- System status updates

### Topic Characteristics

- **Asynchronous**: Publishers and subscribers don't need to be synchronized
- **Broadcast**: One publisher can send to multiple subscribers
- **Decoupled**: Publishers and subscribers don't need to know about each other
- **Typed**: Each topic has a specific message type that defines its structure

### Quality of Service (QoS) in Topics

Topics support various QoS policies that control communication behavior:
- **Reliability**: Reliable (all messages delivered) or Best Effort (no guarantee)
- **Durability**: Whether late-joiners receive previous messages
- **History**: How many messages to keep in the queue
- **Depth**: Size of the message queue

## Services: Request-Response Communication

**Services** implement a request-response pattern where a client sends a request to a server and receives a response. This is ideal for:

- Configuration changes
- One-time computations
- Commands that require acknowledgment
- State queries

### Service Characteristics

- **Synchronous**: The client waits for the response
- **One-to-one**: One client communicates with one server at a time
- **Request-Response**: Structured exchange with defined request and response types
- **Blocking**: The client is blocked until the response is received

## Practical Example: Humanoid Robot Communication

Let's consider how these concepts apply to a humanoid robot:

### Node Organization
```
JointControllerNode
├── Subscribes to: /joint_commands (topics)
├── Publishes to: /joint_states (topics)
└── Provides service: /calibrate_joints (services)

SensorFusionNode
├── Subscribes to: /camera/image_raw, /imu/data, /ft_sensor/data (topics)
└── Publishes to: /robot_pose, /environment_map (topics)

BehaviorPlannerNode
├── Subscribes to: /robot_state, /goal_commands (topics)
├── Publishes to: /motion_commands (topics)
└── Provides service: /get_robot_status (services)
```

### Topic Design for Humanoid Robots

For a humanoid robot with multiple sensors and actuators:

**Sensor Topics:**
- `/sensors/camera/head/image_raw` - Head camera images
- `/sensors/imu/torso/data` - Torso IMU data
- `/sensors/joint_states` - All joint positions, velocities, efforts
- `/sensors/ft/left_foot/force_torque` - Left foot force/torque sensors

**Control Topics:**
- `/joint_commands` - Desired joint positions/velocities
- `/motion_commands` - High-level motion commands
- `/gripper_commands` - Gripper control commands

**Status Topics:**
- `/robot_state` - Overall robot state
- `/battery_state` - Battery information
- `/system_status` - System health information

### Service Examples
- `/calibrate_sensors` - Calibrate various sensors
- `/get_robot_pose` - Query current robot pose
- `/set_operational_mode` - Change robot operational mode
- `/emergency_stop` - Trigger emergency stop sequence

## Best Practices for Humanoid Robot Communication

### Topic Design
1. **Group related data**: Use appropriate message types that group related information
2. **Consider bandwidth**: Balance update frequency with available bandwidth
3. **Use appropriate QoS**: Match QoS policies to the criticality and nature of the data
4. **Follow naming conventions**: Use consistent, descriptive names

### Node Design
1. **Single responsibility**: Each node should have a clear, focused purpose
2. **Error handling**: Implement robust error handling and recovery
3. **Resource management**: Properly manage memory and other resources
4. **Logging**: Include appropriate logging for debugging and monitoring

## Learning Objectives

After completing this chapter, you will be able to:
- Create and configure ROS 2 nodes for robot applications
- Design appropriate topics for different types of robot data
- Implement services for request-response communication
- Apply QoS policies appropriately for different use cases
- Understand the trade-offs between different communication patterns

## Practical Exercise Preparation

In the next chapter, we'll implement these concepts using rclpy to create a basic agent controller for a humanoid robot. Think about:
- What nodes would be needed for a basic humanoid robot?
- What topics would they need to communicate?
- What services would be useful for control and monitoring?

## Next Steps

Now that you understand the core communication primitives, we'll explore how to implement them using the rclpy library to create a basic agent controller flow.