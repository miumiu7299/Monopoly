import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from tkinter import Label
from globals import Globals
import subprocess
class CharacterSelection(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("大富翁選角色")
        self.attributes('-fullscreen', True)  # 隱藏工具欄並全屏顯示
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")  # 設置視窗大小為螢幕大小

        self.selected_character = tk.StringVar()
        self.selected_character.set("未選擇角色")
        
        self.characters = [
            {"name": "馬力歐", "image": "character/馬力歐.png"},
            {"name": "迪迪", "image": "character/迪迪.png"},
            {"name": "路易吉", "image": "character/路易吉.png"},
            {"name": "耀西", "image": "character/耀西.png"},
            {"name": "碧琪", "image": "character/碧琪.png"},
            {"name": "庫巴", "image": "character/庫巴.png"},
            {"name": "布布王", "image": "character/布布王.png"},
            {"name": "奇諾比奧", "image": "character/奇諾比奧.png"},
        ]

        self.create_widgets()

    def create_widgets(self):
        # 顯示玩家人數選擇界面
        self.show_player_selection()

    def show_player_selection(self):
    # 建立主要框架
        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True, fill=tk.BOTH)

        # 玩家人數選擇框架
        player_frame = ttk.Frame(main_frame, padding="20")
        player_frame.grid(row=0, column=0, padx=40, pady=40)

        player_label = ttk.Label(player_frame, text="選擇玩家人數：", font=("Arial", 16))
        player_label.grid(row=0, column=0, columnspan=5, pady=40)

        for i in range(2, 5):  # 玩家人數選擇範圍為2至4
            button = ttk.Button(player_frame, text=f"{i} 人", command=lambda num=i: self.select_players(num))
            button.grid(row=1, column=i-1, padx=10, pady=5)

        # 玩家資金選擇框架
        money_frame = ttk.Frame(main_frame, padding="20")
        money_frame.grid(row=1, column=0, padx=40, pady=10, sticky="n")

        player_money_label = ttk.Label(money_frame, text="選擇玩家資金：", font=("Arial", 16))
        player_money_label.grid(row=0, column=0, columnspan=5, pady=20)

        money = ["10000", "100000", "300000"]
        for i in range(0, 3): 
            button = ttk.Button(money_frame, text=f"${money[i]}", command=lambda amount=money[i]: self.select_money(amount))
            button.grid(row=1, column=i, padx=10, pady=5)

        # 繼續按鈕
        self.continue_button = ttk.Button(main_frame, text="繼續", command=self.continue_selection, state=tk.DISABLED)
        self.continue_button.grid(row=2, column=0, pady=10)
        # 地圖框架
        map_frame = ttk.Frame(main_frame)
        map_frame.grid(row=0, column=1, padx=30, pady=100, rowspan=2)

        # 地圖標籤
        map_label = ttk.Label(map_frame, text="地圖", font=("Arial", 16))
        map_label.pack()

        # 讀取地圖圖片
        map_image = Image.open("map.png")

        # 調整地圖大小
        desired_width = 650  # 設定你想要的寬度
        desired_height = 350  # 設定你想要的高度
        map_image = map_image.resize((desired_width, desired_height), Image.Resampling.LANCZOS)
        # 將圖片轉換為圖片物件
        map_photo = ImageTk.PhotoImage(map_image)

        # 在地圖框架中顯示圖片
        map_label = ttk.Label(map_frame, image=map_photo)
        map_label.image = map_photo
        map_label.pack()

    def select_players(self, num):
        Globals.players = num
        self.show_continue_button()

    def select_money(self, amount):
        Globals.money = amount
        self.show_continue_button()

    def show_continue_button(self):
        if hasattr(Globals, "players") and hasattr(Globals, "money"):
            self.continue_button.config(text=f"已選擇 {Globals.players} 人，資金 ${Globals.money}，選擇角色", state=tk.NORMAL)

    def continue_selection(self):
        self.show_character_selection()

    def show_character_selection(self):
        # 清除玩家人數選擇界面
        for widget in self.winfo_children():
            widget.destroy()

        # 左側顯示選中的角色
        left_frame = ttk.Frame(self, padding="10")
        left_frame.pack(side="left", fill="both", expand=True, pady=20, padx=20)

        selected_label = ttk.Label(left_frame, text=f"玩家 {Globals.current_player} 的選擇", font=("Arial", 16))
        selected_label.pack(pady=10)
        self.selected_character.set("未選擇角色")
        self.selected_image_label = ttk.Label(left_frame)
        self.selected_image_label.pack(pady=10)

        self.selected_name_label = ttk.Label(left_frame, textvariable=self.selected_character, font=("Arial", 14))
        self.selected_name_label.pack(pady=10)

        # 右側顯示所有角色
        self.right_frame = ttk.Frame(self, padding="10")
        self.right_frame.pack(side="right", fill="both", expand=True, pady=20, padx=20)

        self.show_characters()

        # 顯示確定按鈕
        self.confirm_button = ttk.Button(self, text="確定", command=self.confirm_selection)
        self.confirm_button.place(relx=0.9, rely=0.9, anchor="se")
        self.confirm_button.config(state=tk.DISABLED)  # 初始時確定按鈕設為不可用

        # 顯示回到主畫面按鈕
        self.back_button = ttk.Button(self, text="回到主畫面", command=self.back_to_main)
        self.back_button.place(relx=0.1, rely=0.9, anchor="sw")

    def show_characters(self):
        for i, character in enumerate(self.characters):
            frame = ttk.Frame(self.right_frame, padding="5")
            frame.grid(row=i//4, column=i%4, padx=5, pady=10)

            image_path = os.path.join(os.getcwd(), character["image"])
            image = Image.open(image_path)
            image = image.resize((150, 180), Image.Resampling.LANCZOS)  # 調整角色大小
            photo = ImageTk.PhotoImage(image)

            image_label = ttk.Label(frame, image=photo)
            image_label.image = photo
            image_label.pack()

            name_label = ttk.Label(frame, text=character["name"])
            name_label.pack()
            if character["name"] in Globals.selected_characters.values():
                select_button = ttk.Button(frame, text="已選擇", state=tk.DISABLED)
            else:
                select_button = ttk.Button(frame, text="選擇", command=lambda c=character: self.select_character(c, select_button))
            select_button.pack()

    def select_character(self, character, button):
        self.selected_character.set(character["name"])

        # 根據角色名稱生成新圖片的路徑
        new_image_path = os.path.join("character_2", f"{character['name']}_2.png")

        # 打開新圖片並調整大小
        image = Image.open(new_image_path)
        image = image.resize((220, 220), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        # 更新 selected_image_label 的圖像
        self.selected_image_label.config(image=photo)
        self.selected_image_label.image = photo

        # 啟用確定按鈕
        self.confirm_button.config(state=tk.NORMAL)

    def confirm_selection(self):
        # 確認選擇的邏輯
        print(f"玩家 {Globals.current_player} 選擇了角色: {self.selected_character.get()}")   
        Globals.selected_characters[Globals.current_player] = self.selected_character.get()
        Globals.current_player += 1   
        if Globals.current_player > Globals.players:
            for widget in self.winfo_children():
                widget.destroy()
            self.right_frame.pack_forget()
            self.confirm_button.pack_forget()
            self.start_button = ttk.Button(self, text="開始遊戲", command=self.start_game)
            self.start_button.place(relx=0.9, rely=0.9, anchor="se")
            self.back_button = ttk.Button(self, text="回到主畫面", command=self.back_to_main)
            self.back_button.place(relx=0.1, rely=0.9, anchor="sw")
            self.list_all_characters()
        else:
            self.show_character_selection()

    def back_to_main(self):
        Globals.selected_characters = {}
        Globals.current_player = 1

        self.destroy()

        main_screen = StartScreen()
        main_screen.mainloop()

    def list_all_characters(self):
        num_players = len(Globals.selected_characters)
        num_columns = min(num_players, 4) 
        max_players_per_row = num_columns * 2  

        for i, (player, character) in enumerate(Globals.selected_characters.items()):
            row_index = i // num_columns
            column_index = i % num_columns

            # 載入角色圖片並顯示
            image_path = os.path.join(os.getcwd(), f"character/{character}.png")
            image = Image.open(image_path)
            image = image.resize((180, 200), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            character_info_label = Label(self)
            character_info_label.grid(row=row_index*2, column=column_index*2, padx=50, pady=180)

            # 顯示玩家角色圖片
            image_label = Label(character_info_label, image=photo)
            image_label.image = photo
            image_label.grid(row=0, column=0, padx=(100/(num_players-1), 0))

            # 顯示玩家角色名稱
            character_label = Label(character_info_label, text=f"玩家 {player} 選擇了角色: {character}")
            character_label.grid(row=1, column=0, sticky="n")

    def start_game(self):
        print('開始遊戲')
        print(Globals.selected_characters)
        Globals.save_to_file('globals_data.pkl')
        self.destroy()
        subprocess.call(["python", "finial.py"])

class StartScreen(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("大富翁遊戲")
        img = Image.open('ui.png')
        self.bg_image = ImageTk.PhotoImage(img)

        image_width, image_height = img.size

        self.geometry(f"{image_width}x{image_height}")

        startscreen_width = self.winfo_screenwidth()
        startscreen_height = self.winfo_screenheight()

        x_pos = (startscreen_width - image_width) // 2
        y_pos = int((startscreen_height - image_height) // 2 - 0.05 * image_height)

        self.geometry(f"{image_width}x{image_height}+{x_pos}+{y_pos}")

        # 建立Canvas
        canvas = tk.Canvas(self, highlightthickness=0, width=image_width, height=image_height)
        canvas.pack()

        # 在Canvas上顯示背景圖片
        canvas.create_image(image_width//2, image_height//2, image=self.bg_image)

        # 建立遊戲開始按鈕，置中於視窗
        start_button = tk.Button(self, text="開始遊戲", command=self.switch_to_character_selection, bg="blue", fg="white", font=("Arial", 12, "bold"), bd=3, relief=tk.RAISED)
        start_button.place(relx=0.5, rely=0.9, anchor="s")

    def switch_to_character_selection(self):
        self.destroy()
        app = CharacterSelection()
        app.mainloop()

if __name__ == "__main__":
    app = StartScreen()
    app.mainloop()