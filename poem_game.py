import streamlit as st
import random

def load_poems(filename):
    poems = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if '|' in line:
                first, second = line.strip().split('|', 1)
                poems.append((first, second))
    return poems

class PoemFillGame:
    def __init__(self, root, poems):
        self.root = root
        self.poems = poems.copy()
        random.shuffle(self.poems)
        self.current = None

        self.label_top = st.Label(root, text="点击开始", font=('微软雅黑', 28))
        self.label_top.pack(pady=30)

        self.label_hint = st.Label(root, text="", font=('微软雅黑', 22))
        self.label_hint.pack(pady=20)

        self.frame_entry = st.Frame(root)
        self.frame_entry.pack(pady=20)

        self.label_up_hint = st.Label(self.frame_entry, text="", font=('微软雅黑', 20))
        self.label_up_hint.grid(row=0, column=0)
        self.entry_up = st.Entry(self.frame_entry, font=('微软雅黑', 20), width=10, justify='center')
        self.entry_up.grid(row=0, column=1)

        self.label_down_hint = st.Label(self.frame_entry, text="", font=('微软雅黑', 20))
        self.label_down_hint.grid(row=1, column=0)
        self.entry_down = st.Entry(self.frame_entry, font=('微软雅黑', 20), width=10, justify='center')
        self.entry_down.grid(row=1, column=1)

        self.btn_start = st.Button(root, text="开始", font=('微软雅黑', 18), command=self.next_poem)
        self.btn_start.pack(side='left', padx=20)

        self.btn_check = st.Button(root, text="核对", font=('微软雅黑', 18), command=self.check, state='disabled')
        self.btn_check.pack(side='left', padx=20)

        self.btn_next = st.Button(root, text="下一题", font=('微软雅黑', 18), command=self.next_poem, state='disabled')
        self.btn_next.pack(side='left', padx=20)

        self.btn_end = st.Button(root, text="结束", font=('微软雅黑', 18), command=self.end_game)
        self.btn_end.pack(side='left', padx=20)

    def next_poem(self):
        self.entry_up.delete(0, st.END)
        self.entry_down.delete(0, st.END)
        self.label_hint.config(text="")
        self.btn_start.config(state='disabled')
        self.btn_check.config(state='normal')
        self.btn_next.config(state='disabled')

        if not self.poems:
            self.label_top.config(text="全部完成！")
            self.btn_check.config(state='disabled')
            self.btn_next.config(state='disabled')
            return

        self.current = self.poems.pop()
        up, down = self.current
        self.label_top.config(text="填写剩余诗句部分：")
        self.label_up_hint.config(text=f"上句：{up[:2]}")
        self.label_down_hint.config(text=f"下句：{down[:2]}")

    def check(self):
        up_user = self.entry_up.get().strip()
        down_user = self.entry_down.get().strip()
        up_right = self.current[0][2:]
        down_right = self.current[1][2:]

        up_result = ('✔正确' if up_user == up_right else f'✘错误，标准：{up_right}')
        down_result = ('✔正确' if down_user == down_right else f'✘错误，标准：{down_right}')

        result_text = f"""上句：{self.current[0][:2]}{up_user}  {up_result}
下句：{self.current[1][:2]}{down_user}  {down_result}"""
        self.label_hint.config(text=result_text)
        self.btn_check.config(state='disabled')
        self.btn_next.config(state='normal')

    def end_game(self):
        self.label_top.config(text="游戏已结束！")
        self.label_hint.config(text="")
        self.entry_up.delete(0, tk.END)
        self.entry_down.delete(0, tk.END)
        self.btn_check.config(state='disabled')
        self.btn_next.config(state='disabled')
        self.btn_start.config(state='disabled')

if __name__ == "__main__":
    poems = load_poems('./poems.txt')
    root = st.Tk()
    root.title("诗词填写游戏")
    root.geometry("730x540") # 宽大适合平板触控
    game = PoemFillGame(root, poems)

    root.mainloop()

