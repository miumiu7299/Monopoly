import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk
#import os
from tkinter import PhotoImage

class Player:
    def __init__(self, name, position=0, money=5000):
        self.name = name
        self.position = position
        self.money = money
        self.properties = []
        self.in_jail = False
        self.in_hospital = False
        self.is_emergency = False

    def move(self, steps, board_size):
        self.position = (self.position + steps) % board_size

    def update_money(self, amount):
        self.money += amount

    def buy_property(self, property_name, cost):
        if self.money >= cost:
            self.money -= cost
            self.properties.append(property_name)
            return True
        return False

class Property:
    def __init__(self, name, cost=0, type="property"):
        self.name = name
        self.cost = cost
        self.owner = None
        self.type = type

class MonopolyGame:
    def __init__(self, ui):
        self.players = []
        self.current_turn = 0
        self.board_size = 28 #共30格
        self.properties = self.create_properties()
        self.ui = ui

    def create_properties(self):
        properties = []
        for i in range(self.board_size):
            if i in [3, 18]: 
                properties.append(Property(f"Chance or Destiny{i}", type="chanceordestiny"))
            elif i in [25]: 
                properties.append(Property(f"Emergency {i}", type="emergency"))#直接去醫院
            elif i in [21]: 
                properties.append(Property(f"Fat->killed {i}", type="fattokilled"))
            elif i in [14]: 
                properties.append(Property(f"Hospital {i}", type="hospital"))
            elif i in [9]: 
                properties.append(Property(f"Magic Card {i}", type="magiccard"))
            elif i in [6]: 
                properties.append(Property(f"Jail {i}", type="jail"))
        
            elif i in [27]: 
                properties.append(Property(f"媽媽的愛 {i}", 4500))
            elif i in [26]: 
                properties.append(Property(f"A5和牛 {i}", 3000))
                
            elif i in [24]: 
                properties.append(Property(f"魚子醬 {i}", 1500))
            elif i in [23]: 
                properties.append(Property(f"松葉蟹 {i}", 3500))
            elif i in [22]: 
                properties.append(Property(f"鮑魚烏參佛跳牆 {i}", 2200))
            elif i in [20]: 
                properties.append(Property(f"威靈頓牛排 {i}", 2800))
            elif i in [19]: 
                properties.append(Property(f"龍蝦 {i}", 1000))
            elif i in [17]: 
                properties.append(Property(f"火鍋{i}", 350))
            elif i in [16]: 
                properties.append(Property(f"義大利麵 {i}", 400))
            elif i in [15]: 
                properties.append(Property(f"牛排 {i}", 700))
            elif i in [13]: 
                properties.append(Property(f"pizza {i}", 300))
            elif i in [12]: 
                properties.append(Property(f"壽司 {i}", 350))
            elif i in [11]: 
                properties.append(Property(f"燒烤 {i}", 800))
            elif i in [10]: 
                properties.append(Property(f"石鍋拌飯 {i}", 200))
            elif i in [8]: 
                properties.append(Property(f"牛肉麵 {i}", 250))
            elif i in [7]: 
                properties.append(Property(f"咖哩 {i}", 100))
            elif i in [5]: 
                properties.append(Property(f"新竹人的❤️ 麥當勞 {i}", 150))
            elif i in [4]: 
                properties.append(Property(f"便當 {i}", 80))
            elif i in [2]: 
                properties.append(Property(f"想不到吃什麼 7-11 {i}", 70))
            elif i in [1]: 
                properties.append(Property(f"不健康的泡麵{i}", 50))
            elif i in [0]:
                properties.append(Property(f"Start {i}", 0))
        return properties

    def add_player(self, player):
        self.players.append(player)
        self.ui.update_player_list()

    def next_turn(self):
        
        if not self.players:
            messagebox.showerror("Error", "No players in the game.")
            return

        current_player = self.players[self.current_turn]

        if current_player.in_jail:
            self.ui.update_status_label(f"{current_player.name} is in jail and skips this turn.")
            current_player.in_jail = False
            self.ui.update_player_list()
            self.current_turn = (self.current_turn + 1) % len(self.players)
            return
        
        if current_player.in_hospital:
            self.ui.update_status_label(f"{current_player.name} is in hospital and skips this turn.")
            current_player.in_hospital = False
            self.ui.update_player_list()
            self.current_turn = (self.current_turn + 1) % len(self.players)
            return
        
        if current_player.is_emergency:
            self.ui.update_status_label(f"{current_player.name} is in emergency and moved to hospital.")
            current_player.is_emergency = False
            current_player.in_hospital = True
            self.ui.update_player_list()
            self.current_turn = (self.current_turn + 1) % len(self.players)
            return
        
        steps = self.roll_dice()
        current_player.move(steps, self.board_size)
        self.ui.update_status_label(f"{current_player.name} rolled a {steps} and moved to position {current_player.position}.")
        self.handle_space_action(current_player)

        self.ui.update_player_list()

        self.current_turn = (self.current_turn + 1) % len(self.players)

    def roll_dice(self):
        return random.randint(1, 6) 

    def handle_space_action(self, player):
        if 0 <= player.position < len(self.properties):
            property = self.properties[player.position]
            if property.type == "chanceordestiny":
                self.ui.add_message(f"{player.name} landed on a Chance or Destiny space.")
                self.draw_chanceordestiny_card(player)
            elif property.type == "emergency":
                self.ui.add_message(f"{player.name}  landed on a Emergency space and moved to hospital.")
                player.is_emergency = True
                player.position=16
            elif property.type == "fattokilled":
                self.ui.add_message(f"{player.name} landed on a Fat->killed space , you are so fat that you will get killed!!!")
            elif property.type == "hospital":
                self.ui.add_message(f"{player.name} landed on a Hospital space and stays for one turn.")
                player.in_hospital = True
            elif property.type == "magiccard":
                self.ui.add_message(f"{player.name} landed on a Magic Card space")
                self.draw_magic_card(player)
            elif property.type == "jail":
                self.ui.add_message(f"{player.name} landed on a Jail space and stays for one turn.")
                player.in_jail = True
            elif property.owner is None:
                if player.position != 0:
                    self.ui.add_message(f"{player.name} landed on {property.name}, which is unowned.")
                    self.ui.ask_to_buy_property(player, property)
                else:
                    self.ui.add_message(f"{player.name} landed on the Start position and got $100.")
                    player.money+=100
            elif property.owner != player:
                self.ui.add_message(f"{player.name} landed on {property.name}, which is owned by {property.owner.name}.")
                self.pay_rent(player, property)
            else:
                self.ui.add_message(f"{player.name} landed on their own property ({property.name}).")

    def pay_rent(self, player, property):
        rent_amount = property.cost * 0.6
        owner = property.owner
        if player.money >= rent_amount:
            player.update_money(-rent_amount)
            owner.update_money(rent_amount)
            self.ui.add_message(f"{player.name} paid ${rent_amount} in rent to {owner.name} for landing on {property.name}.")
        else:
            self.ui.add_message(f"{player.name} does not have enough money to pay rent and is bankrupt.")
            messagebox.showinfo("Bankrupt", f"{player.name} does not have enough money to pay rent and is bankrupt. {owner.name} is owed ${rent_amount}.")
            self.end_game()
            self.ui.game_over() 
            

    def end_game(self):
        self.ui.add_message("Game Over!")
        richest_player = max(self.players, key=lambda p: p.money)
        self.ui.add_message(f"The winner is {richest_player.name} with ${richest_player.money}!")
        messagebox.showinfo("Game Over", f"The winner is {richest_player.name} with ${richest_player.money}!")
        #self.ui.disable_buttons()

    def draw_chanceordestiny_card(self, player):
        amount = random.choice([50, -50])
        player.update_money(amount)
        if player.money < 0:
            self.ui.add_message(f"{player.name} drew a Chance or Destiny card and lost ${-amount}. {player.name} is bankrupt.")
            self.end_game()
            self.ui.game_over() 
            
        else:
            if amount > 0:
                self.ui.add_message(f"{player.name} drew a Chance or Destiny card and received ${amount}.")
            else:
                self.ui.add_message(f"{player.name} drew a Chance  or Destiny card and lost ${-amount}.")
        
    def draw_magic_card(self, player):
        amount = random.choice([100,10])
        player.update_money(amount)
        self.ui.add_message(f"{player.name} drew a Magic card and received ${amount}.")


