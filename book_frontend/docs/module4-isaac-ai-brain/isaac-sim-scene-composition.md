---
title: Isaac Sim Scene Composition & USD Integration
sidebar_label: Isaac Sim Scene Composition
sidebar_position: 17
description: Advanced techniques for scene composition using Universal Scene Description (USD) in Isaac Sim for robotics simulation
tags: [isaac-sim, usd, scene-composition, robotics-simulation, universal-scene-description, omniverse, gpu-rendering]
---

# Isaac Sim Scene Composition & USD Integration

## Introduction to USD in Robotics Simulation

Universal Scene Description (USD) is Pixar's open-source scene description and interchange format that forms the foundation of Isaac Sim's scene architecture. USD provides a powerful, hierarchical representation of 3D scenes that enables efficient collaboration, versioning, and complex scene assembly for robotics applications.

### Why USD for Robotics?

USD provides several key advantages for robotics simulation:

1. **Hierarchical Structure**: Organize complex robot and environment models
2. **Asset Reusability**: Share and reuse components across scenes
3. **Layered Composition**: Combine multiple USD files into complex scenes
4. **Variant Sets**: Different configurations of the same asset
5. **Schema Extensibility**: Extend with robotics-specific schemas
6. **Performance**: Efficient streaming and instancing for large scenes

### USD Core Concepts

#### Prims (Primitives)
Everything in USD is a "Prim" (Primitive), forming a hierarchical tree structure:

```
World (Xform)
├── Robot (Xform)
│   ├── BaseLink (Xform)
│   │   ├── Body (Mesh)
│   │   ├── Camera (Camera)
│   │   └── IMU (Xform)
│   ├── Joint1 (PhysicsJoint)
│   ├── Link1 (Xform)
│   │   └── Arm (Mesh)
│   └── Joint2 (PhysicsJoint)
└── Environment (Xform)
    ├── GroundPlane (Mesh)
    ├── Walls (Xform)
    │   ├── Wall1 (Mesh)
    │   └── Wall2 (Mesh)
    └── Objects (Xform)
        ├── Box (Mesh)
        └── Cylinder (Mesh)
```

#### Properties and Attributes
Each prim has properties that define its characteristics:
- **Transform Properties**: Position, rotation, scale
- **Geometric Properties**: Shape, size, materials
- **Physics Properties**: Mass, friction, collision properties
- **Animation Properties**: Keyframe animation data

#### Relationships
Connections between prims that define dependencies and interactions:
- **Material Bindings**: Connect materials to geometry
- **Light Relationships**: Define illumination patterns
- **Assembly Relationships**: Define component hierarchies

## USD Schema Extensions for Robotics

### Isaac Sim Robotics Schemas

Isaac Sim extends USD with robotics-specific schemas:

```python
# Example: Creating a robot with Isaac Sim schemas
import omni
from pxr import Usd, UsdGeom, UsdPhysics, PhysxSchema, UsdShade
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.core.utils.prims import get_prim_at_path, define_prim
import numpy as np

def create_humanoid_robot_in_usd(stage, prim_path, robot_config):
    """
    Create a humanoid robot in USD with Isaac Sim extensions

    Args:
        stage: USD stage to add robot to
        prim_path: Path for the robot prim
        robot_config: Configuration dictionary with robot specifications
    """

    # Create the robot root prim
    robot_prim = UsdGeom.Xform.Define(stage, prim_path)

    # Add Isaac Sim-specific schemas
    # Physics properties
    rigid_body_api = PhysxSchema.PhysxRigidBodyAPI.Apply(robot_prim.GetPrim())
    rigid_body_api.CreateSleepThresholdAttr(1e-5)
    rigid_body_api.CreateStabilizationThresholdAttr(1e-5)

    # Add robot links
    links = robot_config.get('links', [])
    for link_config in links:
        create_robot_link(stage, f"{prim_path}/{link_config['name']}", link_config)

    # Add joints
    joints = robot_config.get('joints', [])
    for joint_config in joints:
        create_robot_joint(stage, f"{prim_path}/{joint_config['name']}", joint_config)

    # Add sensors
    sensors = robot_config.get('sensors', [])
    for sensor_config in sensors:
        create_robot_sensor(stage, f"{prim_path}/{sensor_config['name']}", sensor_config)

    return robot_prim

def create_robot_link(stage, link_path, link_config):
    """Create a robot link with physics properties"""

    # Determine geometry type
    geom_type = link_config.get('geometry_type', 'capsule')

    if geom_type == 'capsule':
        link_geom = UsdGeom.Capsule.Define(stage, link_path)
        link_geom.CreateRadiusAttr(link_config.get('radius', 0.05))
        link_geom.CreateHeightAttr(link_config.get('height', 0.2))
    elif geom_type == 'box':
        link_geom = UsdGeom.Cube.Define(stage, link_path)
        size = link_config.get('size', [0.1, 0.1, 0.1])
        link_geom.CreateSizeAttr(max(size))
    elif geom_type == 'sphere':
        link_geom = UsdGeom.Sphere.Define(stage, link_path)
        link_geom.CreateRadiusAttr(link_config.get('radius', 0.1))
    else:
        # Default to capsule
        link_geom = UsdGeom.Capsule.Define(stage, link_path)
        link_geom.CreateRadiusAttr(0.05)
        link_geom.CreateHeightAttr(0.2)

    # Set position and orientation
    position = link_config.get('position', [0, 0, 0])
    orientation = link_config.get('orientation', [0, 0, 0, 1])  # w, x, y, z quaternion

    link_geom.AddTranslateOp().Set(position)
    link_geom.AddOrientOp().Set(orientation)

    # Add mass and inertial properties
    mass_api = PhysxSchema.PhysxMassAPI.Apply(link_geom.GetPrim())
    mass_api.CreateMassAttr(link_config.get('mass', 1.0))

    # Add collision properties
    collision_api = PhysxSchema.PhysxCollisionAPI.Apply(link_geom.GetPrim())
    collision_api.CreateContactOffsetAttr(0.001)
    collision_api.CreateRestOffsetAttr(0.0)

    # Add material
    material_path = f"{link_path}_material"
    material = create_material(stage, material_path, link_config.get('color', [0.8, 0.8, 0.8]))

    # Apply material to geometry
    UsdShade.MaterialBindingAPI(link_geom).Bind(material)

def create_robot_joint(stage, joint_path, joint_config):
    """Create a robot joint with constraints"""

    joint_type = joint_config.get('type', 'revolute')

    if joint_type == 'revolute':
        # Revolute joint (rotational)
        joint = PhysxSchema.PhysxRevoluteJoint.Define(stage, joint_path)

        # Set joint properties
        joint.CreateAxisAttr(joint_config.get('axis', 'X'))
        joint.CreateLowerLimitAttr(joint_config.get('lower_limit', -1.57))  # -90 degrees
        joint.CreateUpperLimitAttr(joint_config.get('upper_limit', 1.57))   # 90 degrees

    elif joint_type == 'fixed':
        # Fixed joint (no movement)
        joint = PhysxSchema.PhysxFixedJoint.Define(stage, joint_path)

    elif joint_type == 'prismatic':
        # Prismatic joint (linear motion)
        joint = PhysxSchema.PhysxPrismaticJoint.Define(stage, joint_path)
        joint.CreateAxisAttr(joint_config.get('axis', 'X'))
        joint.CreateLowerLimitAttr(joint_config.get('lower_limit', -0.1))
        joint.CreateUpperLimitAttr(joint_config.get('upper_limit', 0.1))

    else:
        # Default to revolute
        joint = PhysxSchema.PhysxRevoluteJoint.Define(stage, joint_path)
        joint.CreateAxisAttr('X')
        joint.CreateLowerLimitAttr(-1.57)
        joint.CreateUpperLimitAttr(1.57)

    # Set joint transforms
    position = joint_config.get('position', [0, 0, 0])
    joint.GetPrim().GetAttribute('xformOp:translate').Set(position)

def create_robot_sensor(stage, sensor_path, sensor_config):
    """Create a robot sensor"""

    sensor_type = sensor_config.get('type', 'camera')

    if sensor_type == 'camera':
        # Create camera sensor
        camera = UsdGeom.Camera.Define(stage, sensor_path)

        # Set camera properties
        camera.CreateFocalLengthAttr(sensor_config.get('focal_length', 24.0))
        camera.CreateHorizontalApertureAttr(sensor_config.get('horizontal_aperture', 36.0))
        camera.CreateVerticalApertureAttr(sensor_config.get('vertical_aperture', 24.0))
        camera.CreateClippingRangeAttr((0.1, 100.0))

        # Position camera
        position = sensor_config.get('position', [0, 0, 0])
        camera.AddTranslateOp().Set(position)

    elif sensor_type == 'lidar':
        # Create LiDAR sensor (conceptual - actual implementation in Isaac Sim)
        lidar = UsdGeom.Cone.Define(stage, sensor_path)
        lidar.CreateHeightAttr(0.05)
        lidar.CreateRadiusAttr(0.02)

        position = sensor_config.get('position', [0, 0, 0])
        lidar.AddTranslateOp().Set(position)

    elif sensor_type == 'imu':
        # Create IMU sensor (conceptual)
        imu = UsdGeom.Sphere.Define(stage, sensor_path)
        imu.CreateRadiusAttr(0.01)

        position = sensor_config.get('position', [0, 0, 0])
        imu.AddTranslateOp().Set(position)

def create_material(stage, material_path, color):
    """Create a material with specified color"""

    material = UsdShade.Material.Define(stage, material_path)

    # Create USD Preview Surface shader
    shader = UsdShade.Shader.Define(stage, f"{material_path}/Shader")
    shader.CreateIdAttr("UsdPreviewSurface")

    # Set material properties
    shader.CreateInput("diffuseColor", Usd.Sdf.ValueTypeNames.Color3f).Set(color)
    shader.CreateInput("metallic", Usd.Sdf.ValueTypeNames.Float).Set(0.0)
    shader.CreateInput("roughness", Usd.Sdf.ValueTypeNames.Float).Set(0.5)

    # Connect shader to material
    surface_output = material.CreateSurfaceOutput()
    shader_output = shader.CreateOutput("surface", Usd.Sdf.ValueTypeNames.Token)
    surface_output.ConnectToSource(shader_output)

    return material

# Example usage
def example_robot_creation():
    """Example of creating a simple humanoid robot"""

    # Get the current stage
    stage = omni.usd.get_context().get_stage()

    # Define robot configuration
    robot_config = {
        'links': [
            {
                'name': 'pelvis',
                'geometry_type': 'box',
                'size': [0.2, 0.2, 0.1],
                'position': [0, 0, 0.8],
                'mass': 5.0,
                'color': [0.7, 0.7, 0.7]
            },
            {
                'name': 'torso',
                'geometry_type': 'capsule',
                'radius': 0.1,
                'height': 0.6,
                'position': [0, 0, 1.1],
                'mass': 8.0,
                'color': [0.6, 0.6, 0.6]
            },
            {
                'name': 'head',
                'geometry_type': 'sphere',
                'radius': 0.12,
                'position': [0, 0, 1.5],
                'mass': 2.0,
                'color': [0.8, 0.8, 0.8]
            },
            # Add legs, arms, etc.
        ],
        'joints': [
            {
                'name': 'torso_pelvis',
                'type': 'revolute',
                'axis': 'Y',
                'lower_limit': -0.5,
                'upper_limit': 0.5,
                'position': [0, 0, 0.85]
            }
        ],
        'sensors': [
            {
                'name': 'head_camera',
                'type': 'camera',
                'position': [0, 0, 0.1],  # Relative to head
                'focal_length': 24.0,
                'horizontal_aperture': 36.0
            }
        ]
    }

    # Create the robot
    robot_prim = create_humanoid_robot_in_usd(stage, '/World/HumanoidRobot', robot_config)

    print(f"Humanoid robot created at {robot_prim.GetPath()}")
    return robot_prim
```

