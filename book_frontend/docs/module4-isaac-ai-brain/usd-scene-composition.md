---
title: USD Scene Composition in Isaac Sim
sidebar_label: USD Scene Composition
sidebar_position: 4
description: Advanced techniques for creating and managing scenes using Universal Scene Description in Isaac Sim
tags: [usd, omniverse, scene-composition, universal-scene-description, isaac-sim, 3d-scene]
---

# USD Scene Composition in Isaac Sim

## Introduction to Universal Scene Description (USD)

Universal Scene Description (USD) is Pixar's open-source scene description and interchange format that serves as the foundation for Isaac Sim's scene architecture. USD provides a powerful, hierarchical representation of 3D scenes that enables efficient collaboration, versioning, and complex scene assembly.

### Core Concepts of USD

USD is built around several key concepts:

- **Prims (Primitives)**: The basic building blocks of USD scenes
- **Properties**: Attributes that define prim characteristics
- **Relationships**: Connections between prims
- **Variants**: Different versions of the same asset
- **Composition Arcs**: Mechanisms for combining multiple USD files

### Benefits in Isaac Sim

USD provides several advantages for robotics simulation:

- **Hierarchical Structure**: Organize complex robot and environment models
- **Asset Reusability**: Share and reuse components across scenes
- **Layered Composition**: Combine multiple scene elements efficiently
- **Version Control**: Track changes to scene configurations
- **Collaboration**: Multiple users can work on different aspects of scenes

## USD Fundamentals for Isaac Sim

### Understanding Prims

In USD, everything in a scene is represented as a "Prim" (short for Primitive). Prims form a hierarchical tree structure:

```python
# Example: Creating a simple USD hierarchy in Isaac Sim
from pxr import Usd, UsdGeom, Gf
import omni

# Get the current USD stage
stage = omni.usd.get_context().get_stage()

# Create a root Xform prim
world_prim = UsdGeom.Xform.Define(stage, "/World")

# Add a robot as a child of the world
robot_prim = UsdGeom.Xform.Define(stage, "/World/Robot")

# Add robot components as children of the robot
base_link = UsdGeom.Xform.Define(stage, "/World/Robot/BaseLink")
camera_link = UsdGeom.Xform.Define(stage, "/World/Robot/Camera")

# Set transformations
robot_prim.AddTranslateOp().Set(Gf.Vec3d(0, 0, 1.0))  # Position robot 1m above ground
camera_link.AddTranslateOp().Set(Gf.Vec3d(0.1, 0, 0.1))  # Position camera on robot
```

### USD Schema Types

USD provides various schema types for different purposes:

- **Xform**: For transformations (position, rotation, scale)
- **Mesh**: For 3D mesh geometry
- **Camera**: For camera properties
- **Light**: For lighting elements
- **Material**: For surface materials
- **Physics schemas**: For physics properties

```python
# Example: Using different USD schemas
from pxr import UsdLux, UsdShade

# Create a dome light using USD Lux schema
dome_light = UsdLux.DomeLight.Define(stage, "/World/DomeLight")
dome_light.CreateIntensityAttr(50000)  # Set intensity
dome_light.CreateColorAttr(Gf.Vec3f(1.0, 1.0, 1.0))  # Set color to white

# Create a material using USD Shade schema
material = UsdShade.Material.Define(stage, "/World/Materials/RedMaterial")
shader = UsdShade.Shader.Define(stage, "/World/Materials/RedMaterial/PreviewSurface")
shader.CreateIdAttr("UsdPreviewSurface")

# Set shader inputs
shader.CreateInput("diffuseColor", Usd.Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(1.0, 0.0, 0.0))
shader.CreateInput("metallic", Usd.Sdf.ValueTypeNames.Float).Set(0.0)
shader.CreateInput("roughness", Usd.Sdf.ValueTypeNames.Float).Set(0.5)

# Connect shader to material
material_surface_output = material.CreateSurfaceOutput()
shader_surface_input = shader.CreateOutput("surface", Usd.Sdf.ValueTypeNames.Token)
material_surface_output.ConnectToSource(shader_surface_input)
```

