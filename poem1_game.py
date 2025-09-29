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

if 'poems' not in st.session_state:
    st.session_state.poems = load_poems('poems.txt')
    random.shuffle(st.session_state.poems)
    st.session_state.index = 0
    st.session_state.right = 0

st.title('诗词填写小游戏（网页版）')

if st.session_state.index < len(st.session_state.poems):
    up, down = st.session_state.poems[st.session_state.index]
    st.write(f"上句：{up[:2]}____")
    st.write(f"下句：{down[:2]}____")
    up_input = st.text_input('填写上句后半部分', key='up'+str(st.session_state.index))
    down_input = st.text_input('填写下句后半部分', key='down'+str(st.session_state.index))
    if st.button('核对', key='chk'+str(st.session_state.index)):
        up_right = up[2:]
        down_right = down[2:]
        flag_up = up_input == up_right
        flag_down = down_input == down_right
        st.write(f"正确答案：{up}｜{down}")
        st.write('上句判定：' + ('✔正确' if flag_up else '✘错误'))
        st.write('下句判定：' + ('✔正确' if flag_down else '✘错误'))
        st.session_state.index += 1
        if flag_up and flag_down:
            st.session_state.right += 1
    st.write(f"当前得分：{st.session_state.right}")

else:
    st.write(f"游戏结束，答对 {st.session_state.right} / {len(st.session_state.poems)}")