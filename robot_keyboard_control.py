#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import sys, select, termios, tty

# 键盘按键与速度的映射
moveBindings = {
    'i': (1, 0, 0, 0),   # 前进
    'o': (1, 0, 0, -1),
    'j': (0, 0, 0, 1),   # 左转
    'l': (0, 0, 0, -1),  # 右转
    'u': (1, 0, 0, 1),
    ',': (-1, 0, 0, 0),  # 后退
    '.': (-1, 0, 0, 1),
    'm': (-1, 0, 0, -1),
    'k': (0, 0, 0, 0),   # 停止
}

def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)
    
    rospy.init_node('robot_keyboard_control')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10) # 发布到/cmd_vel话题
    
    speed = 0.5
    turn = 1.0
    x = 0; y = 0; z = 0; th = 0
    
    try:
        print("使用键盘控制机器人!")
        print("i:前进 , :后退 j:左转 l:右转 k:停止 q:退出")
        while not rospy.is_shutdown():
            key = getKey()
            if key in moveBindings.keys():
                x = moveBindings[key][0] * speed
                th = moveBindings[key][3] * turn
            elif key == 'q':  # 按q退出
                break
            
            # 创建并发布速度消息
            twist = Twist()
            twist.linear.x = x; twist.linear.y = y; twist.linear.z = z
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = th
            pub.publish(twist)
            
    except Exception as e:
        print(e)
    finally:
        # 退出前发布停止指令
        twist = Twist()
        pub.publish(twist)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
