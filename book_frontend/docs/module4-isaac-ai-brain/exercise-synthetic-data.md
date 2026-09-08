---
title: Practical Exercise - Synthetic Data Generation
sidebar_label: Exercise - Synthetic Data Generation
sidebar_position: 7
description: Hands-on exercise to generate synthetic datasets for AI training using Isaac Sim
tags: [exercise, synthetic-data, ai-training, isaac-sim, computer-vision, robotics]
---

# Practical Exercise: Synthetic Data Generation

## Exercise Overview

In this exercise, you will create a complete synthetic data generation pipeline using Isaac Sim. You'll set up a scene with objects, configure sensors, implement domain randomization techniques, and generate a dataset suitable for training a computer vision model.

### Learning Objectives
By completing this exercise, you will be able to:
- Configure a scene for synthetic data generation in Isaac Sim
- Implement domain randomization techniques
- Set up and configure sensors for data capture
- Generate and validate synthetic datasets
- Export datasets in standard formats for AI training

### Prerequisites
- Basic understanding of Isaac Sim and USD scene composition
- Python programming experience
- Understanding of computer vision concepts
- Completed previous Isaac Sim modules

## Exercise Setup

### Required Assets
- Isaac Sim installation with Python API
- Basic robot or camera platform
- Object models for scene
- Understanding of camera and sensor concepts

### Initial Configuration
1. Launch Isaac Sim with the Python API enabled
2. Create a new, empty stage
3. Prepare your working directory for dataset output

## Part 1: Scene Configuration

### Task 1.1: Create Basic Environment
Create a simple environment with a ground plane and basic lighting.

**Implementation Steps:**
1. Create a USD stage with proper units
2. Add a ground plane at the origin
3. Configure dome lighting for the environment
4. Add a few basic objects to the scene

**Sample Code:**
```python
import omni
from pxr import Usd, UsdGeom, UsdLux, Gf
from omni.isaac.core import World
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.core.utils.prims import create_prim
import numpy as np

# Get the current stage
stage = omni.usd.get_context().get_stage()

# Create the world root
world_prim = UsdGeom.Xform.Define(stage, "/World")

# Create ground plane
ground_plane = UsdGeom.Mesh.Define(stage, "/World/GroundPlane")
# Define simple plane geometry (simplified for brevity)
points = [
    Gf.Vec3f(-5, -5, 0), Gf.Vec3f(5, -5, 0),
    Gf.Vec3f(5, 5, 0), Gf.Vec3f(-5, 5, 0)
]
ground_plane.CreatePointsAttr(points)

# Create dome light
dome_light = UsdLux.DomeLight.Define(stage, "/World/DomeLight")
dome_light.CreateIntensityAttr(30000)
dome_light.CreateColorAttr(Gf.Vec3f(1.0, 1.0, 1.0))

print("Basic environment created successfully")
```

### Task 1.2: Add Objects for Data Generation
Add various objects that will be used for training data generation.

**Implementation Steps:**
1. Create multiple objects with different shapes and colors
2. Position objects in a semi-random pattern
3. Apply different materials to objects
4. Ensure objects don't intersect with each other

