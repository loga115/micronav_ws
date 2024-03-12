import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial
import time

class SerialBiDirectional(Node):
    def __init__(self):
        super().__init__('serial_bidirectional')
        self.serial_port = '/dev/ttyS0'  # Update this with your actual serial port
        self.serial_baudrate = 9600  # Update this with your ESP8266 baudrate
        self.serial_connection = serial.Serial(self.serial_port, self.serial_baudrate)
        time.sleep(2)  # Wait for the serial connection to be established
        self.get_logger().info('Serial com established')
        self.publisher_ = self.create_publisher(String, 'esp8266_data', 10)
        self.subscription = self.create_subscription(
            String,
            'esp8266_commands',
            self.receive_command_callback,
            10)

    def receive_command_callback(self, msg):
        command = msg.data
        self.get_logger().info('Received command: %s' % command)
        self.serial_connection.write(command.encode())

    def publish_serial_data(self):
        if self.serial_connection.is_open:
            try:
                line = self.serial_connection.readline().decode('utf-8').strip()
                self.get_logger().info('Received data from ESP8266: %s' % line)
                msg = String()
                msg.data = line
                self.publisher_.publish(msg)
            except serial.SerialException as e:
                self.get_logger().error('Serial connection error: %s' % str(e))

def main(args=None):
    rclpy.init(args=args)
    serial_bidirectional = SerialBiDirectional()
    rclpy.spin(serial_bidirectional)
    serial_bidirectional.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
