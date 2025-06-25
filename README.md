
# 3 DOF Rehabilitation Arm Robot

This repository contains all the essential resources for controlling a 3 DOF rehabilitation robotic arm using ROS 2 and MoveIt 2. It includes robot description files (URDF/Xacro), meshes, and configuration files required for motion planning and control.

---

## 🛠️ Setup Instructions

### 1. Create the ROS 2 Workspace

```bash
mkdir -p ~/Workspace/src
cd ~/Workspace
colcon build
```

### 2. Export URDF from SolidWorks

Use the [SolidWorks to URDF Exporter](https://github.com/ros/solidworks_urdf_exporter) plugin to export your robot model. Make sure the exported folder includes:

- `URDF` files
    
- `meshes/` directory with STL or DAE files
    

Place the exported folder inside `~/Workspace/src/`.

### 3. Convert URDF to Xacro

Rewrite your URDF into a Xacro format to make it modular and maintainable. Use existing Xacro files in this repository as a reference for structure and syntax.

### 4. Modify CMakeLists.txt and package.xml

Ensure the following are added to make your package ROS 2 compatible:

- In `CMakeLists.txt`:
    
    ```cmake
    find_package(ament_cmake REQUIRED)
    find_package(xacro REQUIRED)
    install(DIRECTORY launch urdf meshes
      DESTINATION share/${PROJECT_NAME}/
    )
    ament_package()
    ```
    
- In `package.xml`:
    
    ```xml
    <buildtool_depend>ament_cmake</buildtool_depend>
    <exec_depend>xacro</exec_depend>
    ```
    

### 5. Build the Package

```bash
cd ~/Workspace/
colcon build
source install/setup.bash
```

### 6. Launch MoveIt Setup Assistant

Use the MoveIt 2 Setup Assistant to generate the MoveIt configuration:

```bash
cd ~/Workspace/
source install/setup.bash
ros2 launch moveit_setup_assistant setup_assistant.launch.py
```

### 7. Export Configuration to MoveIt Package

Export the generated configuration to a new package, ideally named:

```
<your_robot_name>_moveit_config
```

Place it inside the `src` folder and build the workspace again.

```bash
colcon build
source install/setup.bash
```

### 8. Add Controllers and Launch Files

Modify the MoveIt config package:

- Add appropriate controllers (e.g., `ros2_control`)
    
- Include a launch file (e.g., `demo.launch.py`) to spawn the robot and start the MoveIt planning pipeline
    

Example launch command:

```bash
ros2 launch <your_robot_name>_moveit_config demo.launch.py
```

---

## ✅ Running the Demo

After everything is set up, simply run:

```bash
cd ~/Workspace/
source install/setup.bash
ros2 launch <your_robot_name>_moveit_config demo.launch.py
```

You should see your robot model appear in RViz and be ready for motion planning using MoveIt 2.

---