### Physics Simulation with USD

USD provides robust physics simulation capabilities through NVIDIA PhysX integration:

#### Rigid Body Dynamics

```python
# Example: Physics configuration for humanoid robot
def configure_robot_physics(robot_prim_path, stage):
    """Configure physics properties for humanoid robot"""

    # Get the robot prim
    robot_prim = stage.GetPrimAtPath(robot_prim_path)

    # Configure global physics properties
    scene_prim = stage.GetPrimAtPath('/World/PhysicsScene')
    if not scene_prim.IsValid():
        # Create physics scene if it doesn't exist
        scene_prim = UsdPhysics.Scene.Define(stage, '/World/PhysicsScene')

    # Set gravity
    scene_prim.CreateGravityDirectionAttr().Set([0, 0, -1])
    scene_prim.CreateGravityMagnitudeAttr().Set(9.81)

    # Set solver parameters
    scene_prim.CreateEnableCCDAttr(True)  # Continuous collision detection
    scene_prim.CreateEnableStabilizationAttr(True)

    # Configure individual links with specific physics properties
    configure_link_physics(robot_prim, stage)

def configure_link_physics(robot_prim, stage):
    """Configure physics properties for individual robot links"""

    # Iterate through all children of the robot
    for child_prim in robot_prim.GetChildren():
        prim_path = child_prim.GetPath()

        # Apply rigid body properties
        rigid_body_api = PhysxSchema.PhysxRigidBodyAPI.Apply(child_prim)
        rigid_body_api.CreateSleepThresholdAttr(1e-4)
        rigid_body_api.CreateStabilizationThresholdAttr(1e-4)

        # Apply mass properties
        mass_api = PhysxSchema.PhysxMassAPI.Apply(child_prim)

        # Set mass based on geometry (example calculation)
        geom_type = get_geometry_type(child_prim)
        if geom_type == 'capsule':
            radius = get_capsule_radius(child_prim)
            height = get_capsule_height(child_prim)
            volume = 3.14159 * radius * radius * height  # Approximate volume
            density = 1000  # kg/m³ (water density)
            mass = volume * density
            mass_api.CreateMassAttr(mass)
        elif geom_type == 'box':
            size_attr = child_prim.GetAttribute('size')
            size = size_attr.Get() if size_attr.Get() else [0.1, 0.1, 0.1]
            volume = size[0] * size[1] * size[2]
            mass = volume * 1000  # density = 1000 kg/m³
            mass_api.CreateMassAttr(mass)
        elif geom_type == 'sphere':
            radius_attr = child_prim.GetAttribute('radius')
            radius = radius_attr.Get() if radius_attr.Get() else 0.1
            volume = (4/3) * 3.14159 * radius * radius * radius
            mass = volume * 1000
            mass_api.CreateMassAttr(mass)

        # Apply collision properties
        collision_api = PhysxSchema.PhysxCollisionAPI.Apply(child_prim)
        collision_api.CreateContactOffsetAttr(0.001)
        collision_api.CreateRestOffsetAttr(0.0)

        # Apply material properties
        material_path = f"{prim_path}_physx_material"
        create_physx_material(stage, material_path)

        # Bind material to collision
        collision_api.CreateMaterialRel().SetTargets([material_path])

def create_physx_material(stage, material_path):
    """Create PhysX material with friction and restitution properties"""

    physx_material = PhysxSchema.PhysxMaterial.Define(stage, material_path)

    # Set material properties for humanoid robot
    physx_material.CreateStaticFrictionAttr(0.7)    # High static friction for stable standing
    physx_material.CreateDynamicFrictionAttr(0.5)   # Moderate dynamic friction
    physx_material.CreateRestitutionAttr(0.1)       # Low restitution (not bouncy)

    return physx_material

def get_geometry_type(prim):
    """Determine geometry type from USD prim"""
    if prim.IsA(UsdGeom.Capsule):
        return 'capsule'
    elif prim.IsA(UsdGeom.Cube):
        return 'box'
    elif prim.IsA(UsdGeom.Sphere):
        return 'sphere'
    else:
        return 'unknown'

def get_capsule_radius(prim):
    """Get radius of capsule geometry"""
    radius_attr = prim.GetAttribute('radius')
    return radius_attr.Get() if radius_attr.Get() else 0.1

def get_capsule_height(prim):
    """Get height of capsule geometry"""
    height_attr = prim.GetAttribute('height')
    return height_attr.Get() if height_attr.Get() else 0.2
```

## Advanced USD Composition Techniques

### Composition Arcs and Variants

USD provides several composition mechanisms for building complex scenes:

#### References
References allow including content from another USD file:

```python
# Example: Using USD references for scene assembly
def create_scene_with_references(stage):
    """Create a scene using USD references"""

    # Create world root
    world = UsdGeom.Xform.Define(stage, "/World")

    # Reference a pre-made robot
    robot_prim = UsdGeom.Xform.Define(stage, "/World/Robot")
    robot_prim.GetPrim().GetReferences().AddReference(
        "/Isaac/Robots/Franka/franka.usd"
    )

    # Reference a pre-made environment
    env_prim = UsdGeom.Xform.Define(stage, "/World/Environment")
    env_prim.GetPrim().GetReferences().AddReference(
        "/Isaac/Environments/SimpleRoom.usd"
    )

    # Add custom objects that aren't in references
    add_custom_objects(stage)

    return world

def add_custom_objects(stage):
    """Add custom objects to a scene with references"""

    # Add a custom table
    table = UsdGeom.Cube.Define(stage, "/World/Environment/Table")
    table.CreateSizeAttr(1.0)
    table.AddTranslateOp().Set(Gf.Vec3d(1.0, 0, 0.5))

    # Add a custom object on the table
    object_on_table = UsdGeom.Sphere.Define(stage, "/World/Environment/Table/Object")
    object_on_table.CreateRadiusAttr(0.1)
    object_on_table.AddTranslateOp().Set(Gf.Vec3d(0, 0, 0.6))
```

#### Payloads
Payloads provide lazy-loaded references for performance:

```python
# Example: Using payloads for large scenes
def create_large_scene_with_payloads(stage):
    """Create a large scene using payloads for performance"""

    world = UsdGeom.Xform.Define(stage, "/World")

    # Use payloads for complex environments that are loaded on demand
    city_env = UsdGeom.Xform.Define(stage, "/World/CityEnvironment")
    city_env.GetPrim().GetPayloads().AddPayload(
        "/Isaac/Environments/LargeCity.usd"
    )

    # Load specific areas on demand
    building_1 = UsdGeom.Xform.Define(stage, "/World/CityEnvironment/Building1")
    building_1.GetPrim().GetPayloads().AddPayload(
        "/Isaac/Environments/Buildings/OfficeBuilding.usd"
    )

    # Robot is always loaded
    robot = UsdGeom.Xform.Define(stage, "/World/Robot")
    robot.GetPrim().GetReferences().AddReference(
        "/Isaac/Robots/Franka/franka.usd"
    )

    return world
```

#### Variants
Variants allow multiple versions of the same asset:

```python
# Example: Using USD variants for different robot configurations
def create_robot_with_variants(stage, robot_path):
    """Create a robot with configuration variants"""

    # Create robot prim with variants
    robot = UsdGeom.Xform.Define(stage, robot_path)

    # Create a variant set for robot configurations
    config_variant_set = robot.GetPrim().GetVariantSet("Configuration")
    config_variant_set.SetVariantSelection("Standard")

    # Define different configuration variants
    with stage.GetEditTarget():
        # Standard configuration
        config_variant_set.AddVariant("Standard")
        with config_variant_set.GetVariantEditContext("Standard", stage.GetEditTarget()):
            # Add standard gripper
            standard_gripper = UsdGeom.Cone.Define(stage, f"{robot_path}/Gripper")
            standard_gripper.CreateHeightAttr(0.1)
            standard_gripper.CreateRadiusAttr(0.05)

        # Heavy-duty configuration
        config_variant_set.AddVariant("HeavyDuty")
        with config_variant_set.GetVariantEditContext("HeavyDuty", stage.GetEditTarget()):
            # Add heavy-duty gripper
            heavy_gripper = UsdGeom.Cylinder.Define(stage, f"{robot_path}/Gripper")
            heavy_gripper.CreateHeightAttr(0.15)
            heavy_gripper.CreateRadiusAttr(0.08)

        # Precision configuration
        config_variant_set.AddVariant("Precision")
        with config_variant_set.GetVariantEditContext("Precision", stage.GetEditTarget()):
            # Add precision gripper
            precision_gripper = UsdGeom.Mesh.Define(stage, f"{robot_path}/Gripper")
            # Add more complex precision gripper geometry

    return robot

def switch_robot_configuration(robot_prim, configuration):
    """Switch robot configuration using variants"""
    config_variant_set = robot_prim.GetPrim().GetVariantSet("Configuration")
    config_variant_set.SetVariantSelection(configuration)
```

## Isaac Sim Scene Composition Patterns

### Modular Scene Architecture

Create reusable scene components:

