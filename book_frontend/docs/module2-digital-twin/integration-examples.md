---
title: Integration Examples for Digital Twin Systems
sidebar_label: Integration Examples
sidebar_position: 7
description: Practical examples of integrating Gazebo physics simulation, Unity visualization, and ROS communication for comprehensive digital twin solutions
tags: [integration, digital-twin, gazebo, unity, ros, robotics, examples]
---

# Integration Examples for Digital Twin Systems

## Introduction to Digital Twin Integration

Digital twin systems for humanoid robotics require seamless integration between multiple components: physics simulation, visualization, sensor simulation, and communication frameworks. This chapter provides practical examples of how to integrate these systems to create comprehensive digital twin solutions that bridge the gap between simulation and reality.

The integration process involves connecting:
- **Gazebo**: For accurate physics simulation and sensor modeling
- **Unity**: For high-fidelity visualization and HRI interfaces
- **ROS/ROS2**: For communication and coordination between systems
- **Real Hardware**: When transitioning from simulation to reality

## Architecture Patterns for Digital Twin Integration

### Centralized Architecture

In a centralized architecture, one system (typically ROS/ROS2) acts as the central hub coordinating all components:

```
         Real Robot
             |
             v
        ROS Bridge
             |
    +--------+--------+
    |                 |
    v                 v
 Gazebo           Unity
Simulation    Visualization
```

#### Implementation Example
```python
#!/usr/bin/env python3
# Centralized integration example using ROS

import rospy
import roslib
from sensor_msgs.msg import JointState, LaserScan, Imu, Image
from geometry_msgs.msg import Twist, Pose
from nav_msgs.msg import Odometry
import threading
import time

class CentralizedDigitalTwin:
    def __init__(self):
        rospy.init_node('digital_twin_integration')

        # Publishers for Gazebo simulation
        self.joint_pub = rospy.Publisher('/gazebo/joint_commands', JointState, queue_size=10)
        self.cmd_vel_pub = rospy.Publisher('/gazebo/cmd_vel', Twist, queue_size=10)

        # Publishers for Unity visualization
        self.unity_joint_pub = rospy.Publisher('/unity/joint_states', JointState, queue_size=10)
        self.unity_pose_pub = rospy.Publisher('/unity/robot_pose', Pose, queue_size=10)

        # Subscribers from Gazebo
        rospy.Subscriber('/gazebo/joint_states', JointState, self.gazebo_joint_callback)
        rospy.Subscriber('/gazebo/laser_scan', LaserScan, self.laser_callback)
        rospy.Subscriber('/gazebo/imu/data', Imu, self.imu_callback)
        rospy.Subscriber('/gazebo/odom', Odometry, self.odom_callback)

        # Subscribers from Unity
        rospy.Subscriber('/unity/user_commands', Twist, self.user_command_callback)

        # Internal state
        self.current_joint_states = JointState()
        self.current_pose = Pose()

        print("Centralized Digital Twin initialized")

    def gazebo_joint_callback(self, msg):
        """Receive joint states from Gazebo and forward to Unity"""
        self.current_joint_states = msg
        self.unity_joint_pub.publish(msg)

    def laser_callback(self, msg):
        """Process LiDAR data and publish for visualization"""
        # Forward to Unity for visualization
        # Process for navigation algorithms
        pass

    def imu_callback(self, msg):
        """Process IMU data"""
        # Forward relevant data to Unity
        # Use for state estimation
        pass

    def odom_callback(self, msg):
        """Process odometry data"""
        self.current_pose.position = msg.pose.pose.position
        self.current_pose.orientation = msg.pose.pose.orientation
        self.unity_pose_pub.publish(self.current_pose)

    def user_command_callback(self, msg):
        """Process user commands from Unity interface"""
        # Forward to Gazebo for simulation
        self.cmd_vel_pub.publish(msg)

    def run(self):
        """Main execution loop"""
        rate = rospy.Rate(50)  # 50 Hz
        while not rospy.is_shutdown():
            # Synchronize data between systems
            self.synchronize_systems()
            rate.sleep()

    def synchronize_systems(self):
        """Ensure data consistency between Gazebo and Unity"""
        # Additional synchronization logic here
        pass

if __name__ == '__main__':
    dt = CentralizedDigitalTwin()
    try:
        dt.run()
    except rospy.ROSInterruptException:
        print("Digital twin integration stopped")
```

