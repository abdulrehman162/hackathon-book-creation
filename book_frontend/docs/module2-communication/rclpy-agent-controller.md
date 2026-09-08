---
title: rclpy Agent Controller Implementation
sidebar_label: rclpy Agent Controller
sidebar_position: 3
description: Implementing a basic agent controller using rclpy in ROS 2
tags: [rclpy, ros2, controller, python, implementation]
---

# rclpy Agent Controller Implementation

## Introduction to rclpy

**rclpy** is the Python client library for ROS 2. It provides Python bindings for the ROS 2 client library (rcl), allowing you to create ROS 2 nodes, publish and subscribe to topics, provide and use services, and more, all using Python.

For humanoid robotics applications, rclpy is particularly valuable because:
- Python is excellent for rapid prototyping and algorithm development
- Many AI and machine learning libraries have Python interfaces
- It's accessible to researchers and developers with varying backgrounds
- It integrates well with scientific computing libraries

## Basic Node Structure

Let's start by examining the basic structure of a ROS 2 node using rclpy:

```python
import rclpy
from rclpy.node import Node

class SimpleControllerNode(Node):
    def __init__(self):
        super().__init__('simple_controller')
        self.get_logger().info('Simple Controller Node initialized')

def main(args=None):
    rclpy.init(args=args)
    node = SimpleControllerNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Implementing a Basic Agent Controller

An agent controller in humanoid robotics typically needs to:
1. Subscribe to sensor data
2. Process information and make decisions
3. Publish control commands
4. Handle services for configuration and monitoring

Let's implement a simple agent controller that demonstrates these concepts:

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration

class AgentController(Node):
    def __init__(self):
        super().__init__('agent_controller')

        # Subscribe to joint states
        self.joint_state_subscriber = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )

        # Publisher for joint commands
        self.joint_command_publisher = self.create_publisher(
            JointTrajectory,
            '/joint_trajectory_controller/joint_trajectory',
            10
        )

        # Timer for control loop
        self.control_timer = self.create_timer(0.01, self.control_loop)  # 100Hz

        # Internal state
        self.current_joint_positions = {}
        self.target_positions = {}

        self.get_logger().info('Agent Controller initialized')

    def joint_state_callback(self, msg):
        """Callback for processing joint state messages"""
        for i, name in enumerate(msg.name):
            if i < len(msg.position):
                self.current_joint_positions[name] = msg.position[i]

    def control_loop(self):
        """Main control loop"""
        # This is where the agent's decision-making happens
        # For this example, we'll implement a simple position controller

        # Create a joint trajectory message
        trajectory_msg = JointTrajectory()
        trajectory_msg.joint_names = list(self.current_joint_positions.keys())

        # Create trajectory point
        point = JointTrajectoryPoint()

        # Set positions (in this example, we're just echoing current positions)
        # In a real controller, this would be computed based on desired behavior
        for joint_name in trajectory_msg.joint_names:
            current_pos = self.current_joint_positions.get(joint_name, 0.0)
            # Simple example: target is current position + small offset
            target_pos = current_pos + 0.01
            point.positions.append(target_pos)

        # Set time from start (100ms duration)
        point.time_from_start = Duration(sec=0, nanosec=100000000)

        trajectory_msg.points.append(point)

        # Publish the trajectory
        self.joint_command_publisher.publish(trajectory_msg)

def main(args=None):
    rclpy.init(args=args)
    agent_controller = AgentController()

    try:
        rclpy.spin(agent_controller)
    except KeyboardInterrupt:
        agent_controller.get_logger().info('Shutting down agent controller...')
    finally:
        agent_controller.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Advanced Agent Controller Features

### State Management

A more sophisticated agent controller needs to maintain state and make decisions based on that state:

```python
from enum import Enum

class RobotState(Enum):
    IDLE = 1
    MOVING = 2
    STABILIZING = 3
    EMERGENCY_STOP = 4

