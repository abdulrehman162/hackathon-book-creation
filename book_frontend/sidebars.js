// @ts-check

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.

 @type {import('@docusaurus/plugin-content-docs').SidebarsConfig}
 */
const sidebars = {
  // Manual sidebar structure for the ROS 2 educational content
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Module 1: Introduction to ROS 2 for Physical AI',
      link: {type: 'doc', id: 'module1-intro-ros2/index'},
      items: [
        'module1-intro-ros2/index',
        'module1-intro-ros2/dds-concepts',
        'module1-intro-ros2/why-ros2-for-humanoids',
        'module1-intro-ros2/quiz-fundamentals',
        'module1-intro-ros2/exercise-dds'
      ],
    },
    {
      type: 'category',
      label: 'Module 2: Digital Twin Simulation with Gazebo & Unity',
      link: {type: 'doc', id: 'module2-digital-twin/index'},
      items: [
        'module2-digital-twin/index',
        'module2-digital-twin/physics-simulation-gazebo',
        'module2-digital-twin/robot-models-gazebo',
        'module2-digital-twin/physics-parameters',
        'module2-digital-twin/digital-twins-unity',
        'module2-digital-twin/hri-implementation',
        'module2-digital-twin/sensor-simulation',
        'module2-digital-twin/validation-methods',
        'module2-digital-twin/integration-examples',
        'module2-digital-twin/quiz-gazebo-physics',
        'module2-digital-twin/quiz-unity-digital-twins',
        'module2-digital-twin/quiz-sensor-simulation',
        'module2-digital-twin/exercise-gazebo-modeling',
        'module2-digital-twin/exercise-hri-implementation',
        'module2-digital-twin/exercise-sensor-validation',
        'module2-digital-twin/exercises-examples'
      ],
    },
    {
      type: 'category',
      label: 'Module 3: ROS 2 Communication Model',
      link: {type: 'doc', id: 'module2-communication/index'},
      items: [
        'module2-communication/index',
        'module2-communication/nodes-topics-services',
        'module2-communication/rclpy-agent-controller',
        'module2-communication/quiz-communication'
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Robot Structure with URDF',
      link: {type: 'doc', id: 'module3-urdf/index'},
      items: [
        'module3-urdf/index',
        'module3-urdf/robot-structure',
        'module3-urdf/simulation-readiness',
        'module3-urdf/quiz-urdf',
        'module3-urdf/exercise-urdf'
      ],
    },
    {
      type: 'category',
      label: 'Module 5: Isaac AI-Robot Brain (NVIDIA Isaac™)',
      link: {type: 'doc', id: 'module4-isaac-ai-brain/index'},
      items: [
        'module4-isaac-ai-brain/index',
        'module4-isaac-ai-brain/isaac-sim-introduction',
        'module4-isaac-ai-brain/isaac-sim-setup',
        'module4-isaac-ai-brain/isaac-sim-advanced-features',
        'module4-isaac-ai-brain/isaac-ros-introduction',
        'module4-isaac-ai-brain/isaac-ros-setup',
        'module4-isaac-ai-brain/vslam-implementation',
        'module4-isaac-ai-brain/hardware-acceleration',
        'module4-isaac-ai-brain/perception-pipeline',
        'module4-isaac-ai-brain/isaac-sim-ros-bridge',
        'module4-isaac-ai-brain/isaac-ecosystem-integration',
        'module4-isaac-ai-brain/isaac-integration',
        'module4-isaac-ai-brain/photorealistic-simulation',
        'module4-isaac-ai-brain/synthetic-data-generation',
        'module4-isaac-ai-brain/usd-scene-composition',
        'module4-isaac-ai-brain/nav2-introduction',
        'module4-isaac-ai-brain/path-planning-bipedal',
        'module4-isaac-ai-brain/isaac-ros-navigation-algorithms',
        'module4-isaac-ai-brain/isaac-ros-perception-algorithms',
        'module4-isaac-ai-brain/humanoid-kinematic-constraints',
        'module4-isaac-ai-brain/nav2-humanoid-configuration',
        'module4-isaac-ai-brain/navigation-recovery-behaviors',
        'module4-isaac-ai-brain/quiz-isaac-sim',
        'module4-isaac-ai-brain/quiz-isaac-ros',
        'module4-isaac-ai-brain/quiz-nav2',
        'module4-isaac-ai-brain/quiz-bridge-integration',
        'module4-isaac-ai-brain/quiz-ecosystem-integration',
        'module4-isaac-ai-brain/quiz-navigation',
        'module4-isaac-ai-brain/quiz-perception',
        'module4-isaac-ai-brain/exercise-synthetic-data',
        'module4-isaac-ai-brain/exercise-vslam',
        'module4-isaac-ai-brain/exercise-vslam-implementation',
        'module4-isaac-ai-brain/exercise-humanoid-navigation',
        'module4-isaac-ai-brain/exercise-bridge-integration',
        'module4-isaac-ai-brain/exercise-ecosystem-integration',
        'module4-isaac-ai-brain/exercises-examples',
        'module4-isaac-ai-brain/simulation-to-reality',
        'module4-isaac-ai-brain/complete-project-example'
      ],
    },
    {
      type: 'category',
      label: 'Tutorial',
      items: ['tutorial-basics/create-a-document'],
    },
  ],
};

export default sidebars;
