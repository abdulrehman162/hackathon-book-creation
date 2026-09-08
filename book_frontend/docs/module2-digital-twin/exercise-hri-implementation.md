---
title: Practical Exercise - HRI Implementation in Unity
sidebar_label: Exercise - HRI Implementation
sidebar_position: 9
description: Hands-on exercise to implement Human-Robot Interaction interfaces in Unity for digital twin applications
tags: [exercise, hri, unity, interaction, robotics, humanoid, practical]
---

# Practical Exercise: HRI Implementation in Unity

## Exercise Overview

In this exercise, you will implement a complete Human-Robot Interaction (HRI) interface in Unity for a humanoid robot digital twin. You'll create intuitive controls, safety systems, and visualization elements that allow users to safely interact with and control a simulated humanoid robot.

### Learning Objectives
By completing this exercise, you will be able to:
- Design and implement intuitive HRI interfaces in Unity
- Create safety systems for robot control interfaces
- Implement multi-modal interaction mechanisms
- Validate HRI interface effectiveness through user testing

### Prerequisites
- Basic knowledge of Unity UI system
- Understanding of ROS/ROS2 communication
- Familiarity with humanoid robot kinematics
- Completed previous chapters on Unity integration

## Exercise Setup

### Required Assets
- Unity 2021.3 LTS or later
- Unity Robotics Package
- Humanoid robot model (URDF or FBX)
- Sample environment scene

### Initial Configuration
1. Create a new Unity 3D project
2. Import the Unity Robotics Package
3. Import your humanoid robot model
4. Set up a basic scene with the robot model

## Part 1: Basic Control Interface

### Task 1.1: Create Robot Status Dashboard
Create a UI dashboard that displays real-time robot status information.

**Implementation Steps:**
1. Create a Canvas with a Robot Status Panel
2. Add text elements for:
   - Robot name and ID
   - Battery level
   - Operational status
   - Current task
   - Joint temperatures (simulated)
3. Add visual indicators (colored images) for status
4. Create a script to update status information

**Sample Script:**
```csharp
using UnityEngine;
using UnityEngine.UI;

public class RobotStatusDashboard : MonoBehaviour
{
    [Header("Status Elements")]
    public Text robotNameText;
    public Text batteryLevelText;
    public Text operationalStatusText;
    public Text currentTaskText;
    public Image statusIndicator;
    public Slider batterySlider;

    [Header("Joint Temperature Indicators")]
    public Text[] jointTempTexts;
    public Slider[] jointTempSliders;

    [Header("ROS Connection")]
    public string statusTopic = "/robot/status";

    private float batteryLevel = 100f;
    private string operationalStatus = "OPERATIONAL";
    private string currentTask = "IDLE";

    void Start()
    {
        // Initialize the dashboard
        InitializeDashboard();
    }

    void InitializeDashboard()
    {
        robotNameText.text = "Humanoid Robot HR-01";
        UpdateBatteryLevel(batteryLevel);
        UpdateOperationalStatus(operationalStatus);
        UpdateCurrentTask(currentTask);
    }

    public void UpdateBatteryLevel(float level)
    {
        batteryLevel = Mathf.Clamp(level, 0f, 100f);
        batteryLevelText.text = $"Battery: {batteryLevel:F1}%";
        batterySlider.value = batteryLevel;

        // Update color based on battery level
        if (batteryLevel > 50)
            batteryLevelText.color = Color.green;
        else if (batteryLevel > 20)
            batteryLevelText.color = Color.yellow;
        else
            batteryLevelText.color = Color.red;
    }

    public void UpdateOperationalStatus(string status)
    {
        operationalStatus = status;
        operationalStatusText.text = $"Status: {status}";

        // Update status indicator color
        switch (status.ToUpper())
        {
            case "OPERATIONAL":
                statusIndicator.color = Color.green;
                break;
            case "WARNING":
                statusIndicator.color = Color.yellow;
                break;
            case "ERROR":
            case "EMERGENCY":
                statusIndicator.color = Color.red;
                break;
            default:
                statusIndicator.color = Color.gray;
                break;
        }
    }

    public void UpdateCurrentTask(string task)
    {
        currentTask = task;
        currentTaskText.text = $"Current Task: {task}";
    }

    public void UpdateJointTemperatures(float[] temperatures)
    {
        for (int i = 0; i < jointTempTexts.Length && i < temperatures.Length; i++)
        {
            float temp = temperatures[i];
            jointTempTexts[i].text = $"Joint {i}: {temp:F1}°C";

            // Update slider if available
            if (i < jointTempSliders.Length)
            {
                jointTempSliders[i].value = temp;
            }

            // Color code based on temperature
            if (temp > 70)
                jointTempTexts[i].color = Color.red;
            else if (temp > 60)
                jointTempTexts[i].color = Color.yellow;
            else
                jointTempTexts[i].color = Color.green;
        }
    }
}
```