### Decentralized Architecture

In a decentralized architecture, systems communicate directly with each other:

```
Real Robot ↔ ROS ↔ Gazebo ↔ Unity
                    ↕
                 Other Systems
```

#### Implementation Example
```csharp
// Unity-side integration with direct ROS communication
using UnityEngine;
using RosSharp;

public class DecentralizedDigitalTwin : MonoBehaviour
{
    [Header("ROS Connection")]
    public string rosBridgeUrl = "ws://localhost:9090";

    [Header("Robot Configuration")]
    public Transform robotModel;
    public Transform[] jointTransforms;
    public string[] jointNames;

    private RosSocket rosSocket;
    private bool isConnected = false;

    void Start()
    {
        ConnectToROS();
    }

    void ConnectToROS()
    {
        try
        {
            rosSocket = new RosSocket(rosBridgeUrl);
            rosSocket.OnConnected += OnRosConnected;
            rosSocket.OnClosed += OnRosDisconnected;

            // Subscribe to Gazebo topics
            rosSocket.Subscribe<sensor_msgs.JointState>("/gazebo/joint_states", JointStateCallback);
            rosSocket.Subscribe<sensor_msgs.LaserScan>("/gazebo/laser_scan", LaserScanCallback);
            rosSocket.Subscribe<sensor_msgs.Imu>("/gazebo/imu/data", ImuCallback);

            // Subscribe to Unity topics (for HRI)
            rosSocket.Subscribe<geometry_msgs.Twist>("/unity/cmd_vel", UnityCommandCallback);
        }
        catch (System.Exception e)
        {
            Debug.LogError($"Failed to connect to ROS: {e.Message}");
        }
    }

    void OnRosConnected()
    {
        isConnected = true;
        Debug.Log("Connected to ROS bridge");

        // Publish initial robot state
        PublishRobotState();
    }

    void OnRosDisconnected()
    {
        isConnected = false;
        Debug.LogWarning("Disconnected from ROS bridge");
    }

    void JointStateCallback(sensor_msgs.JointState jointState)
    {
        // Update Unity robot model based on Gazebo joint states
        for (int i = 0; i < jointState.name.Count; i++)
        {
            string jointName = jointState.name[i];
            double jointPosition = jointState.position[i];

            for (int j = 0; j < jointNames.Length; j++)
            {
                if (jointNames[j] == jointName)
                {
                    // Apply joint rotation (simplified)
                    jointTransforms[j].localRotation = Quaternion.Euler(0, (float)jointPosition * Mathf.Rad2Deg, 0);
                    break;
                }
            }
        }
    }

    void LaserScanCallback(sensor_msgs.LaserScan scan)
    {
        // Process LiDAR data for visualization
        // Update point cloud visualization
        VisualizeLaserScan(scan);
    }

    void ImuCallback(sensor_msgs.Imu imu)
    {
        // Update robot orientation based on IMU data
        robotModel.rotation = new Quaternion(
            (float)imu.orientation.x,
            (float)imu.orientation.y,
            (float)imu.orientation.z,
            (float)imu.orientation.w
        );
    }

    void UnityCommandCallback(geometry_msgs.Twist cmd)
    {
        // Process commands from Unity HRI interface
        // Forward to Gazebo for simulation
        SendCommandToGazebo(cmd);
    }

    void VisualizeLaserScan(sensor_msgs.LaserScan scan)
    {
        // Create point cloud visualization in Unity
        // This would involve creating and updating Unity objects
    }

    void SendCommandToGazebo(geometry_msgs.Twist cmd)
    {
        // Publish command to Gazebo
        rosSocket.Publish("/gazebo/cmd_vel", cmd);
    }

    void PublishRobotState()
    {
        // Publish current Unity robot state
        sensor_msgs.JointState jointState = new sensor_msgs.JointState();
        jointState.header = new std_msgs.Header { stamp = new Time() };

        for (int i = 0; i < jointNames.Length; i++)
        {
            jointState.name.Add(jointNames[i]);
            jointState.position.Add(jointTransforms[i].localRotation.eulerAngles.y * Mathf.Deg2Rad);
        }

        rosSocket.Publish("/unity/joint_states", jointState);
    }

    void Update()
    {
        if (isConnected)
        {
            // Continuously publish Unity state for synchronization
            if (Time.frameCount % 30 == 0) // Every 30 frames
            {
                PublishRobotState();
            }
        }
    }
}
```

