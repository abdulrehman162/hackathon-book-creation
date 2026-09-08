---
title: Synthetic Data Generation with Isaac Sim
sidebar_label: Synthetic Data Generation
sidebar_position: 3
description: Techniques for generating high-quality synthetic data for AI training using Isaac Sim
tags: [isaac-sim, synthetic-data, ai-training, domain-randomization, data-augmentation, computer-vision]
---

# Synthetic Data Generation with Isaac Sim

## Introduction to Synthetic Data

Synthetic data generation is a cornerstone of modern AI development, particularly in robotics where real-world data collection can be expensive, time-consuming, and sometimes dangerous. Isaac Sim provides powerful tools to generate high-quality synthetic datasets that can rival real-world data for training AI models, with the added benefits of perfect ground truth annotations and controlled experimental conditions.

### Benefits of Synthetic Data

1. **Cost-Effective**: Generate unlimited data without physical hardware
2. **Perfect Annotations**: Automatic ground truth for all objects and properties
3. **Controlled Conditions**: Test edge cases safely and repeatably
4. **Scalability**: Generate large datasets quickly and consistently
5. **Diversity**: Create diverse scenarios that might be rare in reality
6. **Safety**: Test dangerous scenarios without risk to hardware or humans

### Applications in Robotics

- **Perception Training**: Object detection, segmentation, and classification
- **Navigation**: Training for obstacle avoidance and path planning
- **Manipulation**: Grasping and manipulation skill learning
- **Simulation-to-Reality Transfer**: Bridging the reality gap
- **Edge Case Testing**: Rare scenarios that are difficult to encounter in reality

## Synthetic Data Pipeline Architecture

### Core Components

The synthetic data generation pipeline in Isaac Sim consists of several interconnected components:

1. **Scene Generator**: Creates and randomizes simulation environments
2. **Sensor Simulator**: Generates realistic sensor outputs
3. **Annotation Engine**: Creates ground truth labels
4. **Data Exporter**: Formats data for AI training frameworks
5. **Quality Assurance**: Validates synthetic data quality

### Data Generation Workflow

```python
# Example synthetic data generation workflow
def synthetic_data_pipeline():
    # 1. Initialize simulation environment
    world = initialize_simulation()

    # 2. Randomize scene parameters
    scene_config = randomize_scene_parameters()

    # 3. Configure sensors
    sensors = setup_sensors(world)

    # 4. Run simulation and capture data
    for frame in range(num_frames):
        world.step(render=True)
        sensor_data = capture_sensor_data(sensors)
        annotations = generate_annotations(sensor_data)

        # 5. Validate and store data
        if validate_data_quality(sensor_data, annotations):
            store_data(sensor_data, annotations)

    # 6. Export dataset
    export_dataset()
```

## Domain Randomization Techniques

### Concept and Benefits

Domain randomization is a technique where simulation parameters are randomized to increase the diversity of synthetic data and improve the transfer of models from simulation to reality:

- **Lighting Randomization**: Varying illumination conditions
- **Material Randomization**: Changing surface appearances
- **Geometry Randomization**: Modifying object shapes and positions
- **Camera Parameter Randomization**: Varying intrinsic and extrinsic parameters

### Implementation Example

