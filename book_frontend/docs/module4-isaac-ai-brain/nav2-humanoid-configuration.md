---
title: Nav2 Configuration for Humanoid Robots
sidebar_label: Nav2 Humanoid Configuration
sidebar_position: 26
description: Comprehensive guide to configuring Nav2 specifically for bipedal humanoid robots
tags: [nav2, configuration, humanoid, navigation, path-planning, setup]
---

# Nav2 Configuration for Humanoid Robots

## Overview
This chapter provides a comprehensive guide to configuring Navigation2 (Nav2) specifically for bipedal humanoid robots. Unlike traditional wheeled robots, humanoid robots have unique kinematic constraints, balance requirements, and locomotion patterns that require specialized Nav2 configuration.

## Understanding Humanoid Navigation Requirements

### Key Differences from Wheeled Navigation
1. **Balance Constraints**: Must maintain dynamic balance during movement
2. **Step-based Locomotion**: Movement occurs in discrete steps, not continuous motion
3. **Stability Requirements**: Center of mass must remain within support polygon
4. **Terrain Limitations**: Limited ability to traverse rough terrain
5. **Energy Efficiency**: Bipedal locomotion requires careful energy management

### Critical Configuration Areas
- Costmap parameters adapted for bipedal locomotion
- Path planning algorithms considering step constraints
- Controller configurations for stable walking
- Recovery behaviors specific to humanoid robots

## Complete Nav2 Configuration for Humanoid Robots

### 1. Main Parameters File (nav2_params.yaml)

