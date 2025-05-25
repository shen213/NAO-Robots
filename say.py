# coding=utf-8
from random import random
import random
from naoqi import ALProxy
import config  # 导入配置文件中的参数
import os

# 读取 answer.txt 文件中的内容，并提取最新的 AI 回答
def read_text_file(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            # 找到最后一个 AI 回答
            latest_answer = ""
            for line in reversed(lines):  # 从后向前遍历
                if line.startswith("AI（修改后）："):
                    latest_answer = line.replace("AI（修改后）：", "").strip()
                    break
            return latest_answer
    except IOError as e:
        print("文件读取失败，请检查路径：{}".format(file_path))
        print("错误信息：{}".format(e))
        exit(1)

# 初始化 NAO 的文本到语音模块
def initialize_tts(ip, port):
    try:
        tts = ALProxy("ALTextToSpeech", ip, port)
        return tts
    except Exception as e:
        print("连接到 NAO 机器人失败，请检查 IP 和端口是否正确：")
        print("错误信息：{}".format(e))
        exit(1)

# 初始化 NAO 的动画语音模块
def initialize_animated_speech(ip, port):
    try:
        animated_speech = ALProxy("ALAnimatedSpeech", ip, port)
        return animated_speech
    except Exception as e:
        print("连接到 NAO 机器人失败，请检查 IP 和端口是否正确：")
        print("错误信息：{}".format(e))
        exit(1)

# 初始化 NAO 的动作模块
def initialize_motion(ip, port):
    try:
        motion = ALProxy("ALMotion", ip, port)
        return motion
    except Exception as e:
        print("连接到 NAO 机器人失败，请检查 IP 和端口是否正确：")
        print("错误信息：{}".format(e))
        exit(1)

# 初始化 NAO 的姿态模块
def initialize_posture(ip, port):
    try:
        posture = ALProxy("ALRobotPosture", ip, port)
        return posture
    except Exception as e:
        print("连接到 NAO 机器人失败，请检查 IP 和端口是否正确：")
        print("错误信息：{}".format(e))
        exit(1)

# 让 NAO 机器人边说边做动作
def speak_with_animation(tts, animated_speech, text):
    try:
        # 设置音调（范围：0.5到2.0，默认为1.0）
        tts.setParameter("pitchShift", 1)
        # 设置语速（范围：0.5到2.0，默认为1.0）
        tts.setParameter("speed", 1.3)
        # 设置音量（范围：0到100，默认为50）
        tts.setVolume(0.8)

        # 使用动画语音模块
        configuration = {"bodyLanguageMode": "contextual"}  # 动作模式
        animated_speech.say(text, configuration)
        print("NAO 机器人已成功边说边做动作：{}".format(text))
    except Exception as e:
        print("NAO 机器人边说边做动作失败：")
        print("错误信息：{}".format(e))

# 让 NAO 机器人站正
def stand_up(motion, posture):
    try:
        # 停止当前动作
        motion.stopMove()
        # 站正
        posture.goToPosture("Stand", 0.8)
        print("NAO 机器人已成功站正")
    except Exception as e:
        print("NAO 机器人站正失败：")
        print("错误信息：{}".format(e))

#让 NAO 机器人在思考时发声
def speak_thinking():
    # 从配置文件中获取参数
    nao_ip = config.NAO_IP
    nao_port = config.NAO_PORT

    # 初始化 NAO 的文本到语音模块
    tts = initialize_tts(nao_ip, nao_port)

    # 初始化 NAO 的动画语音模块
    animated_speech = initialize_animated_speech(nao_ip, nao_port)

    # 初始化 NAO 的动作模块
    motion = initialize_motion(nao_ip, nao_port)

    # 初始化 NAO 的姿态模块
    posture = initialize_posture(nao_ip, nao_port)

    # 使用函数属性来记录是否是第一次调用
    if not hasattr(speak_thinking, "first_time"):
        speak_thinking.first_time = True

    # 定义思考消息列表
    thinking_messages = ["呀，我昨天晚上没有休息好，不知道会不会给你添乱啊", "看着我的样子，就知道我正在思考哈", "好嘞，我先静下心来，让我想想哈", "我得把我的小脑瓜子掏空，让我想一下哈", "我正在思考哈，我的脑子像台CPU全力运转"]

    if speak_thinking.first_time:
        message = thinking_messages[0]  # 第一次对话使用第一个消息
        speak_thinking.first_time = False  # 标记为非第一次调用
    else:
        # 从第二个消息开始随机选择
        message = random.choice(thinking_messages[1:])

    # 让 NAO 机器人边说边做动作
    speak_with_animation(tts, animated_speech, message)

    # 等待机器人说完话后站正
    stand_up(motion, posture)

# 封装成函数，可供 main.py 调用
def speak_answer():
    # 从配置文件中获取参数
    nao_ip = config.NAO_IP
    nao_port = config.NAO_PORT
    answer_file = r"C:\Users\17582\Desktop\nao\dialogue\answer.txt"  # 指定 answer.txt 文件路径

    # 读取文件内容并提取最新的 AI 回答
    text_to_speak = read_text_file(answer_file)

    # 初始化 NAO 的文本到语音模块
    tts = initialize_tts(nao_ip, nao_port)

    # 初始化 NAO 的动画语音模块
    animated_speech = initialize_animated_speech(nao_ip, nao_port)

    # 初始化 NAO 的动作模块
    motion = initialize_motion(nao_ip, nao_port)

    # 初始化 NAO 的姿态模块
    posture = initialize_posture(nao_ip, nao_port)

    # 让 NAO 机器人边说边做动作
    speak_with_animation(tts, animated_speech, text_to_speak)

    # 等待机器人说完话后站正
    stand_up(motion, posture)

# 如果直接运行此脚本，则调用 speak_answer()
if __name__ == "__main__":
    speak_answer()