```python
# Domain randomization implementation
import random
import numpy as np

class DomainRandomizer:
    def __init__(self):
        self.lighting_params = {
            'intensity_range': (10000, 50000),
            'color_temperature_range': (3000, 8000),
            'direction_range': ((-1, -1, -1), (1, 1, 1))
        }

        self.material_params = {
            'albedo_range': ((0.1, 0.1, 0.1), (1.0, 1.0, 1.0)),
            'roughness_range': (0.05, 0.95),
            'metallic_range': (0.0, 0.8)
        }

    def randomize_lighting(self, stage):
        """Randomize lighting conditions in the scene"""
        # Randomize dome light
        dome_light = stage.GetPrimAtPath("/World/DomeLight")
        if dome_light:
            intensity = random.uniform(*self.lighting_params['intensity_range'])
            dome_light.GetAttribute("inputs:intensity").Set(intensity)

            # Randomize color temperature (converted to RGB approximation)
            color_temp = random.uniform(*self.lighting_params['color_temperature_range'])
            rgb_color = self.color_temperature_to_rgb(color_temp)
            dome_light.GetAttribute("inputs:color").Set(rgb_color)

        # Add random directional lights
        for i in range(random.randint(1, 3)):
            light_name = f"/World/RandomLight_{i}"
            create_prim(prim_path=light_name, prim_type="DistantLight")

            light_prim = stage.GetPrimAtPath(light_name)
            light_prim.GetAttribute("inputs:intensity").Set(random.uniform(1000, 5000))

            # Random direction
            direction = [
                random.uniform(*self.lighting_params['direction_range'][j][0:1]) if j == 0
                else random.uniform(*self.lighting_params['direction_range'][j])
                for j in range(3)
            ]
            # Set light direction (simplified approach)

    def randomize_materials(self, stage, material_paths):
        """Randomize material properties"""
        for mat_path in material_paths:
            material = stage.GetPrimAtPath(mat_path)
            if material:
                shader = material.GetShadeMaster().GetShader()

                # Randomize albedo
                albedo_min, albedo_max = self.material_params['albedo_range']
                albedo = tuple(
                    random.uniform(albedo_min[i], albedo_max[i]) for i in range(3)
                )
                shader.GetInput("diffuseColor").Set(albedo)

                # Randomize roughness
                roughness = random.uniform(*self.material_params['roughness_range'])
                shader.GetInput("roughness").Set(roughness)

                # Randomize metallic
                metallic = random.uniform(*self.material_params['metallic_range'])
                shader.GetInput("metallic").Set(metallic)

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

        return tuple(np.clip([red, green, blue], 0, 255) / 255.0)

# Usage example
randomizer = DomainRandomizer()
stage = omni.usd.get_context().get_stage()
randomizer.randomize_lighting(stage)
randomizer.randomize_materials(stage, ["/World/Materials/Mat1", "/World/Materials/Mat2"])
```

## Sensor Simulation and Data Capture

### RGB Camera Data Generation

```python
# RGB camera data generation with realistic effects
from omni.isaac.sensor import Camera
import cv2

class RGBCameraSimulator:
    def __init__(self, robot_prim_path, camera_name, width=640, height=480):
        self.camera = Camera(
            prim_path=f"{robot_prim_path}/{camera_name}",
            frequency=30,
            resolution=(width, height)
        )
        self.width = width
        self.height = height

    def capture_image(self):
        """Capture RGB image with realistic effects"""
        # Get raw image data
        raw_image = self.camera.get_rgb_data()

        # Apply realistic camera effects
        processed_image = self.add_camera_effects(raw_image)

        return processed_image

    def add_camera_effects(self, image):
        """Add realistic camera effects to image"""
        # Add noise
        image = self.add_sensor_noise(image)

        # Add chromatic aberration
        image = self.add_chromatic_aberration(image)

        # Add vignetting
        image = self.add_vignetting(image)

        # Add motion blur if needed
        image = self.add_motion_blur(image)

        return image

    def add_sensor_noise(self, image):
        """Add realistic sensor noise"""
        # Shot noise (proportional to signal)
        shot_noise = np.random.poisson(image * 255) / 255.0
        shot_noise = (shot_noise - image) * 0.02  # Scale factor

        # Read noise (constant)
        read_noise = np.random.normal(0, 0.01, image.shape)

        noisy_image = np.clip(image + shot_noise + read_noise, 0, 1)
        return noisy_image

    def add_chromatic_aberration(self, image):
        """Add chromatic aberration effect"""
        # Simple chromatic aberration by slightly offsetting color channels
        if len(image.shape) == 3:  # Color image
            # Offset red and blue channels slightly
            red_channel = np.roll(image[:, :, 0], 1, axis=1)  # Shift red horizontally
            green_channel = image[:, :, 1]  # Keep green unchanged
            blue_channel = np.roll(image[:, :, 2], -1, axis=1)  # Shift blue horizontally

            aberrated_image = np.stack([red_channel, green_channel, blue_channel], axis=2)
            return aberrated_image
        return image

    def add_vignetting(self, image):
        """Add vignetting effect (darker edges)"""
        rows, cols = image.shape[:2]
        centerX, centerY = cols // 2, rows // 2

        # Create coordinate grid
        X_resultant_cord = np.zeros((rows, cols))
        for i in range(rows):
            for j in range(cols):
                X_resultant_cord[i, j] = (j - centerX)**2 + (i - centerY)**2

        # Create vignette mask
        max_distance = np.sqrt((centerX)**2 + (centerY)**2)
        vignette_mask = (max_distance - np.sqrt(X_resultant_cord)) / max_distance
        vignette_mask = np.repeat(vignette_mask[:, :, np.newaxis], 3, axis=2)

        # Apply vignette
        vignette_image = image * vignette_mask
        return np.clip(vignette_image, 0, 1)

    def add_motion_blur(self, image):
        """Add motion blur effect"""
        # Simple motion blur kernel
        kernel_size = 3
        kernel = np.zeros((kernel_size, kernel_size))
        kernel[int((kernel_size-1)/2), :] = np.ones(kernel_size)
        kernel = kernel / kernel_size

        # Apply blur
        if len(image.shape) == 3:
            blurred = cv2.filter2D(image, -1, kernel)
        else:
            blurred = cv2.filter2D(image, -1, kernel)

        return blurred
```

