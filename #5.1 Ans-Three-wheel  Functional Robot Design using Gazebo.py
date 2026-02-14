"""
Helper: write SDF/world and a small ROS2 controller into the working directory.

Usage:
    python #Q5.1\ Answer.py
Then launch Ignition/Gazebo with the generated empty_world.sdf:
    ign gazebo empty_world.sdf   # or `gazebo` depending on your Gazebo/Ignition version

If using ROS 2, run the cmd_vel_controller.py node:
    ros2 run <your_package> cmd_vel_controller.py
(Or run it directly after sourcing ROS 2.)
"""
import os
BASE_DIR = os.path.dirname(__file__)

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    # Write SDF, world and controller
    write_file(os.path.join(BASE_DIR, "three_wheel_bot.sdf"), THREE_WHEEL_SDF)
    write_file(os.path.join(BASE_DIR, "empty_world.sdf"), EMPTY_WORLD_SDF)
    write_file(os.path.join(BASE_DIR, "cmd_vel_controller.py"), CMD_VEL_PY)
    print("Wrote three_wheel_bot.sdf, empty_world.sdf, cmd_vel_controller.py in", BASE_DIR)
    print("Launch Ignition/Gazebo with: ign gazebo empty_world.sdf   (or use `gazebo` if using classic Gazebo)")
    print("Run ROS2 node (after sourcing): python3 cmd_vel_controller.py")

# --- File contents ---
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
          <ixy>0</ixy><ixz>0</ixz><iyz>0</iyz>
        </inertia>
      </inertial>
      <collision name="base_collision">
        <geometry>
          <box><size>0.35 0.25 0.1</size></box>
        </geometry>
        <surface>
          <friction>
            <ode>
              <mu>1.0</mu><mu2>1.0</mu2>
            </ode>
          </friction>
          <bounce><restitution_coeff>0.0</restitution_coeff></bounce>
        </surface>
      </collision>
      <visual name="base_visual">
        <geometry>
          <box><size>0.35 0.25 0.1</size></box>
        </geometry>
        <material><ambient>0.2 0.2 0.2 1</ambient></material>
      </visual>
    </link>

    <!-- Left driven wheel -->
    <link name="left_wheel">
      <pose>0 -0.13 0.05 0 0 0</pose>
      <inertial>
        <mass>0.6</mass>
        <inertia>
          <ixx>0.002</ixx><iyy>0.004</iyy><izz>0.004</izz>
        </inertia>
      </inertial>
      <collision name="left_wheel_collision">
        <geometry><cylinder><radius>0.05</radius><length>0.03</length></cylinder></geometry>
      </collision>
      <visual name="left_wheel_visual">
        <geometry><cylinder><radius>0.05</radius><length>0.03</length></cylinder></geometry>
        <material><ambient>0.0 0.0 0.0 1</ambient></material>
      </visual>
    </link>

    <!-- Right driven wheel -->
    <link name="right_wheel">
      <pose>0 0.13 0.05 0 0 0</pose>
      <inertial>
        <mass>0.6</mass>
        <inertia>
          <ixx>0.002</ixx><iyy>0.004</iyy><izz>0.004</izz>
        </inertia>
      </inertial>
      <collision name="right_wheel_collision">
        <geometry><cylinder><radius>0.05</radius><length>0.03</length></cylinder></geometry>
      </collision>
      <visual name="right_wheel_visual">
        <geometry><cylinder><radius>0.05</radius><length>0.03</length></cylinder></geometry>
        <material><ambient>0.0 0.0 0.0 1</ambient></material>
      </visual>
    </link>

    <!-- Front caster (passive) -->
    <link name="front_caster">
      <pose>0.15 0 0.03 0 0 0</pose>
      <inertial>
        <mass>0.3</mass>
        <inertia>
          <ixx>0.001</ixx><iyy>0.001</iyy><izz>0.001</izz>
        </inertia>
      </inertial>
      <collision name="caster_collision">
        <geometry><sphere><radius>0.03</radius></sphere></geometry>
      </collision>
      <visual name="caster_visual">
        <geometry><sphere><radius>0.03</radius></sphere></geometry>
        <material><ambient>0.3 0.3 0.3 1</ambient></material>
      </visual>
    </link>

    <!-- Wheel joints -->
    <joint name="left_wheel_joint" type="revolute">
      <parent>base_link</parent><child>left_wheel</child>
      <pose>0 -0.13 0.05 0 0 0</pose>
      <axis><xyz>0 1 0</xyz>
        <limit><lower>-1e16</lower><upper>1e16</upper></limit>
        <dynamics><damping>0.01</damping></dynamics>
      </axis>
    </joint>
    <joint name="right_wheel_joint" type="revolute">
      <parent>base_link</parent><child>right_wheel</child>
      <pose>0 0.13 0.05 0 0 0</pose>
      <axis><xyz>0 1 0</xyz>
        <limit><lower>-1e16</lower><upper>1e16</upper></limit>
        <dynamics><damping>0.01</damping></dynamics>
      </axis>
    </joint>
    <joint name="caster_joint" type="revolute">
      <parent>base_link</parent><child>front_caster</child>
      <pose>0.15 0 0.03 0 0 0</pose>
      <axis><xyz>0 0 1</xyz><dynamics><damping>0.05</damping></dynamics></axis>
    </joint>

    <!-- Sensor mount link -->
    <link name="sensor_mount">
      <pose>0.15 0 0.12 0 0 0</pose>
      <inertial><mass>0.2</mass><inertia><ixx>0.0005</ixx><iyy>0.0005</iyy><izz>0.0005</izz></inertia></inertial>
    </link>
    <joint name="sensor_mount_joint" type="fixed">
      <parent>base_link</parent><child>sensor_mount</child>
      <pose>0 0 0 0 0 0</pose>
    </joint>

    <!-- IMU -->
    <sensor name="imu" type="imu">
      <pose>0 0 0 0 0 0</pose>
      <update_rate>100</update_rate>
      <always_on>true</always_on>
      <plugin name="imu_plugin" filename="gz-sensors-imu-system">
        <topic>/imu/data</topic>
      </plugin>
    </sensor>

    <!-- RGB camera -->
    <sensor name="camera" type="camera">
      <pose>0.05 0 0.02 0 0 0</pose>
      <update_rate>30</update_rate>
      <camera>
        <horizontal_fov>1.047</horizontal_fov>
        <image><width>640</width><height>480</height><format>R8G8B8</format></image>
        <clip><near>0.05</near><far>50</far></clip>
      </camera>
      <plugin name="camera_plugin" filename="gz-sensors-camera-system">
        <topic>/camera/image_raw</topic>
      </plugin>
    </sensor>

    <!-- Planar LiDAR -->
    <sensor name="lidar" type="gpu_lidar">
      <pose>0 0 0.05 0 0 0</pose>
      <update_rate>15</update_rate>
      <ray>
        <scan><horizontal><samples>720</samples><resolution>1</resolution><min_angle>-1.57</min_angle><max_angle>1.57</max_angle></horizontal></scan>
        <range><min>0.05</min><max>15.0</max></range>
      </ray>
      <plugin name="lidar_plugin" filename="gz-sensors-gpu-lidar-system">
        <topic>/scan</topic>
      </plugin>
    </sensor>

    <!-- Differential drive control plugin
         Note: on Classic Gazebo you might use `libgazebo_ros_diff_drive.so` and a gazebo_ros_control setup.
         For Ignition / Gazebo Garden use the appropriate `gz` plugin (name may vary by distro). -->
    <plugin name="diff_drive" filename="gz-sim-diff-drive-system">
      <left_joint>left_wheel_joint</left_joint>
      <right_joint>right_wheel_joint</right_joint>
      <wheel_separation>0.26</wheel_separation>
      <wheel_radius>0.05</wheel_radius>
      <odom_publish_frequency>50</odom_publish_frequency>
      <cmd_vel_topic>/cmd_vel</cmd_vel_topic>
      <odom_topic>/odom</odom_topic>
      <robot_base_frame>base_link</robot_base_frame>
    </plugin>

  </model>
