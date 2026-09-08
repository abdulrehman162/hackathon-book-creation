---
title: Practical Exercise - Isaac ROS VSLAM Implementation
sidebar_label: Exercise - VSLAM Implementation
sidebar_position: 14
description: Hands-on exercise to implement Visual SLAM using Isaac ROS hardware-accelerated algorithms
tags: [exercise, vslam, isaac-ros, visual-slam, robotics, gpu-acceleration, computer-vision, slam]
---

# Practical Exercise: Isaac ROS VSLAM Implementation

## Exercise Overview

In this hands-on exercise, you will implement a complete Visual SLAM (Simultaneous Localization and Mapping) system using NVIDIA Isaac ROS. You'll learn to configure and deploy hardware-accelerated VSLAM nodes, integrate them with a robotics system, and validate the performance of your implementation.

### Learning Objectives
By completing this exercise, you will be able to:
- Configure Isaac ROS Visual SLAM nodes for your specific robot
- Integrate VSLAM into a complete robotics pipeline
- Optimize VSLAM performance for your hardware
- Validate and troubleshoot VSLAM results
- Evaluate VSLAM performance metrics

### Prerequisites
- Isaac ROS installation completed
- Working ROS 2 environment
- Camera sensor connected to your robot or simulated environment
- Understanding of SLAM concepts
- Completed previous Isaac ROS modules

## Exercise Setup

### Required Equipment
- NVIDIA GPU (RTX 2060 or higher recommended)
- Robot with calibrated camera or Isaac Sim environment
- Calibration data for camera sensors
- ROS 2 Humble environment with Isaac ROS packages

### Initial Configuration
1. Verify Isaac ROS installation with `ros2 pkg list | grep isaac_ros`
2. Ensure GPU is accessible with `nvidia-smi`
3. Verify camera calibration files are available

## Part 1: Basic VSLAM Configuration

### Task 1.1: Launch Isaac ROS Visual SLAM Node

Create a launch file to configure and launch the Isaac ROS Visual SLAM node:

```python
# Create file: launch/basic_vslam.launch.py
import launch
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    """Launch Isaac ROS Visual SLAM with basic configuration"""

    # Get Isaac ROS share directory
    isaac_ros_visual_slam_dir = get_package_share_directory('isaac_ros_visual_slam')

    # Load configuration file
    config_file_path = os.path.join(
        isaac_ros_visual_slam_dir,
        'config',
        'visual_slam_config.yaml'
    )

    # Create Visual SLAM node
    visual_slam_node = Node(
        package='isaac_ros_visual_slam',
        executable='visual_slam_node',
        parameters=[
            config_file_path,
            {
                # Basic configuration
                'enable_rectification': True,
                'enable_debug_mode': False,

                # Frame IDs
                'map_frame': 'map',
                'odom_frame': 'odom',
                'base_frame': 'base_link',
                'camera_frame': 'camera_link',

                # Feature tracking parameters
                'enable_localization': True,
                'max_num_landmarks': 1000,
                'min_num_images': 3,
                'max_num_images': 5,

                # Map building parameters
                'enable_occupancy_map': False,  # Enable only if needed
                'occupancy_map_resolution': 0.05,  # 5cm resolution
            }
        ],
        remappings=[
            # Remap topics to match your camera topic names
            ('/visual_slam/image', '/camera/image_rect_color'),
            ('/visual_slam/camera_info', '/camera/camera_info'),
        ],
        output='screen'
    )

    # Create pose graph optimizer node
    pose_graph_optimizer_node = Node(
        package='isaac_ros_visual_slam',
        executable='pose_graph_optimizer',
        parameters=[
            {
                'max_iterations': 100,
                'convergence_threshold': 1e-6,
                'lambda_initial': 1e-4,
            }
        ],
        output='screen'
    )

    return launch.LaunchDescription([
        visual_slam_node,
        pose_graph_optimizer_node
    ])
```

### Task 1.2: Create Custom VSLAM Configuration

