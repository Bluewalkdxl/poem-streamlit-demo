import streamlit as st
import random
import time

# 读取诗词文件函数
def load_poems(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        poems = [line.strip().split('|') for line in file.readlines()]
    return poems

# 载入诗词文件（假设文件为poems.txt）
poems = load_poems("poems.txt")

# 游戏状态
used_poems = set()

# 页面标题
st.title("诗词对话游戏")
# 使用 Streamlit 自带的 st.title 方法

# 游戏开始
if 'started' not in st.session_state:
    st.session_state.started = False  # 默认游戏没有开始

# 控制游戏逻辑的函数
def start_game():
    st.session_state.started = True
    st.session_state.used_poems = set()  # 重置已使用诗句

def end_game():
    st.session_state.started = False
    st.session_state.used_poems = set()  # 重置游戏状态

# 按钮控制
if not st.session_state.started:
    st.button("开始游戏", on_click=start_game)
else:
    # 随机选择诗句
    available_poems = [p for p in poems if tuple(p) not in st.session_state.used_poems]
    
    if available_poems:
        poem = random.choice(available_poems)
        st.session_state.used_poems.add(tuple(poem))  # 记录已经显示过的诗句

        # 显示上句
        st.write(f"上句: {poem[0]}")
        
        # 1秒后显示下句
        time.sleep(1)
        st.write(f"下句: {poem[1]}")
        
        # 等待用户点击继续
        if st.button("继续"):
            start_game()
    else:
        st.write("游戏结束！所有诗句已显示。")
        st.button("重新开始", on_click=end_game)