### Task 1.2: Implement Basic Movement Controls
Create intuitive controls for basic robot movement.

**Implementation Steps:**
1. Create movement control buttons (forward, backward, turn left, turn right)
2. Add speed control slider
3. Implement command sending functionality
4. Add safety checks before movement

**Sample Script:**
```csharp
using UnityEngine;
using UnityEngine.UI;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Geometry;

public class RobotMovementControls : MonoBehaviour
{
    [Header("Movement Controls")]
    public Button moveForwardButton;
    public Button moveBackwardButton;
    public Button turnLeftButton;
    public Button turnRightButton;
    public Button stopButton;
    public Slider speedSlider;
    public Text speedText;

    [Header("Safety Controls")]
    public Button emergencyStopButton;
    public Toggle collisionAvoidanceToggle;

    [Header("ROS Configuration")]
    public string cmdVelTopic = "/robot/cmd_vel";
    public float maxLinearSpeed = 1.0f;
    public float maxAngularSpeed = 1.5f;

    private ROSConnection ros;
    private float currentSpeed = 0.5f;

    void Start()
    {
        ros = ROSConnection.GetOrCreateInstance();

        SetupButtonEvents();
        SetupSliderEvents();

        // Initialize speed slider
        speedSlider.value = currentSpeed;
        speedText.text = $"Speed: {currentSpeed:F1}";
    }

    void SetupButtonEvents()
    {
        moveForwardButton.onClick.AddListener(() => SendMoveCommand(currentSpeed, 0f));
        moveBackwardButton.onClick.AddListener(() => SendMoveCommand(-currentSpeed, 0f));
        turnLeftButton.onClick.AddListener(() => SendMoveCommand(0f, maxAngularSpeed * currentSpeed));
        turnRightButton.onClick.AddListener(() => SendMoveCommand(0f, -maxAngularSpeed * currentSpeed));
        stopButton.onClick.AddListener(() => SendStopCommand());
        emergencyStopButton.onClick.AddListener(EmergencyStop);
    }

    void SetupSliderEvents()
    {
        speedSlider.onValueChanged.AddListener(OnSpeedChanged);
    }

    void OnSpeedChanged(float value)
    {
        currentSpeed = value;
        speedText.text = $"Speed: {currentSpeed:F1}";
    }

    void SendMoveCommand(float linear, float angular)
    {
        // Check if collision avoidance is active
        if (collisionAvoidanceToggle.isOn)
        {
            // Perform safety check before sending command
            if (IsSafeToMove(linear, angular))
            {
                SendVelocityCommand(linear, angular);
            }
            else
            {
                Debug.LogWarning("Movement blocked by collision avoidance system");
            }
        }
        else
        {
            SendVelocityCommand(linear, angular);
        }
    }

    bool IsSafeToMove(float linear, float angular)
    {
        // In a real implementation, this would check sensor data
        // For this exercise, we'll return true
        return true;
    }

    void SendVelocityCommand(float linear, float angular)
    {
        if (ros == null) return;

        var cmdVel = new TwistMsg();
        cmdVel.linear = new Vector3Msg(linear, 0, 0);
        cmdVel.angular = new Vector3Msg(0, 0, angular);

        ros.Publish(cmdVelTopic, cmdVel);
    }

    void SendStopCommand()
    {
        SendVelocityCommand(0f, 0f);
    }

    void EmergencyStop()
    {
        SendVelocityCommand(0f, 0f);
        Debug.LogWarning("EMERGENCY STOP ACTIVATED");
    }
}
```