Create a custom configuration file for your specific use case:

```yaml
# Create file: config/custom_vslam_config.yaml
/**:
  ros__parameters:
    # Feature detection and tracking
    feature_detector:
      max_features: 1000
      quality_level: 0.01
      min_distance: 10
      block_size: 3
      use_harris_detector: false
      k: 0.04

    # Descriptor extraction
    descriptor_extractor:
      patch_size: 31
      fast_threshold: 20
      upright: false

    # Tracking parameters
    tracker:
      window_size: [21, 21]
      max_level: 3
      criteria: [20, 0.03]
      min_eigenvalue_threshold: 0.001

    # Optimization parameters
    optimizer:
      max_iterations: 50
      convergence_threshold: 1e-5
      trust_region_radius: 1.0
      regularization_parameter: 1e-8

    # Loop closure detection
    loop_closure:
      enable_loop_closure: true
      descriptor_matching_threshold: 0.7
      minimum_inliers: 20
      minimum_pose_distance: 1.0
      minimum_yaw_difference: 0.5

    # Map management
    map_manager:
      max_map_size: 5000
      landmark_visibility_threshold: 0.5
      outlier_rejection_threshold: 3.0
```

### Task 1.3: Launch and Test Basic Configuration

1. Save both files in your workspace
2. Build your workspace: `cd ~/isaac_ros_workspace && colcon build`
3. Source the workspace: `source install/setup.bash`
4. Launch the VSLAM system: `ros2 launch your_package basic_vslam.launch.py`

Verify that:
- The Visual SLAM node starts without errors
- GPU usage increases (monitor with `nvidia-smi`)
- Appropriate topics are published (check with `ros2 topic list`)

## Part 2: Advanced VSLAM Features

### Task 2.1: Implement Loop Closure Detection

Enhance your VSLAM configuration with loop closure capabilities:

```python
# Create file: launch/advanced_vslam.launch.py
import launch
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    """Launch Isaac ROS Visual SLAM with advanced features"""

    # Declare launch arguments
    input_width_arg = DeclareLaunchArgument(
        'input_width',
        default_value='640',
        description='Input image width'
    )

    input_height_arg = DeclareLaunchArgument(
        'input_height',
        default_value='480',
        description='Input image height'
    )

    # Get Isaac ROS share directory
    isaac_ros_visual_slam_dir = get_package_share_directory('isaac_ros_visual_slam')

    # Create Visual SLAM node with advanced configuration
    visual_slam_node = Node(
        package='isaac_ros_visual_slam',
        executable='visual_slam_node',
        parameters=[
            os.path.join(isaac_ros_visual_slam_dir, 'config', 'visual_slam_config.yaml'),
            {
                'enable_rectification': True,
                'enable_debug_mode': False,
                'enable_localization': True,
                'enable_mapping': True,

                # Frame configuration
                'map_frame': 'map',
                'odom_frame': 'odom',
                'base_frame': 'base_link',
                'camera_frame': 'camera_color_optical_frame',

                # Feature parameters
                'max_num_landmarks': 2000,
                'min_num_images': 4,
                'max_num_images': 10,

                # Advanced loop closure
                'enable_loop_closure': True,
                'loop_closure_threshold': 0.7,
                'minimum_inliers': 25,
                'minimum_pose_distance': 1.0,
                'minimum_yaw_difference': 0.5,

                # Input dimensions
                'input_width': LaunchConfiguration('input_width'),
                'input_height': LaunchConfiguration('input_height'),
            }
        ],
        remappings=[
            ('/visual_slam/image', '/camera/color/image_rect_color'),
            ('/visual_slam/camera_info', '/camera/color/camera_info'),
        ],
        output='screen'
    )

    # Create loop closure detection node
    loop_closure_node = Node(
        package='isaac_ros_visual_slam',
        executable='loop_closure_node',
        parameters=[
            {
                'database_size': 1000,
                'matching_threshold': 0.7,
                'num_neighbors': 5,
                'min_matches': 20,
            }
        ],
        output='screen'
    )

    # Create pose graph optimizer
    pose_graph_optimizer = Node(
        package='isaac_ros_visual_slam',
        executable='pose_graph_optimizer',
        parameters=[
            {
                'max_iterations': 100,
                'convergence_threshold': 1e-6,
                'lambda_initial': 1e-4,
                'enable_marginalization': True,
                'marginalization_window_size': 50,
            }
        ],
        output='screen'
    )

    return launch.LaunchDescription([
        input_width_arg,
        input_height_arg,
        visual_slam_node,
        loop_closure_node,
        pose_graph_optimizer
    ])
```

