---
title: Physics Parameters and Configurations
sidebar_label: Physics Parameters
sidebar_position: 7
description: Detailed guide to configuring physics parameters for optimal humanoid robot simulation in Gazebo
tags: [gazebo, physics, parameters, simulation, robotics, humanoid, configuration]
---

# Physics Parameters and Configurations

## Introduction

Physics parameters are crucial for achieving realistic and stable simulation of humanoid robots in Gazebo. Proper configuration of these parameters ensures that simulated robots behave similarly to their real-world counterparts, enabling effective testing and validation of control algorithms, planning strategies, and interaction scenarios.

This chapter provides a comprehensive guide to understanding and configuring physics parameters for optimal humanoid robot simulation, covering both basic and advanced configuration options.

## Understanding the Physics Engine

### Physics Engine Fundamentals

Gazebo's physics engine performs several critical functions:

1. **Integration**: Numerically integrates equations of motion over time
2. **Collision Detection**: Identifies when objects come into contact
3. **Contact Resolution**: Computes forces and responses when contacts occur
4. **Constraint Solving**: Maintains joint relationships and other constraints

The accuracy and stability of these computations depend heavily on the chosen parameters.

### Time Integration

The physics engine updates the simulation state at discrete time intervals:

- **Time Step**: Duration between simulation updates
- **Integration Method**: Algorithm used to compute state changes
- **Real-time Factor**: Target simulation speed relative to real time

## Core Physics Parameters

### Time Step Configuration

The time step is one of the most critical parameters affecting simulation quality:

```xml
<physics type="ode">
  <max_step_size>0.001</max_step_size>
  <real_time_update_rate>1000</real_time_update_rate>
  <real_time_factor>1.0</real_time_factor>
</physics>
```

**Parameters:**
- `max_step_size`: Simulation time step in seconds
- `real_time_update_rate`: Updates per second (1/max_step_size)
- `real_time_factor`: Target simulation speed (1.0 = real-time)

**Guidelines for humanoid robots:**
- Start with 0.001s (1ms) for stable simulation
- For complex models, consider 0.0005s (0.5ms)
- For performance-critical applications, 0.002s may be acceptable
- Always validate that real-time factor remains close to target

### Solver Configuration

The constraint solver handles joint constraints and contact forces:

```xml
<physics type="ode">
  <ode>
    <solver>
      <type>quick</type>
      <iters>100</iters>
      <sor>1.3</sor>
    </solver>
  </ode>
</physics>
```

**Key solver parameters:**
- `iters`: Number of solver iterations per time step
- `sor`: Successive Over-Relaxation parameter (typically 1.2-1.3)
- `type`: Solver algorithm (quick, PGS, Dantzig)

**Humanoid-specific recommendations:**
- Start with 100 iterations for stable humanoid simulation
- Increase to 200-500 for complex contact scenarios
- Monitor performance impact when increasing iterations

### Constraint Parameters

Fine-tune constraint handling for improved stability:

```xml
<physics type="ode">
  <ode>
    <constraints>
      <cfm>0.0</cfm>
      <erp>0.2</erp>
      <contact_max_correcting_vel>100.0</contact_max_correcting_vel>
      <contact_surface_layer>0.001</contact_surface_layer>
    </constraints>
  </ode>
</physics>
```

**Parameters:**
- `cfm`: Constraint Force Mixing (stability vs. accuracy)
- `erp`: Error Reduction Parameter (0.0-1.0, how quickly errors are corrected)
- `contact_max_correcting_vel`: Maximum velocity for contact correction
- `contact_surface_layer`: Penetration depth before contact force activates

## Advanced Physics Configuration

### ODE-Specific Parameters

For the Open Dynamics Engine (ODE):

```xml
<physics type="ode">
  <ode>
    <solver>
      <type>quick</type>
      <iters>100</iters>
      <sor>1.3</sor>
      <use_dynamic_moi_rescaling>0</use_dynamic_moi_rescaling>
    </solver>
    <constraints>
      <contact_surface_layer>0.001</contact_surface_layer>
      <contact_max_correcting_vel>100</contact_max_correcting_vel>
      <cfm>0.0</cfm>
      <erp>0.2</erp>
    </constraints>
  </ode>
</physics>
```

### Performance vs. Accuracy Trade-offs

**High Accuracy Configuration:**
```xml
<physics type="ode">
  <max_step_size>0.0005</max_step_size>
  <ode>
    <solver>
      <iters>500</iters>
      <sor>1.2</sor>
    </solver>
    <constraints>
      <erp>0.1</erp>
      <cfm>0.00001</cfm>
    </constraints>
  </ode>
</physics>
```

**High Performance Configuration:**
```xml
<physics type="ode">
  <max_step_size>0.002</max_step_size>
  <ode>
    <solver>
      <iters>50</iters>
      <sor>1.4</sor>
    </solver>
    <constraints>
      <erp>0.3</erp>
      <cfm>0.001</cfm>
    </constraints>
  </ode>
</physics>
```