**Sample Code:**
```python
# Define object properties
object_configs = [
    {"name": "Cube1", "type": "Cube", "position": [1, 0, 0.5], "color": [1.0, 0.0, 0.0]},
    {"name": "Sphere1", "type": "Sphere", "position": [-1, 1, 0.5], "color": [0.0, 1.0, 0.0]},
    {"name": "Cylinder1", "type": "Cylinder", "position": [0, -1, 0.5], "color": [0.0, 0.0, 1.0]},
    {"name": "Cube2", "type": "Cube", "position": [1.5, -1.5, 0.5], "color": [1.0, 1.0, 0.0]},
    {"name": "Sphere2", "type": "Sphere", "position": [-1.5, 1.5, 0.5], "color": [1.0, 0.0, 1.0]}
]

def create_colored_object(stage, config):
    """Create an object with specific color material"""
    import omni.kit.commands
    from pxr import UsdShade

    # Create the geometry
    if config["type"] == "Cube":
        prim = UsdGeom.Cube.Define(stage, f"/World/Objects/{config['name']}")
        prim.CreateSizeAttr(0.5)
    elif config["type"] == "Sphere":
        prim = UsdGeom.Sphere.Define(stage, f"/World/Objects/{config['name']}")
        prim.CreateRadiusAttr(0.25)
    elif config["type"] == "Cylinder":
        prim = UsdGeom.Cylinder.Define(stage, f"/World/Objects/{config['name']}")
        prim.CreateRadiusAttr(0.25)
        prim.CreateHeightAttr(0.5)

    # Set position
    prim.AddTranslateOp().Set(Gf.Vec3d(*config["position"]))

    # Create and apply colored material
    material_path = f"/World/Materials/{config['name']}_Material"
    create_colored_material(stage, material_path, config["color"])

    # Apply material to prim
    from omni.isaac.core.utils.materials import set_material
    # Note: This is conceptual; actual material application in Isaac Sim
    # would use USD Shade APIs as shown in previous examples

def create_colored_material(stage, material_path, color):
    """Create a colored material using USD Shade"""
    from pxr import UsdShade

    material = UsdShade.Material.Define(stage, material_path)
    shader = UsdShade.Shader.Define(stage, f"{material_path}/PreviewSurface")
    shader.CreateIdAttr("UsdPreviewSurface")
    shader.CreateInput("diffuseColor", Usd.Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(*color))
    shader.CreateInput("metallic", Usd.Sdf.ValueTypeNames.Float).Set(0.0)
    shader.CreateInput("roughness", Usd.Sdf.ValueTypeNames.Float).Set(0.5)

    surface_output = material.CreateSurfaceOutput()
    surface_input = shader.CreateOutput("surface", Usd.Sdf.ValueTypeNames.Token)
    surface_output.ConnectToSource(surface_input)

# Create all objects
for config in object_configs:
    create_colored_object(stage, config)

print(f"Created {len(object_configs)} objects for synthetic data generation")
```

## Part 2: Domain Randomization Implementation

### Task 2.1: Implement Lighting Randomization
Create a system that randomizes lighting conditions for each data sample.

**Implementation Steps:**
1. Create a function to randomize dome light properties
2. Add random point lights to the scene
3. Implement color temperature variation
4. Add shadows and reflections with randomization

**Sample Code:**
```python
import random

class LightingRandomizer:
    def __init__(self, stage):
        self.stage = stage
        self.light_count = 0

    def randomize_lighting(self):
        """Randomize the lighting in the scene"""
        # Randomize dome light
        dome_light = self.stage.GetPrimAtPath("/World/DomeLight")
        if dome_light:
            # Randomize intensity (between 10000 and 50000)
            intensity = random.uniform(10000, 50000)
            dome_light.GetAttribute("inputs:intensity").Set(intensity)

            # Randomize color (warm to cool daylight)
            color_temp = random.uniform(3000, 8000)
            rgb_color = self.color_temperature_to_rgb(color_temp)
            dome_light.GetAttribute("inputs:color").Set(Gf.Vec3f(*rgb_color))

        # Remove existing random lights
        self.remove_random_lights()

        # Add 1-3 random point lights
        num_lights = random.randint(1, 3)
        for i in range(num_lights):
            self.add_random_light(i)

    def add_random_light(self, light_id):
        """Add a random light to the scene"""
        from pxr import UsdLux

        light_path = f"/World/RandomLights/Light_{light_id}"
        point_light = UsdLux.SphereLight.Define(self.stage, light_path)

        # Random position (above objects)
        x = random.uniform(-3, 3)
        y = random.uniform(-3, 3)
        z = random.uniform(2, 5)
        point_light.AddTranslateOp().Set(Gf.Vec3d(x, y, z))

        # Random properties
        intensity = random.uniform(1000, 5000)
        point_light.CreateIntensityAttr(intensity)

        color = self.random_color()
        point_light.CreateColorAttr(Gf.Vec3f(*color))

        self.light_count += 1

    def remove_random_lights(self):
        """Remove all random lights from the scene"""
        # In practice, you'd iterate through and remove all random lights
        # For this exercise, we'll just reset the counter
        self.light_count = 0

    def color_temperature_to_rgb(self, temp):
        """Convert color temperature to RGB approximation"""
        temp = temp / 100

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

    def random_color(self):
        """Generate a random RGB color"""
        return [random.random(), random.random(), random.random()]

# Initialize lighting randomizer
lighting_randomizer = LightingRandomizer(stage)

# Test lighting randomization
lighting_randomizer.randomize_lighting()
print("Lighting randomization applied")
```

