# coding=utf-8
import threading

from face_recognition import detect_face
from audio_recorder import record_audio, transfer_file
from speech_recognition import recognize_speech, speak_text
from sensor import wait_for_sensor
from say import speak_answer, speak_thinking
from ai import generate_answer  # 导入 ai.py 中的 generate_answer 函数

def main():
    print("等待人脸识别...")
    if detect_face(speak_text):
        print("人脸识别成功，进入操作模式...")

    while True:
        wait_for_sensor()
        record_audio()
        transfer_file()
        recognize_speech()

        # 启动一个子线程，让NAO机器人发声
        thinking_thread = threading.Thread(target=speak_thinking)
        thinking_thread.start()

        generate_answer()  # 在 recognize_speech() 执行结束后调用 generate_answer()
        speak_answer()
        print("任务完成，返回待命状态...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("程序被手动中断，退出。")