## Gazebo-Unity Integration Examples

### Real-time Synchronization

Creating real-time synchronization between Gazebo physics and Unity visualization:

#### ROS Bridge Configuration
```xml
<!-- launch file for Gazebo-Unity integration -->
<launch>
  <!-- Start Gazebo with robot model -->
  <include file="$(find gazebo_ros)/launch/empty_world.launch">
    <arg name="world_name" value="$(find my_robot_description)/worlds/humanoid_world.world"/>
    <arg name="paused" value="false"/>
    <arg name="use_sim_time" value="true"/>
    <arg name="gui" value="false"/>
    <arg name="headless" value="false"/>
    <arg name="debug" value="false"/>
  </include>

  <!-- Spawn robot in Gazebo -->
  <node name="spawn_urdf" pkg="gazebo_ros" type="spawn_model"
        args="-file $(find my_robot_description)/urdf/humanoid.urdf
              -urdf -model humanoid_robot -x 0 -y 0 -z 1" />

  <!-- Start ROS bridge for Unity communication -->
  <include file="$(find rosbridge_server)/launch/rosbridge_websocket.launch">
    <arg name="port" value="9090"/>
  </include>

  <!-- Start integration node -->
  <node name="gazebo_unity_bridge" pkg="my_integration_pkg" type="gazebo_unity_bridge.py" output="screen"/>

  <!-- TF broadcaster -->
  <node name="robot_state_publisher" pkg="robot_state_publisher" type="robot_state_publisher" />
</launch>
```

#### Synchronization Node
```python
#!/usr/bin/env python3
# Gazebo-Unity synchronization node

import rospy
import tf2_ros
import tf2_geometry_msgs
from sensor_msgs.msg import JointState
from geometry_msgs.msg import TransformStamped, Pose
from nav_msgs.msg import Odometry
import threading
import time

class GazeboUnitySync:
    def __init__(self):
        rospy.init_node('gazebo_unity_sync')

        # Publishers for Unity
        self.unity_joint_pub = rospy.Publisher('/unity/sync/joint_states', JointState, queue_size=10)
        self.unity_odom_pub = rospy.Publisher('/unity/sync/odometry', Odometry, queue_size=10)

        # Subscribers from Gazebo
        rospy.Subscriber('/gazebo/joint_states', JointState, self.joint_state_callback)
        rospy.Subscriber('/gazebo/odom', Odometry, self.odom_callback)

        # TF broadcaster for Unity
        self.tf_broadcaster = tf2_ros.TransformBroadcaster()

        # Synchronization parameters
        self.sync_rate = rospy.Rate(60)  # 60 Hz sync
        self.last_sync_time = rospy.Time.now()

        # State storage
        self.gazebo_joint_states = JointState()
        self.gazebo_odom = Odometry()
        self.state_lock = threading.Lock()

        rospy.loginfo("Gazebo-Unity synchronization initialized")

    def joint_state_callback(self, msg):
        """Receive joint states from Gazebo"""
        with self.state_lock:
            self.gazebo_joint_states = msg
            self.gazebo_joint_states.header.stamp = rospy.Time.now()

    def odom_callback(self, msg):
        """Receive odometry from Gazebo"""
        with self.state_lock:
            self.gazebo_odom = msg

    def synchronize(self):
        """Main synchronization loop"""
        while not rospy.is_shutdown():
            # Publish synchronized data to Unity
            self.publish_sync_data()

            # Broadcast transforms for Unity
            self.broadcast_transforms()

            self.sync_rate.sleep()

    def publish_sync_data(self):
        """Publish synchronized data to Unity"""
        with self.state_lock:
            # Publish joint states
            if len(self.gazebo_joint_states.name) > 0:
                self.unity_joint_pub.publish(self.gazebo_joint_states)

            # Publish odometry
            self.unity_odom_pub.publish(self.gazebo_odom)

    def broadcast_transforms(self):
        """Broadcast transforms for Unity visualization"""
        # Robot base transform
        t = TransformStamped()
        t.header.stamp = rospy.Time.now()
        t.header.frame_id = "world"
        t.child_frame_id = "robot_base"

        t.transform.translation.x = self.gazebo_odom.pose.pose.position.x
        t.transform.translation.y = self.gazebo_odom.pose.pose.position.y
        t.transform.translation.z = self.gazebo_odom.pose.pose.position.z

        t.transform.rotation = self.gazebo_odom.pose.pose.orientation

        self.tf_broadcaster.sendTransform(t)

        # Additional transforms for robot parts...
        # (joint-specific transforms would go here)

def main():
    sync_node = GazeboUnitySync()
    try:
        sync_node.synchronize()
    except rospy.ROSInterruptException:
        rospy.loginfo("Gazebo-Unity synchronization stopped")

if __name__ == '__main__':
    main()
```

