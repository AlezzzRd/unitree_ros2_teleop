#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from visualization_msgs.msg import InteractiveMarker, InteractiveMarkerControl
from visualization_msgs.msg import InteractiveMarkerFeedback
from interactive_markers import InteractiveMarkerServer
from geometry_msgs.msg import PoseStamped, Pose, Point, Quaternion
from std_msgs.msg import Header
import tf_transformations
import numpy as np

class InteractiveMarkerNode(Node):
    def __init__(self):
        super().__init__('interactive_marker_node')
        
        # 创建交互标记服务器
        self.marker_server = InteractiveMarkerServer(self, "interactive_marker")
        
        # 创建位姿发布器
        self.pose_publisher = self.create_publisher(PoseStamped, 'marker_pose', 10)
        
        # 创建初始位姿
        self.marker_pose = Pose()
        self.marker_pose.position.x = 0.0
        self.marker_pose.position.y = 0.0
        self.marker_pose.position.z = 1.0
        self.marker_pose.orientation.w = 1.0  # 默认四元数 (无旋转)
        
        # 创建交互标记
        self.create_interactive_marker()
        
        # 设置反馈回调
        self.marker_server.setCallback(
            "unitree_marker", 
            self.marker_feedback_callback,
            InteractiveMarkerFeedback.POSE_UPDATE
        )
        
        self.get_logger().info("Interactive Marker 节点已启动. 在 RViz 中打开 InteractiveMarkers 显示插件查看")

    def create_interactive_marker(self):
        """创建交互式标记"""
        # 创建标记对象
        int_marker = InteractiveMarker()
        int_marker.header.frame_id = "world"  # 参考坐标系
        int_marker.name = "unitree_marker"
        int_marker.description = "Unitree Control Marker"
        int_marker.pose = self.marker_pose
        int_marker.scale = 0.5  # 标记大小

        # ================= 平移控制 =================
        # X轴平移
        move_x = InteractiveMarkerControl()
        move_x.orientation_mode = InteractiveMarkerControl.INHERIT
        move_x.interaction_mode = InteractiveMarkerControl.MOVE_AXIS
        q = tf_transformations.quaternion_from_euler(0, 0, 0)
        move_x.orientation.x = q[0]
        move_x.orientation.y = q[1]
        move_x.orientation.z = q[2]
        move_x.orientation.w = q[3]
        int_marker.controls.append(move_x)

        # Y轴平移
        move_y = InteractiveMarkerControl()
        move_y.orientation_mode = InteractiveMarkerControl.INHERIT
        move_y.interaction_mode = InteractiveMarkerControl.MOVE_AXIS
        q = tf_transformations.quaternion_from_euler(0, 0, np.pi/2)
        move_y.orientation.x = q[0]
        move_y.orientation.y = q[1]
        move_y.orientation.z = q[2]
        move_y.orientation.w = q[3]
        int_marker.controls.append(move_y)

        # Z轴平移
        move_z = InteractiveMarkerControl()
        move_z.orientation_mode = InteractiveMarkerControl.INHERIT
        move_z.interaction_mode = InteractiveMarkerControl.MOVE_AXIS
        q = tf_transformations.quaternion_from_euler(0, -np.pi/2, 0)
        move_z.orientation.x = q[0]
        move_z.orientation.y = q[1]
        move_z.orientation.z = q[2]
        move_z.orientation.w = q[3]
        int_marker.controls.append(move_z)

        # ================= 旋转控制 =================
        # X轴旋转
        rotate_x = InteractiveMarkerControl()
        rotate_x.orientation_mode = InteractiveMarkerControl.INHERIT
        rotate_x.interaction_mode = InteractiveMarkerControl.ROTATE_AXIS
        q = tf_transformations.quaternion_from_euler(0, 0, 0)
        rotate_x.orientation.x = q[0]
        rotate_x.orientation.y = q[1]
        rotate_x.orientation.z = q[2]
        rotate_x.orientation.w = q[3]
        int_marker.controls.append(rotate_x)

        # Y轴旋转
        rotate_y = InteractiveMarkerControl()
        rotate_y.orientation_mode = InteractiveMarkerControl.INHERIT
        rotate_y.interaction_mode = InteractiveMarkerControl.ROTATE_AXIS
        q = tf_transformations.quaternion_from_euler(0, 0, np.pi/2)
        rotate_y.orientation.x = q[0]
        rotate_y.orientation.y = q[1]
        rotate_y.orientation.z = q[2]
        rotate_y.orientation.w = q[3]
        int_marker.controls.append(rotate_y)

        # Z轴旋转
        rotate_z = InteractiveMarkerControl()
        rotate_z.orientation_mode = InteractiveMarkerControl.INHERIT
        rotate_z.interaction_mode = InteractiveMarkerControl.ROTATE_AXIS
        q = tf_transformations.quaternion_from_euler(0, -np.pi/2, 0)
        rotate_z.orientation.x = q[0]
        rotate_z.orientation.y = q[1]
        rotate_z.orientation.z = q[2]
        rotate_z.orientation.w = q[3]
        int_marker.controls.append(rotate_z)

        # ================= 可视化球体 =================
        sphere_control = InteractiveMarkerControl()
        sphere_control.always_visible = True
        sphere_control.interaction_mode = InteractiveMarkerControl.NONE
        
        # 创建球体标记
        from visualization_msgs.msg import Marker
        sphere_marker = Marker()
        sphere_marker.type = Marker.SPHERE
        sphere_marker.scale.x = 0.1
        sphere_marker.scale.y = 0.1
        sphere_marker.scale.z = 0.1
        sphere_marker.color.r = 0.0
        sphere_marker.color.g = 1.0
        sphere_marker.color.b = 0.0
        sphere_marker.color.a = 0.8  # 透明度
        sphere_control.markers.append(sphere_marker)
        int_marker.controls.append(sphere_control)

        # 将标记添加到服务器
        self.marker_server.insert(int_marker)
        self.marker_server.applyChanges()

    def marker_feedback_callback(self, feedback):
        """处理标记反馈"""
        # 只在位姿更新时处理
        if feedback.event_type == InteractiveMarkerFeedback.POSE_UPDATE:
            self.marker_pose = feedback.pose
            
            # 发布当前位姿
            pose_msg = PoseStamped()
            pose_msg.header = Header(frame_id="world", stamp=self.get_clock().now().to_msg())
            pose_msg.pose = feedback.pose
            self.pose_publisher.publish(pose_msg)
            
            # 日志输出
            pos = feedback.pose.position
            ori = feedback.pose.orientation
            self.get_logger().info(
                f"标记位姿更新: 位置({pos.x:.2f}, {pos.y:.2f}, {pos.z:.2f}) "
                f"方向({ori.x:.2f}, {ori.y:.2f}, {ori.z:.2f}, {ori.w:.2f})",
                throttle_duration_sec=0.5  # 节流输出
        )

def main(args=None):
    rclpy.init(args=args)
    node = InteractiveMarkerNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # 清理
        node.marker_server.shutdown()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()