## Humanoid-Specific Physics Tuning

### Balancing and Stability Parameters

For humanoid robots that need to maintain balance:

```xml
<physics type="ode">
  <max_step_size>0.001</max_step_size>
  <ode>
    <solver>
      <iters>200</iters>
      <sor>1.25</sor>
    </solver>
    <constraints>
      <erp>0.15</erp>
      <cfm>0.0001</cfm>
      <contact_max_correcting_vel>10.0</contact_max_correcting_vel>
      <contact_surface_layer>0.0005</contact_surface_layer>
    </constraints>
  </ode>
</physics>
```

### Walking and Locomotion Parameters

For humanoid robots performing walking or other locomotion:

```xml
<physics type="ode">
  <max_step_size>0.001</max_step_size>
  <ode>
    <solver>
      <iters>300</iters>
      <sor>1.2</sor>
    </solver>
    <constraints>
      <erp>0.1</erp>
      <cfm>0.00005</cfm>
      <!-- Allow slight penetration to reduce contact instability -->
      <contact_surface_layer>0.002</contact_surface_layer>
      <contact_max_correcting_vel>5.0</contact_max_correcting_vel>
    </constraints>
  </ode>
</physics>
```

## Contact Parameters for Humanoid Robots

### Ground Contact Optimization

Humanoid robots spend significant time in contact with the ground:

```xml
<!-- In world file or ground plane model -->
<model name="ground_plane">
  <link name="link">
    <collision name="collision">
      <surface>
        <friction>
          <ode>
            <mu>1.0</mu>
            <mu2>1.0</mu2>
          </ode>
        </friction>
        <contact>
          <ode>
            <soft_cfm>0.0001</soft_cfm>
            <soft_erp>0.2</soft_erp>
            <kp>1000000000000.0</kp>
            <kd>1.0</kd>
            <max_vel>100.0</max_vel>
            <min_depth>0.001</min_depth>
          </ode>
        </contact>
      </surface>
    </collision>
  </link>
</model>
```

### Foot Contact Configuration

For realistic foot-ground interaction:

```xml
<!-- In robot model -->
<collision name="foot_collision">
  <surface>
    <friction>
      <ode>
        <mu>0.8</mu>
        <mu2>0.8</mu2>
      </ode>
    </friction>
    <contact>
      <ode>
        <soft_cfm>0.00001</soft_cfm>
        <soft_erp>0.1</soft_erp>
        <kp>100000000000.0</kp>
        <kd>10.0</kd>
        <max_vel>10.0</max_vel>
        <min_depth>0.0005</min_depth>
      </ode>
    </contact>
  </surface>
</collision>
```

## Joint-Specific Physics Parameters

### Joint Dynamics Configuration

Configure individual joints for realistic behavior:

```xml
<joint name="knee_joint" type="revolute">
  <axis>
    <xyz>0 1 0</xyz>
    <limit>
      <lower>-2.0</lower>
      <upper>0.5</upper>
      <effort>200</effort>
      <velocity>5</velocity>
    </limit>
    <dynamics>
      <damping>1.0</damping>
      <friction>0.1</friction>
      <spring_reference>0.0</spring_reference>
      <spring_stiffness>0.0</spring_stiffness>
    </dynamics>
  </axis>
</joint>
```

### Humanoid Joint Parameter Guidelines

**Hip Joints (Ball joints):**
- Damping: 2.0-5.0 N⋅m⋅s/rad
- Friction: 0.1-0.5 N⋅m
- Effort limits: 300-500 N⋅m

**Knee Joints (Revolute):**
- Damping: 1.0-3.0 N⋅m⋅s/rad
- Friction: 0.1-0.3 N⋅m
- Effort limits: 200-400 N⋅m

**Ankle Joints:**
- Damping: 0.5-2.0 N⋅m⋅s/rad
- Friction: 0.05-0.2 N⋅m
- Effort limits: 100-200 N⋅m

**Shoulder Joints:**
- Damping: 1.0-2.0 N⋅m⋅s/rad
- Friction: 0.1-0.3 N⋅m
- Effort limits: 150-300 N⋅m

**Elbow Joints:**
- Damping: 0.5-1.5 N⋅m⋅s/rad
- Friction: 0.05-0.2 N⋅m
- Effort limits: 100-200 N⋅m

## Physics Debugging and Optimization

### Performance Monitoring

Monitor these metrics to optimize physics parameters:

```bash
# Check real-time factor and performance
gz topic -e /stats

# Monitor specific joint behaviors
gz topic -e /joint_states
```

### Common Performance Issues

**Low Real-time Factor:**
- Reduce solver iterations
- Increase time step (with caution)
- Simplify collision geometry
- Reduce number of contacts

**Instability:**
- Decrease time step
- Increase solver iterations
- Adjust ERP and CFM values
- Verify mass/inertia properties

### Validation Techniques

