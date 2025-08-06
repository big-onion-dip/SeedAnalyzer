import serial
import serial.tools.list_ports
import threading
from tkinter import messagebox

class SerialCommunication:
    def __init__(self):
        self.ser = None
        self.ser_running = False
        self.latest_weight = None

    def list_ports(self):
        return [f"{port.device} - {port.description}" for port in serial.tools.list_ports.comports()]

    def connect(self, port, baudrate=9600):
        try:
            self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=1)
            self.ser_running = True
            threading.Thread(target=self.read_serial).start()
        except Exception as e:
            raise Exception(f"连接串口失败: {str(e)}")

    def disconnect(self):
        self.ser_running = False
        if self.ser:
            self.ser.close()

    def read_serial(self):
        while self.ser_running and self.ser:
            if self.ser.in_waiting > 0:
                data = self.ser.readline().decode('utf-8', errors='ignore').rstrip()
                self.latest_weight = data
                # 这里可以添加更新界面的逻辑