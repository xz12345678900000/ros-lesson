#! /usr/bin/env python
#coding:utf-8
# 1.导包
import rospy
import sys
from turtlesim.msg import Pose
from geometry_msgs.msg import TransformStamped
import tf2_ros
import tf
#接收乌龟名字变量
turtle_name = ""

def doPose(pose):
    #1.创建坐标系广播器
    pub = tf2_ros.TransformBroadcaster()
    #2.将 pose 信息转换成 TransFormStamped
    ts = TransformStamped()
    ts.header.frame_id = "world"
    ts.header.stamp = rospy.Time.now()
    ts.child_frame_id = turtle_name
#子级坐标系相对于父级坐标系的偏移量
    ts.transform.translation.x = pose.x
    ts.transform.translation.y = pose.y
    ts.transform.translation.z = 0
#四元数
#从欧拉角转换四元数
    qtn = tf.transformations.quaternion_from_euler(0, 0, pose.theta)
    ts.transform.rotation.x = qtn[0]
    ts.transform.rotation.y = qtn[1]
    ts.transform.rotation.z = qtn[2]
    ts.transform.rotation.w = qtn[3]
    #3.广播器发布 tfs
    pub.sendTransform(ts)


if __name__ == "__main__":
    # 2.初始化 ros 结点
    rospy.init_node("dynamic_pub_p")
    # 3.解析传入的参数是否正确
    if len(sys.argv) !=4:
        rospy.loginfo("input wrong")
        sys.exit(1)
    else:
        turtle_name = sys.argv[1]
    sub=rospy.Subscriber(turtle_name + "/pose",Pose,doPose,queue_size=100)
    #     4.创建订阅对象
    #     5.回调函数处理订阅的 pose 信息
    #         5-1.创建 TF 广播器
    #         5-2.将 pose 信息转换成 TransFormStamped
    #         5-3.发布
#     6.spin
    rospy.spin()

