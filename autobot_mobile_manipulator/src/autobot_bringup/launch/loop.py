import time
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import FollowWaypoints
from rclpy.action import ActionClient

class WaypointNavigator(Node):
    def __init__(self):
        super().__init__('waypoint_navigator')
        self.client = ActionClient(self, FollowWaypoints, 'follow_waypoints')
        self.client.wait_for_server()
        self.send_waypoints()

    def send_waypoints(self):
        goal = FollowWaypoints.Goal()
        goal.poses = self.generate_waypoints()
        
        for _ in range(50 * 60):  # Loop for 50 hours (assuming 1 min per loop)
            future = self.client.send_goal_async(goal)
            rclpy.spin_until_future_complete(self, future)
            time.sleep(60)  # Wait a minute before restarting loop

    def generate_waypoints(self):
        waypoints = []
        positions = [(0.0, 0.0), (0.0, 15.0), (-3.0, 0.0), (0.0, -15.0), (3.0, 0.0)]  # Define your loop path
        for x, y in positions:
            pose = PoseStamped()
            pose.header.frame_id = 'map'
            pose.pose.position.x = x
            pose.pose.position.y = y
            pose.pose.orientation.w = 1.0
            waypoints.append(pose)
        return waypoints

def main(args=None):
    rclpy.init(args=args)
    navigator = WaypointNavigator()
    rclpy.spin(navigator)
    navigator.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