### Sensor Data Integration

Integrating sensor data from Gazebo to Unity for visualization:

#### Sensor Processing Node
```python
#!/usr/bin/env python3
# Sensor data integration node

import rospy
import numpy as np
from sensor_msgs.msg import LaserScan, Image, Imu
from std_msgs.msg import Float32MultiArray
from visualization_msgs.msg import Marker, MarkerArray
import struct

class SensorIntegration:
    def __init__(self):
        rospy.init_node('sensor_integration')

        # Publishers for Unity visualization
        self.lidar_marker_pub = rospy.Publisher('/unity/lidar_markers', MarkerArray, queue_size=10)
        self.imu_viz_pub = rospy.Publisher('/unity/imu_visualization', Marker, queue_size=10)
        self.sensor_status_pub = rospy.Publisher('/unity/sensor_status', Float32MultiArray, queue_size=10)

        # Subscribers from Gazebo
        rospy.Subscriber('/gazebo/laser_scan', LaserScan, self.lidar_callback)
        rospy.Subscriber('/gazebo/imu/data', Imu, self.imu_callback)
        rospy.Subscriber('/gazebo/camera/image_raw', Image, self.camera_callback)

        # Sensor processing parameters
        self.lidar_range_threshold = 30.0  # meters
        self.imu_update_rate = 100  # Hz

        rospy.loginfo("Sensor integration node initialized")

    def lidar_callback(self, scan_msg):
        """Process LiDAR data for Unity visualization"""
        # Convert scan data to point cloud markers
        marker_array = MarkerArray()

        for i, range_val in enumerate(scan_msg.ranges):
            if range_val < scan_msg.range_max and range_val > scan_msg.range_min:
                marker = Marker()
                marker.header = scan_msg.header
                marker.ns = "lidar_points"
                marker.id = i
                marker.type = Marker.SPHERE
                marker.action = Marker.ADD

                # Calculate point position
                angle = scan_msg.angle_min + i * scan_msg.angle_increment
                x = range_val * np.cos(angle)
                y = range_val * np.sin(angle)
                z = 0.0  # Assuming 2D scan

                marker.pose.position.x = x
                marker.pose.position.y = y
                marker.pose.position.z = z
                marker.pose.orientation.w = 1.0

                marker.scale.x = 0.05
                marker.scale.y = 0.05
                marker.scale.z = 0.05

                marker.color.r = 1.0
                marker.color.g = 0.0
                marker.color.b = 0.0
                marker.color.a = 1.0

                marker_array.markers.append(marker)

        self.lidar_marker_pub.publish(marker_array)

    def imu_callback(self, imu_msg):
        """Process IMU data for Unity visualization"""
        # Create visualization marker for IMU orientation
        marker = Marker()
        marker.header = imu_msg.header
        marker.ns = "imu_orientation"
        marker.id = 0
        marker.type = Marker.ARROW
        marker.action = Marker.ADD

        # Set arrow direction based on orientation
        marker.pose.orientation = imu_msg.orientation
        marker.pose.position.z = 1.0  # Position above robot

        marker.scale.x = 0.5  # Arrow length
        marker.scale.y = 0.1
        marker.scale.z = 0.1

        marker.color.r = 0.0
        marker.color.g = 1.0
        marker.color.b = 0.0
        marker.color.a = 1.0

        self.imu_viz_pub.publish(marker)

        # Publish sensor status
        status_array = Float32MultiArray()
        status_array.data = [
            imu_msg.linear_acceleration.x,
            imu_msg.linear_acceleration.y,
            imu_msg.linear_acceleration.z,
            imu_msg.angular_velocity.x,
            imu_msg.angular_velocity.y,
            imu_msg.angular_velocity.z
        ]
        self.sensor_status_pub.publish(status_array)

    def camera_callback(self, img_msg):
        """Process camera data for Unity visualization"""
        # Camera data processing would go here
        # This could involve publishing image data to Unity
        pass

def main():
    sensor_node = SensorIntegration()
    rospy.spin()

if __name__ == '__main__':
    main()
```