## Part 2: Advanced HRI Features

### Task 2.1: Implement Joint Control Interface
Create an interface for precise joint control of the humanoid robot.

**Implementation Steps:**
1. Create sliders for each major joint
2. Add joint position displays
3. Implement joint command sending
4. Add joint limits and safety checks

**Sample Script:**
```csharp
using UnityEngine;
using UnityEngine.UI;
using System.Collections.Generic;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Sensor;

public class JointControlInterface : MonoBehaviour
{
    [Header("Joint Control Elements")]
    public List<JointControlElement> jointControls = new List<JointControlElement>();

    [Header("Joint Commands")]
    public Button sendCommandButton;
    public Button resetToHomeButton;
    public Button getCurrentPositionButton;

    [Header("ROS Configuration")]
    public string jointCommandTopic = "/robot/joint_commands";
    public string jointStateTopic = "/robot/joint_states";

    private ROSConnection ros;
    private List<string> jointNames = new List<string>();
    private List<float> jointPositions = new List<float>();

    void Start()
    {
        ros = ROSConnection.GetOrCreateInstance();

        InitializeJointControls();
        SetupButtonEvents();

        // Subscribe to joint states
        ros.Subscribe<JointStateMsg>(jointStateTopic, OnJointStateReceived);
    }

    void InitializeJointControls()
    {
        // Initialize joint names and positions based on your robot
        jointNames.Add("left_hip_joint");
        jointNames.Add("left_knee_joint");
        jointNames.Add("left_ankle_joint");
        jointNames.Add("right_hip_joint");
        jointNames.Add("right_knee_joint");
        jointNames.Add("right_ankle_joint");
        jointNames.Add("left_shoulder_joint");
        jointNames.Add("left_elbow_joint");
        jointNames.Add("right_shoulder_joint");
        jointNames.Add("right_elbow_joint");

        // Initialize joint positions to zero
        for (int i = 0; i < jointNames.Count; i++)
        {
            jointPositions.Add(0f);
        }

        // Create joint control elements
        for (int i = 0; i < jointNames.Count && i < jointControls.Count; i++)
        {
            JointControlElement element = jointControls[i];
            element.Initialize(jointNames[i], i, OnJointValueChanged);
        }
    }

    void SetupButtonEvents()
    {
        sendCommandButton.onClick.AddListener(SendJointCommands);
        resetToHomeButton.onClick.AddListener(ResetToHome);
        getCurrentPositionButton.onClick.AddListener(GetCurrentJointPositions);
    }

    void OnJointValueChanged(int jointIndex, float value)
    {
        if (jointIndex >= 0 && jointIndex < jointPositions.Count)
        {
            jointPositions[jointIndex] = value;

            // Update the corresponding joint control element
            if (jointIndex < jointControls.Count)
            {
                jointControls[jointIndex].UpdateValueText(value);
            }
        }
    }

    void SendJointCommands()
    {
        if (ros == null) return;

        var jointCommand = new JointStateMsg();
        jointCommand.name = new List<string>(jointNames);
        jointCommand.position = new List<double>();

        for (int i = 0; i < jointPositions.Count; i++)
        {
            jointCommand.position.Add(jointPositions[i]);
        }

        ros.Publish(jointCommandTopic, jointCommand);
        Debug.Log("Joint commands sent to robot");
    }

    void ResetToHome()
    {
        for (int i = 0; i < jointControls.Count; i++)
        {
            if (i < jointPositions.Count)
            {
                jointPositions[i] = 0f; // Reset to zero position
                jointControls[i].ResetToZero();
            }
        }
        SendJointCommands();
    }

    void GetCurrentJointPositions()
    {
        // This would typically trigger a request for current joint states
        // The response would be handled by OnJointStateReceived
        Debug.Log("Requesting current joint positions...");
    }

    void OnJointStateReceived(JointStateMsg jointState)
    {
        // Update joint positions based on received state
        for (int i = 0; i < jointState.name.Count; i++)
        {
            string jointName = jointState.name[i];
            double position = jointState.position[i];

            int index = jointNames.IndexOf(jointName);
            if (index >= 0 && index < jointControls.Count)
            {
                jointPositions[index] = (float)position;
                jointControls[index].UpdateSliderValue((float)position);
            }
        }
    }
}

[System.Serializable]
public class JointControlElement
{
    public Slider jointSlider;
    public Text jointNameText;
    public Text jointValueText;
    public float minValue = -1.57f; // -90 degrees in radians
    public float maxValue = 1.57f;  // 90 degrees in radians

    private int jointIndex;
    private System.Action<int, float> valueChangedCallback;

    public void Initialize(string name, int index, System.Action<int, float> callback)
    {
        jointIndex = index;
        valueChangedCallback = callback;

        if (jointNameText != null)
            jointNameText.text = name;

        if (jointSlider != null)
        {
            jointSlider.minValue = minValue;
            jointSlider.maxValue = maxValue;
            jointSlider.value = 0f; // Default to zero position

            // Add listener for slider value changes
            jointSlider.onValueChanged.AddListener(OnSliderValueChanged);
        }

        UpdateValueText(0f);
    }

    void OnSliderValueChanged(float value)
    {
        if (valueChangedCallback != null)
        {
            valueChangedCallback(jointIndex, value);
        }
        UpdateValueText(value);
    }

    public void UpdateValueText(float value)
    {
        if (jointValueText != null)
        {
            jointValueText.text = $"{value:F3} rad";
        }
    }

    public void UpdateSliderValue(float value)
    {
        if (jointSlider != null)
        {
            jointSlider.value = value;
            UpdateValueText(value);
        }
    }

    public void ResetToZero()
    {
        if (jointSlider != null)
        {
            jointSlider.value = 0f;
            UpdateValueText(0f);
        }
    }
}
```

