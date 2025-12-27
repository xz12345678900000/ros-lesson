#!/usr/bin/env python3
import rospy
import tf
from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState
from nav_msgs.msg import Odometry
import math

class SimpleRobotSimulator:
    def __init__(self):
        rospy.init_node('robot_simulator')
        
        # 机器人初始位置和朝向
        self.x = 0.0
        self.y = 0.0
        self.th = 0.0  # 朝向角（偏航角）
        
        # 上一个更新时间
        self.last_time = rospy.Time.now()
        
        # 订阅速度指令
        rospy.Subscriber('/cmd_vel', Twist, self.cmd_vel_callback)
        
        # 发布虚拟关节状态（让robot_state_publisher能发布TF）
        self.joint_state_pub = rospy.Publisher('/joint_states', JointState, queue_size=10)
        
        # 也可以发布里程计信息（可选）
        self.odom_pub = rospy.Publisher('/odom', Odometry, queue_size=10)
        
        # 设置一个定时器，定期更新并发布机器人状态
        self.timer = rospy.Timer(rospy.Duration(0.05), self.timer_callback) # 20Hz
        
        rospy.loginfo("Simple Robot Simulator Started.")
        
    def cmd_vel_callback(self, msg):
        # 当收到速度指令时，更新内部速度状态
        # 注意：实际的积分计算在定时器回调里做，以保证固定的更新周期
        self.vx = msg.linear.x
        self.vth = msg.angular.z

    def timer_callback(self, event):
        current_time = rospy.Time.now()
        dt = (current_time - self.last_time).to_sec()
        self.last_time = current_time
        
        # 根据当前速度和dt，计算机器人新位姿（简单的欧拉积分）
        delta_x = self.vx * math.cos(self.th) * dt
        delta_y = self.vx * math.sin(self.th) * dt
        delta_th = self.vth * dt
        
        self.x += delta_x
        self.y += delta_y
        self.th += delta_th
        
        # 发布虚拟关节状态
        joint_state = JointState()
        joint_state.header.stamp = current_time
        joint_state.name = ['base_to_world']  # 一个虚拟的关节名
        joint_state.position = [0.0]          # 虚拟关节位置
        joint_state.velocity = []
        joint_state.effort = []
        self.joint_state_pub.publish(joint_state)
        
        # 发布TF变换：从“odom”坐标系到“base_link”坐标系
        br = tf.TransformBroadcaster()
        br.sendTransform((self.x, self.y, 0.0),
                         tf.transformations.quaternion_from_euler(0, 0, self.th),
                         current_time,
                         "base_link",
                         "odom")
        
        # 发布里程计消息（可选）
        odom = Odometry()
        odom.header.stamp = current_time
        odom.header.frame_id = "odom"
        odom.child_frame_id = "base_link"
        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.orientation.z = math.sin(self.th / 2.0)
        odom.pose.pose.orientation.w = math.cos(self.th / 2.0)
        self.odom_pub.publish(odom)

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    simulator = SimpleRobotSimulator()
    # 初始化速度为零
    simulator.vx = 0.0
    simulator.vth = 0.0
    simulator.run()