```python
# Example: Modular scene architecture
class IsaacSimSceneComposer:
    def __init__(self, stage):
        self.stage = stage
        self.scene_components = {}
        self.asset_library = AssetLibrary()

    def create_modular_environment(self, config):
        """Create environment using modular components"""

        # Create base environment
        environment = self.create_base_environment(config)

        # Add modular components based on configuration
        for component_type in config.get('components', []):
            if component_type == 'obstacles':
                self.add_obstacle_course(environment, config.get('obstacle_config', {}))
            elif component_type == 'furniture':
                self.add_furniture(environment, config.get('furniture_config', {}))
            elif component_type == 'interactive_objects':
                self.add_interactive_objects(environment, config.get('interactive_config', {}))
            elif component_type == 'sensors':
                self.add_sensor_equipment(environment, config.get('sensor_config', {}))

        return environment

    def create_base_environment(self, config):
        """Create base environment structure"""
        # Create world root
        world = UsdGeom.Xform.Define(self.stage, "/World")

        # Add ground plane
        ground = self.create_ground_plane(config.get('ground_config', {}))

        # Add lighting
        lighting = self.create_environment_lighting(config.get('lighting_config', {}))

        # Add basic structure
        structure = self.create_basic_structure(config.get('structure_config', {}))

        return {
            'world': world,
            'ground': ground,
            'lighting': lighting,
            'structure': structure
        }

    def create_ground_plane(self, config):
        """Create configurable ground plane"""
        ground_path = config.get('path', '/World/GroundPlane')

        # Create plane geometry
        plane = UsdGeom.Mesh.Define(self.stage, ground_path)

        # Configure plane based on parameters
        size = config.get('size', [10.0, 10.0])
        resolution = config.get('resolution', [20, 20])

        # Create plane vertices
        vertices = []
        for i in range(resolution[0] + 1):
            for j in range(resolution[1] + 1):
                x = (i / resolution[0] - 0.5) * size[0]
                y = (j / resolution[1] - 0.5) * size[1]
                vertices.append(Gf.Vec3f(x, y, 0.0))

        # Create face indices
        face_vertex_indices = []
        face_vertex_counts = []
        for i in range(resolution[0]):
            for j in range(resolution[1]):
                base_idx = i * (resolution[1] + 1) + j
                face_vertex_indices.extend([
                    base_idx,
                    base_idx + resolution[1] + 1,
                    base_idx + resolution[1] + 2,
                    base_idx + 1
                ])
                face_vertex_counts.append(4)

        # Set mesh properties
        plane.CreatePointsAttr(vertices)
        plane.CreateFaceVertexIndicesAttr(face_vertex_indices)
        plane.CreateFaceVertexCountsAttr(face_vertex_counts)

        # Apply material
        material_config = config.get('material', {})
        material = self.create_surface_material(f"{ground_path}_material", material_config)
        UsdShade.MaterialBindingAPI(plane).Bind(material)

        # Apply physics properties for collision
        collision_api = PhysxSchema.PhysxCollisionAPI.Apply(plane.GetPrim())
        collision_api.CreateRestOffsetAttr(0.0)
        collision_api.CreateContactOffsetAttr(0.001)

        return plane

    def create_environment_lighting(self, config):
        """Create configurable environment lighting"""
        lighting_config = config.get('type', 'dome')

        if lighting_config == 'dome':
            return self.create_dome_lighting(config)
        elif lighting_config == 'directional':
            return self.create_directional_lighting(config)
        elif lighting_config == 'mixed':
            return self.create_mixed_lighting(config)
        else:
            # Default to dome lighting
            return self.create_dome_lighting(config)

    def create_dome_lighting(self, config):
        """Create dome light for environment lighting"""
        from pxr import UsdLux

        dome_light = UsdLux.DomeLight.Define(self.stage, "/World/Lights/DomeLight")

        # Set dome light properties
        dome_light.CreateIntensityAttr(config.get('intensity', 30000))
        dome_light.CreateColorAttr(Gf.Vec3f(*config.get('color', [1.0, 1.0, 1.0])))
        dome_light.CreateTextureFileAttr(config.get('texture_file', ''))

        return dome_light

    def create_directional_lighting(self, config):
        """Create directional lighting"""
        from pxr import UsdLux

        directional_light = UsdLux.DistantLight.Define(self.stage, "/World/Lights/DirectionalLight")

        # Set directional light properties
        directional_light.CreateIntensityAttr(config.get('intensity', 50000))
        directional_light.CreateColorAttr(Gf.Vec3f(*config.get('color', [1.0, 0.98, 0.9])))

        # Set direction
        direction = config.get('direction', [0, 0, -1])
        directional_light.AddOrientOp().Set(Gf.Quatf().SetRotate(Gf.Vec3f(*direction)))

        return directional_light

    def add_obstacle_course(self, environment, config):
        """Add configurable obstacle course"""
        obstacles = config.get('obstacles', [])
        obstacle_parent = UsdGeom.Xform.Define(self.stage, "/World/Obstacles")

        for i, obstacle_config in enumerate(obstacles):
            obstacle_path = f"/World/Obstacles/Obstacle_{i:03d}"

            if obstacle_config['type'] == 'box':
                self.create_box_obstacle(obstacle_path, obstacle_config)
            elif obstacle_config['type'] == 'cylinder':
                self.create_cylinder_obstacle(obstacle_path, obstacle_config)
            elif obstacle_config['type'] == 'slope':
                self.create_slope_obstacle(obstacle_path, obstacle_config)
            elif obstacle_config['type'] == 'gap':
                self.create_gap_obstacle(obstacle_path, obstacle_config)

    def create_box_obstacle(self, path, config):
        """Create box-shaped obstacle"""
        box = UsdGeom.Cube.Define(self.stage, path)

        # Set box properties
        size = config.get('size', [1.0, 1.0, 1.0])
        box.CreateSizeAttr(max(size))  # USD Cube uses uniform size

        # Position
        position = config.get('position', [0, 0, 0])
        box.AddTranslateOp().Set(Gf.Vec3d(*position))

        # Apply material
        material = self.create_surface_material(f"{path}_material", config.get('material', {}))
        UsdShade.MaterialBindingAPI(box).Bind(material)

        # Apply physics properties
        collision_api = PhysxSchema.PhysxCollisionAPI.Apply(box.GetPrim())
        collision_api.CreateRestOffsetAttr(0.0)
        collision_api.CreateContactOffsetAttr(0.001)

        return box

    def create_cylinder_obstacle(self, path, config):
        """Create cylinder-shaped obstacle"""
        cylinder = UsdGeom.Cylinder.Define(self.stage, path)

        # Set cylinder properties
        radius = config.get('radius', 0.5)
        height = config.get('height', 1.0)
        cylinder.CreateRadiusAttr(radius)
        cylinder.CreateHeightAttr(height)

        # Position
        position = config.get('position', [0, 0, height/2])  # Center at base
        cylinder.AddTranslateOp().Set(Gf.Vec3d(*position))

        # Apply material and physics
        material = self.create_surface_material(f"{path}_material", config.get('material', {}))
        UsdShade.MaterialBindingAPI(cylinder).Bind(material)

        collision_api = PhysxSchema.PhysxCollisionAPI.Apply(cylinder.GetPrim())
        collision_api.CreateRestOffsetAttr(0.0)
        collision_api.CreateContactOffsetAttr(0.001)

        return cylinder

    def create_slope_obstacle(self, path, config):
        """Create slope obstacle"""
        slope = UsdGeom.Mesh.Define(self.stage, path)

        # Create slope geometry
        length = config.get('length', 2.0)
        width = config.get('width', 1.0)
        height = config.get('height', 0.5)
        angle = config.get('angle', 30.0)  # degrees

        # Calculate slope points
        vertices = [
            Gf.Vec3f(-width/2, -length/2, 0),
            Gf.Vec3f(width/2, -length/2, 0),
            Gf.Vec3f(width/2, length/2, height),
            Gf.Vec3f(-width/2, length/2, height)
        ]

        # Create faces
        face_vertex_indices = [0, 1, 2, 0, 2, 3]
        face_vertex_counts = [3, 3]

        # Set mesh properties
        slope.CreatePointsAttr(vertices)
        slope.CreateFaceVertexIndicesAttr(face_vertex_indices)
        slope.CreateFaceVertexCountsAttr(face_vertex_counts)

        # Position and rotate
        position = config.get('position', [0, 0, 0])
        slope.AddTranslateOp().Set(Gf.Vec3d(*position))
        slope.AddRotateYOp().Set(config.get('rotation', 0))

        return slope

    def create_surface_material(self, material_path, config):
        """Create configurable surface material"""
        material = UsdShade.Material.Define(self.stage, material_path)

        # Create shader
        shader = UsdShade.Shader.Define(self.stage, f"{material_path}/PreviewSurface")
        shader.CreateIdAttr("UsdPreviewSurface")

        # Set material properties
        shader.CreateInput("diffuseColor", Usd.Sdf.ValueTypeNames.Color3f).Set(
            Gf.Vec3f(*config.get('color', [0.7, 0.7, 0.7]))
        )
        shader.CreateInput("metallic", Usd.Sdf.ValueTypeNames.Float).Set(
            config.get('metallic', 0.0)
        )
        shader.CreateInput("roughness", Usd.Sdf.ValueTypeNames.Float).Set(
            config.get('roughness', 0.5)
        )
        shader.CreateInput("specular", Usd.Sdf.ValueTypeNames.Float).Set(
            config.get('specular', 0.5)
        )

        # Connect shader to material
        surface_output = material.CreateSurfaceOutput()
        shader_surface_output = shader.CreateOutput("surface", Usd.Sdf.ValueTypeNames.Token)
        surface_output.ConnectToSource(shader_surface_output)

        return material

    def add_robot_to_environment(self, environment, robot_config):
        """Add robot to the environment"""
        robot_path = robot_config.get('path', '/World/Robot')

        # Create robot reference
        robot_xform = UsdGeom.Xform.Define(self.stage, robot_path)

        # Add robot model reference
        robot_model_path = robot_config.get('model_path', '/Isaac/Robots/DefaultRobot.usd')
        robot_xform.GetPrim().GetReferences().AddReference(robot_model_path)

        # Position robot
        initial_pose = robot_config.get('initial_pose', [0, 0, 0, 0, 0, 0])  # [x, y, z, rx, ry, rz]
        robot_xform.AddTranslateOp().Set(Gf.Vec3d(*initial_pose[:3]))

        # Apply rotation
        rotation = Gf.Vec3f(*initial_pose[3:])
        robot_xform.AddOrientOp().Set(Gf.Quatf().SetRotate(rotation))

        return robot_xform
```

## Domain Randomization with USD

### Advanced Domain Randomization

Implement domain randomization techniques for synthetic data generation:

```python
# Example: USD-based domain randomization
class USDSceneRandomizer:
    def __init__(self, stage):
        self.stage = stage
        self.randomization_params = self.load_randomization_parameters()

    def load_randomization_parameters(self):
        """Load domain randomization configuration"""
        params = {
            'lighting': {
                'intensity_range': [20000, 60000],
                'color_temperature_range': [3000, 8000],
                'position_jitter': 3.0
            },
            'materials': {
                'albedo_range': [[0.1, 0.1, 0.1], [1.0, 1.0, 1.0]],
                'roughness_range': [0.05, 0.95],
                'metallic_range': [0.0, 0.8]
            },
            'textures': {
                'scale_range': [0.1, 10.0],
                'rotation_range': [0, 360],
                'randomize_every_n_frames': 5
            },
            'objects': {
                'position_jitter': 1.0,
                'rotation_jitter': 45.0,
                'scale_jitter': 0.2
            }
        }
        return params

    def randomize_scene(self, scene_elements):
        """Randomize scene elements for domain randomization"""
        for element_type, elements in scene_elements.items():
            if element_type == 'lights':
                self.randomize_lights(elements)
            elif element_type == 'materials':
                self.randomize_materials(elements)
            elif element_type == 'objects':
                self.randomize_objects(elements)
            elif element_type == 'environment':
                self.randomize_environment(elements)

    def randomize_lights(self, light_prims):
        """Randomize lighting conditions"""
        for light_path in light_prims:
            light_prim = self.stage.GetPrimAtPath(light_path)
            if light_prim:
                # Randomize intensity
                intensity = random.uniform(
                    self.randomization_params['lighting']['intensity_range'][0],
                    self.randomization_params['lighting']['intensity_range'][1]
                )
                light_prim.GetAttribute('inputs:intensity').Set(intensity)

                # Randomize color temperature (converted to RGB approximation)
                color_temp = random.uniform(
                    self.randomization_params['lighting']['color_temperature_range'][0],
                    self.randomization_params['lighting']['color_temperature_range'][1]
                )
                rgb_color = self.color_temperature_to_rgb(color_temp)
                light_prim.GetAttribute('inputs:color').Set(rgb_color)

                # Randomize position
                current_pos = light_prim.GetAttribute('xformOp:translate').Get()
                if current_pos:
                    jitter = self.randomization_params['lighting']['position_jitter']
                    new_pos = [
                        current_pos[0] + random.uniform(-jitter, jitter),
                        current_pos[1] + random.uniform(-jitter, jitter),
                        current_pos[2] + random.uniform(-jitter, jitter)
                    ]
                    light_prim.GetAttribute('xformOp:translate').Set(new_pos)

    def randomize_materials(self, material_prims):
        """Randomize material properties"""
        for material_path in material_prims:
            material_prim = self.stage.GetPrimAtPath(material_path)
            if material_prim:
                # Get material shader
                shader_prim = self.get_material_shader(material_prim)

                if shader_prim:
                    # Randomize albedo/diffuse color
                    albedo_min, albedo_max = self.randomization_params['materials']['albedo_range']
                    albedo = [
                        random.uniform(albedo_min[i], albedo_max[i]) for i in range(3)
                    ]

                    shader_input = shader_prim.GetAttribute('inputs:diffuseColor')
                    if shader_input:
                        shader_input.Set(albedo)

                    # Randomize roughness
                    roughness = random.uniform(
                        self.randomization_params['materials']['roughness_range'][0],
                        self.randomization_params['materials']['roughness_range'][1]
                    )

                    shader_input = shader_prim.GetAttribute('inputs:roughness')
                    if shader_input:
                        shader_input.Set(roughness)

                    # Randomize metallic
                    metallic = random.uniform(
                        self.randomization_params['materials']['metallic_range'][0],
                        self.randomization_params['materials']['metallic_range'][1]
                    )

                    shader_input = shader_prim.GetAttribute('inputs:metallic')
                    if shader_input:
                        shader_input.Set(metallic)

    def randomize_objects(self, object_prims):
        """Randomize object positions, rotations, and scales"""
        for object_path in object_prims:
            object_prim = self.stage.GetPrimAtPath(object_path)
            if object_prim:
                # Randomize position
                current_pos = object_prim.GetAttribute('xformOp:translate').Get()
                if current_pos:
                    jitter = self.randomization_params['objects']['position_jitter']
                    new_pos = [
                        current_pos[0] + random.uniform(-jitter, jitter),
                        current_pos[1] + random.uniform(-jitter, jitter),
                        current_pos[2] + random.uniform(-jitter, jitter)
                    ]
                    object_prim.GetAttribute('xformOp:translate').Set(new_pos)

                # Randomize rotation
                current_rot = object_prim.GetAttribute('xformOp:rotateXYZ').Get()
                if current_rot:
                    jitter = self.randomization_params['objects']['rotation_jitter']
                    new_rot = [
                        current_rot[0] + random.uniform(-jitter, jitter),
                        current_rot[1] + random.uniform(-jitter, jitter),
                        current_rot[2] + random.uniform(-jitter, jitter)
                    ]
                    object_prim.GetAttribute('xformOp:rotateXYZ').Set(new_rot)

                # Randomize scale
                current_scale = object_prim.GetAttribute('xformOp:scale').Get()
                if current_scale:
                    jitter = self.randomization_params['objects']['scale_jitter']
                    scale_factor = 1.0 + random.uniform(-jitter, jitter)
                    new_scale = [
                        current_scale[0] * scale_factor,
                        current_scale[1] * scale_factor,
                        current_scale[2] * scale_factor
                    ]
                    object_prim.GetAttribute('xformOp:scale').Set(new_scale)

    def color_temperature_to_rgb(self, color_temp):
        """Convert color temperature to RGB approximation"""
        temp = color_temp / 100
        if temp <= 66:
            red = 255
            green = temp
            green = 99.4708025861 * np.log(green) - 161.1195681661
        else:
            red = temp - 60
            red = 329.698727446 * (red ** -0.1332047592)
            green = temp - 60
            green = 288.1221695283 * (green ** -0.0755148492)

        if temp >= 66:
            blue = 255
        elif temp <= 19:
            blue = 0
        else:
            blue = temp - 10
            blue = 138.5177312231 * np.log(blue) - 305.0447927307

        return [max(0, min(255, x)) / 255.0 for x in [red, green, blue]]

    def get_material_shader(self, material_prim):
        """Get the shader prim associated with a material"""
        # In USD, materials are connected to shaders through relationships
        surface_output = material_prim.GetRelationship('outputs:surface')
        if surface_output:
            targets = surface_output.GetTargets()
            if targets:
                shader_path = targets[0]
                return self.stage.GetPrimAtPath(str(shader_path))
        return None

# Example usage of domain randomization
def setup_domain_randomization():
    """Setup domain randomization for synthetic data generation"""

    # Get current stage
    stage = omni.usd.get_context().get_stage()

    # Initialize domain randomizer
    randomizer = USDSceneRandomizer(stage)

    # Define scene elements to randomize
    scene_elements = {
        'lights': ['/World/DomeLight', '/World/SpotLight1', '/World/SpotLight2'],
        'materials': [
            '/World/Materials/WallMaterial',
            '/World/Materials/FloorMaterial',
            '/World/Materials/ObjectMaterial'
        ],
        'objects': [
            '/World/Environment/Object1',
            '/World/Environment/Object2',
            '/World/Environment/Object3'
        ],
        'environment': ['/World/Environment']
    }

    # Randomize scene for each data sample
    for sample_idx in range(1000):  # Generate 1000 training samples
        randomizer.randomize_scene(scene_elements)

        # Capture data sample (this would be done in Isaac Sim)
        # capture_data_sample(sample_idx)

        print(f"Generated sample {sample_idx + 1}/1000")
```

## Performance Optimization

### Efficient Scene Composition

Optimize USD scenes for better performance:

```python
# Example: Performance optimization for USD scenes
class USDSceneOptimizer:
    def __init__(self, stage):
        self.stage = stage
        self.optimization_strategies = {
            'instancing': self.apply_instancing,
            'level_of_detail': self.apply_level_of_detail,
            'occlusion_culling': self.setup_occlusion_culling,
            'material_sharing': self.optimize_materials,
            'geometry_optimization': self.optimize_geometry
        }

    def optimize_scene_for_performance(self):
        """Apply performance optimizations to scene"""
        for strategy_name, strategy_func in self.optimization_strategies.items():
            self.get_logger().info(f'Applying optimization: {strategy_name}')
            strategy_func()

    def apply_instancing(self):
        """Apply instancing for repeated objects"""
        # Find repeated objects and create instances
        object_instances = {}

        for prim in self.stage.TraverseAll():
            if prim.GetTypeName() and prim.GetTypeName() != '':
                type_name = prim.GetTypeName()
                if type_name not in object_instances:
                    object_instances[type_name] = []
                object_instances[type_name].append(prim)

        # For objects that appear multiple times, consider instancing
        for type_name, instances in object_instances.items():
            if len(instances) > 5:  # Arbitrary threshold
                # Create instancer for this object type
                self.create_instancer_for_type(type_name, instances)

    def create_instancer_for_type(self, type_name, instances):
        """Create instancer for repeated object type"""
        # In USD, instancing can be achieved through:
        # 1. UsdGeom.PointInstancer for GPU-instanced rendering
        # 2. Shared references for repeated objects
        # 3. Procedural instancing in shaders

        # Example: Create a point instancer
        instancer_path = f"/World/Instancers/{type_name}_Instancer"
        instancer = UsdGeom.PointInstancer.Define(self.stage, instancer_path)

        # Get prototype from first instance
        prototype_path = instances[0].GetPath()
        proto_indices = instancer.CreatePrototypesRel()
        proto_indices.AddTarget(prototype_path)

        # Set instance positions and transforms
        positions = []
        ids = []
        for i, instance in enumerate(instances):
            # Get world position of instance
            xform = UsdGeom.Xform(instance)
            transform_ops = xform.GetOrderedXformOps()
            # Extract position from transform (simplified)
            positions.append(instance.GetAttribute('xformOp:translate').Get() or Gf.Vec3f(0, 0, 0))
            ids.append(i)

        instancer.CreatePositionsAttr(positions)
        instancer.CreateProtoIndicesAttr(ids)

        # Remove original instances as they're now handled by instancer
        for instance in instances:
            self.stage.RemovePrim(instance.GetPath())

    def apply_level_of_detail(self):
        """Apply level of detail for complex objects"""
        # Create LOD groups for complex objects
        for prim in self.stage.TraverseAll():
            if self.is_complex_object(prim):
                self.create_lod_group(prim)

    def is_complex_object(self, prim):
        """Determine if object is complex enough for LOD"""
        # Check if prim has many triangles or complex geometry
        geom = UsdGeom.Mesh(prim)
        if geom:
            points_attr = geom.GetPointsAttr()
            if points_attr:
                points = points_attr.Get()
                if points and len(points) > 10000:  # More than 10k vertices
                    return True
        return False

    def create_lod_group(self, complex_prim):
        """Create LOD group for complex object"""
        # Create LOD group
        lod_group_path = f"{complex_prim.GetPath()}_LOD"
        lod_group = UsdGeom.LOD.Define(self.stage, lod_group_path)

        # Create simplified versions of the object
        original_resolution = self.get_mesh_resolution(complex_prim)

        # LOD0: Full resolution
        lod0_path = f"{lod_group_path}/LOD0"
        self.copy_mesh_with_resolution(complex_prim, lod0_path, original_resolution)

        # LOD1: Medium resolution (half vertices)
        lod1_path = f"{lod_group_path}/LOD1"
        medium_resolution = original_resolution // 2
        self.copy_mesh_with_resolution(complex_prim, lod1_path, medium_resolution)

        # LOD2: Low resolution (quarter vertices)
        lod2_path = f"{lod_group_path}/LOD2"
        low_resolution = original_resolution // 4
        self.copy_mesh_with_resolution(complex_prim, lod2_path, low_resolution)

        # Set LOD distances
        lod_group.CreateResolutionAttrib([0, 10, 30])  # Distances in meters

    def get_mesh_resolution(self, mesh_prim):
        """Get resolution metric for mesh"""
        mesh = UsdGeom.Mesh(mesh_prim)
        points_attr = mesh.GetPointsAttr()
        points = points_attr.Get()
        return len(points) if points else 0

    def copy_mesh_with_resolution(self, source_mesh, target_path, target_resolution):
        """Copy mesh with specified resolution (conceptual - would involve mesh simplification)"""
        # This would involve actual mesh simplification algorithms
        # For now, just copy the original
        pass

    def setup_occlusion_culling(self):
        """Setup occlusion culling for performance"""
        # In Isaac Sim, this involves setting up occlusion culling volumes
        # and configuring rendering settings
        pass

    def optimize_materials(self):
        """Optimize materials for performance"""
        # Find similar materials and merge them
        material_groups = self.group_similar_materials()

        for group_name, materials in material_groups.items():
            if len(materials) > 1:
                # Create shared material
                shared_material_path = f"/World/Materials/Shared_{group_name}"
                shared_material = self.create_shared_material(shared_material_path, materials)

                # Replace individual materials with shared material
                for material in materials:
                    self.replace_material_with_shared(material, shared_material)

    def group_similar_materials(self):
        """Group similar materials for sharing"""
        material_groups = {}

        for prim in self.stage.TraverseAll():
            if prim.IsA(UsdShade.Material):
                material = UsdShade.Material(prim)
                material_signature = self.get_material_signature(material)

                if material_signature not in material_groups:
                    material_groups[material_signature] = []
                material_groups[material_signature].append(material)

        return material_groups

    def get_material_signature(self, material):
        """Get signature that identifies similar materials"""
        # Extract key material properties to identify similarity
        shader = self.get_material_shader(material)
        if shader:
            diffuse_color = shader.GetInput('diffuseColor').Get()
            roughness = shader.GetInput('roughness').Get()
            metallic = shader.GetInput('metallic').Get()

            # Create signature based on key properties
            signature = f"diff_{diffuse_color}_rough_{roughness}_metal_{metallic}"
            return signature

        return str(material.GetPath())

    def optimize_geometry(self):
        """Optimize geometry for performance"""
        # Apply various geometry optimization techniques:
        # - Merge static geometry
        # - Remove duplicate vertices
        # - Optimize triangle strips
        # - Apply mesh optimization algorithms

        for prim in self.stage.TraverseAll():
            if prim.IsA(UsdGeom.Mesh):
                mesh = UsdGeom.Mesh(prim)

                # Optimize mesh if it's static (doesn't animate)
                if self.is_static_mesh(mesh):
                    self.optimize_static_mesh(mesh)

    def is_static_mesh(self, mesh):
        """Check if mesh is static (doesn't animate)"""
        # Check if mesh has animation curves or changes over time
        points_attr = mesh.GetPointsAttr()
        return not points_attr.HasValue() or not points_attr.GetConnections()

    def optimize_static_mesh(self, mesh):
        """Optimize static mesh geometry"""
        # Apply mesh optimization algorithms
        # This would typically involve external tools or algorithms
        pass

class IsaacSimScenePerformanceMonitor:
    def __init__(self, stage):
        self.stage = stage
        self.metrics = {
            'scene_complexity': 0,
            'render_performance': 0,
            'physics_performance': 0,
            'memory_usage': 0
        }

    def measure_scene_metrics(self):
        """Measure various scene performance metrics"""
        self.metrics['scene_complexity'] = self.calculate_scene_complexity()
        self.metrics['render_performance'] = self.estimate_render_performance()
        self.metrics['physics_performance'] = self.estimate_physics_performance()
        self.metrics['memory_usage'] = self.estimate_memory_usage()

        return self.metrics

    def calculate_scene_complexity(self):
        """Calculate scene complexity metric"""
        complexity_score = 0

        # Count different types of prims
        prim_counts = {
            'meshes': 0,
            'lights': 0,
            'cameras': 0,
            'materials': 0,
            'instances': 0
        }

        for prim in self.stage.TraverseAll():
            if prim.IsA(UsdGeom.Mesh):
                prim_counts['meshes'] += 1
                # Add complexity based on mesh size
                mesh = UsdGeom.Mesh(prim)
                points_attr = mesh.GetPointsAttr()
                points = points_attr.Get()
                if points:
                    complexity_score += len(points) / 1000  # Complexity per 1k vertices
            elif prim.IsA(UsdLux.Light):
                prim_counts['lights'] += 1
                complexity_score += 10  # Lights add complexity
            elif prim.IsA(UsdGeom.Camera):
                prim_counts['cameras'] += 1
                complexity_score += 5  # Cameras add complexity
            elif prim.IsA(UsdShade.Material):
                prim_counts['materials'] += 1
                complexity_score += 2  # Materials add complexity
            elif prim.IsA(UsdGeom.PointInstancer):
                prim_counts['instances'] += 1
                complexity_score += 1  # Instances affect complexity differently

        self.prim_counts = prim_counts
        return complexity_score

    def estimate_render_performance(self):
        """Estimate rendering performance based on scene content"""
        # Calculate based on:
        # - Number of lights and their types
        # - Material complexity
        # - Geometry complexity
        # - Texture resolution
        # - Shadow complexity

        performance_score = 100  # Base score

        # Reduce score based on complexity factors
        if self.prim_counts['lights'] > 10:
            performance_score -= (self.prim_counts['lights'] - 10) * 5

        if self.metrics['scene_complexity'] > 1000:
            performance_score -= (self.metrics['scene_complexity'] - 1000) * 0.1

        return max(0, performance_score)

    def estimate_physics_performance(self):
        """Estimate physics simulation performance"""
        # Count physics-enabled objects
        physics_objects = 0
        complex_shapes = 0

        for prim in self.stage.TraverseAll():
            if prim.HasAPI(PhysxSchema.PhysxCollisionAPI):
                physics_objects += 1

                # Check if shape is complex
                if prim.IsA(UsdGeom.Mesh):  # Complex mesh vs simple primitives
                    complex_shapes += 1

        # Calculate performance impact
        base_score = 100
        base_score -= physics_objects * 2  # Each physics object costs performance
        base_score -= complex_shapes * 5  # Complex shapes cost more

        return max(0, base_score)

    def estimate_memory_usage(self):
        """Estimate memory usage"""
        # Estimate based on:
        # - Number of prims
        # - Geometry size
        # - Texture sizes
        # - Material count

        estimated_mb = 0

        # Base scene overhead
        estimated_mb += 10

        # Add memory for each prim type
        estimated_mb += self.prim_counts['meshes'] * 5  # 5MB per mesh average
        estimated_mb += self.prim_counts['lights'] * 0.1  # 0.1MB per light
        estimated_mb += self.prim_counts['materials'] * 0.5  # 0.5MB per material
        estimated_mb += self.prim_counts['instances'] * 0.01  # 0.01MB per instance

        return estimated_mb
```

## Advanced USD Features

### Custom USD Schemas for Robotics

Create custom USD schemas for robotics-specific data:

```python
# Example: Custom USD schemas for robotics
from pxr import Tf, Sdf, Usd, UsdGeom

# Define custom schema for robot-specific properties
class RobotComponentAPI(Usd.APISchemaBase):
    """Custom API schema for robot components"""

    def __init__(self, prim=Usd.Prim()):
        super().__init__(prim)

    @staticmethod
    def define(stage, path):
        """Define a RobotComponentAPI on a prim"""
        return RobotComponentAPI(UsdGeom.Xform.Define(stage, path).GetPrim())

    def create_robot_type_attr(self, robot_type="mobile_base", customData=None):
        """Create robot type attribute"""
        return self._create_attr('robot:type', Sdf.ValueTypeNames.Token,
                                customData, False, robot_type)

    def create_component_role_attr(self, role="sensor", customData=None):
        """Create component role attribute"""
        return self._create_attr('component:role', Sdf.ValueTypeNames.Token,
                                customData, False, role)

    def create_max_payload_attr(self, payload=5.0, customData=None):
        """Create max payload attribute"""
        return self._create_attr('robot:maxPayload', Sdf.ValueTypeNames.Double,
                                customData, False, payload)

    def create_dof_count_attr(self, dof=6, customData=None):
        """Create degrees of freedom count attribute"""
        return self._create_attr('robot:dofCount', Sdf.ValueTypeNames.Int,
                                customData, False, dof)

    def get_robot_type_attr(self):
        """Get robot type attribute"""
        return self._get_attr('robot:type', Sdf.ValueTypeNames.Token)

    def get_component_role_attr(self):
        """Get component role attribute"""
        return self._get_attr('component:role', Sdf.ValueTypeNames.Token)

    def get_max_payload_attr(self):
        """Get max payload attribute"""
        return self._get_attr('robot:maxPayload', Sdf.ValueTypeNames.Double)

    def get_dof_count_attr(self):
        """Get DOF count attribute"""
        return self._get_attr('robot:dofCount', Sdf.ValueTypeNames.Int)

    @staticmethod
    def can_apply(prim, apiNameSpace=""):
        """Check if API can be applied to prim"""
        return prim.IsA(UsdGeom.Xform)

Tf.Type.Define(RobotComponentAPI)

# Usage example
def create_robot_with_custom_schema(stage, robot_path):
    """Create robot using custom robotics schema"""

    # Create robot prim
    robot_prim = UsdGeom.Xform.Define(stage, robot_path)

    # Apply custom robot API
    robot_api = RobotComponentAPI.Apply(robot_prim.GetPrim())

    # Set robot-specific properties
    robot_api.create_robot_type_attr("humanoid")
    robot_api.create_max_payload_attr(10.0)
    robot_api.create_dof_count_attr(32)  # Humanoid typically has many DOFs

    # Create robot links with custom properties
    torso_path = f"{robot_path}/Torso"
    torso_prim = UsdGeom.Xform.Define(stage, torso_path)
    torso_api = RobotComponentAPI.Apply(torso_prim.GetPrim())
    torso_api.create_component_role_attr("torso")
    torso_api.create_max_payload_attr(5.0)

    # Create arm with custom properties
    arm_path = f"{robot_path}/RightArm"
    arm_prim = UsdGeom.Xform.Define(stage, arm_path)
    arm_api = RobotComponentAPI.Apply(arm_prim.GetPrim())
    arm_api.create_component_role_attr("manipulator")
    arm_api.create_dof_count_attr(7)  # 7-DOF arm

    return robot_prim
```

### USD Composition for Multi-Robot Scenarios

Creating complex multi-robot scenarios:

```python
# Example: Multi-robot scene composition
class MultiRobotSceneComposer:
    def __init__(self, stage):
        self.stage = stage
        self.robots = {}
        self.environments = {}

    def create_multi_robot_scene(self, scene_config):
        """Create scene with multiple robots"""

        # Create environment
        environment = self.create_environment(scene_config.get('environment', {}))

        # Create robots
        for i, robot_config in enumerate(scene_config.get('robots', [])):
            robot_path = f"/World/Robot_{i:02d}"
            robot = self.create_robot(robot_path, robot_config)

            # Position robot in environment
            self.position_robot_in_environment(robot, robot_config.get('initial_pose', [0, 0, 0, 0, 0, 0]))

            self.robots[f"robot_{i}"] = robot

        # Create interactions between robots
        self.setup_robot_interactions(scene_config.get('interactions', []))

        return {'environment': environment, 'robots': self.robots}

    def create_environment(self, env_config):
        """Create environment for multi-robot scenario"""

        # Create world root
        world = UsdGeom.Xform.Define(self.stage, "/World")

        # Create shared environment components
        env_components = env_config.get('components', [])

        for component_config in env_components:
            if component_config['type'] == 'arena':
                self.create_arena(component_config)
            elif component_config['type'] == 'obstacles':
                self.create_shared_obstacles(component_config)
            elif component_config['type'] == 'landmarks':
                self.create_shared_landmarks(component_config)
            elif component_config['type'] == 'charging_stations':
                self.create_charging_stations(component_config)

        return world

    def create_arena(self, arena_config):
        """Create arena for multi-robot competition/cooperation"""

        arena_size = arena_config.get('size', [10.0, 10.0, 3.0])
        arena_position = arena_config.get('position', [0, 0, 0])

        # Create arena floor
        floor_path = "/World/Arena/Floor"
        floor = UsdGeom.Mesh.Define(self.stage, floor_path)

        # Create floor geometry (rectangle)
        vertices = [
            Gf.Vec3f(-arena_size[0]/2, -arena_size[1]/2, 0),
            Gf.Vec3f(arena_size[0]/2, -arena_size[1]/2, 0),
            Gf.Vec3f(arena_size[0]/2, arena_size[1]/2, 0),
            Gf.Vec3f(-arena_size[0]/2, arena_size[1]/2, 0)
        ]

        face_indices = [0, 1, 2, 0, 2, 3]
        face_counts = [3, 3]

        floor.CreatePointsAttr(vertices)
        floor.CreateFaceVertexIndicesAttr(face_indices)
        floor.CreateFaceVertexCountsAttr(face_counts)

        # Create arena walls
        wall_height = arena_config.get('wall_height', 1.0)
        wall_thickness = arena_config.get('wall_thickness', 0.1)

        # North wall
        north_wall = self.create_arena_wall(
            "/World/Arena/NorthWall",
            [-arena_size[0]/2, arena_size[1]/2, wall_height/2],
            [arena_size[0], wall_thickness, wall_height]
        )

        # South wall
        south_wall = self.create_arena_wall(
            "/World/Arena/SouthWall",
            [-arena_size[0]/2, -arena_size[1]/2, wall_height/2],
            [arena_size[0], wall_thickness, wall_height]
        )

        # East wall
        east_wall = self.create_arena_wall(
            "/World/Arena/EastWall",
            [arena_size[0]/2, -arena_size[1]/2, wall_height/2],
            [wall_thickness, arena_size[1], wall_height]
        )

        # West wall
        west_wall = self.create_arena_wall(
            "/World/Arena/WestWall",
            [-arena_size[0]/2, -arena_size[1]/2, wall_height/2],
            [wall_thickness, arena_size[1], wall_height]
        )

    def create_arena_wall(self, path, position, size):
        """Create a wall for the arena"""

        wall = UsdGeom.Cube.Define(self.stage, path)
        wall.CreateSizeAttr(max(size))

        # Position the wall
        wall.AddTranslateOp().Set(Gf.Vec3d(*position))

        # Apply material
        wall_material = self.create_arena_material(f"{path}_material")
        UsdShade.MaterialBindingAPI(wall).Bind(wall_material)

        return wall

    def create_arena_material(self, material_path):
        """Create material for arena components"""

        material = UsdShade.Material.Define(self.stage, material_path)
        shader = UsdShade.Shader.Define(self.stage, f"{material_path}/PreviewSurface")
        shader.CreateIdAttr("UsdPreviewSurface")

        # Set arena-specific material properties
        shader.CreateInput("diffuseColor", Usd.Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(0.3, 0.3, 0.3))
        shader.CreateInput("roughness", Usd.Sdf.ValueTypeNames.Float).Set(0.6)
        shader.CreateInput("metallic", Usd.Sdf.ValueTypeNames.Float).Set(0.0)

        surface_output = material.CreateSurfaceOutput()
        shader_surface_output = shader.CreateOutput("surface", Usd.Sdf.ValueTypeNames.Token)
        surface_output.ConnectToSource(shader_surface_output)

        return material

    def create_shared_obstacles(self, obstacle_config):
        """Create obstacles shared by all robots"""

        obstacles = obstacle_config.get('obstacles', [])

        for i, obs_config in enumerate(obstacles):
            obstacle_path = f"/World/SharedObstacles/Obstacle_{i:03d}"

            if obs_config['type'] == 'box':
                self.create_shared_box_obstacle(obstacle_path, obs_config)
            elif obs_config['type'] == 'cylinder':
                self.create_shared_cylinder_obstacle(obstacle_path, obs_config)
            elif obs_config['type'] == 'ramp':
                self.create_shared_ramp_obstacle(obstacle_path, obs_config)

    def create_shared_box_obstacle(self, path, config):
        """Create shared box obstacle"""

        box = UsdGeom.Cube.Define(self.stage, path)
        box.CreateSizeAttr(config.get('size', 1.0))

        # Position
        position = config.get('position', [0, 0, 0])
        box.AddTranslateOp().Set(Gf.Vec3d(*position))

        # Apply collision properties
        collision_api = PhysxSchema.PhysxCollisionAPI.Apply(box.GetPrim())
        collision_api.CreateContactOffsetAttr(0.01)
        collision_api.CreateRestOffsetAttr(0.0)

        return box

    def position_robot_in_environment(self, robot, pose):
        """Position robot in the environment with the given pose"""

        # Extract position and orientation from pose [x, y, z, roll, pitch, yaw]
        position = Gf.Vec3d(pose[0], pose[1], pose[2])

        # Convert Euler angles to quaternion
        roll, pitch, yaw = pose[3], pose[4], pose[5]
        cy = np.cos(yaw * 0.5)
        sy = np.sin(yaw * 0.5)
        cp = np.cos(pitch * 0.5)
        sp = np.sin(pitch * 0.5)
        cr = np.cos(roll * 0.5)
        sr = np.sin(roll * 0.5)

        w = cr * cp * cy + sr * sp * sy
        x = sr * cp * cy - cr * sp * sy
        y = cr * sp * cy + sr * cp * sy
        z = cr * cp * sy - sr * sp * cy

        orientation = Gf.Quatf(w, x, y, z)

        # Apply transform to robot
        robot.AddTranslateOp().Set(position)
        robot.AddOrientOp().Set(orientation)

    def setup_robot_interactions(self, interactions):
        """Setup interactions between robots"""

        for interaction in interactions:
            if interaction['type'] == 'formation':
                self.setup_formation_interaction(interaction)
            elif interaction['type'] == 'cooperation':
                self.setup_cooperation_interaction(interaction)
            elif interaction['type'] == 'competition':
                self.setup_competition_interaction(interaction)

    def setup_formation_interaction(self, interaction_config):
        """Setup formation flying/swarming interaction"""

        # Define formation pattern
        formation_pattern = interaction_config.get('pattern', 'line')
        leader_robot = interaction_config.get('leader', 'robot_00')
        follower_robots = interaction_config.get('followers', [])

        # Apply formation constraints
        for i, follower in enumerate(follower_robots):
            offset = self.calculate_formation_offset(formation_pattern, i)

            # Create constraint between leader and follower
            self.create_formation_constraint(leader_robot, follower, offset)

    def calculate_formation_offset(self, pattern, robot_index):
        """Calculate offset for formation pattern"""

        if pattern == 'line':
            return [robot_index * 2.0, 0, 0]  # Line formation
        elif pattern == 'diamond':
            # Diamond formation pattern
            positions = [
                [0, 0, 0],      # Leader
                [1, 1, 0],      # Right front
                [1, -1, 0],     # Left front
                [2, 0, 0]       # Front
            ]
            idx = robot_index % len(positions)
            return positions[idx]
        elif pattern == 'circle':
            # Circular formation
            radius = 3.0
            angle = (2 * np.pi * robot_index) / len(follower_robots) if 'follower_robots' in locals() else 0
            return [radius * np.cos(angle), radius * np.sin(angle), 0]
        else:
            return [0, 0, 0]  # Default offset

    def create_formation_constraint(self, leader_path, follower_path, offset):
        """Create formation constraint between robots"""

        # This would create physics constraints or path planning constraints
        # to maintain formation between robots
        pass
```