### Task 2.2: Create Safety System Interface
Implement a comprehensive safety system with multiple layers of protection.

**Implementation Steps:**
1. Create emergency stop button with confirmation
2. Add safety distance configuration
3. Implement collision avoidance controls
4. Create safety log display

**Sample Script:**
```csharp
using UnityEngine;
using UnityEngine.UI;
using System.Collections.Generic;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Std;

public class SafetySystemInterface : MonoBehaviour
{
    [Header("Safety Controls")]
    public Button emergencyStopButton;
    public Button safetyResetButton;
    public Text safetyStatusText;
    public Image safetyIndicator;

    [Header("Safety Configuration")]
    public Slider safetyDistanceSlider;
    public Text safetyDistanceText;
    public Toggle collisionAvoidanceToggle;
    public Toggle speedLimitToggle;
    public Slider speedLimitSlider;
    public Text speedLimitText;

    [Header("Safety Log")]
    public Text safetyLogText;
    public Scrollbar safetyLogScrollbar;

    [Header("ROS Configuration")]
    public string safetyCommandTopic = "/robot/safety_command";
    public string safetyStatusTopic = "/robot/safety_status";

    private ROSConnection ros;
    private List<string> safetyLogEntries = new List<string>();
    private string currentSafetyStatus = "SAFE";

    void Start()
    {
        ros = ROSConnection.GetOrCreateInstance();

        SetupSafetyControls();
        SubscribeToSafetyStatus();
        InitializeSafetySystem();
    }

    void SetupSafetyControls()
    {
        emergencyStopButton.onClick.AddListener(EmergencyStop);
        safetyResetButton.onClick.AddListener(ResetSafetySystem);

        safetyDistanceSlider.onValueChanged.AddListener(OnSafetyDistanceChanged);
        collisionAvoidanceToggle.onValueChanged.AddListener(OnCollisionAvoidanceToggled);
        speedLimitToggle.onValueChanged.AddListener(OnSpeedLimitToggled);
        speedLimitSlider.onValueChanged.AddListener(OnSpeedLimitChanged);

        // Initialize values
        safetyDistanceSlider.value = 0.5f; // 0.5m default
        speedLimitSlider.value = 1.0f; // 100% default
        OnSafetyDistanceChanged(safetyDistanceSlider.value);
        OnSpeedLimitChanged(speedLimitSlider.value);
    }

    void SubscribeToSafetyStatus()
    {
        ros.Subscribe<StringMsg>(safetyStatusTopic, OnSafetyStatusReceived);
    }

    void InitializeSafetySystem()
    {
        UpdateSafetyStatus("SAFE");
        AddToSafetyLog("Safety system initialized");
    }

    void EmergencyStop()
    {
        if (ros != null)
        {
            var cmd = new StringMsg();
            cmd.data = "EMERGENCY_STOP";
            ros.Publish(safetyCommandTopic, cmd);
        }

        UpdateSafetyStatus("EMERGENCY_STOP");
        AddToSafetyLog("EMERGENCY STOP activated by operator");
    }

    void ResetSafetySystem()
    {
        if (ros != null)
        {
            var cmd = new StringMsg();
            cmd.data = "RESET_SAFETY";
            ros.Publish(safetyCommandTopic, cmd);
        }

        AddToSafetyLog("Safety system reset by operator");
    }

    void OnSafetyDistanceChanged(float distance)
    {
        safetyDistanceText.text = $"Safety Distance: {distance:F2}m";

        if (ros != null)
        {
            var cmd = new StringMsg();
            cmd.data = $"SET_SAFETY_DISTANCE:{distance}";
            ros.Publish(safetyCommandTopic, cmd);
        }
    }

    void OnCollisionAvoidanceToggled(bool enabled)
    {
        if (ros != null)
        {
            var cmd = new StringMsg();
            cmd.data = $"COLLISION_AVOIDANCE:{(enabled ? "ENABLE" : "DISABLE")}";
            ros.Publish(safetyCommandTopic, cmd);
        }

        AddToSafetyLog($"Collision avoidance {(enabled ? "enabled" : "disabled")}");
    }

    void OnSpeedLimitToggled(bool enabled)
    {
        speedLimitSlider.interactable = enabled;

        if (ros != null)
        {
            var cmd = new StringMsg();
            cmd.data = $"SPEED_LIMIT:{(enabled ? "ENABLE" : "DISABLE")}";
            ros.Publish(safetyCommandTopic, cmd);
        }

        AddToSafetyLog($"Speed limit {(enabled ? "enabled" : "disabled")}");
    }

    void OnSpeedLimitChanged(float limit)
    {
        speedLimitText.text = $"Max Speed: {limit * 100:F0}%";

        if (ros != null)
        {
            var cmd = new StringMsg();
            cmd.data = $"SET_SPEED_LIMIT:{limit}";
            ros.Publish(safetyCommandTopic, cmd);
        }
    }

    void OnSafetyStatusReceived(StringMsg statusMsg)
    {
        UpdateSafetyStatus(statusMsg.data);
    }

    void UpdateSafetyStatus(string status)
    {
        currentSafetyStatus = status;
        safetyStatusText.text = $"Safety Status: {status}";

        // Update indicator color
        switch (status.ToUpper())
        {
            case "SAFE":
                safetyIndicator.color = Color.green;
                break;
            case "WARNING":
                safetyIndicator.color = Color.yellow;
                break;
            case "DANGER":
            case "EMERGENCY_STOP":
                safetyIndicator.color = Color.red;
                break;
            default:
                safetyIndicator.color = Color.gray;
                break;
        }
    }

    public void AddToSafetyLog(string message)
    {
        string timestamp = System.DateTime.Now.ToString("HH:mm:ss");
        string logEntry = $"[{timestamp}] {message}";

        safetyLogEntries.Add(logEntry);

        // Keep only recent entries to prevent memory issues
        if (safetyLogEntries.Count > 100)
        {
            safetyLogEntries.RemoveAt(0);
        }

        // Update the UI
        safetyLogText.text = string.Join("\n", safetyLogEntries.ToArray());

        // Auto-scroll to bottom
        if (safetyLogScrollbar != null)
        {
            safetyLogScrollbar.value = 0f;
        }
    }
}
```

