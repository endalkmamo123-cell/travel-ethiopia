"""Write robot SDF, world and a simple ROS2 controller into the folder."""
import os

BASE_DIR = os.path.dirname(__file__)

def write(path, content):
    with open(os.path.join(BASE_DIR, path), "w", encoding="utf-8") as f:
        f.write(content)

def main():
    write("three_wheel_bot.sdf", THREE_WHEEL_SDF)
    write("empty_world.sdf", EMPTY_WORLD_SDF)
    write("cmd_vel_controller.py", CMD_VEL_PY)
    print("Wrote three_wheel_bot.sdf, empty_world.sdf, cmd_vel_controller.py")
    print("Launch Ignition:    ign gazebo empty_world.sdf")
    print("Or Classic Gazebo:  gazebo empty_world.sdf")
    print("Run ROS2 publisher (after sourcing): python3 cmd_vel_controller.py")

# --- file contents ---
THREE_WHEEL_SDF = r'''<?xml version="1.0" ?>
<sdf version="1.9">
  <model name="three_wheel_bot">
    <pose>0 0 0.05 0 0 0</pose>
    <static>false</static>

    <!-- Base -->
    <link name="base_link">
      <pose>0 0 0.05 0 0 0</pose>
      <inertial>
        <mass>6.0</mass>
        <inertia>
          <ixx>0.12</ixx><iyy>0.12</iyy><izz>0.2</izz>
        </inertia>
      </inertial>
      <collision name="base_collision">
        <geometry><box><size>0.35 0.25 0.1</size></box></geometry>
      </collision>
      <visual name="base_visual">
        <geometry><box><size>0.35 0.25 0.1</size></box></geometry>
      </visual>
    </link>

    <!-- Wheels -->
    <link name="left_wheel">
      <pose>0 -0.13 0.05 0 0 0</pose>
      <inertial><mass>0.6</mass><inertia><ixx>0.002</ixx><iyy>0.004</iyy><izz>0.004</izz></inertia></inertial>
      <collision name="left_wheel_collision"><geometry><cylinder><radius>0.05</radius><length>0.03</length></cylinder></geometry></collision>
      <visual name="left_wheel_visual"><geometry><cylinder><radius>0.05</radius><length>0.03</length></cylinder></geometry></visual>
    </link>

    <link name="right_wheel">
      <pose>0 0.13 0.05 0 0 0</pose>
      <inertial><mass>0.6</mass><inertia><ixx>0.002</ixx><iyy>0.004</iyy><izz>0.004</izz></inertia></inertial>
      <collision name="right_wheel_collision"><geometry><cylinder><radius>0.05</radius><length>0.03</length></cylinder></geometry></collision>
      <visual name="right_wheel_visual"><geometry><cylinder><radius>0.05</radius><length>0.03</length></cylinder></geometry></visual>
    </link>

    <!-- Front caster -->
    <link name="front_caster">
      <pose>0.15 0 0.03 0 0 0</pose>
      <inertial><mass>0.3</mass><inertia><ixx>0.001</ixx><iyy>0.001</iyy><izz>0.001</izz></inertia></inertial>
      <collision name="caster_collision"><geometry><sphere><radius>0.03</radius></sphere></geometry></collision>
      <visual name="caster_visual"><geometry><sphere><radius>0.03</radius></sphere></geometry></visual>
    </link>

    <!-- Joints -->
    <joint name="left_wheel_joint" type="revolute">
      <parent>base_link</parent><child>left_wheel</child>
      <axis><xyz>0 1 0</xyz><dynamics><damping>0.01</damping></dynamics></axis>
    </joint>

    <joint name="right_wheel_joint" type="revolute">
      <parent>base_link</parent><child>right_wheel</child>
      <axis><xyz>0 1 0</xyz><dynamics><damping>0.01</damping></dynamics></axis>
    </joint>

    <joint name="caster_joint" type="revolute">
      <parent>base_link</parent><child>front_caster</child>
      <axis><xyz>0 0 1</xyz><dynamics><damping>0.05</damping></dynamics></axis>
    </joint>

    <!-- Sensor mount -->
    <link name="sensor_mount">
      <pose>0.12 0 0.14 0 0 0</pose>
      <inertial><mass>0.2</mass><inertia><ixx>0.0005</ixx><iyy>0.0005</iyy><izz>0.0005</izz></inertia></inertial>

      <!-- IMU -->
      <sensor name="imu" type="imu">
        <update_rate>200</update_rate>
        <always_on>true</always_on>
        <plugin name="imu_plugin" filename="gz-sensors-imu-system"><topic>/imu/data</topic></plugin>
      </sensor>

      <!-- RGB camera -->
      <sensor name="camera" type="camera">
        <update_rate>30</update_rate>
        <camera><horizontal_fov>1.047</horizontal_fov><image><width>640</width><height>480</height><format>R8G8B8</format></image><clip><near>0.05</near><far>50</far></clip></camera>
        <plugin name="camera_plugin" filename="gz-sensors-camera-system"><topic>/camera/image_raw</topic></plugin>
      </sensor>

      <!-- Planar LiDAR (proximity) -->
      <sensor name="lidar" type="gpu_lidar">
        <update_rate>20</update_rate>
        <ray>
          <scan><horizontal><samples>360</samples><min_angle>-1.57</min_angle><max_angle>1.57</max_angle></horizontal></scan>
          <range><min>0.02</min><max>12.0</max></range>
        </ray>
        <plugin name="lidar_plugin" filename="gz-sensors-gpu-lidar-system"><topic>/scan</topic></plugin>
      </sensor>
    </link>

    <joint name="sensor_mount_joint" type="fixed"><parent>base_link</parent><child>sensor_mount</child></joint>

    <!-- Differential drive plugin (Ignition/Gazebo garden style) -->
    <plugin name="diff_drive" filename="gz-sim-diff-drive-system">
      <left_joint>left_wheel_joint</left_joint>
      <right_joint>right_wheel_joint</right_joint>
      <wheel_separation>0.26</wheel_separation>
      <wheel_radius>0.05</wheel_radius>
      <cmd_vel_topic>/cmd_vel</cmd_vel_topic>
      <odom_topic>/odom</odom_topic>
      <odom_publish_frequency>50</odom_publish_frequency>
      <robot_base_frame>base_link</robot_base_frame>
    </plugin>

  </model>
</sdf>
'''