## Unity-ROS Integration Examples

### Unity Robotics Package Integration

Using Unity's official robotics package for ROS communication:

#### Unity ROS Setup Script
```csharp
using UnityEngine;
using Unity.Robotics.Core;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Sensor;
using RosMessageTypes.Geometry;
using RosMessageTypes.Nav;

public class UnityROSBridge : MonoBehaviour
{
    [Header("ROS Configuration")]
    public string rosIP = "127.0.0.1";
    public int rosPort = 9090;

    [Header("Robot Components")]
    public Transform robotBase;
    public Transform[] jointTransforms;
    public string[] jointNames;

    private ROSConnection ros;
    private float updateRate = 30f; // Hz
    private float lastUpdateTime;

    void Start()
    {
        // Initialize ROS connection
        ros = ROSConnection.GetOrCreateInstance();
        ros.Initialize(rosIP, rosPort);

        // Subscribe to ROS topics
        ros.Subscribe<JointStateMsg>("/gazebo/joint_states", JointStateCallback);
        ros.Subscribe<LaserScanMsg>("/gazebo/laser_scan", LaserScanCallback);
        ros.Subscribe<ImuMsg>("/gazebo/imu/data", ImuCallback);

        // Start publishers
        InvokeRepeating("PublishJointStates", 0f, 1f/updateRate);

        Debug.Log("Unity-ROS bridge initialized");
    }

    void JointStateCallback(JointStateMsg jointState)
    {
        // Update Unity robot model based on ROS joint states
        for (int i = 0; i < jointState.name.Count; i++)
        {
            string jointName = jointState.name[i];
            double position = jointState.position[i];

            for (int j = 0; j < jointNames.Length; j++)
            {
                if (jointNames[j] == jointName)
                {
                    // Update joint transform
                    UpdateJointTransform(jointTransforms[j], (float)position);
                    break;
                }
            }
        }
    }

    void LaserScanCallback(LaserScanMsg scan)
    {
        // Process LiDAR data for visualization
        VisualizeLaserScan(scan);
    }

    void ImuCallback(ImuMsg imu)
    {
        // Update robot orientation based on IMU
        robotBase.rotation = new Quaternion(
            (float)imu.orientation.x,
            (float)imu.orientation.y,
            (float)imu.orientation.z,
            (float)imu.orientation.w
        );
    }

    void UpdateJointTransform(Transform joint, float angleRadians)
    {
        // Apply rotation to joint (adjust axis as needed)
        joint.localRotation = Quaternion.Euler(0, angleRadians * Mathf.Rad2Deg, 0);
    }

    void VisualizeLaserScan(LaserScanMsg scan)
    {
        // Create visualization of LiDAR points
        // This could involve instantiating game objects or updating point clouds
    }

    void PublishJointStates()
    {
        // Publish current Unity joint states back to ROS
        JointStateMsg jointState = new JointStateMsg();
        jointState.header = new std_msgs.Header();
        jointState.header.stamp = new Time();
        jointState.header.frame_id = "unity";

        for (int i = 0; i < jointNames.Length; i++)
        {
            jointState.name.Add(jointNames[i]);
            // Convert Unity rotation to joint position
            float jointPos = jointTransforms[i].localRotation.eulerAngles.y * Mathf.Deg2Rad;
            jointState.position.Add(jointPos);
        }

        ros.Publish("/unity/joint_states", jointState);
    }

    void OnApplicationQuit()
    {
        if (ros != null)
        {
            ros.Close();
        }
    }
}
```

### HRI Interface Integration

Creating HRI interfaces that work with the integrated system:

