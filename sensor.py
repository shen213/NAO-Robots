# coding=utf-8
from naoqi import ALProxy
import time
from config import NAO_IP, NAO_PORT


def wait_for_sensor():
    print("等待触摸传感器触发...")
    memory = ALProxy("ALMemory", NAO_IP, NAO_PORT)

    triggered = False
    while True:
        sensor_value = memory.getData("Device/SubDeviceList/Head/Touch/Front/Sensor/Value")
        if sensor_value == 1.0:
            print("前传感器触发，开始操作...")
            return True

        # 检测后额头传感器，退出程序
        rear_sensor = memory.getData("Device/SubDeviceList/Head/Touch/Rear/Sensor/Value")
        if rear_sensor == 1.0:
            print("后传感器触发，正在退出程序...")
            exit(0)

        time.sleep(0.1)