class MonopolyUI:
    def __init__(self, root):
        self.root = root
        self.root.title("大富翁遊戲")
        self.root.geometry("1600x900")  # 假設全螢幕或足夠大的解析度
        
        
        # 設置地圖參數
        self.grid_size = 70  # 格子大小
        self.map_width = 10  # 地圖寬度
        self.map_height = 5  # 地圖高度
        
        # 計算地圖容器的大小
        map_frame_width = self.map_width * self.grid_size
        map_frame_height = self.map_height * self.grid_size
        

        
        # 創建地圖容器
        self.map_frame = tk.Frame(self.root, width=map_frame_width, height=map_frame_height)
        self.map_frame.grid(row=1, column=1, padx=100, pady=10)  # 使用 grid 佈局管理器
        
        
        # 創建地圖格子
        self.create_map()
        
        # 在四個角落放置玩家
        self.place_players()
    
        self.game = MonopolyGame(self)
        
        # 主框架設置
        self.main_container = tk.Frame(self.root)
        self.main_container.grid(row=0, column=1, sticky='nsew')
        self.main_frame = tk.Frame(self.main_container)
        self.main_frame.pack(fill=tk.BOTH, expand=True)  # 在主框架容器內使用pack

        
        # 主框架設置
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=2, column=1, sticky='nsew')
 
        

        # 玩家信息框架，放在畫面的四個角落
        self.players_frame = [None] * 4
        positions = ['nw', 'ne', 'sw', 'se']  # 四個角落的位置配置
        self.player_texts = []
        padding_x = 0.015  # 左右保持 5% 的邊距
        padding_y = 0.3   # 上下增加到 10% 的邊距
        
        
        for i in range(4):
            self.players_frame[i] = tk.Frame(self.main_frame)
            self.players_frame[i].place(relx=0.05, rely=0.05, anchor='center')
            # 使用 padding_x 和 padding_y 調整 relx 和 rely 位置
            relx_value = 0 + padding_x if i % 2 == 0 else 1 - padding_x
            rely_value = 0 + padding_y if i < 2 else 1 - padding_y
            
            self.players_frame[i].place(relx=relx_value, rely=rely_value, anchor=positions[i], relwidth=0.15, relheight=0.2)
            text_widget = tk.Text(self.players_frame[i], font=('Arial', 12))
            text_widget.pack(fill=tk.BOTH, expand=True)
            self.player_texts.append(text_widget)
        

       # 控制元件框架，放置於畫面正中間
        self.control_frame = tk.Frame(self.main_frame)
        self.control_frame.place(relx=0.5, rely=0.5, anchor='center')
      
        # 在control_frame內部使用grid布局
        self.control_frame.columnconfigure(0, weight=1)
        self.control_frame.columnconfigure(1, weight=1)

        # 玩家名稱輸入
        self.player_name_var = tk.StringVar()
        self.player_name_entry = tk.Entry(self.control_frame, textvariable=self.player_name_var)
        self.player_name_entry.grid(row=0, column=0, columnspan=2, pady=10, sticky='ew')

        # 消息列表框
        self.message_listbox = tk.Listbox(self.control_frame, width=50, height=10)
        self.message_listbox.grid(row=1, column=0, padx=20, pady=20, sticky='nsew')

        # 按鈕
        self.button_frame = tk.Frame(self.control_frame)
        self.button_frame.grid(row=1, column=1, padx=20, pady=20, sticky='ns')

        self.add_player_button = tk.Button(self.button_frame, text="添加玩家", command=self.add_player)
        self.add_player_button.pack(side=tk.TOP, padx=5, pady=5)  # 按鈕垂直排列

        self.next_turn_button = tk.Button(self.button_frame, text="丟骰子", command=self.next_turn)
        self.next_turn_button.pack(side=tk.TOP, padx=5, pady=5)  # 按鈕垂直排列

        # 狀態顯示欄
        self.status_label = tk.Label(self.control_frame, text="遊戲狀態")
        self.status_label.grid(row=2, column=0, columnspan=2, sticky='ew', pady=10)
        
        # 假定棋盤格子名稱
        self.cell_names = [
            "pizza", "Hospital", "牛排", "義大利麵", "火鍋","Chance or Destiny","龍蝦","威靈頓牛排",
            "壽司","","","","","","","Fat->killed",
            "燒烤","","","","","","","鮑魚烏參佛跳牆",
            "石鍋拌飯", "","","","","","","松葉蟹",
            "Magic Card", "","","","","","","魚子醬",
            "牛肉麵", "","","","","","","Emergency",
            "咖哩", "","","","","","","A5和牛",
            "jail", "新竹人的❤️ 麥當勞", "便當", "Chance or Destiny", "想不到吃什麼 7-11","不健康的泡麵","Start","媽媽的愛",
        ]
        
        self.food()
    
       
    def food(self):
        food_image_paths = [
            "character/hospital.png",
            "character/steak.png",#pizza
<<<<<<< Updated upstream
            "character/pasta.png",
            "character/pasta.png",
            "character/pasta.png",#hotpot
=======
>>>>>>> Stashed changes
            "character/chance.png",
            "character/pasta.png",
            "character/pasta.png",#hotpot
            "character/too_many_delicy.png",
            "character/lobster.png",
<<<<<<< Updated upstream
            "character/steak.png",#威
=======
            "character/advanced_steak.png",#威
>>>>>>> Stashed changes
            "character/chinese_dish.png",
            "character/eat_too_much.png",
            "character/barbecue.png",
            "character/fish.png",
            "character/korean_meal.png",
            "character/a5.png",
            "character/magic_card.png",
            "character/mom_love.png",
            "character/prison.png",
            "character/beef_noodle.png",
            "character/sushi.png",
            "character/curry.png",
            "character/chance.png",
            "character/korean_fried_chicken.png",
            "character/mcdonal's.png",
            "character/bento.png",
            "character/instant_noodle.png",
            "character/start.png"
            
            
            
            # Add more food image paths as needed
        ]
        food_cell_index = [
            0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 19, 20, 29, 30, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49
        ]

        for food_image_path, cell_index in zip(food_image_paths, food_cell_index):
            if food_image_path:  # 确保路径不是空的
                try:
                    image = Image.open(food_image_path)
                    image = image.resize((self.grid_size, self.grid_size), Image.LANCZOS)
                    food_photo = ImageTk.PhotoImage(image)

                    cell_row = cell_index // self.map_width
                    cell_column = cell_index % self.map_width

                    # 获取对应的单元格控件
                    cell_widgets = self.map_frame.grid_slaves(row=cell_row, column=cell_column)
                    if cell_widgets:
                        cell_widget = cell_widgets[0]
                        cell_widget.config(image=food_photo, width=self.grid_size, height=self.grid_size)
                        cell_widget.image = food_photo
                except Exception as e:
                    print(f"Error loading image {food_image_path}: {e}")

       
    def create_map(self):
        # 創建地圖格子
        for y in range(self.map_height):
            for x in range(self.map_width):
                if x == 0 or x == self.map_width - 1 or y == 0 or y == self.map_height - 1:
                    cell = tk.Label(self.map_frame, width=10, height=5, borderwidth=1, relief="solid")  # 調整格子大小
                    cell.grid(row=y, column=x, padx=1, pady=1)
                    
                    # 綁定點擊事件
                    cell.bind("<Button-1>", lambda event, cell=cell, x=x, y=y: self.on_cell_click(cell, x, y))
    
    def place_players(self):
        # 調整玩家圖像大小
        player_image_path = "character/馬力歐.png"
        image = Image.open(player_image_path)
        image = image.resize((100, 120), Image.LANCZOS)
        player_photo = ImageTk.PhotoImage(image)
        
        # 在四個角落放置玩家
        player1 = tk.Label(self.root, image=player_photo)
        player1.image = player_photo
        player1.grid(row=0, column=0, padx=20, pady=20, sticky="nw")
        
        player2 = tk.Label(self.root, image=player_photo)
        player2.image = player_photo
        player2.grid(row=0, column=2, padx=20, pady=20, sticky="ne")
        
        player3 = tk.Label(self.root, image=player_photo)
        player3.image = player_photo
        player3.grid(row=2, column=0, padx=20, pady=20, sticky="sw")
        
        player4 = tk.Label(self.root, image=player_photo)
        player4.image = player_photo
        player4.grid(row=2, column=2, padx=20, pady=20, sticky="se")
        
    def on_cell_click(self, cell, x, y):
        # 顯示點擊的格子編號
        index = y * self.map_width + x + 1
        messagebox.showinfo("Info", "You clicked on grid: {}".format(index))
        
    def draw_board(self):
        cell_size = 97.5  # 780 / 8
        for row in range(8):
            for col in range(8):
                x1 = col * cell_size
                y1 = row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                
                # 计算格子的索引，假设每个格子都有一个名字存储在 self.cell_names 列表中
                cell_index = row * 8 + col
                cell_name = self.cell_names[cell_index % len(self.cell_names)]  # 循环使用名字列表

                # 检查是否是边缘的格子
                if row == 0 or row == 7 or col == 0 or col == 7:
                    outline_color = 'black'
                else:
                    outline_color = ''
                
                # 创建矩形并绑定点击事件
                rectangle = self.board_canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline=outline_color)
                self.board_canvas.tag_bind(rectangle, '<Button-1>', lambda event, name=cell_name: self.show_cell_name(name=name))
                #self.show_cell_name(name)
            
    def show_cell_name(self, name):
        messagebox.showinfo("物業信息", f"您點擊了：{name}")

    def add_player(self):
        name = self.player_name_var.get()
        if name:
            player = Player(name)
            self.game.add_player(player)
            self.player_name_var.set("")
            self.update_player_list()
        else:
            messagebox.showerror("Error", "Player name cannot be empty.")

    def next_turn(self):
        self.game.next_turn()
        self.update_player_list()

    def update_player_list(self):
        for i, player in enumerate(self.game.players):
            if i < len(self.player_texts):
                text_widget = self.player_texts[i]
                text_widget.delete('1.0', tk.END)  # 清空文本框
                player_info = f"{player.name}\nPosition: {player.position}\nMoney: ${player.money}\nCuisines: {', '.join(player.properties)}"
                text_widget.insert(tk.END, player_info)  # 插入新的玩家資訊

    def update_status_label(self, status):
        self.status_label.config(text=status)
        self.status_label.update_idletasks()# 刷新

    def add_message(self, message):
        self.message_listbox.insert(tk.END, message)
        self.message_listbox.yview(tk.END)# 自動滾動到最新訊息

    def ask_to_buy_property(self, player, property):
        response = messagebox.askyesno("Buy Property", f"Do {player.name} want to buy {property.name} for ${property.cost}?")
        if response:
            if player.buy_property(property.name, property.cost):
                property.owner = player
                self.add_message(f"{player.name} bought {property.name} for ${property.cost}.")
            else:
                messagebox.showerror("Error", "Not enough money to buy this property.")
    
    def disable_buttons(self):
        self.add_player_button.config(state=tk.DISABLED)
        self.next_turn_button.config(state=tk.DISABLED)
    
    def game_over(self):
        response = messagebox.askyesno("Game Over", "A player has gone bankrupt. Do you want to play another round?")
        if response:
            self.reset_game()
        else:
            self.root.destroy()  # 關閉遊戲視窗

    def reset_game(self):
        for text_widget in self.player_texts:
            text_widget.delete('1.0', tk.END)
        self.message_listbox.delete(0, tk.END)
        self.game = MonopolyGame(self)  # 重置遊戲
        self.update_status_label("Game has been reset. Ready to play again!")
        self.disable_buttons(False)  # 重新啟用按鈕等可能在遊戲中變更的UI元件