**Stability Test:**
1. Load robot in simulation
2. Apply small disturbances
3. Verify return to stable equilibrium
4. Check for oscillations or divergence

**Accuracy Test:**
1. Compare simulation results with known physics
2. Validate conservation of energy (in frictionless cases)
3. Check for non-physical behaviors

## Physics Parameter Tuning Process

### Systematic Tuning Approach

1. **Start with defaults**: Use Gazebo's recommended parameters
2. **Test basic behavior**: Ensure robot is stable under gravity
3. **Adjust time step**: Find balance between stability and performance
4. **Tune solver**: Increase iterations until stable
5. **Fine-tune constraints**: Adjust ERP and CFM for desired response
6. **Validate**: Test with intended use cases

### Parameter Sensitivity Analysis

**High Sensitivity Parameters:**
- `max_step_size`: Small changes significantly affect stability
- `iters`: Directly impacts constraint satisfaction
- `erp`: Affects error correction speed

**Medium Sensitivity Parameters:**
- `cfm`: Affects constraint stiffness
- Joint damping: Affects motion smoothness
- `sor`: Affects solver convergence

**Low Sensitivity Parameters:**
- `contact_max_correcting_vel`: Fine-tunes contact behavior
- `contact_surface_layer`: Minor stability adjustment

## Multi-Physics Engine Considerations

### ODE vs. Bullet vs. Simbody

**ODE (Default):**
- Pros: Well-tested, good balance of performance/stability
- Cons: Less advanced contact handling
- Best for: General humanoid simulation

**Bullet:**
- Pros: Advanced collision detection, better contact handling
- Cons: May require more tuning
- Best for: Complex contact scenarios

**Simbody:**
- Pros: High accuracy for biomechanical applications
- Cons: More computationally expensive
- Best for: Precise dynamic analysis

## Hardware-in-the-Loop Considerations

### Real-time Constraints

When using simulation for HIL testing:

```xml
<physics type="ode">
  <max_step_size>0.001</max_step_size>
  <real_time_factor>1.0</real_time_factor>
  <ode>
    <solver>
      <iters>100</iters>  <!-- Balance between stability and performance -->
    </solver>
  </ode>
</physics>
```

### Synchronization Parameters

Ensure simulation timing aligns with hardware:

- Match simulation update rate to hardware control rate
- Consider communication latency in timing
- Implement appropriate buffering strategies

## Best Practices for Humanoid Physics

### Parameter Selection Guidelines

1. **Start conservative**: Begin with stable parameters and optimize gradually
2. **Match real robot**: Base parameters on physical robot characteristics
3. **Test thoroughly**: Validate with multiple scenarios
4. **Document changes**: Keep track of parameter effects
5. **Iterate systematically**: Change one parameter at a time when possible

### Performance Optimization

1. **Profile first**: Identify bottlenecks before optimizing
2. **Reduce complexity**: Simplify collision geometry where possible
3. **Adjust solver**: Use minimum iterations for stability
4. **Optimize contacts**: Minimize unnecessary collision elements
5. **Validate results**: Ensure optimization doesn't compromise accuracy

## Troubleshooting Common Physics Issues

### Robot Falling Through Ground

**Causes and Solutions:**
- Insufficient contact parameters: Increase ERP, decrease CFM
- Incorrect mass: Verify realistic mass values
- Time step too large: Reduce max_step_size
- Solver iterations too low: Increase iterations

### Joint Oscillations

**Causes and Solutions:**
- Insufficient damping: Add joint damping
- High ERP values: Reduce ERP for smoother response
- Mass distribution issues: Verify inertial properties
- Time step too large: Reduce time step

### Unstable Balance

**Causes and Solutions:**
- Inadequate solver iterations: Increase iterations
- Poor mass distribution: Verify CoM placement
- Insufficient friction: Increase ground friction
- Contact parameters: Optimize contact surface parameters

## Simulation Validation

### Quantitative Validation

Compare simulation results with:
- Analytical solutions for simple cases
- Real robot data when available
- Other simulation tools
- Physical experiments

### Qualitative Validation

Ensure the simulation exhibits:
- Realistic motion patterns
- Appropriate response to disturbances
- Stable behavior under various conditions
- Expected failure modes

## Conclusion

Proper configuration of physics parameters is essential for achieving realistic and stable humanoid robot simulation in Gazebo. The parameters discussed in this chapter form the foundation for effective simulation, but remember that optimal values depend on your specific robot design and application requirements.

Always validate your parameter choices through systematic testing, and be prepared to iterate on your configuration as you develop more complex behaviors and scenarios.

The next chapter will focus on adding exercises and examples to Module 2 content as specified in task T016, building upon the physics concepts covered here.

## Exercises

1. Create a simple physics configuration for a basic humanoid model
2. Tune parameters to achieve stable balance for a standing robot
3. Test the effect of different time steps on simulation stability
4. Experiment with solver iterations to find the minimum required for stability
5. Validate that your configuration produces realistic walking behavior