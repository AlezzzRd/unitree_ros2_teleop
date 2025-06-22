import rclpy
import pinocchio as pin      

class RobotControl(Node):
    def __init__(self):
        super().__init__('robot_control_node')
        self.robot = pin.RobotWrapper.BuildFromURDF('/home/rundong/avp_teleoperation/workspace/src/unitree_robot_description/urdf/g1/g1_body29_hand14.urdf', \
                                                    '/home/rundong/avp_teleoperation/workspace/src/unitree_robot_description/urdf/g1/')

def main(args=None):
    rclpy.init(args=args)
    node = RobotControl()
    
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