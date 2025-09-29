import streamlit as st
import random

def load_poems(path):
    poems = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if '|' in line:
                up, down = line.strip().split('|', 1)
                poems.append((up, down))
    return poems

# 初始化 session_state 变量
def init_game():
    st.session_state.poems = load_poems('poems.txt')
    random.shuffle(st.session_state.poems)
    st.session_state.index = 0
    st.session_state.right = 0
    st.session_state.started = False
    st.session_state.finished = False
    st.session_state.message = ""
    st.session_state.up_input = ""
    st.session_state.down_input = ""

# 仅首次加载时初始化（或点击“开始”时）
if 'poems' not in st.session_state:
    init_game()

st.title("诗词填写小游戏（网页版）")

# 开始按钮，点击后重置状态
if not st.session_state.started:
    if st.button('开始'):
        init_game()
        st.session_state.started = True
        st.session_state.message = ""
    else:
        st.stop()  # 展示“开始”按钮前不往下运行

# 如果已结束
if st.session_state.finished:
    st.success(f"游戏结束！答对 {st.session_state.right} / {len(st.session_state.poems)}")
    # 显示“开始新游戏”按钮
    if st.button("重新开始"):
        init_game()
        st.session_state.started = True
    st.stop()

# 如果没题了，自动结束
if st.session_state.index >= len(st.session_state.poems):
    st.session_state.finished = True
    st.experimental_rerun()

up, down = st.session_state.poems[st.session_state.index]

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"### 上句：{up[:2]}____")
    st.session_state.up_input = st.text_input(
        "填写上句后半部分", 
        key=f'up_input_{st.session_state.index}', 
        value=st.session_state.up_input
    )
with col2:
    st.markdown(f"### 下句：{down[:2]}____")
    st.session_state.down_input = st.text_input(
        "填写下句后半部分", 
        key=f'down_input_{st.session_state.index}',
        value=st.session_state.down_input
    )

# 信息提示
if st.session_state.message:
    st.info(st.session_state.message)

col_start, col_check, col_next, col_end = st.columns([1