### Depth Data Generation

```python
# Depth sensor simulation
class DepthSensorSimulator:
    def __init__(self, robot_prim_path, sensor_name, width=640, height=480):
        self.camera = Camera(
            prim_path=f"{robot_prim_path}/{sensor_name}",
            frequency=30,
            resolution=(width, height)
        )
        self.width = width
        self.height = height

    def capture_depth(self):
        """Capture depth data with realistic noise"""
        # Get raw depth data
        raw_depth = self.camera.get_distance_to_camera_data()

        # Add realistic depth noise
        noisy_depth = self.add_depth_noise(raw_depth)

        return noisy_depth

    def add_depth_noise(self, depth_data):
        """Add realistic depth sensor noise"""
        # Depth noise typically increases with distance
        # Formula: noise = bias + scale * distance + scale² * distance²
        distance_based_noise = 0.001 + 0.005 * depth_data + 0.002 * depth_data**2

        # Add random noise based on distance
        noise = np.random.normal(0, distance_based_noise, depth_data.shape)
        noisy_depth = depth_data + noise

        # Ensure depth is positive and within reasonable bounds
        noisy_depth = np.clip(noisy_depth, 0.01, 100.0)  # 1cm to 100m range

        return noisy_depth

    def get_point_cloud(self, depth_data):
        """Convert depth data to point cloud"""
        # Camera intrinsic parameters
        fx, fy = self.width / (2 * np.tan(np.radians(60) / 2)), self.height / (2 * np.tan(np.radians(45) / 2))
        cx, cy = self.width / 2, self.height / 2

        # Create coordinate grids
        y_coords, x_coords = np.mgrid[0:self.height, 0:self.width]

        # Convert to 3D coordinates
        x_3d = (x_coords - cx) * depth_data / fx
        y_3d = (y_coords - cy) * depth_data / fy
        z_3d = depth_data

        # Stack to create point cloud
        point_cloud = np.stack([x_3d, y_3d, z_3d], axis=-1)

        return point_cloud
```

### Semantic Segmentation Generation

