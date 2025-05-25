# coding=utf-8
from naoqi import ALProxy
import paramiko
import time
from config import NAO_IP, NAO_PORT, NAO_AUDIO_FILE, LOCAL_AUDIO_FILE, NAO_USERNAME, NAO_PASSWORD, DURATION


def record_audio():
    print("开始录音...")
    try:
        audio_recorder = ALProxy("ALAudioRecorder", NAO_IP, NAO_PORT)
        print("ALAudioRecorder 代理创建成功")
        audio_recorder.startMicrophonesRecording(NAO_AUDIO_FILE, 'wav', 16000, [0, 1, 0, 0])
        print("录音已开始")

        # 记录录音开始时间
        start_time = time.time()

        time.sleep(DURATION)
        audio_recorder.stopMicrophonesRecording()
        print("录音已停止")

        # 记录录音结束时间
        end_time = time.time()

        # 计算录音耗时（保留两位小数）
        elapsed_time = end_time - start_time
        print("录音耗时：{:.2f} 秒".format(elapsed_time))

    except Exception as e:
        print("录音失败：{}".format(str(e)))


def transfer_file():
    print("开始传输音频文件...")
    try:
        # 记录传输开始时间
        transfer_start_time = time.time()

        transport = paramiko.Transport((NAO_IP, 22))
        transport.connect(username=NAO_USERNAME, password=NAO_PASSWORD)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.get(NAO_AUDIO_FILE, LOCAL_AUDIO_FILE)
        sftp.close()
        transport.close()

        # 记录传输结束时间
        transfer_end_time = time.time()

        # 计算传输耗时（保留两位小数）
        transfer_elapsed_time = transfer_end_time - transfer_start_time
        print("音频文件传输完成")
        print("音频文件传输耗时：{:.2f} 秒".format(transfer_elapsed_time))

    except Exception as e:
        print("文件传输失败：{}".format(str(e)))


if __name__ == "__main__":
    record_audio()
    transfer_file()