import os
import sys
import re
import subprocess
import shutil
import ctypes
import time
import tkinter as tk
from tkinter import ttk

# --- ЦВЕТОВАЯ ПАЛИТРА ---
C_WHITE = "\033[0m"
C_CYAN = "\033[36m"
C_GREEN = "\033[32m"
C_YELLOW = "\033[33m"
C_RED = "\033[31m"
BG, ACCENT, TEXT = "#121212", "#1E1E1E", "#E0E0E0"

class FoxEngine:
    def __init__(self, filename_arg):
        self.filename = os.path.abspath(filename_arg) if filename_arg else ""
        self.root = None
        self.elements = {}
        os.system("") 

    def draw_global_bar(self, percent):
        bar_len = 30
        filled = int(bar_len * percent / 100)
        bar = f"{C_GREEN}" + "/" * filled + f"{C_WHITE}" + "." * (bar_len - filled)
        sys.stdout.write(f"\033[s\033[2;0HОБЩИЙ ПРОГРЕСС: [{bar}] {C_YELLOW}{percent}%{C_WHITE}   \033[u")
        sys.stdout.flush()

    def anim_log(self, message, line_idx):
        chars = ["/", "-", "\\", "|"]
        target_line = line_idx + 2
        for i in range(0, 101, 20):
            char = chars[(i // 20) % 4]
            dots = "." * (1 + (i // 25) % 3)
            sys.stdout.write(f"\033[{target_line};0H{C_CYAN}{char}{C_WHITE} {message} {C_YELLOW}({i}%){C_WHITE}{dots}    ")
            sys.stdout.flush()
            time.sleep(0.01)
        sys.stdout.write(f"\033[{target_line};0H{C_GREEN}√{C_WHITE} {message} {C_GREEN}Готово!{C_WHITE}       \n")

    def get_path(self, target):
        if not target: return os.path.join(os.environ['USERPROFILE'], 'Desktop')
        if ":" in target or target.startswith(("/", "\\")): return os.path.normpath(target)
        desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
        return os.path.normpath(os.path.join(desktop, target))

    def apply_dark_theme(self):
        if not self.root: return
        try:
            self.root.update()
            hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
            if hwnd == 0: hwnd = self.root.winfo_id()
            rendering = ctypes.c_int(1)
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(rendering), 4)
            self.root.configure(bg=BG)
        except: pass

    def parse(self, line):
        args = re.findall(r'"(.*?)"', line)
        cmd = line.split('"')[0].strip().lower()
        return cmd, args

    def execute(self, line, idx):
        line = line.strip()
        if not line or line.startswith("#"): return True
        cmd, args = self.parse(line)
        try:
            if "папка" in cmd:
                os.makedirs(self.get_path(args[0]), exist_ok=True)
                self.anim_log(f"Папка {args[0]}", idx)
            elif "файл" in cmd:
                with open(self.get_path(args[0]), "w", encoding="utf-8") as f:
                    f.write(args[1].replace("\\n", "\n"))
                self.anim_log(f"Файл {os.path.basename(args[0])}", idx)
            elif "запусти" in cmd:
                p = self.get_path(args[0])
                if os.path.exists(p): os.startfile(p)
                else: subprocess.Popen(args[0], shell=True)
                self.anim_log(f"Запуск {args[0]}", idx)
            elif "окно" in cmd:
                self.root = tk.Tk(); self.root.withdraw()
                self.root.title(args[0]); self.root.configure(bg=BG)
                for i in range(10): 
                    self.root.columnconfigure(i, weight=1)
                    self.root.rowconfigure(i, weight=1)
            elif "блок" in cmd:
                t, r, c, sp, fid, orient = args[0], args[1], args[2], args[3], args[4], args[5]
                f = tk.LabelFrame(self.root, text=f" {t} ", bg=BG, fg=TEXT, bd=1, relief="solid")
                f.grid(row=int(r), column=int(c), columnspan=int(sp), sticky="nsew", padx=5, pady=5)
                self.elements[fid] = {"frame": f, "side": "left" if orient == "гор" else "top"}
            elif "надпись" in cmd:
                tk.Label(self.elements[args[1]]["frame"], text=args[0], bg=BG, fg=TEXT, font=("Arial", 10)).pack(side=self.elements[args[1]]["side"], padx=5, expand=True)
            elif "поле" in cmd:
                e = tk.Entry(self.elements[args[1]]["frame"], bg=ACCENT, fg=TEXT, width=int(args[2]), bd=0, justify="center", font=("Arial", 11))
                e.insert(0, args[0]); e.pack(side=self.elements[args[1]]["side"], padx=5, expand=True)
            elif "выбор" in cmd:
                c = ttk.Combobox(self.elements[args[1]]["frame"], values=args[0].split(", "), state="readonly", font=("Arial", 10))
                c.current(0); c.pack(side=self.elements[args[1]]["side"], padx=5, expand=True)
            elif "кнопка" in cmd:
                t, act, r, col, sp = args[0], args[1], args[2], args[3], args[4]
                btn = tk.Button(self.root, text=t, bg=ACCENT, fg=TEXT, font=("Arial", 10, "bold"), relief="flat", command=lambda a=act: subprocess.Popen(a, shell=True))
                btn.grid(row=int(r), column=int(col), columnspan=int(sp), sticky="nsew", padx=5, pady=10)
            return True
        except: return False

    def run(self):
        if not self.filename or not os.path.exists(self.filename): return
        os.system("cls")
        print(f"{C_CYAN}{'FoxCod v2.6a stability'.center(50)}{C_WHITE}\n\n")
        with open(self.filename, 'r', encoding="utf-8") as f:
            lines = [l for l in f.readlines() if l.strip() and not l.startswith("#")]
        for i, line in enumerate(lines, 1):
            self.draw_global_bar(int((i/len(lines))*100))
            if not self.execute(line, i): break
        if self.root:
            print(f"\n{C_GREEN}√ ИНФРАСТРУКТУРА ГОТОВА.{C_WHITE}")
            self.apply_dark_theme(); self.root.deiconify(); self.root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        FoxEngine(sys.argv[1]).run()