```python
# Semantic segmentation generation
class SemanticSegmentationGenerator:
    def __init__(self, camera):
        self.camera = camera

    def generate_segmentation(self):
        """Generate semantic segmentation with object IDs"""
        # Get semantic segmentation data from Isaac Sim
        segmentation = self.camera.get_semantic_segmentation()

        # Process segmentation for training
        processed_segmentation = self.process_segmentation(segmentation)

        return processed_segmentation

    def process_segmentation(self, segmentation_data):
        """Process raw segmentation for training use"""
        # Convert to class IDs
        class_ids = self.map_to_class_ids(segmentation_data)

        # Apply post-processing if needed
        processed = self.post_process_segmentation(class_ids)

        return processed

    def map_to_class_ids(self, segmentation_data):
        """Map object IDs to semantic class IDs"""
        # Define mapping from object properties to class IDs
        class_mapping = {
            'robot': 1,
            'obstacle': 2,
            'ground': 3,
            'wall': 4,
            'furniture': 5,
            'person': 6,
            'unknown': 0
        }

        # Process segmentation based on object properties
        class_ids = np.zeros_like(segmentation_data, dtype=np.int32)

        # This would involve querying object properties in the scene
        # and mapping them to appropriate class IDs

        return class_ids

    def post_process_segmentation(self, segmentation):
        """Apply post-processing to segmentation"""
        # Apply morphological operations to clean up segmentation
        import cv2

        # Apply median filter to reduce noise
        cleaned = cv2.medianBlur(segmentation.astype(np.uint8), 3)

        # Apply morphological closing to fill small holes
        kernel = np.ones((3, 3), np.uint8)
        closed = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel)

        return closed
```

## Annotation Generation

### Automatic Annotation Pipeline

```python
# Automatic annotation generation
class AnnotationGenerator:
    def __init__(self, stage):
        self.stage = stage

    def generate_bounding_boxes(self, segmentation):
        """Generate bounding boxes from segmentation"""
        import cv2

        annotations = []

        # Get unique class IDs
        unique_classes = np.unique(segmentation)

        for class_id in unique_classes:
            if class_id == 0:  # Skip background
                continue

            # Create binary mask for this class
            mask = (segmentation == class_id).astype(np.uint8)

            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                # Calculate bounding box
                x, y, w, h = cv2.boundingRect(contour)

                annotation = {
                    'class_id': int(class_id),
                    'bbox': [int(x), int(y), int(w), int(h)],
                    'area': int(cv2.contourArea(contour)),
                    'confidence': 1.0  # Perfect annotation
                }

                annotations.append(annotation)

        return annotations

    def generate_instance_masks(self, segmentation):
        """Generate instance segmentation masks"""
        import cv2

        instances = []

        # Get unique instance IDs (this would come from instance segmentation)
        unique_instances = np.unique(segmentation)

        for instance_id in unique_instances:
            if instance_id == 0:  # Skip background
                continue

            # Create mask for this instance
            mask = (segmentation == instance_id).astype(np.uint8)

            # Calculate instance properties
            props = cv2.moments(mask)
            if props['m00'] > 0:
                cx = int(props['m10'] / props['m00'])
                cy = int(props['m01'] / props['m00'])
            else:
                continue

            instance_info = {
                'instance_id': int(instance_id),
                'mask': mask,
                'centroid': (cx, cy),
                'area': int(props['m00'])
            }

            instances.append(instance_info)

        return instances

    def generate_keypoints(self, robot_prim_path):
        """Generate 3D keypoints for articulated objects"""
        # Get robot joint positions in 3D space
        from omni.isaac.core.utils.prims import get_prim_at_path
        from omni.isaac.core.utils.transformations import get_tf

        robot_prim = get_prim_at_path(robot_prim_path)
        joint_paths = self.get_robot_joint_paths(robot_prim)

        keypoints_3d = []
        for joint_path in joint_paths:
            joint_prim = get_prim_at_path(joint_path)
            world_transform = get_tf(joint_prim, robot_prim)

            # Extract 3D position
            pos_3d = world_transform[0]  # [x, y, z]

            # Project to 2D image space
            pos_2d = self.project_3d_to_2d(pos_3d)

            keypoint = {
                'name': joint_path.split('/')[-1],
                'position_3d': pos_3d,
                'position_2d': pos_2d,
                'visibility': 1.0  # Always visible in simulation
            }

            keypoints_3d.append(keypoint)

        return keypoints_3d

    def project_3d_to_2d(self, pos_3d):
        """Project 3D point to 2D image coordinates"""
        # This would use camera intrinsic parameters
        # Simplified pinhole camera model
        fx, fy = 320, 320  # Focal lengths (example values)
        cx, cy = 320, 240  # Principal point (example values)

        # Perspective projection
        x_2d = fx * pos_3d[0] / pos_3d[2] + cx
        y_2d = fy * pos_3d[1] / pos_3d[2] + cy

        return [x_2d, y_2d]

    def get_robot_joint_paths(self, robot_prim):
        """Get paths to robot joints"""
        # This would query the robot articulation structure
        # For now, return a placeholder list
        return [
            f"{robot_prim.GetPrimPath()}/joint1",
            f"{robot_prim.GetPrimPath()}/joint2",
            f"{robot_prim.GetPrimPath()}/joint3"
        ]
```

