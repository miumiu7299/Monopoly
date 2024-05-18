import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk
import os

#file_path = os.path.join("Users", "yejiayu", "Desktop", "python", "map.png")
#self.image = Image.open(file_path)


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
        self.board_size = 30 #共30格
        self.properties = self.create_properties()
        self.ui = ui

    def create_properties(self):
        properties = []
        for i in range(self.board_size):
            if i in [5, 20]: 
                properties.append(Property(f"Chance or Destiny{i}", type="chanceordestiny"))
            elif i in [27]: 
                properties.append(Property(f"Emergency {i}", type="emergency"))#直接去醫院
            elif i in [23]: 
                properties.append(Property(f"Fat->killed {i}", type="fattokilled"))
            elif i in [16]: 
                properties.append(Property(f"Hospital {i}", type="hospital"))
            elif i in [11]: 
                properties.append(Property(f"Magic Card {i}", type="magiccard"))
            elif i in [8]: 
                properties.append(Property(f"Jail {i}", type="jail"))
            elif i in [29]: 
                properties.append(Property(f"媽媽的愛 {i}", 4500))
            elif i in [28]: 
                properties.append(Property(f"A5和牛 {i}", 3000))
            elif i in [26]: 
                properties.append(Property(f"魚子醬 {i}", 1500))
            elif i in [25]: 
                properties.append(Property(f"松葉蟹 {i}", 3500))
            elif i in [24]: 
                properties.append(Property(f"鮑魚烏參佛跳牆 {i}", 2200))
            elif i in [22]: 
                properties.append(Property(f"威靈頓牛排 {i}", 2800))
            elif i in [21]: 
                properties.append(Property(f"龍蝦 {i}", 1000))
            elif i in [19]: 
                properties.append(Property(f"火鍋{i}", 350))
            elif i in [18]: 
                properties.append(Property(f"義大利麵 {i}", 400))
            elif i in [17]: 
                properties.append(Property(f"牛排 {i}", 700))
            elif i in [15]: 
                properties.append(Property(f"pizza {i}", 300))
            elif i in [14]: 
                properties.append(Property(f"壽司 {i}", 350))
            elif i in [13]: 
                properties.append(Property(f"燒烤 {i}", 800))
            elif i in [12]: 
                properties.append(Property(f"石鍋拌飯 {i}", 200))
            elif i in [10]: 
                properties.append(Property(f"牛肉麵 {i}", 250))
            elif i in [9]: 
                properties.append(Property(f"咖哩 {i}", 100))
            elif i in [7]: 
                properties.append(Property(f"新竹人的❤️ 麥當勞 {i}", 150))
            elif i in [6]: 
                properties.append(Property(f"便當 {i}", 80))
            elif i in [4]: 
                properties.append(Property(f"想不到吃什麼 7-11 {i}", 70))
            elif i in [3]: 
                properties.append(Property(f"不健康的泡麵{i}", 50))
            elif i in [2]: 
                properties.append(Property(f"噴水火雞肉飯 {i}", 35))
            elif i in [1]: 
                properties.append(Property(f"啃饅頭 {i}", 10))
            else:
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

        self.game = MonopolyGame(self)

        # 主框架設置
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 左側用於地圖
        self.map_frame = tk.Frame(self.main_frame, width=800)
        self.map_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 右側用於控制和消息
        self.control_frame = tk.Frame(self.main_frame, width=800)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 加載並顯示地圖圖像
        #file_path = os.path.join("/Users", "yejiayu", "Desktop", "python", "map.png")
        #original_image = Image.open(file_path)
        image_path = "map.png"
        original_image = Image.open(image_path)
        resized_image = original_image.resize((780, 780), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(resized_image)
        self.image_label = tk.Label(self.map_frame, image=self.photo)
        self.image_label.pack(fill=tk.BOTH, expand=True)
        
        # 玩家信息框架
        self.players_frame = tk.Frame(self.control_frame)
        self.players_frame.pack(pady=20)

        # 創建四個玩家信息顯示 Text 組件，田字格布局
        self.player_texts = []
        for i in range(4):
            frame = tk.Frame(self.players_frame)
            # 使用 grid 來安排田字格布局，每兩個一組橫排
            frame.grid(row=i//2, column=i%2, padx=10, pady=10)
            text_widget = tk.Text(frame, height=8, width=30, font=('Arial', 12))
            text_widget.pack(fill=tk.BOTH, expand=True)
            self.player_texts.append(text_widget)

        # 控制元件，包括按鈕在內的 Frame
        self.button_frame = tk.Frame(self.control_frame)
        self.button_frame.pack(pady=10)

        self.player_name_var = tk.StringVar()
        self.player_name_entry = tk.Entry(self.control_frame, textvariable=self.player_name_var)
        self.player_name_entry.pack(pady=10)

        self.add_player_button = tk.Button(self.button_frame, text="添加玩家", command=self.add_player)
        self.add_player_button.pack(side=tk.LEFT, padx=5)

        self.next_turn_button = tk.Button(self.button_frame, text="丟骰子", command=self.next_turn)
        self.next_turn_button.pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(self.control_frame, text="遊戲狀態")
        self.status_label.pack(fill=tk.X, expand=True, pady=10)

        # 提升消息框的高度
        self.message_listbox = tk.Listbox(self.control_frame, height=20)
        # 在這裡添加 padx 和 pady 以增加邊距
        self.message_listbox.pack(fill=tk.X, expand=True, padx=20, pady=20)

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