### Task 2.2: Add Visual Odometry Integration

Create a launch file that integrates visual odometry with the VSLAM system:

```python
# Create file: launch/integrated_vslam.launch.py
import launch
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    """Launch integrated VSLAM with visual odometry"""

    # Visual Odometry node
    visual_odometry_node = Node(
        package='isaac_ros_visual_slam',
        executable='visual_odometry_node',
        parameters=[
            {
                'enable_rectification': True,
                'max_num_features': 1000,
                'min_num_features': 100,
                'tracking_threshold': 20,
                'relocalization_threshold': 50,
                'max_keyframes': 200,
            }
        ],
        remappings=[
            ('/visual_odometry/image', '/camera/image_rect_color'),
            ('/visual_odometry/camera_info', '/camera/camera_info'),
        ],
        output='screen'
    )

    # VSLAM node
    visual_slam_node = Node(
        package='isaac_ros_visual_slam',
        executable='visual_slam_node',
        parameters=[
            {
                'enable_localization': True,
                'enable_mapping': True,
                'max_num_landmarks': 1500,
                'min_num_images': 3,
                'max_num_images': 8,
                'enable_loop_closure': True,
            }
        ],
        remappings=[
            ('/visual_slam/image', '/camera/image_rect_color'),
            ('/visual_slam/camera_info', '/camera/camera_info'),
        ],
        output='screen'
    )

    # Odometry to TF broadcaster
    odom_broadcaster = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[
            {
                'use_sim_time': False,
                'publish_frequency': 50.0,
            }
        ],
        output='screen'
    )

    return launch.LaunchDescription([
        visual_odometry_node,
        visual_slam_node,
        odom_broadcaster
    ])
```

## Part 3: Performance Optimization

### Task 3.1: Configure GPU Memory Management

Create a performance-optimized configuration for your VSLAM system:

```yaml
# Create file: config/performance_vslam.yaml
/**:
  ros__parameters:
    # GPU memory management
    gpu_memory_pool_size: 100000000  # 100MB
    enable_gpu_memory_pool: true
    cuda_device_id: 0

    # Performance parameters
    enable_async_processing: true
    max_queue_size: 10
    enable_profiler: false  # Set to true only for debugging

    # Feature processing optimization
    feature_detector:
      max_features: 800  # Reduced for performance
      quality_level: 0.02  # Increased for performance
      min_distance: 8  # Reduced for more features
      adaptive_suppression: true

    # Descriptor optimization
    descriptor_extractor:
      patch_size: 21  # Smaller for speed
      compute_dtype: 'fp16'  # Half precision for speed

    # Tracking optimization
    tracker:
      window_size: [15, 15]  # Smaller window
      max_level: 2  # Fewer pyramid levels
      criteria: [15, 0.05]  # Fewer iterations

    # Optimization performance
    optimizer:
      max_iterations: 30  # Reduced for real-time
      convergence_threshold: 1e-4  # Looser threshold
      enable_sparse_solver: true
      sparse_solver_type: 'cuda_cholmod'

    # Loop closure performance
    loop_closure:
      enable_loop_closure: true
      descriptor_matching_threshold: 0.6  # Lower for more matches
      minimum_inliers: 15  # Reduced for speed
      detection_frequency: 5  # Check every 5th frame
```

### Task 3.2: Implement Adaptive Processing