## Data Export and Format Conversion

### Standard Dataset Formats

```python
# Data export utilities
import json
import os
import cv2
from PIL import Image

class DataExporter:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.create_output_structure()

    def create_output_structure(self):
        """Create directory structure for dataset export"""
        os.makedirs(os.path.join(self.output_dir, "images"), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "labels"), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "depth"), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "segmentation"), exist_ok=True)

    def export_coco_format(self, samples, dataset_name):
        """Export dataset in COCO format"""
        coco_dataset = {
            "info": {
                "description": f"Synthetic dataset generated with Isaac Sim: {dataset_name}",
                "version": "1.0",
                "year": 2025,
                "contributor": "Isaac Sim Synthetic Data Generator",
                "date_created": "2025-12-19"
            },
            "licenses": [
                {
                    "id": 1,
                    "name": "Synthetic Data License",
                    "url": "http://creativecommons.org/licenses/by/4.0/"
                }
            ],
            "categories": self.get_categories(),
            "images": [],
            "annotations": []
        }

        annotation_id = 1
        for sample_idx, sample in enumerate(samples):
            # Add image info
            image_info = {
                "id": sample_idx + 1,
                "width": sample['rgb'].shape[1],
                "height": sample['rgb'].shape[0],
                "file_name": f"images/{sample_idx:06d}.jpg",
                "license": 1,
                "date_captured": "2025-12-19"
            }
            coco_dataset["images"].append(image_info)

            # Add annotations
            for bbox in sample['annotations']:
                annotation_info = {
                    "id": annotation_id,
                    "image_id": sample_idx + 1,
                    "category_id": bbox['class_id'],
                    "bbox": bbox['bbox'],
                    "area": bbox['area'],
                    "iscrowd": 0,
                    "segmentation": [],  # Could add segmentation polygons here
                    "keypoints": [],    # Could add keypoints here
                    "num_keypoints": 0
                }
                coco_dataset["annotations"].append(annotation_info)
                annotation_id += 1

        # Save COCO JSON
        coco_path = os.path.join(self.output_dir, f"{dataset_name}_coco.json")
        with open(coco_path, 'w') as f:
            json.dump(coco_dataset, f, indent=2)

        return coco_path

    def export_yolo_format(self, samples, dataset_name):
        """Export dataset in YOLO format"""
        # Create YOLO dataset structure
        yolo_dir = os.path.join(self.output_dir, f"{dataset_name}_yolo")
        os.makedirs(os.path.join(yolo_dir, "images", "train"), exist_ok=True)
        os.makedirs(os.path.join(yolo_dir, "labels", "train"), exist_ok=True)

        # Write YOLO labels
        for sample_idx, sample in enumerate(samples):
            # Save image
            img_path = os.path.join(yolo_dir, "images", "train", f"{sample_idx:06d}.jpg")
            Image.fromarray((sample['rgb'] * 255).astype(np.uint8)).save(img_path)

            # Write label file
            label_path = os.path.join(yolo_dir, "labels", "train", f"{sample_idx:06d}.txt")
            with open(label_path, 'w') as f:
                for bbox in sample['annotations']:
                    # YOLO format: class_id center_x center_y width height (normalized)
                    img_width, img_height = sample['rgb'].shape[1], sample['rgb'].shape[0]
                    x, y, w, h = bbox['bbox']
                    center_x = (x + w/2) / img_width
                    center_y = (y + h/2) / img_height
                    norm_width = w / img_width
                    norm_height = h / img_height

                    f.write(f"{bbox['class_id']} {center_x:.6f} {center_y:.6f} {norm_width:.6f} {norm_height:.6f}\n")

        # Create YOLO dataset config
        config_content = f"""
path: {os.path.abspath(yolo_dir)}
train: images/train
val: images/train

nc: {len(self.get_categories())}
names: {[cat['name'] for cat in self.get_categories()]}
"""
        config_path = os.path.join(yolo_dir, "dataset.yaml")
        with open(config_path, 'w') as f:
            f.write(config_content)

        return yolo_dir

    def get_categories(self):
        """Define dataset categories"""
        return [
            {"id": 1, "name": "robot", "supercategory": "object"},
            {"id": 2, "name": "obstacle", "supercategory": "object"},
            {"id": 3, "name": "ground", "supercategory": "surface"},
            {"id": 4, "name": "wall", "supercategory": "structure"},
            {"id": 5, "name": "furniture", "supercategory": "object"},
            {"id": 6, "name": "person", "supercategory": "living"}
        ]

    def save_sample_data(self, sample_idx, rgb_image, depth_data, segmentation, annotations):
        """Save individual sample data"""
        # Save RGB image
        img_path = os.path.join(self.output_dir, "images", f"{sample_idx:06d}.jpg")
        Image.fromarray((rgb_image * 255).astype(np.uint8)).save(img_path)

        # Save depth data
        depth_path = os.path.join(self.output_dir, "depth", f"{sample_idx:06d}.npy")
        np.save(depth_path, depth_data)

        # Save segmentation
        seg_path = os.path.join(self.output_dir, "segmentation", f"{sample_idx:06d}.png")
        Image.fromarray((segmentation * 255).astype(np.uint8)).save(seg_path)

        # Save annotations
        annot_path = os.path.join(self.output_dir, "labels", f"{sample_idx:06d}.json")
        with open(annot_path, 'w') as f:
            json.dump(annotations, f, indent=2)
```

