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

idx = st.session_state.index

if f'up_input_{idx}' not in st.session_state:
    st.session_state[f'up_input_{idx}'] = ""
if f'down_input_{idx}' not in st.session_state:
    st.session_state[f'down_input_{idx}'] = ""

col1, col2 = st.columns(2)
with col1:
    st.text_input("填写上句后半部分", key=f'up_input_{idx}')
with col2:
    st.text_input("填写下句后半部分", key=f'down_input_{idx}')

# 信息提示
if st.session_state.message:
    st.info(st.session_state.message)

col_start, col_check, col_next, col_end = st.columns([1,1,1,1])

with col_check:
    # 核对按钮
    if st.button("核对"):
        up_right = up[2:]
        down_right = down[2:]
        up_user = st.session_state[f'up_input_{idx}'].strip()
        down_user = st.session_state[f'down_input_{idx}'].strip()
        msg = f"上句参考答案：{up}\n下句参考答案：{down}\n"
        up_ok = up_user == up_right
        down_ok = down_user == down_right
        if up_ok and down_ok:
            msg += "回答：✔全对"
            st.session_state.right += 1
        else:
            msg += ("上句" + ("✔正确" if up_ok else "✘错误")) + "，"
            msg += ("下句" + ("✔正确" if down_ok else "✘错误"))
        st.session_state.message = msg

with col_next:
    # 下一题按钮，点击后题号+1、清空输入和提示
    if st.button("下一题"):
        st.session_state.index += 1
        st.session_state.up_input = ""
        st.session_state.down_input = ""
        st.session_state.message = ""

with col_end:
    # 结束按钮，点击后结束游戏
    if st.button("结束"):
        st.session_state.finished = True
        st.experimental_rerun()