```yaml
amcl:
  ros__parameters:
    use_sim_time: True
    alpha1: 0.2
    alpha2: 0.2
    alpha3: 0.2
    alpha4: 0.2
    alpha5: 0.2
    base_frame_id: "base_footprint"
    beam_skip_distance: 0.5
    beam_skip_error_threshold: 0.9
    beam_skip_threshold: 0.3
    do_beamskip: False
    global_frame_id: "map"
    lambda_short: 0.1
    laser_likelihood_max_dist: 2.0
    laser_max_range: 100.0
    laser_min_range: -1.0
    max_beams: 60
    max_particles: 2000
    min_particles: 500
    odom_frame_id: "odom"
    pf_err: 0.05
    pf_z: 0.99
    recovery_alpha_fast: 0.0
    recovery_alpha_slow: 0.0
    resample_interval: 1
    robot_model_type: "nav2_amcl::DifferentialMotionModel"
    save_pose_rate: 0.5
    sigma_hit: 0.2
    tf_broadcast: True
    transform_tolerance: 1.0
    update_min_a: 0.2
    update_min_d: 0.25
    z_hit: 0.5
    z_max: 0.05
    z_rand: 0.5
    z_short: 0.05

bt_navigator:
  ros__parameters:
    use_sim_time: True
    global_frame: map
    robot_base_frame: base_footprint
    odom_topic: /odom
    default_bt_xml_filename: "humanoid_navigator.xml"
    plugin_lib_names:
    - nav2_compute_path_to_pose_action_bt_node
    - nav2_follow_path_action_bt_node
    - nav2_back_up_action_bt_node
    - nav2_spin_action_bt_node
    - nav2_wait_action_bt_node
    - nav2_clear_costmap_service_bt_node
    - nav2_is_stuck_condition_bt_node
    - nav2_goal_reached_condition_bt_node
    - nav2_goal_updated_condition_bt_node
    - nav2_initial_pose_received_condition_bt_node
    - nav2_reinitialize_global_localization_service_bt_node
    - nav2_rate_controller_bt_node
    - nav2_distance_controller_bt_node
    - nav2_speed_controller_bt_node
    - nav2_truncate_path_action_bt_node
    - nav2_goal_updater_node_bt_node
    - nav2_recovery_node_bt_node
    - nav2_pipeline_sequence_bt_node
    - nav2_round_robin_node_bt_node
    - nav2_transform_available_condition_bt_node
    - nav2_time_expired_condition_bt_node
    - nav2_path_expiring_timer_condition
    - nav2_distance_traveled_condition_bt_node
    - nav2_single_trigger_bt_node
    - nav2_is_battery_low_condition_bt_node
    - nav2_navigate_through_poses_action_bt_node
    - nav2_navigate_to_pose_action_bt_node
    - nav2_remove_passed_goals_action_bt_node
    - nav2_planner_selector_bt_node
    - nav2_controller_selector_bt_node
    - nav2_goal_checker_selector_bt_node
    - nav2_controller_cancel_bt_node
    - nav2_path_longer_on_approach_bt_node
    - nav2_wait_on_matrix_size_bt_node
    - nav2_compute_path_through_poses_action_bt_node

controller_server:
  ros__parameters:
    use_sim_time: True
    controller_frequency: 10.0
    min_x_velocity_threshold: 0.05
    min_y_velocity_threshold: 0.05
    min_theta_velocity_threshold: 0.05
    progress_checker_plugin: "progress_checker"
    goal_checker_plugin: "goal_checker"
    controller_plugins: ["FollowPath"]

    # Humanoid-specific controller
    FollowPath:
      plugin: "nav2_mppi_controller::MPPIController"
      time_steps: 25
      model_dt: 0.05
      batch_size: 1000
      vx_std: 0.2
      vy_std: 0.05
      wz_std: 0.3
      vx_max: 0.5
      vx_min: -0.1
      vy_max: 0.1
      vy_min: -0.1
      wz_max: 0.3
      wz_min: -0.3
      iteration_count: 3
      motion_model: "DiffDrive"
      xy_goal_tolerance: 0.5  # Larger tolerance for bipedal stability
      yaw_goal_tolerance: 0.2
      stateful: True
      transform_tolerance: 0.3
      goal_reached_tol: 0.25
      path_tolerance: 0.1
      reference_speed: 0.2
      # Humanoid-specific parameters
      balance_weight: 10.0
      step_constraint_weight: 5.0

local_costmap:
  ros__parameters:
    use_sim_time: True
    global_frame: odom
    robot_base_frame: base_footprint
    update_frequency: 10.0
    publish_frequency: 5.0
    static_map: False
    rolling_window: True
    width: 10
    height: 10
    resolution: 0.025  # Higher resolution for precise planning
    robot_type: "bipedal"
    robot_radius: 0.4  # Effective radius considering stance width
    plugins: ["static_layer", "obstacle_layer", "inflation_layer", "humanoid_constraint_layer"]

    static_layer:
      plugin: "nav2_costmap_2d::StaticLayer"
      map_subscribe_transient_local: True

    obstacle_layer:
      plugin: "nav2_costmap_2d::ObstacleLayer"
      enabled: True
      observation_sources: scan
      scan:
        topic: /scan
        max_obstacle_height: 2.0
        clearing: True
        marking: True
        data_type: "LaserScan"
        raytrace_max_range: 10.0
        raytrace_min_range: 0.0
        obstacle_max_range: 8.0
        obstacle_min_range: 0.0

    inflation_layer:
      plugin: "nav2_costmap_2d::InflationLayer"
      enabled: True
      cost_scaling_factor: 5.0
      inflation_radius: 1.0
      # Humanoid-specific inflation for stability
      step_height_threshold: 0.2

    humanoid_constraint_layer:
      plugin: "humanoid_navigation::HumanoidConstraintLayer"
      enabled: True
      # Balance and step constraints
      max_com_deviation: 0.15
      max_step_height: 0.2
      safety_margin: 0.1

global_costmap:
  ros__parameters:
    use_sim_time: True
    global_frame: map
    robot_base_frame: base_footprint
    update_frequency: 1.0
    static_map: True
    rolling_window: False
    track_unknown_space: True
    plugins: ["static_layer", "obstacle_layer", "inflation_layer", "step_constraint_layer"]

    static_layer:
      plugin: "nav2_costmap_2d::StaticLayer"
      map_subscribe_transient_local: True

    obstacle_layer:
      plugin: "nav2_costmap_2d::ObstacleLayer"
      enabled: True
      observation_sources: scan
      scan:
        topic: /scan
        max_obstacle_height: 2.0
        clearing: True
        marking: True
        data_type: "LaserScan"
        raytrace_max_range: 10.0
        raytrace_min_range: 0.0
        obstacle_max_range: 8.0
        obstacle_min_range: 0.0

    inflation_layer:
      plugin: "nav2_costmap_2d::InflationLayer"
      enabled: True
      cost_scaling_factor: 3.0
      inflation_radius: 2.0

    step_constraint_layer:
      plugin: "humanoid_navigation::StepConstraintLayer"
      enabled: True
      # Step-based navigation constraints
      max_step_height: 0.2
      max_step_length: 0.6
      min_step_length: 0.1

planner_server:
  ros__parameters:
    use_sim_time: True
    planner_plugins: ["GridBased"]
    GridBased:
      plugin: "nav2_navfn_planner::NavfnPlanner"
      tolerance: 0.5
      use_astar: false
      allow_unknown: true
      # Humanoid-specific planning parameters
      step_constraint_enabled: true
      max_step_height: 0.2
      max_step_length: 0.6

smoother_server:
  ros__parameters:
    use_sim_time: True
    smoother_plugins: ["simple_smoother"]
    simple_smoother:
      plugin: "nav2_smoother::SimpleSmoother"
      tolerance: 0.1
      max_its: 1000
      do_refinement: True
      # Humanoid-specific smoothing
      max_deviation: 0.2
      smoothness_weight: 0.8
      stability_weight: 1.0

behavior_server:
  ros__parameters:
    use_sim_time: True
    local_costmap_topic: local_costmap/costmap_raw
    global_costmap_topic: global_costmap/costmap_raw
    local_footprint_topic: local_costmap/published_footprint
    global_footprint_topic: global_costmap/published_footprint
    cycle_frequency: 10.0
    behavior_plugins: ["spin", "backup", "wait", "humanoid_balance"]
    spin:
      plugin: "nav2_behaviors::Spin"
      # Bipedal-specific spin parameters
      max_rotation_speed: 0.5
      min_duration: 2.0
      time_allowance: 10.0
    backup:
      plugin: "nav2_behaviors::BackUp"
      # Bipedal-specific backup parameters
      duration: 5.0
      sim_frequency: 50
      max_translation_speed: 0.05  # Slower for stability
      min_translation_speed: 0.01
      translation_threshold: 0.2
    wait:
      plugin: "nav2_behaviors::Wait"
      # Bipedal-specific wait parameters
      duration: 5.0
    humanoid_balance:
      plugin: "humanoid_behaviors::BalanceRecovery"
      max_recovery_attempts: 3
      recovery_delay: 2.0

velocity_smoother:
  ros__parameters:
    use_sim_time: True
    smoothing_frequency: 20.0
    scale_velocities: False
    feedback: "OPEN_LOOP"
    velocity_timeout: 1.0
    filter_duration: 0.2
    max_accel: 2.5
    max_decel: 2.5
    # Humanoid-specific velocity constraints
    max_humanoid_velocity: 0.3

waypoint_follower:
  ros__parameters:
    loop_rate: 20
    stop_on_failure: false
    waypoint_task_executor_plugin: "wait_at_waypoint"
    wait_at_waypoint:
      plugin: "nav2_waypoint_follower::WaitAtWaypoint"
      enabled: true
      waypoint_pause_duration: 200
```

