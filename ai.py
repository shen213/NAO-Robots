# coding=utf-8
import requests
import json
import os
import time

API_KEY = ""
URL = ""
MODEL = ""

# 获取最近的上下文记录
def get_context(file_path, max_turns=5):
    context = []
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
            dialogues = []
            current_dialogue = []
            for line in lines:
                if line.strip():
                    current_dialogue.append(line.strip())
                else:
                    if current_dialogue:
                        dialogues.append(current_dialogue)
                        current_dialogue = []
            if current_dialogue:
                dialogues.append(current_dialogue)
            # 取最近的 max_turns 轮对话作为上下文
            recent_dialogues = dialogues[-max_turns:]
            for dialogue in recent_dialogues:
                if len(dialogue) >= 2:
                    user_input = dialogue[0].split("用户：")[-1]
                    ai_response = dialogue[1].split("AI：")[-1]
                    context.append({"role": "user", "content": user_input})
                    context.append({"role": "assistant", "content": ai_response})
    return context

# 调用API获取回答
def call_api(user_question, context=[]):
    messages = context + [{"role": "user", "content": user_question}]

    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False,
        "max_tokens": 150,
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "frequency_penalty": 0.5,
        "n": 1,
        "response_format": {"type": "text"},
    }

    headers = {
        "Authorization": "Bearer {}".format(API_KEY),
        "Content-Type": "application/json"
    }

    response = requests.post(URL, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        if 'choices' in response_data and isinstance(response_data['choices'], list) and len(response_data['choices']) > 0:
            choice = response_data['choices'][0]
            return choice.get('message', {}).get('content', '').strip()
    else:
        print("请求失败，状态码: {}, 错误信息: {}".format(response.status_code, response.text))
        return None

# 生成回答
def generate_answer():
    file_path = r""
    answer_file_path = r""

    # 记录整个生成回答过程的开始时间
    start_time = time.time()

    try:
        with open(file_path, "r") as file:
            user_question = file.read().strip()
    except IOError as e:
        print("文件读取失败，请检查路径：{}".format(file_path))
        print("错误信息：{}".format(e))
        return

    # 获取最近的上下文（最多取 5 轮）
    context = get_context(answer_file_path)

    # 第一次调用 API，生成初始回答
    print("正在生成初始回答...")
    first_answer = call_api(user_question, context)
    if not first_answer:
        print("第一次调用 API 失败，无法获取初始回答。")
        return

    # 第二次调用 API，对初始回答进行修改并控制在100个汉字以内
    print("正在修改回答，控制在30个汉字以内...")
    modified_prompt = "请将上述回答修改并控制在30个汉字以内，同时要求使用带有情绪化的口语。"
    context.append({"role": "user", "content": user_question})
    context.append({"role": "assistant", "content": first_answer})
    context.append({"role": "user", "content": modified_prompt})

    final_answer = call_api(modified_prompt, context)
    if not final_answer:
        print("第二次调用 API 失败，无法获取修改后的回答。")
        return

    # 将最终回答保存到文件中
    try:
        current_count = 0
        if os.path.exists(answer_file_path):
            with open(answer_file_path, "r") as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith(tuple(str(i) for i in range(10))):
                        try:
                            current_count = int(line.split("、")[0])
                        except ValueError:
                            continue

        next_count = current_count + 1

        with open(answer_file_path, "a") as file:
            file.write("{}、用户：{}\n".format(next_count, user_question))
            file.write("AI（初始回答）：{}\n".format(first_answer.encode("utf-8")))
            file.write("AI（修改后）：{}\n\n".format(final_answer.encode("utf-8")))

        print("最终回答已成功保存到文件：{}".format(answer_file_path))
    except IOError as e:
        print("保存回答到文件时出错：{}".format(e))

    # 记录整个生成回答过程的结束时间
    end_time = time.time()
    print("最后AI给出答案的时间：{:.2f} 秒".format(end_time - start_time))

if __name__ == "__main__":
    generate_answer()