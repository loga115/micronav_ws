import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class VideoPublisher(Node):
    def __init__(self):
        super().__init__('video_publisher')
        self.publisher_ = self.create_publisher(Image, 'camera/image_raw', 10)
        self.bridge = CvBridge()
        self.capture = cv2.VideoCapture(0)  # assuming the Pi camera is at index 0

    def publish_video(self):
        ret, frame = self.capture.read()
        if ret:
            msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
            self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    video_publisher = VideoPublisher()
    while rclpy.ok():
        video_publisher.publish_video()
        rclpy.spin_once(video_publisher)
    video_publisher.capture.release()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