## Quality Assessment and Validation

### Data Quality Metrics

```python
# Data quality assessment
class QualityAssessor:
    def __init__(self):
        pass

    def assess_image_quality(self, image):
        """Assess the quality of generated images"""
        metrics = {}

        # Sharpness assessment using Laplacian variance
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) if len(image.shape) == 3 else image
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        metrics['sharpness'] = laplacian_var

        # Brightness assessment
        brightness = np.mean(gray)
        metrics['brightness'] = brightness

        # Contrast assessment (standard deviation)
        contrast = np.std(gray)
        metrics['contrast'] = contrast

        # Colorfulness assessment
        if len(image.shape) == 3:
            rg = np.absolute(image[:, :, 0] - image[:, :, 1])
            yb = np.absolute(image[:, :, 1] - image[:, :, 2])
            colorfulness = np.std(rg) + np.std(yb)
            metrics['colorfulness'] = colorfulness

        return metrics

    def validate_annotations(self, image, annotations):
        """Validate the quality of annotations"""
        validation_results = {}

        # Check if annotations are within image bounds
        height, width = image.shape[:2]
        valid_annotations = []
        invalid_count = 0

        for ann in annotations:
            x, y, w, h = ann['bbox']
            if x >= 0 and y >= 0 and x + w <= width and y + h <= height:
                valid_annotations.append(ann)
            else:
                invalid_count += 1

        validation_results['valid_bbox_ratio'] = 1.0 - (invalid_count / len(annotations)) if annotations else 1.0

        # Check annotation sizes (should not be too small)
        small_annotations = sum(1 for ann in annotations if ann['area'] < 100)  # Less than 100 pixels
        validation_results['small_annotation_ratio'] = small_annotations / len(annotations) if annotations else 0.0

        return validation_results

    def compare_real_synthetic(self, real_data, synthetic_data):
        """Compare real and synthetic data distributions"""
        from scipy.stats import wasserstein_distance, ks_2samp

        comparison_results = {}

        # Compare color distributions
        if len(real_data.shape) == 3 and len(synthetic_data.shape) == 3:
            for channel in range(min(real_data.shape[2], synthetic_data.shape[2])):
                real_channel = real_data[:, :, channel].flatten()
                synth_channel = synthetic_data[:, :, channel].flatten()

                # Earth Mover's Distance (Wasserstein)
                emd = wasserstein_distance(real_channel, synth_channel)
                comparison_results[f'color_channel_{channel}_emd'] = emd

                # Kolmogorov-Smirnov test
                ks_stat, ks_p = ks_2samp(real_channel, synth_channel)
                comparison_results[f'color_channel_{channel}_ks_stat'] = ks_stat
                comparison_results[f'color_channel_{channel}_ks_p'] = ks_p

        # Compare texture properties using local binary patterns (simplified)
        comparison_results['texture_similarity'] = self.compare_textures(real_data, synthetic_data)

        return comparison_results

    def compare_textures(self, img1, img2):
        """Compare texture properties between images"""
        # Simplified texture comparison using variance of gradients
        gray1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY) if len(img1.shape) == 3 else img1
        gray2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY) if len(img2.shape) == 3 else img2

        grad_x1 = cv2.Sobel(gray1, cv2.CV_64F, 1, 0, ksize=3)
        grad_y1 = cv2.Sobel(gray1, cv2.CV_64F, 0, 1, ksize=3)
        texture_var1 = np.var(np.sqrt(grad_x1**2 + grad_y1**2))

        grad_x2 = cv2.Sobel(gray2, cv2.CV_64F, 1, 0, ksize=3)
        grad_y2 = cv2.Sobel(gray2, cv2.CV_64F, 0, 1, ksize=3)
        texture_var2 = np.var(np.sqrt(grad_x2**2 + grad_y2**2))

        # Return similarity score (higher is more similar)
        return abs(texture_var1 - texture_var2) / max(texture_var1, texture_var2, 1e-6)
```