## Creating Complex Scenes

### Environment Setup with USD

Creating realistic environments using USD composition:

```python
# Example: Building a complex environment
def create_indoor_environment(stage):
    """Create an indoor environment with multiple rooms and objects"""

    # Create the main environment
    environment = UsdGeom.Xform.Define(stage, "/World/Environment")

    # Create floors
    create_floor(stage, "/World/Environment/Floor1", (0, 0, 0), (10, 10, 0.1))
    create_floor(stage, "/World/Environment/Floor2", (0, -10, 0), (10, 10, 0.1))

    # Create walls
    create_room_walls(stage, "/World/Environment/Room1")

    # Add furniture
    add_furniture(stage, "/World/Environment/Furniture")

    # Add lighting
    add_environment_lighting(stage, "/World/Environment/Lighting")

    return environment

def create_floor(stage, prim_path, position, size):
    """Create a floor plane"""
    floor = UsdGeom.Mesh.Define(stage, prim_path)

    # Set up simple plane geometry
    points = [
        Gf.Vec3f(-size[0]/2, -size[1]/2, size[2]/2),
        Gf.Vec3f(size[0]/2, -size[1]/2, size[2]/2),
        Gf.Vec3f(size[0]/2, size[1]/2, size[2]/2),
        Gf.Vec3f(-size[0]/2, size[1]/2, size[2]/2)
    ]

    face_vertex_counts = [4]
    face_vertex_indices = [0, 1, 2, 3]

    floor.CreatePointsAttr(points)
    floor.CreateFaceVertexCountsAttr(face_vertex_counts)
    floor.CreateFaceVertexIndicesAttr(face_vertex_indices)

    # Apply floor material
    apply_material_to_prim(stage, prim_path, "FloorMaterial")

    # Position the floor
    floor.AddTranslateOp().Set(Gf.Vec3d(*position))

def create_room_walls(stage, room_path):
    """Create walls for a room"""
    # Create 4 walls
    wall_configs = [
        {"name": "NorthWall", "position": (0, 5, 1.5), "size": (10, 0.2, 3)},
        {"name": "SouthWall", "position": (0, -5, 1.5), "size": (10, 0.2, 3)},
        {"name": "EastWall", "position": (5, 0, 1.5), "size": (0.2, 10, 3)},
        {"name": "WestWall", "position": (-5, 0, 1.5), "size": (0.2, 10, 3)}
    ]

    for wall_config in wall_configs:
        wall_path = f"{room_path}/{wall_config['name']}"
        create_box_wall(stage, wall_path, wall_config['position'], wall_config['size'])
```

### Robot Integration with USD

Integrating robots into USD scenes requires understanding the articulation structure:

```python
# Example: Creating a robot with articulation
def create_simple_robot(stage, robot_path):
    """Create a simple wheeled robot using USD"""

    # Create robot root
    robot_root = UsdGeom.Xform.Define(stage, robot_path)

    # Create robot base
    base = UsdGeom.Cylinder.Define(stage, f"{robot_path}/Base")
    base.CreateRadiusAttr(0.3)
    base.CreateHeightAttr(0.2)
    base.AddTranslateOp().Set(Gf.Vec3d(0, 0, 0.1))  # Position above ground

    # Create wheels
    wheel_positions = [
        ("FrontLeftWheel", Gf.Vec3d(0.2, 0.25, 0.1)),
        ("FrontRightWheel", Gf.Vec3d(0.2, -0.25, 0.1)),
        ("BackLeftWheel", Gf.Vec3d(-0.2, 0.25, 0.1)),
        ("BackRightWheel", Gf.Vec3d(-0.2, -0.25, 0.1))
    ]

    for wheel_name, position in wheel_positions:
        wheel = UsdGeom.Cylinder.Define(stage, f"{robot_path}/{wheel_name}")
        wheel.CreateRadiusAttr(0.1)
        wheel.CreateHeightAttr(0.05)
        wheel.AddTranslateOp().Set(position)

        # Add rotation capability (for articulation)
        wheel.AddRotateYOp()

    # Add sensors
    add_camera_to_robot(stage, f"{robot_path}/Camera")
    add_lidar_to_robot(stage, f"{robot_path}/Lidar")

    # Apply materials
    apply_material_to_prim(stage, f"{robot_path}/Base", "RobotBodyMaterial")

    return robot_root

def add_camera_to_robot(stage, camera_path):
    """Add a camera to the robot"""
    camera = UsdGeom.Camera.Define(stage, camera_path)

    # Set camera properties
    camera.CreateFocalLengthAttr(24.0)  # mm
    camera.CreateHorizontalApertureAttr(36.0)  # mm
    camera.CreateVerticalApertureAttr(24.0)  # mm

    # Position camera
    camera.AddTranslateOp().Set(Gf.Vec3d(0.3, 0, 0.2))

def add_lidar_to_robot(stage, lidar_path):
    """Add a LiDAR sensor to the robot (conceptual - actual LiDAR in Isaac Sim)"""
    lidar = UsdGeom.Cone.Define(stage, lidar_path)
    lidar.CreateHeightAttr(0.1)
    lidar.CreateRadiusAttr(0.05)
    lidar.AddTranslateOp().Set(Gf.Vec3d(0, 0, 0.3))
```

## USD Composition Arcs

### Understanding Composition Arcs

USD composition arcs are the mechanisms that combine multiple USD files into a single scene:

- **References**: Include content from another USD file
- **Payloads**: Lazy-loaded references for performance
- **Inherits**: Inherit from a parent prim definition
- **Specializes**: Specialize a prim with modifications

### Using References for Scene Assembly

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

### Using Payloads for Performance

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

## Advanced USD Techniques

### Variants for Scene Configurations

USD variants allow you to create multiple versions of the same asset:

```python
# Example: Using USD variants for different scene configurations
def create_scene_with_variants(stage):
    """Create a scene with variants for different configurations"""

    # Create a prim with variants
    configurable_room = UsdGeom.Xform.Define(stage, "/World/ConfigurableRoom")

    # Create a variant set for room layouts
    layout_variant_set = configurable_room.GetPrim().GetVariantSet("Layout")
    layout_variant_set.SetVariantSelection("Office")

    # Define different layout variants
    with stage.GetEditTarget():
        # Office layout variant
        layout_variant_set.AddVariant("Office")
        with layout_variant_set.GetVariantEditContext("Office", stage.GetEditTarget()):
            # Add office furniture
            office_desk = UsdGeom.Cube.Define(stage, "/World/ConfigurableRoom/Desk")
            office_desk.CreateSizeAttr(1.5)
            office_desk.AddTranslateOp().Set(Gf.Vec3d(0, 0, 0.4))

            office_chair = UsdGeom.Cylinder.Define(stage, "/World/ConfigurableRoom/Chair")
            office_chair.CreateRadiusAttr(0.3)
            office_chair.CreateHeightAttr(0.8)
            office_chair.AddTranslateOp().Set(Gf.Vec3d(0, -0.8, 0.4))

        # Factory layout variant
        layout_variant_set.AddVariant("Factory")
        with layout_variant_set.GetVariantEditContext("Factory", stage.GetEditTarget()):
            # Add factory equipment
            factory_machine = UsdGeom.Cylinder.Define(stage, "/World/ConfigurableRoom/Machine")
            factory_machine.CreateRadiusAttr(0.5)
            factory_machine.CreateHeightAttr(2.0)
            factory_machine.AddTranslateOp().Set(Gf.Vec3d(0, 0, 1.0))

    # Create a variant set for lighting conditions
    lighting_variant_set = configurable_room.GetPrim().GetVariantSet("Lighting")
    lighting_variant_set.SetVariantSelection("Daylight")

    with stage.GetEditTarget():
        lighting_variant_set.AddVariant("Daylight")
        with lighting_variant_set.GetVariantEditContext("Daylight", stage.GetEditTarget()):
            dome_light = UsdLux.DomeLight.Define(stage, "/World/ConfigurableRoom/DayDomeLight")
            dome_light.CreateIntensityAttr(30000)

        lighting_variant_set.AddVariant("Night")
        with lighting_variant_set.GetVariantEditContext("Night", stage.GetEditTarget()):
            night_light = UsdLux.DomeLight.Define(stage, "/World/ConfigurableRoom/NightDomeLight")
            night_light.CreateIntensityAttr(5000)

    return configurable_room

def switch_scene_configuration(room_prim, layout, lighting):
    """Switch scene configuration using variants"""
    layout_variant_set = room_prim.GetPrim().GetVariantSet("Layout")
    layout_variant_set.SetVariantSelection(layout)

    lighting_variant_set = room_prim.GetPrim().GetVariantSet("Lighting")
    lighting_variant_set.SetVariantSelection(lighting)
```