#### HRI Command Handler
```csharp
using UnityEngine;
using UnityEngine.UI;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Geometry;

public class HRICommandHandler : MonoBehaviour
{
    [Header("HRI Interface Components")]
    public Slider linearVelocitySlider;
    public Slider angularVelocitySlider;
    public Button moveForwardButton;
    public Button moveBackwardButton;
    public Button turnLeftButton;
    public Button turnRightButton;
    public Button stopButton;
    public Text statusText;

    [Header("ROS Configuration")]
    public string cmdVelTopic = "/robot/cmd_vel";

    private ROSConnection ros;
    private float linearVelocity = 0f;
    private float angularVelocity = 0f;

    void Start()
    {
        ros = ROSConnection.GetOrCreateInstance();

        // Setup button events
        SetupButtonEvents();

        // Setup slider events
        linearVelocitySlider.onValueChanged.AddListener(OnLinearVelocityChanged);
        angularVelocitySlider.onValueChanged.AddListener(OnAngularVelocityChanged);

        // Initialize sliders
        linearVelocitySlider.value = 0f;
        angularVelocitySlider.value = 0f;

        statusText.text = "Ready for commands";
    }

    void SetupButtonEvents()
    {
        moveForwardButton.onClick.AddListener(() => SetVelocities(0.5f, 0f));
        moveBackwardButton.onClick.AddListener(() => SetVelocities(-0.5f, 0f));
        turnLeftButton.onClick.AddListener(() => SetVelocities(0f, 0.5f));
        turnRightButton.onClick.AddListener(() => SetVelocities(0f, -0.5f));
        stopButton.onClick.AddListener(() => SetVelocities(0f, 0f));
    }

    void OnLinearVelocityChanged(float value)
    {
        linearVelocity = value;
        SendCommand();
    }

    void OnAngularVelocityChanged(float value)
    {
        angularVelocity = value;
        SendCommand();
    }

    void SetVelocities(float linear, float angular)
    {
        linearVelocitySlider.value = linear;
        angularVelocitySlider.value = angular;
        linearVelocity = linear;
        angularVelocity = angular;
        SendCommand();
    }

    void SendCommand()
    {
        // Create and send velocity command
        TwistMsg cmdVel = new TwistMsg();
        cmdVel.linear = new Vector3Msg(linearVelocity, 0, 0);
        cmdVel.angular = new Vector3Msg(0, 0, angularVelocity);

        ros.Publish(cmdVelTopic, cmdVel);

        // Update status
        statusText.text = $"Cmd: Lin={linearVelocity:F2}, Ang={angularVelocity:F2}";
    }

    public void EmergencyStop()
    {
        SetVelocities(0f, 0f);
        statusText.text = "EMERGENCY STOP";
        Debug.LogWarning("Emergency stop activated!");
    }
}
```

## Practical Integration Scenarios

### Scenario 1: Teleoperation System

A complete teleoperation system integrating all components:

#### Teleoperation System Architecture
```csharp
using UnityEngine;
using System.Collections;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Sensor;
using RosMessageTypes.Geometry;
using RosMessageTypes.Nav;

public class TeleoperationSystem : MonoBehaviour
{
    [Header("System Components")]
    public UnityROSBridge rosBridge;
    public HRICommandHandler hriHandler;
    public Camera mainCamera;

    [Header("Visualization Components")]
    public GameObject lidarPointCloud;
    public GameObject pathVisualization;
    public GameObject targetMarker;

    [Header("Safety Parameters")]
    public float maxLinearVelocity = 1.0f;
    public float maxAngularVelocity = 1.5f;
    public float safetyDistance = 0.5f;
    public bool safetyEnabled = true;

    private bool isConnected = false;
    private Vector3 robotPosition;
    private Quaternion robotOrientation;

    void Start()
    {
        InitializeSystem();
    }

    void InitializeSystem()
    {
        // Initialize ROS connection
        rosBridge = GetComponent<UnityROSBridge>();
        hriHandler = GetComponent<HRICommandHandler>();

        if (rosBridge != null)
        {
            StartCoroutine(CheckConnection());
        }
    }

    IEnumerator CheckConnection()
    {
        yield return new WaitForSeconds(2f); // Wait for ROS connection

        isConnected = true;
        Debug.Log("Teleoperation system ready");

        // Start main system loop
        StartCoroutine(MainLoop());
    }

    IEnumerator MainLoop()
    {
        while (isConnected)
        {
            // Update system status
            UpdateSystemStatus();

            // Check safety conditions
            if (safetyEnabled)
            {
                CheckSafetyConditions();
            }

            yield return new WaitForSeconds(0.033f); // ~30 FPS
        }
    }

    void UpdateSystemStatus()
    {
        // Update robot position and orientation from ROS data
        // This would typically come from TF or odometry topics
    }

    void CheckSafetyConditions()
    {
        // Check for obstacles using LiDAR data
        // This would involve processing point cloud data
        // and stopping the robot if obstacles are too close
    }

    public void SetTargetPosition(Vector3 target)
    {
        if (!isConnected) return;

        // Send navigation goal to robot
        // This would involve sending a navigation goal message
        Debug.Log($"Setting navigation target: {target}");
    }

    public void ToggleSafetySystem()
    {
        safetyEnabled = !safetyEnabled;
        Debug.Log($"Safety system {(safetyEnabled ? "enabled" : "disabled")}");
    }

    void OnApplicationQuit()
    {
        // Ensure robot stops when application exits
        if (hriHandler != null)
        {
            hriHandler.EmergencyStop();
        }
    }
}
```