## Best Practices for USD Scene Composition

### Scene Organization Best Practices

```python
# Best practices for USD scene organization
USD_SCENE_BEST_PRACTICES = {
    "hierarchy": {
        "recommended_structure": [
            "/World",
            "  /Environment",
            "    /Rooms",
            "    /Outdoor",
            "    /Props",
            "  /Robots",
            "    /Robot1",
            "    /Robot2",
            "  /Sensors",
            "  /Lights",
            "  /Materials"
        ],
        "naming_convention": "Use PascalCase for prims, lowercase_with_underscores for properties",
        "max_depth": "Keep hierarchy depth under 10 levels for performance"
    },
    "performance": {
        "use_payloads": "For large, complex scenes that aren't always needed",
        "instance_geometry": "Use instancing for repeated objects",
        "optimize_materials": "Reuse materials across similar objects",
        "cull_inactive": "Deactivate prims that aren't in the camera view"
    },
    "collaboration": {
        "version_control": "Use VCS for USD files",
        "layer_management": "Separate content into logical layers",
        "namespace_convention": "Use consistent namespace conventions",
        "documentation": "Document custom schemas and extensions"
    }
}

def validate_scene_structure(stage):
    """Validate USD scene structure against best practices"""
    issues = []

    # Check hierarchy depth
    def check_depth(prim, current_depth=0):
        if current_depth > 10:  # Recommended max depth
            issues.append(f"Prim {prim.GetPath()} exceeds recommended depth of 10")

        for child in prim.GetChildren():
            check_depth(child, current_depth + 1)

    root_prim = stage.GetPseudoRoot()
    check_depth(root_prim)

    # Check for common issues
    all_prims = stage.TraverseAll()
    for prim in all_prims:
        # Check naming convention
        prim_name = prim.GetName()
        if ' ' in prim_name:  # Has spaces
            issues.append(f"Prim {prim.GetPath()} contains spaces in name")

    return issues
```

### Quality Assurance and Validation

```python
# Scene validation utilities
def validate_scene_for_simulation(stage):
    """Validate scene is ready for physics simulation"""
    validation_results = {
        "errors": [],
        "warnings": [],
        "info": []
    }

    # Check for physics-enabled objects
    prims_with_physics = 0
    all_prims = stage.TraverseAll()

    for prim in all_prims:
        if prim.HasAPI(PhysxSchema.PhysxRigidBodyAPI):
            prims_with_physics += 1

            # Check for proper mass assignment
            if not prim.HasAPI(PhysxSchema.PhysxMassAPI):
                validation_results["warnings"].append(
                    f"Prim {prim.GetPath()} has rigid body API but no mass assigned"
                )

    if prims_with_physics == 0:
        validation_results["warnings"].append("No physics-enabled objects found in scene")

    # Check for proper lighting
    light_count = 0
    for prim in all_prims:
        if (prim.IsA(UsdLux.DomeLight) or
            prim.IsA(UsdLux.DistantLight) or
            prim.IsA(UsdLux.SphereLight)):
            light_count += 1

    if light_count == 0:
        validation_results["warnings"].append("No lights found in scene - sensors may not work properly")

    # Check for materials
    material_count = 0
    for prim in all_prims:
        if prim.IsA(UsdShade.Material):
            material_count += 1

    if material_count == 0:
        validation_results["info"].append("No materials found - default materials will be used")

    return validation_results

def diagnose_usd_issues(stage):
    """Diagnose common USD issues"""
    issues = []

    # Check references
    all_prims = stage.TraverseAll()
    for prim in all_prims:
        # Check if references are resolved
        if prim.HasAuthoredReferences():
            refs = prim.GetReferences()
            for ref in refs.GetAddedOrExplicitItems():
                if not stage.GetPrimAtPath(ref.assetPath):
                    issues.append(f"Reference {ref.assetPath} not found for prim {prim.GetPath()}")

    # Check material bindings
    for prim in all_prims:
        material_binding = UsdShade.MaterialBindingAPI(prim)
        bound_material = material_binding.ComputeBoundMaterial()[0]
        if not bound_material:
            # Check if it should have a material
            if (prim.IsA(UsdGeom.Mesh) or
                prim.IsA(UsdGeom.Cube) or
                prim.IsA(UsdGeom.Sphere)):
                issues.append(f"Geometry prim {prim.GetPath()} has no material assigned")

    return issues
```

## Summary

USD Scene Composition in Isaac Sim provides a powerful and flexible framework for creating complex, realistic simulation environments. By understanding the core concepts of USD - prims, schemas, composition arcs, and variants - you can build sophisticated scenes that are both visually impressive and physically accurate.

The key to effective USD scene composition is to:

1. **Organize hierarchically**: Use a clear, logical hierarchy for your scene elements
2. **Leverage composition arcs**: Use references, payloads, and variants for efficient scene assembly
3. **Apply appropriate schemas**: Use the right USD schemas for geometry, materials, and physics
4. **Optimize for performance**: Use payloads, instancing, and proper culling for large scenes
5. **Validate thoroughly**: Check for common issues before running simulations

With these techniques, you can create rich, complex simulation environments that enable effective AI training and robotics development in Isaac Sim.