## Advanced Techniques

### Sim-to-Real Transfer Optimization

```python
# Sim-to-real transfer techniques
class SimToRealTransfer:
    def __init__(self):
        self.domain_randomization = DomainRandomizer()

    def generate_progressive_dataset(self, complexity_levels=5):
        """Generate dataset with increasing complexity for curriculum learning"""
        datasets = []

        for level in range(complexity_levels):
            # Configure scene complexity based on level
            scene_params = self.get_complexity_parameters(level)

            # Generate dataset for this complexity level
            dataset = self.generate_dataset_with_params(scene_params)
            datasets.append({
                'complexity_level': level,
                'dataset': dataset,
                'parameters': scene_params
            })

        return datasets

    def get_complexity_parameters(self, level):
        """Get parameters for different complexity levels"""
        base_params = {
            'lighting_variation': [0.1, 0.3, 0.5, 0.7, 1.0],  # Increasing variation
            'texture_complexity': [0.2, 0.4, 0.6, 0.8, 1.0],  # Increasing complexity
            'occlusion_frequency': [0.05, 0.1, 0.15, 0.2, 0.25],  # Increasing occlusion
            'background_complexity': [0.1, 0.25, 0.4, 0.6, 0.8]  # Increasing background complexity
        }

        return {
            'lighting_variation': base_params['lighting_variation'][level],
            'texture_complexity': base_params['texture_complexity'][level],
            'occlusion_frequency': base_params['occlusion_frequency'][level],
            'background_complexity': base_params['background_complexity'][level]
        }

    def generate_dataset_with_params(self, params):
        """Generate dataset with specific parameters"""
        # This would implement the actual data generation with the given parameters
        # For now, return a placeholder
        return f"Dataset with params: {params}"

    def apply_texture_adaptation(self, synthetic_image, real_image_stats):
        """Adapt synthetic image statistics to match real image statistics"""
        # Calculate statistics for synthetic image
        synth_mean = np.mean(synthetic_image, axis=(0, 1))
        synth_std = np.std(synthetic_image, axis=(0, 1))

        # Calculate target statistics
        real_mean = real_image_stats['mean']
        real_std = real_image_stats['std']

        # Adapt synthetic image
        adapted_image = synthetic_image.copy()
        for c in range(adapted_image.shape[2]):  # For each color channel
            # Normalize synthetic image
            adapted_image[:, :, c] = (adapted_image[:, :, c] - synth_mean[c]) / (synth_std[c] + 1e-6)
            # Scale to match real image statistics
            adapted_image[:, :, c] = adapted_image[:, :, c] * real_std[c] + real_mean[c]

        # Clamp to valid range
        adapted_image = np.clip(adapted_image, 0, 1)

        return adapted_image
```