### Task 2.2: Implement Material and Texture Randomization
Create a system to randomize materials and textures for domain randomization.

**Implementation Steps:**
1. Create a material library with various properties
2. Implement randomization of albedo, roughness, and metallic properties
3. Add texture variation capabilities
4. Ensure physically plausible material combinations

**Sample Code:**
```python
class MaterialRandomizer:
    def __init__(self, stage):
        self.stage = stage
        self.material_library = self.create_material_library()

    def create_material_library(self):
        """Create a library of different material types"""
        materials = {
            "plastic": {"base_color_range": [(0.1, 0.1, 0.1), (1.0, 1.0, 1.0)],
                       "roughness_range": (0.1, 0.9), "metallic_range": (0.0, 0.05)},
            "metal": {"base_color_range": [(0.5, 0.5, 0.5), (1.0, 1.0, 1.0)],
                     "roughness_range": (0.0, 0.5), "metallic_range": (0.8, 1.0)},
            "fabric": {"base_color_range": [(0.2, 0.1, 0.1), (0.9, 0.9, 0.8)],
                      "roughness_range": (0.5, 0.9), "metallic_range": (0.0, 0.1)},
            "glass": {"base_color_range": [(0.7, 0.8, 0.9), (0.9, 0.95, 1.0)],
                     "roughness_range": (0.0, 0.2), "metallic_range": (0.0, 0.1)}
        }
        return materials

    def randomize_materials(self, object_paths):
        """Randomize materials for specified objects"""
        for obj_path in object_paths:
            # Choose a random material type
            material_type = random.choice(list(self.material_library.keys()))
            material_props = self.material_library[material_type]

            # Generate random material properties
            albedo = self.random_color_in_range(material_props["base_color_range"])
            roughness = random.uniform(*material_props["roughness_range"])
            metallic = random.uniform(*material_props["metallic_range"])

            # Apply material to object (conceptual)
            self.apply_material_to_object(obj_path, albedo, roughness, metallic)

    def random_color_in_range(self, color_range):
        """Generate a random color within specified range"""
        min_color, max_color = color_range
        return [
            random.uniform(min_color[i], max_color[i]) for i in range(3)
        ]

    def apply_material_to_object(self, obj_path, albedo, roughness, metallic):
        """Apply material properties to an object"""
        # In a real implementation, this would create and apply USD materials
        # For this exercise, we'll just print what would be applied
        print(f"Applying material to {obj_path}:")
        print(f"  Albedo: {albedo}")
        print(f"  Roughness: {roughness}")
        print(f"  Metallic: {metallic}")

    def create_random_material(self, material_name, albedo, roughness, metallic):
        """Create a USD material with specified properties"""
        from pxr import UsdShade

        material_path = f"/World/Materials/{material_name}"
        material = UsdShade.Material.Define(self.stage, material_path)

        shader = UsdShade.Shader.Define(self.stage, f"{material_path}/PreviewSurface")
        shader.CreateIdAttr("UsdPreviewSurface")

        # Set material properties
        shader.CreateInput("diffuseColor", Usd.Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(*albedo))
        shader.CreateInput("roughness", Usd.Sdf.ValueTypeNames.Float).Set(roughness)
        shader.CreateInput("metallic", Usd.Sdf.ValueTypeNames.Float).Set(metallic)
        shader.CreateInput("specularColor", Usd.Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(1.0, 1.0, 1.0))

        # Connect shader to material
        surface_output = material.CreateSurfaceOutput()
        surface_input = shader.CreateOutput("surface", Usd.Sdf.ValueTypeNames.Token)
        surface_output.ConnectToSource(surface_input)

        return material

# Initialize material randomizer
material_randomizer = MaterialRandomizer(stage)

# Get all object paths
object_paths = [f"/World/Objects/{config['name']}" for config in object_configs]

# Randomize materials for all objects
material_randomizer.randomize_materials(object_paths)
print("Material randomization applied to all objects")
```