Create a launch file with adaptive processing capabilities:

```python
# Create file: launch/adaptive_vslam.launch.py
import launch
from launch_ros.actions import Node, LifecycleNode
from launch.actions import TimerAction
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    """Launch adaptive VSLAM with performance monitoring"""

    # Performance monitor node
    performance_monitor = Node(
        package='isaac_ros_visual_slam',
        executable='performance_monitor',
        parameters=[
            {
                'monitor_frequency': 10.0,  # 10 Hz monitoring
                'latency_threshold': 0.033,  # 30fps threshold
                'memory_threshold': 0.8,  # 80% memory usage
                'adaptive_processing': True,
            }
        ],
        output='screen'
    )

    # Adaptive VSLAM node
    adaptive_vslam = Node(
        package='isaac_ros_visual_slam',
        executable='adaptive_visual_slam_node',
        parameters=[
            os.path.join(get_package_share_directory('isaac_ros_visual_slam'),
                        'config', 'adaptive_config.yaml'),
            {
                'enable_adaptive_processing': True,
                'performance_target_fps': 30,
                'quality_priority': 'latency',  # 'quality', 'balance', 'latency'
                'min_features': 200,
                'max_features': 1200,
            }
        ],
        remappings=[
            ('/adaptive_vslam/image', '/camera/image_rect_color'),
            ('/adaptive_vslam/camera_info', '/camera/camera_info'),
        ],
        output='screen'
    )

    # Dynamic reconfigure node for runtime parameter adjustment
    dynamic_reconfigure = Node(
        package='dynamic_reconfigure',
        executable='dynamic_reconfigure',
        parameters=[
            {
                'feature_count_range': [200, 1200],
                'processing_quality_levels': ['low', 'medium', 'high'],
            }
        ],
        output='screen'
    )

    return launch.LaunchDescription([
        performance_monitor,
        adaptive_vslam,
        dynamic_reconfigure
    ])
```

## Part 4: Integration and Testing

### Task 4.1: Integrate with Navigation System

Create a launch file that integrates VSLAM with a navigation system:

```python
# Create file: launch/vslam_navigation_integration.launch.py
import launch
from launch_ros.actions import Node
from launch.actions import GroupAction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    """Launch VSLAM integrated with navigation stack"""

    # Launch arguments
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation time'
    )

    # VSLAM system
    vslam_group = GroupAction(
        condition=IfCondition(LaunchConfiguration('enable_vslam', default='true')),
        actions=[
            Node(
                package='isaac_ros_visual_slam',
                executable='visual_slam_node',
                name='visual_slam',
                parameters=[
                    {
                        'enable_localization': True,
                        'enable_mapping': True,
                        'map_frame': 'map',
                        'odom_frame': 'odom',
                        'base_frame': 'base_link',
                        'camera_frame': 'camera_color_optical_frame',
                        'use_sim_time': LaunchConfiguration('use_sim_time'),
                    }
                ],
                remappings=[
                    ('/visual_slam/image', '/camera/image_rect_color'),
                    ('/visual_slam/camera_info', '/camera/camera_info'),
                    ('/visual_slam/pose', '/visual_slam/pose'),
                    ('/visual_slam/trajectory', '/visual_slam/trajectory'),
                ],
                output='screen'
            ),

            Node(
                package='tf2_ros',
                executable='static_transform_publisher',
                name='camera_link_broadcaster',
                arguments=['0.1', '0', '0.2', '0', '0', '0', 'base_link', 'camera_link']
            )
        ]
    )

    # Navigation system
    navigation_group = GroupAction(
        condition=IfCondition(LaunchConfiguration('enable_navigation', default='true')),
        actions=[
            Node(
                package='nav2_map_server',
                executable='map_server',
                parameters=[
                    {
                        'use_sim_time': LaunchConfiguration('use_sim_time'),
                        'yaml_filename': '/path/to/your/map.yaml',  # Replace with actual map
                    }
                ],
                output='screen'
            ),

            Node(
                package='nav2_amcl',
                executable='amcl',
                parameters=[
                    {
                        'use_sim_time': LaunchConfiguration('use_sim_time'),
                        'initial_pose': {'x': 0.0, 'y': 0.0, 'z': 0.0, 'yaw': 0.0},
                        'set_initial_pose': True,
                    }
                ],
                output='screen'
            ),

            Node(
                package='nav2_planner',
                executable='planner_server',
                parameters=[
                    {
                        'use_sim_time': LaunchConfiguration('use_sim_time'),
                    }
                ],
                output='screen'
            ),

            Node(
                package='nav2_controller',
                executable='controller_server',
                parameters=[
                    {
                        'use_sim_time': LaunchConfiguration('use_sim_time'),
                    }
                ],
                output='screen'
            )
        ]
    )

    # TF bridge to connect VSLAM and navigation
    tf_bridge = Node(
        package='isaac_ros_visual_slam',
        executable='tf_bridge_node',
        parameters=[
            {
                'use_sim_time': LaunchConfiguration('use_sim_time'),
                'map_frame': 'map',
                'odom_frame': 'odom',
                'base_frame': 'base_link',
                'vslam_frame': 'visual_slam_frame',
            }
        ],
        output='screen'
    )

    return launch.LaunchDescription([
        use_sim_time_arg,
        vslam_group,
        navigation_group,
        tf_bridge
    ])
```