class AdvancedAgentController(Node):
    def __init__(self):
        super().__init__('advanced_agent_controller')

        # State management
        self.current_state = RobotState.IDLE
        self.previous_state = RobotState.IDLE

        # Subscribe to various sensor topics
        self.imu_subscriber = self.create_subscription(
            Imu,  # Assuming we have an IMU message
            '/imu/data',
            self.imu_callback,
            10
        )

        self.joint_state_subscriber = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )

        # Publisher for commands
        self.command_publisher = self.create_publisher(
            JointTrajectory,
            '/joint_trajectory_controller/joint_trajectory',
            10
        )

        # Timer for state machine
        self.state_machine_timer = self.create_timer(0.01, self.state_machine)

        self.get_logger().info('Advanced Agent Controller initialized')

    def state_machine(self):
        """Main state machine for the agent controller"""
        # Determine next state based on current conditions
        if self.is_emergency_condition():
            self.current_state = RobotState.EMERGENCY_STOP
        elif self.is_stabilizing_condition():
            self.current_state = RobotState.STABILIZING
        elif self.has_motion_command():
            self.current_state = RobotState.MOVING
        else:
            self.current_state = RobotState.IDLE

        # Execute behavior based on current state
        if self.current_state != self.previous_state:
            self.handle_state_transition()

        self.execute_current_state()
        self.previous_state = self.current_state

    def is_emergency_condition(self):
        # Check for emergency conditions (e.g., dangerous IMU readings)
        return False  # Placeholder implementation

    def is_stabilizing_condition(self):
        # Check if stabilization is needed
        return False  # Placeholder implementation

    def has_motion_command(self):
        # Check if there's a motion command to execute
        return False  # Placeholder implementation

    def handle_state_transition(self):
        """Handle actions when transitioning between states"""
        self.get_logger().info(f'State transition: {self.previous_state} -> {self.current_state}')

    def execute_current_state(self):
        """Execute behavior for the current state"""
        if self.current_state == RobotState.IDLE:
            self.execute_idle_behavior()
        elif self.current_state == RobotState.MOVING:
            self.execute_moving_behavior()
        elif self.current_state == RobotState.STABILIZING:
            self.execute_stabilizing_behavior()
        elif self.current_state == RobotState.EMERGENCY_STOP:
            self.execute_emergency_stop()

    def execute_idle_behavior(self):
        # Maintain current position or return to neutral pose
        pass

    def execute_moving_behavior(self):
        # Execute planned motion
        pass

    def execute_stabilizing_behavior(self):
        # Execute stabilization algorithms
        pass

    def execute_emergency_stop(self):
        # Execute emergency stop procedures
        pass
```

## Integration with Humanoid Robotics

For humanoid robots specifically, agent controllers often need to handle:

### Balance and Stability
```python
def calculate_balance_control(self, imu_data, joint_states):
    """Calculate control outputs to maintain balance"""
    # Use IMU data and joint states to compute balance corrections
    # This might involve inverse kinematics, center of mass calculations, etc.
    pass
```

### Multi-Limb Coordination
```python
def coordinate_limbs(self, desired_behavior):
    """Coordinate multiple limbs for complex behaviors"""
    # Plan and execute coordinated movements across arms, legs, and torso
    pass
```

### Human-Robot Interaction
```python
def handle_interaction(self, interaction_data):
    """Process human-robot interaction inputs"""
    # Handle voice commands, gestures, or other interaction modalities
    pass
```

## Testing Your Agent Controller

### Using ROS 2 Command Line Tools

You can test your agent controller using ROS 2 command line tools:

```bash
# Check if your node is running
ros2 node list

# Check the topics your node is publishing/subscribing to
ros2 node info <your_node_name>

# Echo messages from topics
ros2 topic echo /joint_states

# Publish messages to test your controller
ros2 topic pub /joint_commands trajectory_msgs/JointTrajectory "..."
```

### Creating a Simple Test Script

```python
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration

class ControllerTester(Node):
    def __init__(self):
        super().__init__('controller_tester')

        self.test_publisher = self.create_publisher(
            JointTrajectory,
            '/joint_trajectory_controller/joint_trajectory',
            10
        )

        # Send test command after 2 seconds
        self.timer = self.create_timer(2.0, self.send_test_command)

    def send_test_command(self):
        # Create and send a simple test command
        trajectory_msg = JointTrajectory()
        trajectory_msg.joint_names = ['joint1', 'joint2']  # Example joint names

        point = JointTrajectoryPoint()
        point.positions = [0.5, -0.3]  # Example positions
        point.time_from_start = Duration(sec=1, nanosec=0)

        trajectory_msg.points.append(point)

        self.test_publisher.publish(trajectory_msg)
        self.get_logger().info('Test command sent')

def main(args=None):
    rclpy.init(args=args)
    tester = ControllerTester()

    try:
        rclpy.spin_once(tester, timeout_sec=5)  # Run for 5 seconds
    except KeyboardInterrupt:
        pass
    finally:
        tester.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Learning Objectives

After completing this chapter, you will be able to:
- Create ROS 2 nodes using rclpy
- Implement publishers and subscribers for robot communication
- Design and implement agent controllers with state management
- Apply control patterns appropriate for humanoid robots
- Test and validate controller implementations
- Understand the relationship between agent controllers and robot behaviors

## Best Practices for Agent Controllers

1. **Error Handling**: Always include proper error handling and graceful degradation
2. **State Management**: Use clear state machines for complex behaviors
3. **Safety**: Implement safety checks and emergency procedures
4. **Performance**: Optimize for real-time performance requirements
5. **Modularity**: Keep controllers focused on specific tasks
6. **Logging**: Include appropriate logging for debugging and monitoring

## Next Steps

Now that you understand how to implement agent controllers using rclpy, we'll create a quiz to test your understanding of the communication model and practical exercises to reinforce your learning.