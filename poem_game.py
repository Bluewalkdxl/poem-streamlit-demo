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
    st.session_state.show_second_line = False  # 是否显示下句
    st.session_state.game_ended = False  # 游戏是否结束

# 页面标题
st.title('诗词对句游戏')

# 载入诗词
if not st.session_state.poems:
    poems = load_poems('f:/python/test/代码/poems.txt')  # 请确保路径正确
    if poems:
        st.session_state.poems = poems
        random.shuffle(st.session_state.poems)  # 随机打乱诗句顺序

# 游戏开始
if st.button('开始') and not st.session_state.game_started:
    st.session_state.game_started = True
    st.session_state.used.clear()  # 清空已使用的诗句
    st.session_state.current_poem = None
    st.session_state.show_second_line = False  # 重置是否显示下句的状态
    st.session_state.game_ended = False  # 重置游戏结束状态
    st.write("游戏开始！点击“下一题”查看诗句。