EMPTY_WORLD_SDF = r'''<?xml version="1.0" ?>
<sdf version="1.9">
  <world name="three_wheel_world">
    <gravity>0 0 -9.81</gravity>
    <physics name="ode" type="ode">
      <real_time_update_rate>1000</real_time_update_rate>
      <max_step_size>0.001</max_step_size>
      <ode><solver><type>quick</type><iters>50</iters></solver></ode>
    </physics>

    <include><uri>model://ground_plane</uri></include>
    <include><uri>model://sun</uri></include>

    <!-- Spawn robot -->
    <include><uri>file://three_wheel_bot.sdf</uri></include>

    <gui fullscreen="false"/>
  </world>
</sdf>
'''

CMD_VEL_PY = r'''#!/usr/bin/env python3
import rclpy, signal, sys, math
from rclpy.node import Node
from geometry_msgs.msg import Twist

class SimpleController(Node):
    def __init__(self):
        super().__init__('simple_controller')
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.tick)
        self.t = 0.0

    def tick(self):
        msg = Twist()
        msg.linear.x = 0.2
        msg.angular.z = 0.25 * math.sin(self.t)
        self.pub.publish(msg)
        self.t += 0.1

def main():
    rclpy.init()
    node = SimpleController()
    def shutdown(signum, frame):
        node.get_logger().info('Shutting down')
        rclpy.shutdown()
        sys.exit(0)
    signal.signal(signal.SIGINT, shutdown)
    rclpy.spin(node)

if __name__ == '__main__':
    main()
'''
# --- Figure 5 world generation ---
FIGURE5_COORDS = {
    "Addis_Ababa": (0.0, 0.0),
    "Debre_Birhan": (2.0, 3.0),
    "Ambo": (-2.0, 1.0),
    "Nekemte": (-8.0, 5.0),
    "Gimbi": (-9.0, 4.0),
    "Dembi_Dolo": (-11.0, 6.0),
    "Gambella": (-13.0, 7.0),
    "Gore": (-10.0, 3.0),
    "Tepi": (-9.0, 2.0),
    "Mizan_Teferi": (-8.0, 1.0),
    "Bonga": (-7.0, 0.0),
    "Jimma": (-6.0, 1.0),
    "Bedelle": (-8.0, 3.0),
    "Wolaita_Sodo": (-3.0, -3.0),
    "Dawro": (-4.5, -1.5),
    "Dilla": (-2.0, -6.0),
    "Hawassa": (1.0, -3.0),
    "Hossana": (0.0, -1.0),
    "Shashemene": (1.0, -1.0),
    "Butajira": (0.5, 0.2),
    "Wolkite": (-1.0, 0.0),
    "Assela": (3.0, 0.5),
    "Adama": (4.0, 1.0),
    "Matahara": (5.0, 1.5),
    "Awash": (6.0, 2.5),
    "Chiro": (7.0, 3.0),
    "Dire_Dawa": (9.0, 3.5),
    "Harar": (8.0, 2.5),
    "Babille": (9.0, 2.0),
    "Jigjiga": (11.0, 3.5),
    "Dega_Habur": (10.0, 1.5),
    "Kebri_Dehar": (9.0, 0.5),
    "Gode": (11.0, -1.0),
    "Goba": (4.0, -1.5),
    "Dodolla": (3.0, -1.0),
    "Assasa": (2.0, -0.5),
    "Bale": (5.0, -2.0),
    "Sof_Oumer": (5.0, -1.8),
}

