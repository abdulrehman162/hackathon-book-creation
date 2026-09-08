# Data Model: Digital Twin Simulation with Gazebo & Unity

## Content Entities

### Module
- **name**: string - The name of the module (e.g., "Physics Simulation with Gazebo")
- **description**: string - Brief description of the module's purpose
- **chapters**: Chapter[] - List of chapters in this module
- **learningObjectives**: string[] - List of learning objectives for the module
- **prerequisites**: string[] - Knowledge required before starting this module

### Chapter
- **title**: string - The title of the chapter
- **content**: string - The main content in Markdown format
- **learningObjectives**: string[] - Specific objectives for this chapter
- **exercises**: Exercise[] - List of exercises in this chapter
- **duration**: number - Estimated time to complete in minutes
- **simulationExamples**: SimulationExample[] - List of simulation examples in this chapter

### Exercise
- **title**: string - The title of the exercise
- **description**: string - Detailed description of the exercise
- **type**: "practical" | "theoretical" | "quiz" | "simulation" - Type of exercise
- **difficulty**: "beginner" | "intermediate" | "advanced" - Difficulty level
- **solution**: string - Solution or expected outcome
- **simulationRequirements**: string[] - Simulation environment requirements

### SimulationExample
- **title**: string - Title of the simulation example
- **description**: string - Description of what the example demonstrates
- **environment**: "gazebo" | "unity" | "integrated" - Which environment(s) it uses
- **components**: string[] - List of components used in the example
- **expectedOutcome**: string - What the example should demonstrate
- **files**: string[] - List of files needed for the example

### LearningPath
- **modules**: Module[] - The ordered sequence of modules
- **targetAudience**: string - Description of the target audience
- **estimatedDuration**: number - Total estimated time in hours
- **prerequisites**: string[] - Overall prerequisites for the path

## Simulation-Specific Entities

### GazeboSimulation
- **worldFile**: string - Path to the Gazebo world file
- **robotModel**: string - URDF/SDF model of the robot
- **physicsEngine**: string - Physics engine configuration (ODE, Bullet, etc.)
- **sensorConfigurations**: SensorConfiguration[] - Configured sensors for the simulation
- **simulationParameters**: object - Physics parameters and settings

### UnityScene
- **sceneName**: string - Name of the Unity scene
- **robotPrefab**: string - Path to the robot prefab
- **environmentAssets**: string[] - List of environment assets used
- **lightingSettings**: object - Lighting configuration
- **renderSettings**: object - Rendering configuration
- **interactionComponents**: string[] - Components for HRI

### SensorConfiguration
- **sensorType**: "lidar" | "depth_camera" | "imu" | "camera" | "force_torque" - Type of sensor
- **sensorName**: string - Name of the sensor
- **position**: object - Position of the sensor on the robot
- **parameters**: object - Sensor-specific parameters (range, resolution, etc.)
- **topicName**: string - ROS topic name for the sensor data

## Relationships
- A LearningPath contains multiple Modules
- A Module contains multiple Chapters and SimulationExamples
- A Chapter contains multiple Exercises and SimulationExamples
- SimulationExamples may reference GazeboSimulations or UnityScenes
- GazeboSimulations and UnityScenes may share RobotModels

## Validation Rules
- Module names must be unique within a LearningPath
- Chapter titles must be unique within a Module
- Learning objectives must be specific and measurable
- All content must be in Markdown format
- Duration estimates must be realistic based on content complexity
- Simulation examples must have corresponding environment configurations
- Sensor configurations must match the actual capabilities of the simulated sensors

## State Transitions
- Content status: draft → review → approved → published
- Module completion: not_started → in_progress → completed
- Exercise status: available → attempted → completed → verified
- Simulation example: not_configured → configured → tested → validated