## Ethiopia Search Problem ROS 2 Simulation

This repository contains a ROS 2 (Python, `ament_python`) simulation of the Ethiopia travelling/search problem using a three-wheel robot in Gazebo Sim (gz) on **ROS 2 Jazzy**.

### Layout

- **ros_ws/**: ROS 2 workspace
  - **src/ethiopia_sim/**: ROS 2 package
    - `launch/sim_launch.py`: launches Gazebo Sim and loads the Ethiopia world
    - `urdf/three_wheel_robot.urdf`: three-wheel robot model with sensors
    - `worlds/ethiopia.world`: relaxed state-space world with all cities as models
    - `ethiopia_sim/`: Python module containing the search, graph, navigator, and verification utilities

### Prereqs (Ubuntu / ROS 2 Jazzy)

Install Gazebo Sim integration for Jazzy:

```bash
sudo apt-get update
sudo apt-get install ros-jazzy-ros-gz
```

### Build and Run (Linux / ROS 2 Jazzy)

```bash
cd ros_ws
colcon build
source install/setup.bash
ros2 launch ethiopia_sim sim_launch.py
```

From another terminal you can then run (examples):

```bash
cd ros_ws
source install/setup.bash
ros2 run ethiopia_sim navigator
ros2 run ethiopia_sim search_node
ros2 run ethiopia_sim verify_graph
```

Notes:
- `sim_launch.py` starts Gazebo Sim and `robot_state_publisher`. If you want to spawn the URDF into Gazebo Sim, extend the launch file to call `ros_gz_sim spawn_entity/create`.