### Task 4.2: Create Validation Tests

Create a validation script to test your VSLAM implementation:

```python
# Create file: test/vslam_validation.py
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, TransformStamped
from sensor_msgs.msg import Image
from std_msgs.msg import Header
import tf2_ros
import numpy as np
from scipy.spatial.transform import Rotation as R
import time

class VSLAMValidator(Node):
    def __init__(self):
        super().__init__('vslam_validator')

        # Initialize TF2 buffer and listener
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        # Publishers and subscribers
        self.pose_sub = self.create_subscription(
            PoseStamped,
            '/visual_slam/pose',
            self.pose_callback,
            10
        )

        self.image_sub = self.create_subscription(
            Image,
            '/camera/image_rect_color',
            self.image_callback,
            10
        )

        # Storage for validation data
        self.poses = []
        self.timestamps = []
        self.performance_metrics = {
            'average_processing_time': 0,
            'frame_rate': 0,
            'tracking_success_rate': 0,
            'drift_rate': 0
        }

        # Validation timers
        self.validation_timer = self.create_timer(1.0, self.run_validation)
        self.start_time = time.time()

        self.get_logger().info('VSLAM Validator initialized')

    def pose_callback(self, msg):
        """Store pose estimates for validation"""
        self.poses.append({
            'position': [msg.pose.position.x, msg.pose.position.y, msg.pose.position.z],
            'orientation': [msg.pose.orientation.w, msg.pose.orientation.x,
                           msg.pose.orientation.y, msg.pose.orientation.z],
            'timestamp': msg.header.stamp
        })
        self.timestamps.append(msg.header.stamp)

    def image_callback(self, msg):
        """Track image processing for performance validation"""
        # This could be used to measure image processing time
        pass

    def run_validation(self):
        """Run validation checks"""
        if len(self.poses) < 2:
            return

        # Calculate metrics
        self.calculate_frame_rate()
        self.calculate_drift_rate()
        self.calculate_tracking_stability()

        # Print validation results
        self.print_validation_results()

    def calculate_frame_rate(self):
        """Calculate effective frame rate"""
        if len(self.timestamps) < 2:
            return

        # Calculate time difference between first and last pose
        time_diff = (self.timestamps[-1].sec - self.timestamps[0].sec) + \
                   (self.timestamps[-1].nanosec - self.timestamps[0].nanosec) * 1e-9

        if time_diff > 0:
            self.performance_metrics['frame_rate'] = (len(self.timestamps) - 1) / time_diff

    def calculate_drift_rate(self):
        """Calculate position drift rate"""
        if len(self.poses) < 10:  # Need sufficient data
            return

        # Calculate displacement over time
        positions = np.array([pose['position'] for pose in self.poses])
        displacements = np.linalg.norm(np.diff(positions, axis=0), axis=1)

        # Average displacement per frame indicates drift
        avg_displacement = np.mean(displacements)
        self.performance_metrics['drift_rate'] = avg_displacement

    def calculate_tracking_stability(self):
        """Calculate tracking stability metrics"""
        if len(self.poses) < 5:
            return

        # Calculate pose changes to assess stability
        positions = np.array([pose['position'] for pose in self.poses])
        pose_changes = np.linalg.norm(np.diff(positions, axis=0), axis=1)

        # Stability is inversely related to sudden pose changes
        stability_score = 1.0 / (1.0 + np.std(pose_changes))
        self.performance_metrics['tracking_stability'] = stability_score

    def print_validation_results(self):
        """Print validation results"""
        self.get_logger().info('=== VSLAM Validation Results ===')
        self.get_logger().info(f'Frame Rate: {self.performance_metrics["frame_rate"]:.2f} Hz')
        self.get_logger().info(f'Drift Rate: {self.performance_metrics["drift_rate"]:.4f} m/frame')
        self.get_logger().info(f'Tracking Stability: {self.performance_metrics["tracking_stability"]:.4f}')
        self.get_logger().info(f'Total Poses: {len(self.poses)}')

        # Assess quality
        if self.performance_metrics['frame_rate'] >= 25:
            self.get_logger().info('✓ Good frame rate performance')
        else:
            self.get_logger().warn('⚠ Low frame rate - consider optimization')

        if self.performance_metrics['drift_rate'] < 0.01:  # 1cm per frame threshold
            self.get_logger().info('✓ Low drift rate - good localization')
        else:
            self.get_logger().warn('⚠ High drift rate - check calibration or lighting')

    def run_comprehensive_test(self, duration=60):
        """Run comprehensive test for specified duration"""
        self.get_logger().info(f'Starting comprehensive VSLAM test for {duration} seconds')

        start_time = time.time()
        while time.time() - start_time < duration:
            rclpy.spin_once(self, timeout_sec=0.1)

        self.final_validation_report()

    def final_validation_report(self):
        """Generate final validation report"""
        self.get_logger().info('\n=== FINAL VSLAM VALIDATION REPORT ===')

        for metric, value in self.performance_metrics.items():
            self.get_logger().info(f'{metric}: {value}')

        # Overall assessment
        score = 0
        if self.performance_metrics['frame_rate'] >= 25:
            score += 1
        if self.performance_metrics['drift_rate'] < 0.01:
            score += 1
        if self.performance_metrics['tracking_stability'] > 0.5:
            score += 1

        if score >= 2:
            self.get_logger().info('✅ VSLAM SYSTEM PASSED VALIDATION')
        else:
            self.get_logger().error('❌ VSLAM SYSTEM FAILED VALIDATION')

        self.get_logger().info('==================================')

def main(args=None):
    rclpy.init(args=args)

    validator = VSLAMValidator()

    # Run for 60 seconds of testing
    validator.run_comprehensive_test(duration=60)

    validator.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Part 5: Troubleshooting and Optimization

### Task 5.1: Create Performance Monitoring Dashboard

Create a simple performance monitoring script:

```python
# Create file: scripts/vslam_monitor.py
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Float32
import time
import psutil
import GPUtil
from collections import deque