### Scenario 2: Training Environment

A comprehensive training environment for robot learning:

#### Training Environment Manager
```csharp
using UnityEngine;
using System.Collections.Generic;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Actionlib;

public class TrainingEnvironmentManager : MonoBehaviour
{
    [Header("Training Configuration")]
    public int episodeCount = 1000;
    public float maxEpisodeTime = 60f; // seconds
    public float resetDelay = 2f;

    [Header("Environment Components")]
    public GameObject[] obstacles;
    public Transform[] spawnPoints;
    public GameObject[] targetObjects;

    [Header("Reward System")]
    public float successReward = 100f;
    public float timePenalty = -0.1f;
    public float collisionPenalty = -10f;

    private int currentEpisode = 0;
    private float episodeStartTime;
    private bool isEpisodeActive = false;
    private List<float> episodeRewards = new List<float>();

    void Start()
    {
        StartNewEpisode();
    }

    void StartNewEpisode()
    {
        if (currentEpisode >= episodeCount)
        {
            Debug.Log("Training completed!");
            return;
        }

        // Reset environment
        ResetEnvironment();

        // Reset robot position
        ResetRobotPosition();

        // Start episode timer
        episodeStartTime = Time.time;
        isEpisodeActive = true;

        Debug.Log($"Starting episode {currentEpisode + 1}/{episodeCount}");
        currentEpisode++;
    }

    void ResetEnvironment()
    {
        // Randomize obstacle positions
        foreach (GameObject obstacle in obstacles)
        {
            if (obstacle != null)
            {
                int randomSpawn = Random.Range(0, spawnPoints.Length);
                obstacle.transform.position = spawnPoints[randomSpawn].position;
            }
        }

        // Randomize target position
        if (targetObjects.Length > 0)
        {
            int randomTarget = Random.Range(0, targetObjects.Length);
            int randomSpawn = Random.Range(0, spawnPoints.Length);
            targetObjects[randomTarget].transform.position = spawnPoints[randomSpawn].position;
        }
    }

    void ResetRobotPosition()
    {
        // Reset robot to starting position
        // This would involve sending reset commands via ROS
    }

    void Update()
    {
        if (isEpisodeActive)
        {
            float episodeTime = Time.time - episodeStartTime;

            // Check episode timeout
            if (episodeTime > maxEpisodeTime)
            {
                EndEpisode(false, "Episode timeout");
            }
        }
    }

    public void ReportSuccess()
    {
        if (isEpisodeActive)
        {
            EndEpisode(true, "Task completed successfully");
        }
    }

    public void ReportCollision()
    {
        if (isEpisodeActive)
        {
            // Apply collision penalty
            float reward = collisionPenalty;
            SendReward(reward);

            // End episode on collision (typical for safety-critical tasks)
            EndEpisode(false, "Collision detected");
        }
    }

    void EndEpisode(bool success, string reason)
    {
        isEpisodeActive = false;

        float episodeTime = Time.time - episodeStartTime;
        float finalReward = success ? successReward : 0;
        finalReward += episodeTime * timePenalty; // Time penalty

        episodeRewards.Add(finalReward);

        Debug.Log($"Episode {currentEpisode} ended - {reason} | Reward: {finalReward:F2}");

        // Wait before starting next episode
        StartCoroutine(StartNextEpisodeAfterDelay());
    }

    IEnumerator StartNextEpisodeAfterDelay()
    {
        yield return new WaitForSeconds(resetDelay);
        StartNewEpisode();
    }

    void SendReward(float reward)
    {
        // Send reward to learning system via ROS
        // This would involve custom message types for reinforcement learning
    }

    public float GetAverageReward()
    {
        if (episodeRewards.Count == 0) return 0f;

        float sum = 0f;
        foreach (float reward in episodeRewards)
        {
            sum += reward;
        }

        return sum / episodeRewards.Count;
    }
}
```