### 2. Behavior Tree Configuration (humanoid_navigator.xml)

```xml
<root main_tree_to_execute="MainTree">
  <BehaviorTree ID="MainTree">
    <PipelineSequence name="NavigateWithReplanning">
      <RateController hz="1.0">
        <RecoveryNode number_of_retries="6" name="ComputeAndFollowPath">
          <PipelineSequence name="ComputeAndFollowPathWithRecovery">
            <RecoveryNode number_of_retries="2" name="ComputePathToPose">
              <ComputePathToPose goal="{goal}" path="{path}" planner_id="GridBased"/>
              <RecoveryAction name="ClearEntirelyCostmap" action_name="nav2/clear_costmap_service" service_name="clear_entirely_local_costmap">
                <ActionParameters wait_duration="2s"/>
              </RecoveryAction>
            </RecoveryNode>
            <RecoveryNode number_of_retries="2" name="FollowPath">
              <FollowPath path="{path}" controller_id="FollowPath"/>
              <RecoveryAction name="ClearEntirelyLocalCostmap" action_name="nav2/clear_costmap_service" service_name="clear_entirely_local_costmap">
                <ActionParameters wait_duration="2s"/>
              </RecoveryAction>
            </RecoveryNode>
          </PipelineSequence>
          <RecoveryAction name="Spin" action_name="nav2/spin" spin_dist="1.57"/>
        </RecoveryNode>
      </RateController>
      <ReactiveSequence name="OnGoalReached">
        <GoalReached goal="{goal}" path="{path}"/>
        <ClearEntirely global_costmap_service_name="clear_entirely_global_costmap" local_costmap_service_name="clear_entirely_local_costmap"/>
        <RoundRobin name="OnGoalReachedActions">
          <ActionNode name="HumanoidBalanceRecovery" action_name="humanoid_balance_recovery"/>
          <ActionNode name="Wait" action_name="nav2/wait" wait_duration="5s"/>
        </RoundRobin>
      </ReactiveSequence>
    </PipelineSequence>
  </BehaviorTree>
</root>
```

## Humanoid-Specific Plugins

### 1. Humanoid Constraint Layer
A custom costmap layer to enforce balance and step constraints:

```cpp
// Example plugin structure
class HumanoidConstraintLayer : public nav2_costmap_2d::Layer {
public:
  void onInitialize() override;
  void updateBounds(
    double robot_x, double robot_y, double robot_yaw,
    double* min_x, double* min_y, double* max_x, double* max_y) override;
  void updateCosts(
    nav2_costmap_2d::Costmap2D& master_grid,
    int min_i, int min_j, int max_i, int max_j) override;

private:
  double max_com_deviation_;
  double max_step_height_;
  double safety_margin_;
  bool step_constraint_enabled_;
};
```

