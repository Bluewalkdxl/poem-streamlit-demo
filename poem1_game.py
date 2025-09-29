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

# 初始化全局变量
def init_game():
    st.session_state.poems = load_poems('poems.txt')
    random.shuffle(st.session_state.poems)
    st.session_state.index = 0
    st.session_state.right = 0
    st.session_state.started = False
    st.session_state.finished = False
    st.session_state.message = ""

# 首次加载
if 'poems' not in st.session_state:
    init_game()

st.title("诗词填写小游戏（网页版）")

if not st.session_state.started:
    if st.button('开始'):
        init_game()
        st.session_state.started = True
        st.session_state.message = ""
    else:
        st.stop()

if st.session_state.finished:
    st.success(f"游戏结束！答对 {st.session_state.right} / {len(st.session_state.poems)}")
    if st.button("重新开始"):
        init_game()
        st.session_state.started = True
    st.stop()

if st.session_state.index >= len(st.session_state.poems):
    st.session_state.finished = True
    st.experimental_rerun()

# 获取当前题目
up, down = st.session_state.poems[st.session_state.index]
idx = st.session_state.index

# 初始化输入状态
if f'up_input_{idx}' not in st.session_state:
    st.session_state[f'up_input_{idx}'] = ""
if f'down_input_{idx}' not in st.session_state:
    st.session_state[f'down_input_{idx}'] = ""

# 这里明确“**展示前两个字**”
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"### 上句：**{up[:2]}**____")
    st.text_input("填写上句后半部分", key=f'up_input_{idx}')
with col2:
    st.markdown(f"### 下句：**{down[:2]}**____")
    st.text_input("填写下句后半部分", key=f'down_input_{idx}')

# 信息提示
if st.session_state.message:
    st.info(st.session_state.message)

col_check, col_next, col_end = st.columns([1, 1, 1])

with col_check:
    if st.button("核对"):
        up_right = up[2:]
        down_right = down[2:]
        up_user = st.session_state[f'up_input_{idx}'].strip()
        down_user = st.session_state[f'down_input_{idx}'].strip()
        msg = f"参考答案：\n{up} | {down}\n"
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
    if st.button("下一题"):
        st.session_state.index += 1
        st.session_state.message = ""
        st.experimental_rerun()

with col_end:
    if st.button("结束"):
        st.session_state.finished = True
        st.experimental_rerun()
