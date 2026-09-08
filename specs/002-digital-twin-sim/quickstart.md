# Quickstart: Digital Twin Simulation with Gazebo & Unity

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Git for version control
- Basic knowledge of Markdown and React (helpful but not required)
- Gazebo simulation environment (recommended: Garden or Fortress)
- Unity Hub with Unity 2023.2 LTS (for Unity examples)
- Basic understanding of ROS/ROS2 concepts

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Start the development server**
   ```bash
   npm run start
   # or
   yarn start
   ```
   This will start the Docusaurus development server at `http://localhost:3000`

4. **Build for production**
   ```bash
   npm run build
   # or
   yarn build
   ```
   This creates a static build in the `build/` directory

## Project Structure

```
docs/
├── module2-digital-twin/          # Digital Twin Simulation Module
│   ├── index.md                   # Main module page
│   ├── physics-simulation-gazebo.md # Gazebo physics simulation
│   ├── digital-twins-unity.md      # Unity digital twins
│   ├── hri-implementation.md       # Human-robot interaction
│   ├── sensor-simulation.md        # Sensor simulation
│   ├── validation-methods.md       # Validation techniques
│   └── integration-examples.md     # Integration examples
├── sidebar.js                     # Navigation configuration
└── docusaurus.config.js           # Site configuration
```

## Adding New Content

1. **Create a new markdown file** in the appropriate module directory
2. **Add frontmatter** at the top of the file:
   ```markdown
   ---
   title: Your Chapter Title
   description: Brief description of the chapter
   sidebar_label: Label for sidebar
   sidebar_position: 3  # Position in the sidebar
   ---
   ```

3. **Update the sidebar configuration** in `sidebar.js` to include your new content

## Simulation Environment Setup

### Gazebo Setup
- Install Gazebo Garden or Fortress following the official ROS documentation
- Verify installation with: `gz sim --version`
- Ensure proper ROS environment setup for Gazebo integration

### Unity Setup
- Install Unity Hub and Unity 2023.2 LTS
- Install ROS# Unity package for ROS integration
- Configure network settings for ROS communication

## Content Guidelines

- All content must be in Markdown format
- Follow the learning objectives defined in the specification
- Include practical simulation examples and exercises where appropriate
- Link to official Gazebo, Unity, and ROS documentation for technical accuracy
- Ensure content meets accessibility standards

## Deployment

The site is configured for GitHub Pages deployment. After pushing changes to the main branch, GitHub Actions will automatically build and deploy the site.

## Troubleshooting

### Common Issues:
- **Gazebo not launching**: Verify ROS environment variables and Gazebo installation
- **Unity-ROS connection failing**: Check network configuration and firewall settings
- **Documentation build errors**: Verify Markdown syntax and frontmatter format