### 2. Step Constraint Layer
Enforces step-based navigation constraints:

```cpp
class StepConstraintLayer : public nav2_costmap_2d::Layer {
public:
  void onInitialize() override;
  void updateBounds(
    double robot_x, double robot_y, double robot_yaw,
    double* min_x, double* min_y, double* max_x, double* max_y) override;
  void updateCosts(
    nav2_costmap_2d::Costmap2D& master_grid,
    int min_i, int min_j, int max_i, int max_j) override;

private:
  double max_step_height_;
  double max_step_length_;
  double min_step_length_;
};
```

## Launch File Configuration

### humanoid_navigation.launch.py

```python
import launch
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    package_dir = get_package_share_directory('humanoid_navigation')
    use_sim_time = LaunchConfiguration('use_sim_time')

    nav2_params = os.path.join(package_dir, 'config', 'nav2_params.yaml')

    return launch.LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation clock if true'),

        Node(
            package='nav2_controller',
            executable='controller_server',
            output='screen',
            parameters=[nav2_params, {'use_sim_time': use_sim_time}]),

        Node(
            package='nav2_planner',
            executable='planner_server',
            output='screen',
            parameters=[nav2_params, {'use_sim_time': use_sim_time}]),

        Node(
            package='nav2_smoother',
            executable='smoother_server',
            output='screen',
            parameters=[nav2_params, {'use_sim_time': use_sim_time}]),

        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_navigation',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time},
                       {'autostart': True},
                       {'node_names': ['controller_server',
                                      'planner_server',
                                      'smoother_server',
                                      'local_costmap',
                                      'global_costmap',
                                      'bt_navigator',
                                      'velocity_smoother']}]),
    ])
```

## Isaac ROS Integration

### Integration with Isaac Perception

```yaml
# Isaac ROS integration parameters
isaac_perception_integrator:
  ros__parameters:
    use_sim_time: True
    # Perception topics from Isaac ROS
    depth_image_topic: "/depth/image_rect_raw"
    camera_info_topic: "/depth/camera_info"
    # Integration with Nav2
    use_depth_for_navigation: True
    depth_range_min: 0.1
    depth_range_max: 10.0
    # Humanoid-specific perception filtering
    ground_plane_filter: True
    obstacle_height_filter: True
    step_detection_enabled: True
    max_step_detection_height: 0.3
```

## Performance Optimization

### 1. Computational Efficiency
- Use appropriate costmap resolutions (0.025m for local, 0.1m for global)
- Limit planning horizon based on humanoid capabilities
- Optimize controller update frequencies

### 2. Memory Management
- Configure appropriate buffer sizes for path planning
- Limit the number of particles in localization
- Use efficient data structures for constraint checking

### 3. Real-time Performance
- Prioritize critical navigation tasks
- Use multi-threaded processing where possible
- Monitor and optimize CPU/GPU usage

## Testing and Validation

### 1. Simulation Testing
Test configurations in Isaac Sim before deployment:

```bash
# Launch navigation stack in simulation
ros2 launch humanoid_navigation humanoid_navigation.launch.py use_sim_time:=true
```

### 2. Performance Metrics
Monitor key performance indicators:
- Localization accuracy
- Path following precision
- Balance maintenance
- Computational efficiency
- Battery consumption

### 3. Safety Validation
- Verify emergency stop functionality
- Test recovery behaviors
- Validate constraint enforcement
- Assess failure modes

## Troubleshooting Common Issues

### 1. Navigation Instability
- Increase costmap inflation for stability
- Adjust controller parameters for smoother motion
- Verify IMU integration for balance feedback

### 2. Path Planning Failures
- Check step constraint parameters
- Verify terrain traversability settings
- Adjust planning algorithm parameters

### 3. Computational Overhead
- Reduce costmap resolution if possible
- Limit planning frequency
- Optimize custom plugin implementations

## Best Practices

1. **Start Conservative**: Begin with restrictive parameters and gradually relax
2. **Simulation First**: Validate all configurations in simulation
3. **Incremental Testing**: Test components individually before integration
4. **Monitor Performance**: Continuously track navigation metrics
5. **Safety First**: Always implement robust safety mechanisms
6. **Documentation**: Maintain clear configuration documentation

## Resources
- [Navigation2 Official Documentation](https://navigation.ros.org/)
- [ROS 2 Navigation Tutorials](https://navigation.ros.org/tutorials/)
- [Humanoid Robot Navigation Research](https://humanoid-navigation.example.com/)
- [NVIDIA Isaac ROS Integration Guide](https://nvidia-isaac-ros.github.io/)