## Part 3: Sensor Configuration and Data Capture

### Task 3.1: Set Up Camera and Sensors
Configure cameras and sensors for data capture.

**Implementation Steps:**
1. Create a camera with appropriate parameters
2. Configure the camera for RGB and depth capture
3. Set up semantic segmentation capabilities
4. Position the camera for optimal data capture

**Sample Code:**
```python
from omni.isaac.sensor import Camera
import numpy as np

class SensorSetup:
    def __init__(self, world):
        self.world = world
        self.cameras = {}

    def setup_camera(self, prim_path, name, resolution=(640, 480)):
        """Set up a camera for data capture"""
        camera = Camera(
            prim_path=prim_path,
            frequency=30,
            resolution=resolution
        )

        # Configure camera intrinsic parameters
        camera.get_sensor().set_parameter("focal_length", 24.0)  # mm
        camera.get_sensor().set_parameter("horizontal_aperture", 36.0)  # mm
        camera.get_sensor().set_parameter("vertical_aperture", 24.0)  # mm

        self.cameras[name] = camera
        return camera

    def setup_robot_camera(self, robot_prim_path, camera_name="sensor",
                          position=[0.3, 0, 0.2], resolution=(640, 480)):
        """Set up a camera attached to a robot"""
        camera_path = f"{robot_prim_path}/{camera_name}"

        # Create camera prim first
        from pxr import UsdGeom
        camera_prim = UsdGeom.Camera.Define(self.world.stage, camera_path)

        # Add transform
        camera_prim.AddTranslateOp().Set(Gf.Vec3d(*position))

        # Create Isaac Sim camera
        camera = Camera(
            prim_path=camera_path,
            frequency=30,
            resolution=resolution
        )

        self.cameras[camera_name] = camera
        return camera

# Create a simple robot platform for the camera
robot_prim = UsdGeom.Xform.Define(stage, "/World/Robot")
robot_prim.AddTranslateOp().Set(Gf.Vec3d(0, 0, 1.0))  # Position above ground

# Initialize sensor setup
world = World(stage_units_in_meters=1.0)
sensor_setup = SensorSetup(world)

# Set up the main camera
main_camera = sensor_setup.setup_robot_camera("/World/Robot", "main_camera",
                                            position=[0.3, 0, 0.2], resolution=(640, 480))

print("Camera setup completed")
```

### Task 3.2: Implement Data Capture Pipeline
Create a pipeline to capture RGB, depth, and segmentation data.

**Implementation Steps:**
1. Create a data capture function that gets sensor data
2. Implement data validation and quality checks
3. Add realistic sensor noise simulation
4. Store captured data with proper metadata