class VSLAMMonitor(Node):
    def __init__(self):
        super().__init__('vslam_monitor')

        # Performance tracking
        self.frame_times = deque(maxlen=30)  # Last 30 frames
        self.gpu_load_history = deque(maxlen=30)
        self.cpu_load_history = deque(maxlen=30)

        # Subscriptions
        self.image_sub = self.create_subscription(
            Image, '/camera/image_rect_color', self.image_callback, 10
        )
        self.pose_sub = self.create_subscription(
            PoseStamped, '/visual_slam/pose', self.pose_callback, 10
        )

        # Publishers for performance metrics
        self.fps_pub = self.create_publisher(Float32, '/vslam/fps', 10)
        self.gpu_load_pub = self.create_publisher(Float32, '/vslam/gpu_load', 10)
        self.cpu_load_pub = self.create_publisher(Float32, '/vslam/cpu_load', 10)

        # Timers
        self.monitor_timer = self.create_timer(1.0, self.publish_performance_metrics)
        self.last_frame_time = time.time()

        self.get_logger().info('VSLAM Performance Monitor initialized')

    def image_callback(self, msg):
        """Monitor frame processing time"""
        current_time = time.time()
        frame_time = current_time - self.last_frame_time
        self.frame_times.append(frame_time)
        self.last_frame_time = current_time

    def pose_callback(self, msg):
        """Monitor pose update frequency"""
        pass

    def publish_performance_metrics(self):
        """Publish current performance metrics"""
        # Calculate FPS
        if len(self.frame_times) > 0:
            avg_frame_time = sum(self.frame_times) / len(self.frame_times)
            fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0.0

            fps_msg = Float32()
            fps_msg.data = float(fps)
            self.fps_pub.publish(fps_msg)

        # Monitor GPU usage
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu_load = gpus[0].load * 100  # Convert to percentage
            self.gpu_load_history.append(gpu_load)

            gpu_msg = Float32()
            gpu_msg.data = float(gpu_load)
            self.gpu_load_pub.publish(gpu_msg)

        # Monitor CPU usage
        cpu_load = psutil.cpu_percent(interval=1)
        self.cpu_load_history.append(cpu_load)

        cpu_msg = Float32()
        cpu_msg.data = float(cpu_load)
        self.cpu_load_pub.publish(cpu_msg)

        # Log warnings if thresholds exceeded
        if gpus and gpus[0].load > 0.9:  # 90% GPU usage
            self.get_logger().warn('⚠ GPU usage high - consider optimization')

        if cpu_load > 80:  # 80% CPU usage
            self.get_logger().warn('⚠ CPU usage high - consider optimization')

        if len(self.frame_times) > 0 and fps < 20:  # Below 20 FPS
            self.get_logger().warn('⚠ Low frame rate - consider optimization')

        # Print current status
        self.get_logger().info(
            f'FPS: {fps:.1f}, GPU: {gpu_load:.1f}%, CPU: {cpu_load:.1f}%'
        )