if __name__ == "__main__":
    root = tk.Tk()
    app = MonopolyUI(root)
    root.mainloop()

"""
def main():
    root = tk.Tk()
    root.geometry("1500x1500")  # 設置視窗大小
    app = MapApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1500x1500")  # 設置視窗大小
    app = MapApp(root)
    root.mainloop()


class MapApp:
    def __init__(self, master):
        self.master = master
        self.master.title("地圖應用程式")
        
        # 設置地圖參數
        self.grid_size = 20  # 格子大小
        self.map_width = 10  # 地圖寬度
        self.map_height = 5  # 地圖高度
        
        # 計算地圖容器的大小
        map_frame_width = self.map_width * self.grid_size
        map_frame_height = self.map_height * self.grid_size
        
        # 創建地圖容器
        self.map_frame = tk.Frame(self.master, width=map_frame_width, height=map_frame_height)
        self.map_frame.grid(row=1, column=1, padx=100, pady=10)  # 使用 grid 佈局管理器
        
        # 創建地圖格子
        self.create_map()
        
        # 在四個角落放置玩家
        self.place_players()
        
    def create_map(self):
        # 創建地圖格子
        for y in range(self.map_height):
            for x in range(self.map_width):
                if x == 0 or x == self.map_width - 1 or y == 0 or y == self.map_height - 1:
                    cell = tk.Label(self.map_frame, width=10, height=5, borderwidth=1, relief="solid")  # 調整格子大小
                    cell.grid(row=y, column=x, padx=1, pady=1)
                    # 綁定點擊事件
                    cell.bind("<Button-1>", lambda event, cell=cell, x=x, y=y: self.on_cell_click(cell, x, y))
        
    def place_players(self):
        # 調整玩家圖像大小
        player_image_path = "character/馬力歐.png"
        image = Image.open(player_image_path)
        image = image.resize((100, 120), Image.LANCZOS)
        player_photo = ImageTk.PhotoImage(image)
        
        # 在四個角落放置玩家
        player1 = tk.Label(self.master, image=player_photo)
        player1.image = player_photo
        player1.grid(row=0, column=0, padx=20, pady=20, sticky="nw")
        
        player2 = tk.Label(self.master, image=player_photo)
        player2.image = player_photo
        player2.grid(row=0, column=2, padx=20, pady=20, sticky="ne")
        
        player3 = tk.Label(self.master, image=player_photo)
        player3.image = player_photo
        player3.grid(row=2, column=0, padx=20, pady=20, sticky="sw")
        
        player4 = tk.Label(self.master, image=player_photo)
        player4.image = player_photo
        player4.grid(row=2, column=2, padx=20, pady=20, sticky="se")
        
    def on_cell_click(self, cell, x, y):
        # 顯示點擊的格子編號
        index = y * self.map_width + x + 1
        messagebox.showinfo("Info", "You clicked on grid: {}".format(index))

def main():
    root = tk.Tk()
    root.geometry("1500x1500")  # 設置視窗大小
    app = MapApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
"""