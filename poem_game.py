import streamlit as st
import random
import time

# 读取文件内容，格式：每行一个“上句|下句”对
def load_poems(filename):
    res = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                if '|' in line:
                    first, second = line.strip().split('|', 1)
                    res.append((first, second))
    except FileNotFoundError:
        st.error(f"文件 {filename} 未找到！")
    except Exception as e:
        st.error(f"加载文件时出错: {e}")
    return res

# 初始化应用状态
if 'used' not in st.session_state:
    st.session_state.used = set()  # 用于存储已显示的诗句索引
    st.session_state.poems = []  # 诗句列表
    st.session_state.current_poem = None  # 当前诗句
    st.session_state.game_started = False  # 游戏是否已开始

# 页面标题
st.title('诗词对句游戏')

# 载入诗词
if not st.session_state.poems:
    poems = load_poems('poems.txt')  # 请确保路径正确
    if poems:
        st.session_state.poems = poems
        random.shuffle(st.session_state.poems)  # 随机打乱诗句顺序

# 游戏开始
if st.button('开始'):
    st.session_state.game_started = True
    st.session_state.used.clear()  # 清空已使用的诗句
    st.session_state.current_poem = None
    st.write("游戏开始！点击“下一题”查看诗句。")

# 游戏进行中，显示诗句
if st.session_state.game_started:
    if len(st.session_state.used) < len(st.session_state.poems):
        # 显示上句
        if st.session_state.current_poem is None or '下句' not in st.session_state.current_poem:
            # 随机选择一个未用过的诗句
            for i, pair in enumerate(st.session_state.poems):
                if i not in st.session_state.used:
                    st.session_state.used.add(i)
                    st.session_state.current_poem = {'上句': pair[0], '下句': pair[1], 'index': i}
                    st.write(f"上句: {pair[0]}")
                    st.session_state.current_poem['显示上句'] = True
                    time.sleep(1)  # 等待 1 秒显示下句
                    break
    else:
        st.write("游戏结束！所有诗句已显示。")

    # 显示下句
    if st.session_state.current_poem and '显示上句' in st.session_state.current_poem and st.session_state.current_poem['显示上句']:
        if st.button("下一题"):
            st.write(f"下句: {st.session_state.current_poem['下句']}")
            st.session_state.current_poem['显示上句'] = False
    else:
        st.write(f"游戏结束！")
