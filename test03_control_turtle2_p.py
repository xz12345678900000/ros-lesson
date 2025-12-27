#! /usr/bin/env python
#coding:utf-8
# 1.导包
import rospy
import tf2_ros
from tf2_geometry_msgs import tf2_geometry_msgs
from geometry_msgs.msg import TransformStamped,Twist
import math

if __name__ == "__main__":
    # 2.初始化 ros 结点
    rospy.init_node("ststic_sub_p")
    # 3.创建 TF 订阅对象
    buffer = tf2_ros.Buffer()
    sub = tf2_ros.TransformListener(buffer)
    # 4.处理订阅到的 TF
    rate = rospy.Rate(10)
    # 创建速度发布对象
    pub = rospy.Publisher("/turtle2/cmd_vel",Twist,queue_size=1000)
    while not rospy.is_shutdown():
        try:
           #计算turtle1相对于turtle2的坐标关系
            ts = buffer.lookup_transform("turtle2","turtle1",rospy.Time(0))
            rospy.loginfo("father:%s,son:%s,pil(%.2f,%.2f,%.2f)",
                    ts.header.frame_id,
                    ts.child_frame_id,
                    ts.transform.translation.x,
                    ts.transform.translation.y,
                    ts.transform.translation.z,
                    )
            # 根据转变后的坐标计算出速度和角速度信息
            twist = Twist()
            # 间距 = x^2 + y^2  然后开方
            twist.linear.x = 0.5 * math.sqrt(math.pow(ts.transform.translation.x,2) + math.pow(ts.transform.translation.y,2))
            twist.angular.z = 4 * math.atan2(ts.transform.translation.y, ts.transform.translation.x)
            pub.publish(twist)
        except Exception as e:
            rospy.logwarn("警告:%s",e)
        rate.sleep()