## Performance Optimization

### Batch Processing for Efficiency

```python
# Batch processing for efficient data generation
import threading
import queue
from concurrent.futures import ThreadPoolExecutor

class BatchDataGenerator:
    def __init__(self, num_workers=4):
        self.num_workers = num_workers
        self.data_queue = queue.Queue()
        self.result_queue = queue.Queue()

    def generate_batch(self, batch_size, output_dir):
        """Generate a batch of synthetic data efficiently"""
        with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            futures = []

            for i in range(batch_size):
                future = executor.submit(self.generate_single_sample, i, output_dir)
                futures.append(future)

            # Wait for all samples to complete
            for future in futures:
                future.result()

    def generate_single_sample(self, sample_idx, output_dir):
        """Generate a single synthetic data sample"""
        # Initialize simulation for this sample
        world = initialize_simulation()

        # Randomize environment
        self.randomizer.randomize_lighting(world.stage)
        self.randomizer.randomize_materials(world.stage, self.material_paths)

        # Run simulation
        for step in range(10):  # Run for a few steps to stabilize
            world.step(render=True)

        # Capture data from all sensors
        rgb_data = self.rgb_camera.capture_image()
        depth_data = self.depth_sensor.capture_depth()
        segmentation = self.segmentation_generator.generate_segmentation()

        # Generate annotations
        annotations = self.annotation_generator.generate_bounding_boxes(segmentation)

        # Validate data quality
        quality_metrics = self.quality_assessor.assess_image_quality(rgb_data)
        if quality_metrics['sharpness'] < 100:  # Threshold for acceptable sharpness
            print(f"Sample {sample_idx} has low quality, regenerating...")
            return self.generate_single_sample(sample_idx, output_dir)

        # Export sample
        self.exporter.save_sample_data(sample_idx, rgb_data, depth_data, segmentation, annotations)

        print(f"Generated sample {sample_idx}")
        return sample_idx
```

## Best Practices and Guidelines

### Quality Assurance Checklist

```python
# Synthetic data quality checklist
QUALITY_CHECKLIST = {
    "visual_quality": {
        "sharpness_threshold": 100,
        "brightness_range": (50, 200),
        "contrast_range": (20, 100)
    },
    "annotation_quality": {
        "min_object_size": 50,  # pixels
        "max_annotation_ratio": 0.8,  # object should not cover more than 80% of image
        "annotation_accuracy": 1.0  # perfect in simulation
    },
    "diversity_metrics": {
        "min_lighting_variations": 10,
        "min_material_variations": 20,
        "scene_complexity_range": (1, 10)  # 1 = simple, 10 = complex
    },
    "consistency_checks": {
        "temporal_coherence": True,
        "sensor_fusion_consistency": True,
        "physical_plausibility": True
    }
}

def validate_dataset_quality(dataset_path):
    """Validate entire dataset against quality standards"""
    validation_results = {
        "passed": True,
        "issues": [],
        "metrics": {}
    }

    # Check sample count
    samples = os.listdir(os.path.join(dataset_path, "images"))
    if len(samples) < 1000:  # Minimum recommended size
        validation_results["issues"].append("Dataset size too small (<1000 samples)")
        validation_results["passed"] = False

    # Check for quality metrics
    # This would involve more comprehensive checks

    return validation_results
```

## Summary

Synthetic data generation with Isaac Sim provides a powerful approach to creating high-quality training datasets for AI applications in robotics. By leveraging domain randomization, realistic sensor simulation, and automatic annotation generation, you can create diverse and comprehensive datasets that enable the development of robust AI models.

The key to successful synthetic data generation lies in:
1. Properly configuring domain randomization for diversity
2. Accurately simulating sensor characteristics
3. Generating high-quality automatic annotations
4. Validating data quality against real-world standards
5. Optimizing performance for efficient data generation

These techniques enable the creation of AI models that can effectively transfer from simulation to reality, reducing the need for expensive real-world data collection while maintaining high performance in real-world applications.