## Part 3: Multi-User Collaboration Interface

### Task 3.1: Implement User Management System
Create a system that allows multiple users to collaborate on robot control.

**Implementation Steps:**
1. Create user selection dropdown
2. Implement role-based access controls
3. Add control request/release mechanisms
4. Create user activity tracking

**Sample Script:**
```csharp
using UnityEngine;
using UnityEngine.UI;
using System.Collections.Generic;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Std;

public class MultiUserControlInterface : MonoBehaviour
{
    [Header("User Management")]
    public Dropdown userSelectionDropdown;
    public Text currentUserText;
    public Text userRoleText;

    [Header("Control Management")]
    public Button requestControlButton;
    public Button releaseControlButton;
    public Button transferControlButton;
    public Text controlStatusText;

    [Header("Permission Controls")]
    public Toggle navigationPermissionToggle;
    public Toggle manipulationPermissionToggle;
    public Toggle systemPermissionToggle;

    [Header("User List")]
    public Text activeUsersText;

    [Header("ROS Configuration")]
    public string userControlTopic = "/robot/user_control";
    public string userStatusTopic = "/robot/user_status";

    private ROSConnection ros;
    private List<string> availableUsers = new List<string> { "Operator1", "Operator2", "Supervisor", "Trainee" };
    private string currentUser = "";
    private string userRole = "Observer";
    private bool hasControl = false;

    void Start()
    {
        ros = ROSConnection.GetOrCreateInstance();

        InitializeUserInterface();
        SetupControlEvents();
        SubscribeToUserStatus();
    }

    void InitializeUserInterface()
    {
        // Populate user dropdown
        userSelectionDropdown.ClearOptions();
        userSelectionDropdown.AddOptions(availableUsers);

        // Set default user
        currentUser = availableUsers[0];
        currentUserText.text = $"Current User: {currentUser}";
        UpdateUserRole();
    }

    void SetupControlEvents()
    {
        userSelectionDropdown.onValueChanged.AddListener(OnUserChanged);
        requestControlButton.onClick.AddListener(RequestControl);
        releaseControlButton.onClick.AddListener(ReleaseControl);
        transferControlButton.onClick.AddListener(TransferControl);

        // Set up permission toggles (only available to supervisors)
        navigationPermissionToggle.onValueChanged.AddListener(OnPermissionChanged);
        manipulationPermissionToggle.onValueChanged.AddListener(OnPermissionChanged);
        systemPermissionToggle.onValueChanged.AddListener(OnPermissionChanged);
    }

    void SubscribeToUserStatus()
    {
        ros.Subscribe<StringMsg>(userStatusTopic, OnUserStatusReceived);
    }

    void OnUserChanged(int index)
    {
        if (index >= 0 && index < availableUsers.Count)
        {
            currentUser = availableUsers[index];
            currentUserText.text = $"Current User: {currentUser}";
            UpdateUserRole();
            UpdatePermissionControls();
        }
    }

    void UpdateUserRole()
    {
        // Determine role based on username (in a real system, this would come from authentication)
        if (currentUser.Contains("Supervisor"))
            userRole = "Supervisor";
        else if (currentUser.Contains("Trainee"))
            userRole = "Trainee";
        else
            userRole = "Operator";

        userRoleText.text = $"Role: {userRole}";
    }

    void UpdatePermissionControls()
    {
        // Only supervisors can change permissions
        bool isSupervisor = userRole == "Supervisor";
        navigationPermissionToggle.interactable = isSupervisor;
        manipulationPermissionToggle.interactable = isSupervisor;
        systemPermissionToggle.interactable = isSupervisor;
    }

    void RequestControl()
    {
        if (ros != null)
        {
            var cmd = new StringMsg();
            cmd.data = $"REQUEST_CONTROL:{currentUser}";
            ros.Publish(userControlTopic, cmd);
        }

        AddToControlLog($"User {currentUser} requested control");
    }

    void ReleaseControl()
    {
        if (ros != null)
        {
            var cmd = new StringMsg();
            cmd.data = $"RELEASE_CONTROL:{currentUser}";
            ros.Publish(userControlTopic, cmd);
        }

        hasControl = false;
        controlStatusText.text = "Control Status: Released";
        AddToControlLog($"User {currentUser} released control");
    }

    void TransferControl()
    {
        if (!hasControl)
        {
            Debug.LogWarning("Cannot transfer control - you don't have control");
            return;
        }

        string targetUser = availableUsers[userSelectionDropdown.value];
        if (targetUser == currentUser)
        {
            Debug.LogWarning("Cannot transfer control to yourself");
            return;
        }

        if (ros != null)
        {
            var cmd = new StringMsg();
            cmd.data = $"TRANSFER_CONTROL:{currentUser}:{targetUser}";
            ros.Publish(userControlTopic, cmd);
        }

        AddToControlLog($"Control transferred from {currentUser} to {targetUser}");
    }

    void OnUserStatusReceived(StringMsg statusMsg)
    {
        // Parse status message: "USER_STATUS:username:control_status:role"
        string[] parts = statusMsg.data.Split(':');
        if (parts.Length >= 4)
        {
            string user = parts[1];
            string controlStatus = parts[2];
            string role = parts[3];

            if (user == currentUser)
            {
                hasControl = controlStatus == "HAS_CONTROL";
                controlStatusText.text = $"Control Status: {(hasControl ? "Active" : "Released")}";
                userRoleText.text = $"Role: {role}";
            }

            UpdateActiveUsersDisplay();
        }
    }

    void UpdateActiveUsersDisplay()
    {
        // In a real implementation, this would update based on received user status messages
        activeUsersText.text = "Active Users:\n" + string.Join("\n", availableUsers.ToArray());
    }

    void OnPermissionChanged(bool value)
    {
        // Handle permission changes
        AddToControlLog($"Permissions updated by {currentUser}");
    }

    void AddToControlLog(string message)
    {
        Debug.Log(message); // In a real UI, this would update a log display
    }
}
```