**Sample Code:**
```python
import os
import json
from PIL import Image
import cv2

class DataCapturePipeline:
    def __init__(self, camera, output_dir="synthetic_dataset"):
        self.camera = camera
        self.output_dir = output_dir
        self.sample_counter = 0

        # Create output directories
        os.makedirs(os.path.join(output_dir, "rgb"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "depth"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "segmentation"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "metadata"), exist_ok=True)

    def capture_sample(self):
        """Capture a complete data sample"""
        # Capture RGB image
        rgb_data = self.camera.get_rgb_data()

        # Capture depth data
        depth_data = self.camera.get_distance_to_camera_data()

        # Capture semantic segmentation
        segmentation_data = self.camera.get_semantic_segmentation()

        # Add realistic noise to data
        rgb_data = self.add_camera_noise(rgb_data)
        depth_data = self.add_depth_noise(depth_data)

        # Validate data quality
        if not self.validate_data_quality(rgb_data, depth_data, segmentation_data):
            print("Data quality check failed, skipping sample")
            return None

        # Save the sample
        sample_id = self.save_sample(rgb_data, depth_data, segmentation_data)

        # Update counter
        self.sample_counter += 1

        return sample_id

    def add_camera_noise(self, image):
        """Add realistic camera noise to RGB image"""
        # Add shot noise (proportional to signal)
        shot_noise = np.random.poisson(image * 255) / 255.0
        shot_noise = (shot_noise - image) * 0.02  # Scale factor

        # Add read noise (constant)
        read_noise = np.random.normal(0, 0.01, image.shape)

        noisy_image = np.clip(image + shot_noise + read_noise, 0, 1)
        return noisy_image

    def add_depth_noise(self, depth_data):
        """Add realistic depth sensor noise"""
        # Depth noise typically increases with distance
        distance_based_noise = 0.001 + 0.005 * depth_data + 0.002 * depth_data**2
        noise = np.random.normal(0, distance_based_noise, depth_data.shape)
        noisy_depth = depth_data + noise
        return np.clip(noisy_depth, 0.01, 100.0)  # Clamp to reasonable range

    def validate_data_quality(self, rgb, depth, segmentation):
        """Validate the quality of captured data"""
        # Check if RGB image has reasonable brightness
        mean_brightness = np.mean(rgb)
        if mean_brightness < 0.05 or mean_brightness > 0.95:
            return False  # Too dark or too bright

        # Check if depth has reasonable range
        valid_depth_mask = (depth > 0.1) & (depth < 10.0)  # 10cm to 10m range
        valid_ratio = np.sum(valid_depth_mask) / depth.size
        if valid_ratio < 0.5:  # Less than 50% of pixels in valid range
            return False

        # All checks passed
        return True

    def save_sample(self, rgb, depth, segmentation):
        """Save a complete data sample"""
        sample_id = f"sample_{self.sample_counter:06d}"

        # Save RGB image
        rgb_path = os.path.join(self.output_dir, "rgb", f"{sample_id}.png")
        rgb_image = (rgb * 255).astype(np.uint8)
        Image.fromarray(rgb_image).save(rgb_path)

        # Save depth data
        depth_path = os.path.join(self.output_dir, "depth", f"{sample_id}.npy")
        np.save(depth_path, depth)

        # Save segmentation
        seg_path = os.path.join(self.output_dir, "segmentation", f"{sample_id}.png")
        seg_image = (segmentation * 255).astype(np.uint8)
        Image.fromarray(seg_image).save(seg_path)

        # Save metadata
        metadata = {
            "sample_id": sample_id,
            "timestamp": self.sample_counter,  # Simplified timestamp
            "rgb_shape": rgb.shape,
            "depth_shape": depth.shape,
            "segmentation_shape": segmentation.shape,
            "rgb_mean_brightness": float(np.mean(rgb)),
            "depth_valid_ratio": float(np.sum((depth > 0.1) & (depth < 10.0)) / depth.size)
        }

        meta_path = os.path.join(self.output_dir, "metadata", f"{sample_id}.json")
        with open(meta_path, 'w') as f:
            json.dump(metadata, f, indent=2)

        return sample_id

# Initialize data capture pipeline
data_pipeline = DataCapturePipeline(main_camera)

print("Data capture pipeline initialized")
```

## Part 4: Complete Data Generation Loop

### Task 4.1: Implement the Complete Generation Loop
Combine all components into a complete data generation loop.

**Implementation Steps:**
1. Create a loop that randomizes scene
2. Capture data from sensors
3. Apply domain randomization between samples
4. Track and validate generated data

