# -*- coding:utf-8 -*-
import requests
import base64
import json
import io
import time  # 引入时间模块
from naoqi import ALProxy
from config import LOCAL_AUDIO_FILE, TEXT_FILE, NAO_IP, NAO_PORT

# 百度语音识别API参数
APP_ID = '118437579'
API_KEY = 'hEkfdHgmLXGwZiulxbhnOf1A'
SECRET_KEY = 'OiiwhrcTk65BiU49lDGgzumDAN9HddvC'
auth_url = "https://openapi.baidu.com/oauth/2.0/token"

# 获取百度语音识别的访问令牌
def get_access_token():
    params = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": SECRET_KEY
    }
    response = requests.post(auth_url, data=params)
    if response.status_code == 200:
        result = response.json()
        return result.get("access_token")
    else:
        print("获取访问令牌失败，状态码：", response.status_code)
        print("错误信息：", response.text)
        return None

# 语音识别函数
def recognize_speech():
    access_token = get_access_token()
    if not access_token:
        print("无法获取访问令牌，语音识别失败。")
        return

    # 读取音频文件
    try:
        with open(LOCAL_AUDIO_FILE, "rb") as audio_file:
            audio_data = audio_file.read()
    except IOError as e:
        print("读取音频文件失败：", e)
        return

    # 将音频数据编码为Base64
    audio_base64 = base64.b64encode(audio_data).decode('utf-8')

    # 构建请求参数
    params = {
        "format": "wav",
        "rate": 16000,
        "channel": 1,
        "cuid": "nao_robot",
        "token": access_token,
        "speech": audio_base64,
        "len": len(audio_data)
    }

    # 记录语音识别开始时间
    start_time = time.time()
    print("语音识别开始时间：", start_time)

    # 发送请求到百度语音识别API
    url = "http://vop.baidu.com/server_api"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(params))

    # 记录语音识别结束时间
    end_time = time.time()
    print("语音识别结束时间：", end_time)

    # 计算语音识别耗时（保留两位小数）
    elapsed_time = end_time - start_time
    print("语音识别耗时：{:.2f} 秒".format(elapsed_time))  # 保留两位小数

    if response.status_code == 200:
        result = response.json()
        if result.get("err_msg") == "success.":  # 识别成功
            text = result.get("result", [""])[0]
            print("识别结果：", text)
            with io.open(TEXT_FILE, 'w', encoding='utf-8') as f:
                f.write(text)
            print("识别结果已保存到文本文件：{}".format(TEXT_FILE))
        else:
            print("语音识别失败，错误信息：", result.get("err_msg"))
    else:
        print("请求百度语音识别API失败，状态码：", response.status_code)
        print("错误信息：", response.text)

# TTS功能（可选，用于测试）
def speak_text(text):
    tts = ALProxy("ALTextToSpeech", NAO_IP, NAO_PORT)
    tts.setLanguage("Chinese")
    tts.say(text)

if __name__ == "__main__":
    recognize_speech()