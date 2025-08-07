import serial
import threading
import serial.tools.list_ports

class SerialManager:
    def __init__(self, app):
        self.app = app
        self.ser = None
        self.thread = None
        self.running = False

    def list_ports(self):
        return [f"{p.device} - {p.description}" for p in serial.tools.list_ports.comports()]

    def connect(self, port_str):
        if not port_str:
            return
        port = port_str.split(" - ")[0]
        try:
            self.ser = serial.Serial(port=port, baudrate=9600, timeout=1)
            self.running = True
            self.thread = threading.Thread(target=self.read_loop, daemon=True)
            self.thread.start()
            self.app.btn_disconnect.config(state="normal")
            self.app.combo_ports.config(state="disabled")
        except Exception as e:
            self.app.text_serial.insert("end", f"连接失败: {e}\n")

    def read_loop(self):
        while self.running and self.ser:
            if self.ser.in_waiting > 0:
                data = self.ser.readline().decode(errors='ignore').strip()
                self.app.latest_weight = data
                self.app.label_weight.config(text=f"当前重量：{data}")
                self.app.text_serial.insert("end", f"{data}\n")
                self.app.text_serial.see("end")

    def disconnect(self):
        self.running = False
        if self.ser:
            self.ser.close()
            self.ser = None
        self.app.btn_disconnect.config(state="disabled")
        self.app.combo_ports.config(state="readonly")
        self.app.text_serial.insert("end", "串口已断开\n")

    def close(self):
        self.disconnect()