</sdf>
'''

EMPTY_WORLD_SDF = r'''<?xml version="1.0" ?>
<sdf version="1.9">
  <world name="ethiopia_relaxed_world">
    <gravity>0 0 -9.81</gravity>
    <physics name="ode" type="ode">
      <real_time_update_rate>1000</real_time_update_rate>
      <max_step_size>0.001</max_step_size>
      <ode>
        <solver><type>quick</type><iters>50</iters><sor>1.3</sor></solver>
        <constraints><cfm>0.0</cfm><erp>0.2</erp><contact_max_correcting_vel>100</contact_max_correcting_vel></constraints>
      </ode>
    </physics>

    <include><uri>model://ground_plane</uri></include>
    <include><uri>model://sun</uri></include>

    <include><uri>file://three_wheel_bot.sdf</uri></include>

    <gui fullscreen="false"/>
  </world>
</sdf>
'''

CMD_VEL_PY = r'''#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math
import signal
import sys

class SimpleController(Node):
    def __init__(self):
        super().__init__('simple_controller')
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.tick)
        self.t = 0.0

    def tick(self):
        msg = Twist()
        msg.linear.x = 0.2
        msg.angular.z = 0.3 * math.sin(self.t)
        self.pub.publish(msg)
        self.t += 0.1

def main():
    rclpy.init()
    node = SimpleController()
    # graceful shutdown on Ctrl-C
    def shutdown(signum, frame):
        node.get_logger().info('Shutting down controller...')
        node.destroy_node()
        rclpy.shutdown()
        sys.exit(0)
    signal.signal(signal.SIGINT, shutdown)
    rclpy.spin(node)

if __name__ == '__main__':
    main()
'''

if __name__ == "__main__":
    main()
