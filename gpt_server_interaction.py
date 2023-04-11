# gpt_server_interaction.py

import openai
import json
import subprocess

# 设置API密钥
openai.api_key = "your_api_key_here"

def interact_with_gpt(prompt):
    conversation_history = [
        {"role": "system", "content": "You are interacting with a server, GPT-4 will generate server commands based on your input. Please output commands in JSON format as follows:\n{\"command\": \"your_command\"}"},
        {"role": "user", "content": prompt}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation_history,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].message["content"].strip()

def execute_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode('utf-8'), stderr.decode('utf-8')

def main():
    while True:
        # 获取用户输入
        user_input = input("请输入您的问题或命令（输入'退出'以结束）：")

        # 如果用户输入“退出”，则跳出循环
        if user_input.lower() == "退出":
            break

        # 将带有上下文的用户输入发送给GPT-4
        gpt_response = interact_with_gpt(user_input)
        print(f"GPT-4生成的JSON: {gpt_response}")  # 打印GPT-4生成的JSON

        try:
            gpt_command_json = json.loads(gpt_response)
            gpt_command = gpt_command_json["command"]
        except (json.JSONDecodeError, KeyError):
            print("GPT-4没有生成有效的JSON格式命令。请尝试其他问题或命令。")
            continue

        # 执行指令并获取输出
        stdout, stderr = execute_command(gpt_command)

        # 打印服务器输出
        print(f"服务器输出：\n{stdout}\n{stderr}")

        # 将指令的输出发送给GPT-4并获取回应
        prompt = f"我刚刚执行了以下命令：\n{gpt_command}\n服务器的输出如下：\n{stdout}\n{stderr}\n请给出回应。"
        gpt_response = interact_with_gpt(prompt)

        # 打印GPT-4的回应
        print(f"GPT-4回应：{gpt_response}")

if __name__ == "__main__":
    main()
