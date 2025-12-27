#! /usr/bin/env python
#coding:utf-8
#1.导包
import rospy
from turtlesim.srv import Spawn, SpawnRequest, SpawnResponse

if __name__ == "__main__":
    # 2.初始化 ros 结点
    rospy.init_node("service_call_p")
    # 3.创建服务客户端
    client = rospy.ServiceProxy("/spawn",Spawn)
    # 4.等待服务启动
    req = SpawnRequest()
    # 5.创建请求数据
    req.x = 4.5
    req.y = 2.0
    req.theta = -3
    req.name = "turtle2"
    client.wait_for_service()
    # 6.发送请求并处理响应
    try:
        response = client.call(req)
        rospy.loginfo("乌龟创建成功，名字是:%s",response.name)
    except Exception as e:
        rospy.logerr("服务调用失败....")

