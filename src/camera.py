import ctypes
import os
import cv2
from tkinter import messagebox

# ========== DLL 路径 ==========
DLL_PATH = r"../resources/CamLib.dll"
os.add_dll_directory(os.path.dirname(DLL_PATH))
camlib = ctypes.WinDLL(DLL_PATH)

def init_camera():
    if camlib.eInitLib() < 0:
        raise Exception("初始化 SDK 失败")
    if camlib.eGetCameraCount() == 0:
        raise Exception("未检测到摄像头")

def open_camera(device_index, hwnd):
    if camlib.eOpenCamera(device_index, hwnd) < 0:
        raise Exception("打开摄像头失败")

def close_camera(device_index):
    camlib.eCloseCamera(device_index)
    camlib.eUninitLib()

def capture_image(device_index, save_path):
    result = camlib.eCapture(device_index, save_path.encode('gbk'))
    if result < 0:
        raise Exception(f"拍照失败，错误码: {result}")