def main(args=None):
    rclpy.init(args=args)

    monitor = VSLAMMonitor()

    try:
        rclpy.spin(monitor)
    except KeyboardInterrupt:
        pass
    finally:
        monitor.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Task 5.2: Implement Adaptive Parameter Adjustment

Create a node that automatically adjusts VSLAM parameters based on performance:

```python
# Create file: scripts/adaptive_param_controller.py
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from rcl_interfaces.msg import Parameter, ParameterValue
from rcl_interfaces.srv import SetParameters
import time

class AdaptiveParameterController(Node):
    def __init__(self):
        super().__init__('adaptive_parameter_controller')

        # Performance subscriptions
        self.fps_sub = self.create_subscription(Float32, '/vslam/fps', self.fps_callback, 10)
        self.gpu_load_sub = self.create_subscription(Float32, '/vslam/gpu_load', self.gpu_load_callback, 10)
        self.cpu_load_sub = self.create_subscription(Float32, '/vslam/cpu_load', self.cpu_load_callback, 10)

        # Parameter adjustment timer
        self.param_adjust_timer = self.create_timer(5.0, self.adjust_parameters)

        # Performance tracking
        self.current_fps = 30.0
        self.current_gpu_load = 50.0
        self.current_cpu_load = 50.0

        # Parameter clients for VSLAM nodes
        self.vslam_param_client = self.create_client(SetParameters, '/visual_slam/set_parameters')

        # Parameter thresholds
        self.fps_threshold = 25.0  # Target FPS
        self.gpu_threshold = 80.0  # Max GPU usage %
        self.cpu_threshold = 80.0  # Max CPU usage %

        self.get_logger().info('Adaptive Parameter Controller initialized')

    def fps_callback(self, msg):
        self.current_fps = msg.data

    def gpu_load_callback(self, msg):
        self.current_gpu_load = msg.data

    def cpu_load_callback(self, msg):
        self.current_cpu_load = msg.data

    def adjust_parameters(self):
        """Adjust VSLAM parameters based on current performance"""
        self.get_logger().info(f'Current status - FPS: {self.current_fps:.1f}, '
                              f'GPU: {self.current_gpu_load:.1f}%, '
                              f'CPU: {self.current_cpu_load:.1f}%')

        # Adjust parameters based on performance
        params_to_change = []

        # If FPS is too low, reduce computational load
        if self.current_fps < self.fps_threshold * 0.8:  # 80% of target
            self.get_logger().info('FPS below threshold, reducing computational load')

            # Reduce feature count
            feature_param = Parameter()
            feature_param.name = 'max_num_features'
            feature_param.value = ParameterValue(type=3, integer_value=600)  # Reduce from default
            params_to_change.append(feature_param)

            # Reduce optimization iterations
            opt_param = Parameter()
            opt_param.name = 'max_optimization_iterations'
            opt_param.value = ParameterValue(type=3, integer_value=20)  # Reduce from default
            params_to_change.append(opt_param)

        # If GPU usage is too high, reduce GPU load
        elif self.current_gpu_load > self.gpu_threshold:
            self.get_logger().info('GPU usage high, reducing GPU load')

            # Reduce patch size for descriptors
            patch_param = Parameter()
            patch_param.name = 'descriptor_patch_size'
            patch_param.value = ParameterValue(type=3, integer_value=15)  # Smaller patches
            params_to_change.append(patch_param)

        # If performance is good, consider increasing quality
        elif (self.current_fps > self.fps_threshold * 1.1 and
              self.current_gpu_load < self.gpu_threshold * 0.7):
            self.get_logger().info('Performance good, increasing quality')

            # Increase feature count
            feature_param = Parameter()
            feature_param.name = 'max_num_features'
            feature_param.value = ParameterValue(type=3, integer_value=1200)  # Increase
            params_to_change.append(feature_param)

        # Apply parameter changes if needed
        if params_to_change and self.vslam_param_client.service_is_ready():
            future = self.vslam_param_client.call_async(
                SetParameters.Request(parameters=params_to_change)
            )
            future.add_done_callback(self.parameter_change_callback)

    def parameter_change_callback(self, future):
        """Handle parameter change response"""
        try:
            response = future.result()
            for result in response.results:
                if result.successful:
                    self.get_logger().info(f'Parameter changed successfully: {result.name}')
                else:
                    self.get_logger().error(f'Parameter change failed: {result.name} - {result.reason}')
        except Exception as e:
            self.get_logger().error(f'Parameter change service call failed: {e}')

def main(args=None):
    rclpy.init(args=args)

    controller = AdaptiveParameterController()

    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        pass
    finally:
        controller.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Assessment Criteria

Your VSLAM implementation will be evaluated on:
- **Correctness**: VSLAM system properly configured and running
- **Performance**: Achieves target frame rates and accuracy
- **Robustness**: Handles various lighting and motion conditions
- **Optimization**: Efficient use of GPU resources
- **Integration**: Properly integrated with navigation system
- **Validation**: Thorough testing and validation performed

## Conclusion

This exercise provided hands-on experience implementing a complete Isaac ROS VSLAM system. You've learned to:
- Configure and launch Isaac ROS VSLAM nodes
- Optimize performance for your specific hardware
- Integrate VSLAM with navigation systems
- Validate and troubleshoot VSLAM performance
- Implement adaptive parameter control for optimal performance

The skills developed in this exercise are directly applicable to real-world robotics applications where accurate, real-time localization and mapping are critical for autonomous navigation and operation.