### Material Assignment and Management

```python
# Example: Advanced material management with USD
def create_material_library(stage):
    """Create a library of reusable materials"""

    materials_lib = UsdGeom.Xform.Define(stage, "/World/Materials")

    # Create metallic material
    create_metallic_material(stage, "/World/Materials/MetallicRobot")

    # Create plastic material
    create_plastic_material(stage, "/World/Materials/PlasticParts")

    # Create rubber material
    create_rubber_material(stage, "/World/Materials/RubberWheels")

    # Create glass material
    create_glass_material(stage, "/World/Materials/GlassCamera")

    return materials_lib

def create_metallic_material(stage, material_path):
    """Create a realistic metallic material"""
    material = UsdShade.Material.Define(stage, material_path)

    # Create USD preview surface shader
    shader = UsdShade.Shader.Define(stage, f"{material_path}/PreviewSurface")
    shader.CreateIdAttr("UsdPreviewSurface")

    # Set metallic material properties
    shader.CreateInput("diffuseColor", Usd.Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(0.7, 0.7, 0.7))
    shader.CreateInput("metallic", Usd.Sdf.ValueTypeNames.Float).Set(0.95)
    shader.CreateInput("roughness", Usd.Sdf.ValueTypeNames.Float).Set(0.1)
    shader.CreateInput("specularColor", Usd.Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(1.0, 1.0, 1.0))
    shader.CreateInput("clearcoat", Usd.Sdf.ValueTypeNames.Float).Set(0.8)
    shader.CreateInput("clearcoatRoughness", Usd.Sdf.ValueTypeNames.Float).Set(0.05)

    # Connect shader to material
    surface_output = material.CreateSurfaceOutput()
    surface_input = shader.CreateOutput("surface", Usd.Sdf.ValueTypeNames.Token)
    surface_output.ConnectToSource(surface_input)

def apply_material_to_prim(stage, prim_path, material_path):
    """Apply a material to a prim"""
    prim = stage.GetPrimAtPath(prim_path)
    if not prim:
        return False

    # Get the material
    material = UsdShade.Material(stage.GetPrimAtPath(material_path))
    if not material:
        return False

    # Apply material to prim
    UsdShade.MaterialBindingAPI(prim).Bind(material)

    return True
```

## Isaac Sim Specific USD Extensions

### Physics Properties with USD

Isaac Sim extends USD with physics-specific schemas:

```python
# Example: Adding physics properties to USD prims
from omni.isaac.core.utils.prims import set_targets
from omni.physx.scripts import utils

def add_physics_properties(stage):
    """Add physics properties to USD prims"""

    # Create a physics-enabled object
    box_prim = UsdGeom.Cube.Define(stage, "/World/PhysicsBox")
    box_prim.CreateSizeAttr(0.5)
    box_prim.AddTranslateOp().Set(Gf.Vec3d(2, 0, 0.5))

    # Add physics schema
    from pxr import PhysxSchema

    # Create rigid body properties
    rigid_body_api = PhysxSchema.PhysxRigidBodyAPI.Apply(box_prim.GetPrim())
    rigid_body_api.CreateSleepThresholdAttr(0.1)
    rigid_body_api.CreateStabilizationThresholdAttr(0.1)

    # Add mass and density
    mass_api = PhysxSchema.PhysxMassAPI.Apply(box_prim.GetPrim())
    mass_api.CreateMassAttr(1.0)  # 1kg
    mass_api.CreateDensityAttr(1000.0)  # Water density

    # Add collision properties
    collision_api = PhysxSchema.PhysxCollisionAPI.Apply(box_prim.GetPrim())
    collision_api.CreateContactOffsetAttr(0.001)
    collision_api.CreateRestOffsetAttr(0.0)

    # Create material for physical properties
    physics_material = PhysxSchema.PhysxMaterial.Define(stage, "/World/PhysicsMaterials/Default")
    physics_material.CreateStaticFrictionAttr(0.5)
    physics_material.CreateDynamicFrictionAttr(0.4)
    physics_material.CreateRestitutionAttr(0.2)  # Bounciness

    # Apply physics material
    set_targets(
        prim=collision_api.GetPrim(),
        attribute=collision_api.GetMaterialRel(),
        target_paths=[physics_material.GetPath()]
    )

    return box_prim
```

### Sensor Integration with USD

```python
# Example: Defining sensors using USD schemas
def add_sensors_with_usd(stage, robot_path):
    """Add sensors to robot using USD schemas"""

    # Add RGB camera
    camera_prim = UsdGeom.Camera.Define(stage, f"{robot_path}/Camera")

    # Set camera properties for Isaac Sim
    camera_prim.CreateFocalLengthAttr(24.0)
    camera_prim.CreateHorizontalApertureAttr(36.0)
    camera_prim.CreateVerticalApertureAttr(24.0)
    camera_prim.CreateClippingRangeAttr((0.1, 100.0))

    # Position camera
    camera_prim.AddTranslateOp().Set(Gf.Vec3d(0.1, 0, 0.1))

    # Add IMU sensor (conceptual - actual implementation in Isaac Sim)
    imu_prim = UsdGeom.Xform.Define(stage, f"{robot_path}/Imu")
    imu_prim.AddTranslateOp().Set(Gf.Vec3d(0, 0, 0.05))

    # Add LiDAR (conceptual - actual implementation in Isaac Sim)
    lidar_prim = UsdGeom.Cone.Define(stage, f"{robot_path}/Lidar")
    lidar_prim.CreateHeightAttr(0.05)
    lidar_prim.CreateRadiusAttr(0.05)
    lidar_prim.AddTranslateOp().Set(Gf.Vec3d(0, 0, 0.15))

    return [camera_prim, imu_prim, lidar_prim]
```

## Scene Management and Optimization

### Efficient Scene Loading