## Performance Optimization

### Efficient Data Transmission

Optimizing the data flow between integrated systems:

#### Data Compression and Filtering
```csharp
using UnityEngine;
using System.Collections.Generic;

public class DataOptimizationManager : MonoBehaviour
{
    [Header("Optimization Parameters")]
    public float jointUpdateRate = 30f; // Hz
    public float sensorUpdateRate = 10f; // Hz
    public float visualizationUpdateRate = 15f; // Hz
    public float dataCompressionThreshold = 0.01f; // Minimum change to transmit

    private Dictionary<string, float> lastJointPositions = new Dictionary<string, float>();
    private Dictionary<string, float> lastSensorValues = new Dictionary<string, float>();
    private float lastJointUpdateTime;
    private float lastSensorUpdateTime;
    private float lastVisualizationTime;

    public bool ShouldUpdateJoints()
    {
        return Time.time - lastJointUpdateTime >= 1f / jointUpdateRate;
    }

    public bool ShouldUpdateSensors()
    {
        return Time.time - lastSensorUpdateTime >= 1f / sensorUpdateRate;
    }

    public bool ShouldUpdateVisualization()
    {
        return Time.time - lastVisualizationTime >= 1f / visualizationUpdateRate;
    }

    public bool ShouldTransmitJoint(string jointName, float currentValue)
    {
        if (!lastJointPositions.ContainsKey(jointName))
        {
            lastJointPositions[jointName] = currentValue;
            return true;
        }

        float lastValue = lastJointPositions[jointName];
        bool shouldTransmit = Mathf.Abs(currentValue - lastValue) > dataCompressionThreshold;

        if (shouldTransmit)
        {
            lastJointPositions[jointName] = currentValue;
        }

        return shouldTransmit;
    }

    public void UpdateTiming()
    {
        if (ShouldUpdateJoints())
        {
            lastJointUpdateTime = Time.time;
        }

        if (ShouldUpdateSensors())
        {
            lastSensorUpdateTime = Time.time;
        }

        if (ShouldUpdateVisualization())
        {
            lastVisualizationTime = Time.time;
        }
    }
}
```

## Troubleshooting Integration Issues

### Common Integration Problems and Solutions

#### Synchronization Issues
- **Problem**: Gazebo and Unity positions diverge over time
- **Solution**: Implement proper TF synchronization and timestamp handling

#### Performance Problems
- **Problem**: High CPU/GPU usage due to excessive data transmission
- **Solution**: Implement data rate limiting and compression

#### Communication Failures
- **Problem**: ROS bridge connections dropping
- **Solution**: Implement reconnection logic and error handling

#### Data Integrity Issues
- **Problem**: Sensor data corruption or loss
- **Solution**: Implement checksums and data validation

## Best Practices for Integration

### Design Principles

1. **Modular Architecture**: Keep components loosely coupled
2. **Error Handling**: Implement robust error detection and recovery
3. **Performance Monitoring**: Continuously monitor system performance
4. **Documentation**: Maintain clear documentation of integration points
5. **Testing**: Implement comprehensive integration testing

### Security Considerations

- **Network Security**: Secure ROS bridge connections
- **Data Validation**: Validate all incoming data
- **Access Control**: Implement proper authentication mechanisms
- **Monitoring**: Monitor for unusual data patterns

## Summary

Integration of digital twin systems requires careful coordination between multiple complex components. By following established architecture patterns, implementing proper synchronization mechanisms, and maintaining robust error handling, you can create stable and reliable integrated systems that bridge the gap between simulation and reality.

The examples provided demonstrate practical approaches to common integration challenges, from basic ROS-Unity communication to complex multi-component systems. The key to successful integration lies in understanding the specific requirements of your use case and implementing appropriate optimization and validation strategies.

As digital twin technology continues to evolve, integration patterns will also advance, incorporating new technologies and methodologies to create even more sophisticated and capable systems.