## Part 4: Testing and Validation

### Task 4.1: HRI Interface Testing
Test your implemented HRI interface with various scenarios.

**Testing Scenarios:**
1. **Basic Functionality Test**
   - Verify all buttons respond correctly
   - Test slider functionality
   - Check text displays update properly

2. **Safety System Test**
   - Test emergency stop functionality
   - Verify safety distance settings work
   - Check collision avoidance toggle

3. **Multi-User Test**
   - Test user switching
   - Verify control request/release
   - Check permission system

### Task 4.2: Performance Testing
Test the performance of your HRI interface.

**Performance Metrics:**
- UI response time (should be < 100ms)
- Memory usage
- Frame rate maintenance (> 30 FPS)

## Part 5: Enhancement Challenges

### Challenge 1: Voice Command Integration
Implement voice command recognition for basic robot control.

### Challenge 2: Gesture Recognition
Add gesture-based control using Unity's input system or external libraries.

### Challenge 3: VR Interface
Create a VR-compatible version of your HRI interface.

## Assessment Criteria

Your HRI implementation will be evaluated on:
- **Functionality**: All controls work as expected
- **Safety**: Proper safety systems implemented
- **Usability**: Interface is intuitive and user-friendly
- **Robustness**: Handles errors gracefully
- **Documentation**: Code is well-commented and documented

## Conclusion

This exercise provided hands-on experience implementing comprehensive Human-Robot Interaction interfaces in Unity. You've created a functional HRI system with safety features, multi-user capabilities, and intuitive controls that can be used with digital twin systems for humanoid robots.

The skills developed in this exercise are directly applicable to real-world robotics applications where safe and intuitive human-robot interaction is critical for successful operation.