**Sample Code:**
```python
import time

def generate_synthetic_dataset(num_samples=100, output_dir="synthetic_dataset"):
    """Generate a complete synthetic dataset"""
    print(f"Starting synthetic dataset generation: {num_samples} samples")

    # Initialize the world
    world = World(stage_units_in_meters=1.0)
    world.reset()

    # Set up sensors
    sensor_setup = SensorSetup(world)
    camera = sensor_setup.setup_robot_camera("/World/Robot", "main_camera",
                                           position=[0.3, 0, 0.2], resolution=(640, 480))

    # Initialize data pipeline
    data_pipeline = DataCapturePipeline(camera, output_dir)

    # Initialize randomizers
    lighting_randomizer = LightingRandomizer(stage)
    material_randomizer = MaterialRandomizer(stage)
    object_paths = [f"/World/Objects/{config['name']}" for config in object_configs]

    success_count = 0
    start_time = time.time()

    for sample_idx in range(num_samples):
        print(f"Generating sample {sample_idx + 1}/{num_samples}")

        # Randomize the scene
        lighting_randomizer.randomize_lighting()
        material_randomizer.randomize_materials(object_paths)

        # Randomize object positions slightly
        for obj_config in object_configs:
            obj_prim = stage.GetPrimAtPath(f"/World/Objects/{obj_config['name']}")
            if obj_prim:
                # Add small random offset to position
                current_pos = obj_config["position"]
                new_x = current_pos[0] + random.uniform(-0.2, 0.2)
                new_y = current_pos[1] + random.uniform(-0.2, 0.2)
                new_pos = [new_x, new_y, current_pos[2]]  # Keep Z the same

                # Apply new position
                xform = UsdGeom.Xformable(obj_prim)
                xform.ClearXformOpOrder()
                xform.AddTranslateOp().Set(Gf.Vec3d(*new_pos))

        # Step the simulation to apply changes
        world.reset()
        for step in range(5):  # Run for a few steps to stabilize
            world.step(render=True)

        # Capture the data sample
        sample_id = data_pipeline.capture_sample()

        if sample_id:
            success_count += 1
            print(f"  ✓ Sample {sample_id} captured successfully")
        else:
            print(f"  ✗ Sample {sample_idx + 1} failed quality check")

    end_time = time.time()
    total_time = end_time - start_time

    print(f"\nDataset generation completed!")
    print(f"  Total samples requested: {num_samples}")
    print(f"  Successful samples: {success_count}")
    print(f"  Failed samples: {num_samples - success_count}")
    print(f"  Success rate: {success_count/num_samples*100:.2f}%")
    print(f"  Total time: {total_time:.2f} seconds")
    print(f"  Average time per sample: {total_time/num_samples:.2f} seconds")
    print(f"  Output directory: {output_dir}")

    return {
        "total_requested": num_samples,
        "successful": success_count,
        "failed": num_samples - success_count,
        "success_rate": success_count/num_samples,
        "total_time": total_time,
        "output_dir": output_dir
    }

# Run the dataset generation (with a smaller number for the exercise)
results = generate_synthetic_dataset(num_samples=10, output_dir="exercise_dataset")

print("\nDataset generation results:")
for key, value in results.items():
    print(f"  {key}: {value}")
```

### Task 4.2: Validate Generated Dataset
Create validation tools to check the quality of generated data.

**Implementation Steps:**
1. Create statistics about the generated dataset
2. Validate file integrity and format
3. Check for diversity in the dataset
4. Generate quality reports

