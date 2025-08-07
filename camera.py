import os
import ctypes

DLL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "resources", "CamLib.dll"))
os.add_dll_directory(os.path.dirname(DLL_PATH))
camlib = ctypes.WinDLL(DLL_PATH)

class CameraManager:
    def __init__(self, app):
        self.app = app
        self.device_index = 0

    def init_camera(self):
        if camlib.eInitLib() < 0:
            self.app.destroy()
        if camlib.eGetCameraCount() == 0:
            self.app.destroy()
        hwnd = self.app.video_frame.winfo_id()
        if camlib.eOpenCamera(self.device_index, hwnd) < 0:
            self.app.destroy()

    def capture(self, save_path):
        return camlib.eCapture(self.device_index, save_path.encode('gbk')) >= 0

    def close(self):
        camlib.eCloseCamera(self.device_index)
        camlib.eUninitLib()