```python
# Example: Efficient scene management
class SceneManager:
    def __init__(self, stage):
        self.stage = stage
        self.loaded_scenes = {}
        self.active_prims = set()

    def load_scene_layer(self, scene_path, layer_name):
        """Load a scene layer efficiently"""
        if layer_name in self.loaded_scenes:
            return self.loaded_scenes[layer_name]

        # Load the layer
        layer = Usd.Stage.Load(self.stage.GetPrimAtPath(scene_path))
        self.loaded_scenes[layer_name] = layer

        return layer

    def activate_prims_in_range(self, center, radius):
        """Activate only prims within a certain range for performance"""
        all_prims = self.stage.TraverseAll()

        for prim in all_prims:
            if prim.IsA(UsdGeom.Xform):
                # Get prim position
                xform = UsdGeom.Xform(prim)
                transform_ops = xform.GetOrderedXformOps()

                # Calculate distance to center (simplified)
                # In practice, you'd extract the actual position

                # For now, just a conceptual approach
                should_activate = True  # Placeholder logic

                if should_activate:
                    self.active_prims.add(prim.GetPath())
                    # Enable prim for simulation
                    prim.SetActive(True)
                else:
                    prim.SetActive(False)

    def create_scene_template(self, template_name):
        """Create a reusable scene template"""
        template_prim = UsdGeom.Xform.Define(self.stage, f"/Templates/{template_name}")

        # Add common elements to template
        self.add_common_lighting(template_prim)
        self.add_common_materials(template_prim)

        return template_prim

    def instantiate_scene_from_template(self, template_name, instance_name, position):
        """Instantiate a scene from a template"""
        # Create instance
        instance_prim = UsdGeom.Xform.Define(self.stage, f"/World/{instance_name}")
        instance_prim.AddTranslateOp().Set(Gf.Vec3d(*position))

        # Reference the template (in a real implementation)
        # This would involve more complex USD composition

        return instance_prim

    def add_common_lighting(self, parent_prim):
        """Add common lighting setup to a prim container"""
        # Add dome light
        dome_light = UsdLux.DomeLight.Define(self.stage, f"{parent_prim.GetPath()}/DomeLight")
        dome_light.CreateIntensityAttr(30000)
        dome_light.CreateColorAttr(Gf.Vec3f(1.0, 1.0, 1.0))

    def add_common_materials(self, parent_prim):
        """Add common materials to a prim container"""
        # Create common materials
        floor_material = UsdShade.Material.Define(self.stage, f"{parent_prim.GetPath()}/Materials/Floor")
        wall_material = UsdShade.Material.Define(self.stage, f"{parent_prim.GetPath()}/Materials/Wall")

        # Define material properties (simplified)
        self.create_basic_material(floor_material, Gf.Vec3f(0.8, 0.8, 0.8))
        self.create_basic_material(wall_material, Gf.Vec3f(0.7, 0.7, 0.7))

    def create_basic_material(self, material, color):
        """Create a basic material with a color"""
        shader = UsdShade.Shader.Define(self.stage, f"{material.GetPath()}/PreviewSurface")
        shader.CreateIdAttr("UsdPreviewSurface")
        shader.CreateInput("diffuseColor", Usd.Sdf.ValueTypeNames.Color3f).Set(color)

        surface_output = material.CreateSurfaceOutput()
        surface_input = shader.CreateOutput("surface", Usd.Sdf.ValueTypeNames.Token)
        surface_output.ConnectToSource(surface_input)
```

## Best Practices for USD Scene Composition

### Organization and Structure

```python
# Best practices for organizing USD scenes
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
        if prim_name != prim_name.replace(' ', '_'):  # Has spaces
            issues.append(f"Prim {prim.GetPath()} contains spaces in name")

    return issues
```

### Scene Validation

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
        if prim.IsA(UsdLux.DomeLight) or prim.IsA(UsdLux.DistantLight) or prim.IsA(UsdLux.SphereLight):
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
```

## Troubleshooting Common Issues

### USD Composition Issues

```python
# Common USD troubleshooting
USD_TROUBLESHOOTING = {
    "reference_not_loading": {
        "cause": "Incorrect file path or missing USD file",
        "solution": "Verify file paths are correct and files exist"
    },
    "material_not_applying": {
        "cause": "Material binding issue or incorrect shader connections",
        "solution": "Check material paths and ensure proper surface connections"
    },
    "physics_not_working": {
        "cause": "Missing physics schemas or incorrect mass properties",
        "solution": "Verify PhysxSchema is applied and mass is properly set"
    },
    "performance_issues": {
        "cause": "Too many complex objects or inefficient scene structure",
        "solution": "Use payloads, instancing, and optimize geometry"
    }
}

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
            if prim.IsA(UsdGeom.Mesh) or prim.IsA(UsdGeom.Cube) or prim.IsA(UsdGeom.Sphere):
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