**Sample Code:**
```python
import os
import numpy as np
from PIL import Image
import json
from collections import Counter

class DatasetValidator:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.stats = {}

    def validate_dataset(self):
        """Validate the entire dataset"""
        print("Validating generated dataset...")

        # Check directory structure
        required_dirs = ["rgb", "depth", "segmentation", "metadata"]
        for dir_name in required_dirs:
            dir_path = os.path.join(self.dataset_path, dir_name)
            if not os.path.exists(dir_path):
                print(f"  ✗ Missing directory: {dir_name}")
                return False
            else:
                print(f"  ✓ Directory exists: {dir_name}")

        # Count files
        rgb_files = [f for f in os.listdir(os.path.join(self.dataset_path, "rgb"))
                     if f.endswith('.png')]
        depth_files = [f for f in os.listdir(os.path.join(self.dataset_path, "depth"))
                       if f.endswith('.npy')]
        seg_files = [f for f in os.listdir(os.path.join(self.dataset_path, "segmentation"))
                     if f.endswith('.png')]
        meta_files = [f for f in os.listdir(os.path.join(self.dataset_path, "metadata"))
                      if f.endswith('.json')]

        print(f"  RGB images: {len(rgb_files)}")
        print(f"  Depth maps: {len(depth_files)}")
        print(f"  Segmentation: {len(seg_files)}")
        print(f"  Metadata: {len(meta_files)}")

        # Validate file consistency
        base_names_rgb = {f.split('.')[0] for f in rgb_files}
        base_names_depth = {f.split('.')[0] for f in depth_files}
        base_names_seg = {f.split('.')[0] for f in seg_files}
        base_names_meta = {f.split('.')[0] for f in meta_files}

        if base_names_rgb == base_names_depth == base_names_seg == base_names_meta:
            print("  ✓ All file types have consistent naming")
        else:
            print("  ✗ Inconsistent file naming detected")
            return False

        # Validate individual files
        sample_stats = self.analyze_sample_quality()

        # Generate summary
        self.stats = {
            "total_samples": len(base_names_rgb),
            "sample_stats": sample_stats,
            "directory_integrity": True
        }

        print("  ✓ Dataset validation completed successfully")
        return True

    def analyze_sample_quality(self):
        """Analyze quality metrics for samples"""
        rgb_dir = os.path.join(self.dataset_path, "rgb")
        meta_dir = os.path.join(self.dataset_path, "metadata")

        brightness_values = []
        file_sizes = []

        for meta_file in os.listdir(meta_dir):
            if meta_file.endswith('.json'):
                meta_path = os.path.join(meta_dir, meta_file)
                with open(meta_path, 'r') as f:
                    meta_data = json.load(f)

                brightness_values.append(meta_data.get("rgb_mean_brightness", 0))
                rgb_file = meta_file.replace('.json', '.png')
                rgb_path = os.path.join(rgb_dir, rgb_file)
                if os.path.exists(rgb_path):
                    file_sizes.append(os.path.getsize(rgb_path))

        if brightness_values:
            avg_brightness = np.mean(brightness_values)
            brightness_std = np.std(brightness_values)

            print(f"  Average brightness: {avg_brightness:.3f}")
            print(f"  Brightness std dev: {brightness_std:.3f}")
            print(f"  Brightness range: {np.min(brightness_values):.3f} - {np.max(brightness_values):.3f}")

        return {
            "avg_brightness": np.mean(brightness_values) if brightness_values else 0,
            "brightness_std": np.std(brightness_values) if brightness_values else 0,
            "brightness_range": (np.min(brightness_values) if brightness_values else 0,
                               np.max(brightness_values) if brightness_values else 0)
        }

    def generate_report(self):
        """Generate a validation report"""
        if not self.stats:
            print("No validation data available. Run validate_dataset() first.")
            return

        report = f"""
Synthetic Dataset Validation Report
===================================

Total Samples: {self.stats['total_samples']}
Directory Integrity: {'✓' if self.stats.get('directory_integrity', False) else '✗'}

Quality Metrics:
- Average Brightness: {self.stats['sample_stats']['avg_brightness']:.3f}
- Brightness Std Dev: {self.stats['sample_stats']['brightness_std']:.3f}
- Brightness Range: {self.stats['sample_stats']['brightness_range'][0]:.3f} - {self.stats['sample_stats']['brightness_range'][1]:.3f}

Dataset Quality: {'High' if self.stats['sample_stats']['brightness_std'] > 0.1 else 'Low'}
(Indicates good diversity if std dev > 0.1)
        """

        print(report)

        # Save report
        report_path = os.path.join(self.dataset_path, "validation_report.txt")
        with open(report_path, 'w') as f:
            f.write(report)

        print(f"Validation report saved to: {report_path}")

# Validate the generated dataset
validator = DatasetValidator("exercise_dataset")
is_valid = validator.validate_dataset()

if is_valid:
    validator.generate_report()
    print("\n✓ Dataset validation completed successfully!")
else:
    print("\n✗ Dataset validation failed!")
```

## Part 5: Enhancement Challenges

### Challenge 1: Advanced Domain Randomization
Implement additional domain randomization techniques such as weather effects, occlusion, or dynamic objects.

### Challenge 2: Multi-Camera Setup
Extend the system to use multiple cameras for stereo vision or multi-view training data.

### Challenge 3: Annotation Generation
Create more sophisticated annotation formats like COCO or YOLO for specific computer vision tasks.

## Assessment Criteria

Your synthetic data generation implementation will be evaluated on:
- **Completeness**: All required components implemented
- **Quality**: Generated data meets standards for AI training
- **Diversity**: Effective domain randomization techniques
- **Efficiency**: Reasonable performance for data generation
- **Validation**: Proper dataset validation and quality assessment

## Conclusion

This exercise provided hands-on experience with synthetic data generation using Isaac Sim. You've learned to:
- Configure scenes for data generation
- Implement domain randomization techniques
- Set up sensor pipelines for multi-modal data capture
- Validate and assess generated datasets

The skills developed in this exercise are directly applicable to real-world AI training scenarios where synthetic data can significantly reduce the cost and time required for data collection while providing perfect ground truth annotations.