COLORS = [
    "0.8 0.2 0.2",
    "0.6 0.6 0.2",
    "0.3 0.6 0.9",
    "0.4 0.8 0.4",
    "0.9 0.6 0.3",
    "0.6 0.3 0.9",
    "0.3 0.8 0.9",
]


def build_figure5_world(coords):
    """Generate an SDF world string placing a small sphere at each coordinate."""
    header = (
        "<?xml version=\"1.0\" ?>\n"
        "<sdf version=\"1.9\">\n"
        "  <!--\n"
        "  Traveling Ethiopia (Figure 5) -- Cartesian coordinates (meters)\n"
        "  Mapping (city -> (x, y)):\n"
    )
    for name, (x, y) in coords.items():
        header += f"    {name}: ({x}, {y})\n"
    header += (
        "  -->\n"
        "  <world name=\"traveling_ethiopia_figure5\">\n"
        "    <gravity>0 0 -9.81</gravity>\n"
        "    <physics name=\"ode\" type=\"ode\">\n"
        "      <real_time_update_rate>1000</real_time_update_rate>\n"
        "      <max_step_size>0.001</max_step_size>\n"
        "    </physics>\n\n"
        "    <include><uri>model://ground_plane</uri></include>\n"
        "    <include><uri>model://sun</uri></include>\n\n"
    )

    body = ""
    z = 0.12
    for i, (name, (x, y)) in enumerate(coords.items()):
        color = COLORS[i % len(COLORS)]
        body += (
            f'    <model name="{name}">\n'
            "      <static>true</static>\n"
            f"      <pose>{x} {y} {z} 0 0 0</pose>\n"
            "      <link name=\"l\">\n"
            "        <visual name=\"v\">\n"
            "          <geometry><sphere><radius>0.12</radius></sphere></geometry>\n"
            f"          <material><ambient>{color} 1</ambient></material>\n"
            "        </visual>\n"
            "      </link>\n"
            "    </model>\n"
        )

    footer = (
        "\n    <gui fullscreen=\"false\"/>\n"
        "  </world>\n"
        "</sdf>\n"
    )
    return header + body + footer


def main():
    write("three_wheel_bot.sdf", THREE_WHEEL_SDF)
    write("empty_world.sdf", EMPTY_WORLD_SDF)
    write("cmd_vel_controller.py", CMD_VEL_PY)
    write("figure5_traveling.world", build_figure5_world(FIGURE5_COORDS))
    print("Wrote three_wheel_bot.sdf, empty_world.sdf, cmd_vel_controller.py, figure5_traveling.world")
    print("Launch Ignition:    ign gazebo empty_world.sdf")
    print("Or Classic Gazebo:  gazebo empty_world.sdf")
    print("Run ROS2 publisher (after sourcing): python3 cmd_vel_controller.py")


if __name__ == "__main__":
    main()