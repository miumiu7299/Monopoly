import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk,ImageSequence
import os
from tkinter import PhotoImage
import time
from globals import Globals
import pickle
import subprocess

class Globals:
    selected_characters = {}
    current_player = 1
    players = 1
    money = 50000

    @staticmethod
    def load_from_file(filename):
        with open(filename, 'rb') as file:
            data = pickle.load(file)
        Globals.selected_characters = data['selected_characters']
        Globals.current_player = data['current_player']
        Globals.players = data['players']
        Globals.money = data['money']

class DiceAnimationWindow:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("骰子動畫")
        self.root.geometry("200x200")
        self.dice_label = tk.Label(self.root)
        self.dice_label.pack(expand=True)

        self.dice_images = [ImageTk.PhotoImage(Image.open(f'dice/{i}.png')) for i in range(1, 7)]
        self.result = None  # 用於存儲骰子的結果
        self.callback = None  # 回調函數

    def roll_dice_animation(self):
        def animate(count):
            if count > 0:
                img = random.choice(self.dice_images)
                self.dice_label.config(image=img)
                self.root.after(100, animate, count - 1)
            else:
                result_img = random.choice(self.dice_images)
                self.result = self.dice_images.index(result_img) + 1  # 將結果設置為 1 到 6 的整數值
                self.dice_label.config(image=result_img)
                if self.callback:
                    self.callback(self.result)  # 調用回調函數並傳送結果

                # 動畫結束後，等3秒後關閉視窗
                self.root.after(1000, self.root.destroy)
        
        animate(10) 

    def set_callback(self, callback):
        self.callback = callback
class Player:
    def __init__(self, name, position=0, money=4000):
        self.name = name
        self.position = position
        self.skip_turns = 0
        self.money = int(Globals.money)
        self.properties = []
        self.in_jail = False
        self.in_hospital = False
        self.is_emergency = False
        self.has_jail_free_card = False

    def move(self, steps, board_size,ui):
        for step in range(steps):
            self.position = (self.position + 1) % board_size
            ui.update_player_piece_position(self)
            ui.root.update()
            time.sleep(0.5)
    
    def update_money(self, amount):
        self.money += amount

    def buy_property(self, property_name, cost):
        if self.money >= cost:
            self.money -= cost
            self.properties.append(property_name)
            return True
        return False

class GotchaStore:
    def __init__(self, players, current_turn):
        self.store_window = tk.Toplevel()
        self.players = players
        self.current_turn = current_turn
        self.current_player = None
        self.players.money = self.players.money
        print(self.players.money)
        self.store_window.title("Gotcha Store")
        self.store_window.geometry("1050x550")
        self.store_window.resizable(0, 0)
        self.store_window.attributes("-topmost", 1)

        # Load and set initial background image for the initial window
        initial_bg_image_path = "picture/background1.png"
        store_bg_image_path = "picture/background2.png"

        self.initial_bg_image = ImageTk.PhotoImage(Image.open(initial_bg_image_path).resize((1050, 550)))
        self.store_bg_image = ImageTk.PhotoImage(Image.open(store_bg_image_path).resize((1050, 550)))

        self.bg_label = tk.Label(self.store_window, image=self.initial_bg_image)
        self.bg_label.place(relwidth=1, relheight=1)

        self.store_label = tk.Label(self.store_window, text="Welcome to Gotcha Store!", font=("Helvetica", 16), bg="#FFFFFF")
        self.store_label.pack(pady=20)

        self.message_label = tk.Label(self.store_window, text="", font=("Helvetica", 12), fg="green", bg="#FFFFFF")
        self.message_label.pack(pady=10)
        
        self.card_frame = tk.Frame(self.store_window)
        self.card_frame.pack(pady=20)

        # Sample cards with prices and images
        card_image_paths = {
            "Block Opponent": "picture/block_card.png",
            "Get Boost": "picture/fast_card.png",
            "Steal Money": "picture/steal_card.png",
            "Double Roll": "picture/doubleroll_card.png",
            "Immunity": "picture/immune_card.png",
            "Alliance": "picture/Allliance_card.png",
            "Wizard": "picture/Wizard_card.png"
        }

        self.cards = [
            {"name": "Block Opponent", "description": "Block another player for one turn.", "price": 50, "image": card_image_paths["Block Opponent"]},
            {"name": "Get Boost", "description": "Move forward 3 extra spaces on your next turn.", "price": 100, "image": card_image_paths["Get Boost"]},
            {"name": "Steal Money", "description": "Steal $50 from another player.", "price": 75, "image": card_image_paths["Steal Money"]},
            {"name": "Double Roll", "description": "Roll the dice twice on your next turn.", "price": 150, "image": card_image_paths["Double Roll"]},
            {"name": "Immunity", "description": "Immune to any blocks for one turn.", "price": 200, "image": card_image_paths["Immunity"]},
            {"name": "Alliance", "description": "No tolls will be collected from each other for 1 round.", "price": 500, "image": card_image_paths["Alliance"]},
            {"name": "Wizard", "description": "Choose to use magic on a player to make 5 of his cards disappear!", "price": 999, "image": card_image_paths["Wizard"]}
        ]

        self.current_cards = []
        self.enter_store()

    def enter_store(self):
        # Change the background image for the store
        self.bg_label.config(image=self.store_bg_image)
        self.show_cards()
        
    def show_cards(self):
        for widget in self.card_frame.winfo_children():
            widget.destroy()

        if not self.current_cards:
            self.current_cards = random.sample(self.cards, 3)  # Show 3 random cards each turn

        for card in self.current_cards:
            image = Image.open(card["image"])
            resized_image = image.resize((240, 320))  # Resize the card image
            card_image = ImageTk.PhotoImage(resized_image)

            card_button = tk.Button(
                self.card_frame, 
                text=f"{card['name']}\n{card['description']}\nPrice: ${card['price']}",
                image=card_image,
                compound=tk.TOP,
                command=lambda c=card: self.show_confirm_buttons(c)
            )
            card_button.image = card_image  # Keep a reference to avoid garbage collection
            card_button.pack(side=tk.LEFT, padx=10)
        
        # Add Exit button
        exit_button = tk.Button(self.card_frame, text="Exit", command=self.store_window.destroy)
        exit_button.pack(side=tk.BOTTOM, pady=10)
        exit_button.config(width=5, height= 2)

    def show_confirm_buttons(self, card):
        # Hide existing cards
        for widget in self.card_frame.winfo_children():
            widget.pack_forget()

        # Display the chosen card in the middle
        image = Image.open(card["image"])
        resized_image = image.resize((200, 250))  # Resize the card image
        card_image = ImageTk.PhotoImage(resized_image)

        chosen_card_label = tk.Label(self.card_frame, image=card_image)
        chosen_card_label.image = card_image  # Keep a reference to avoid garbage collection
        chosen_card_label.pack(pady=20)

        card_details_label = tk.Label(
            self.card_frame, 
            text=f"{card['name']}\n{card['description']}\nPrice: ${card['price']}", 
            font=("Helvetica", 12), 
            bg="#FFFFFF"
        )
        card_details_label.pack(pady=10)

        # Display Buy and Cancel buttons
        buy_button = tk.Button(self.card_frame, text="Buy", command=lambda: self.buy_card(card))
        cancel_button = tk.Button(self.card_frame, text="Cancel", command=self.show_cards)
        
        buy_button.pack(side=tk.LEFT, padx=20)
        cancel_button.pack(side=tk.RIGHT, padx=20)
    def show_message(self, message, color="green"):
        self.message_label.config(text=message, fg=color)

    def buy_card(self, card):
        print(self.players.money)
        if self.players.money >= card["price"]:
            self.players.money -= card["price"]
            #Globals.money = self.players[self.current_player]  # Update Globals money
            self.show_message(f"Purchase Successful: You bought the card: {card['name']}", "green")
        else:
            self.show_message("Insufficient Funds", "You do not have enough money to buy this card.")
        self.exit_store()

    def exit_store(self):
        print(self.players.money)
        self.store_window.destroy()



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
        self.board_size = 26 #共30格
        self.properties = self.create_properties()
        self.ui = ui
        self.chance_fate_ui_instance = None
        

    def create_properties(self):
        properties = []
        for i in range(self.board_size):
            if i in [4, 16]: 
                properties.append(Property(f"Chance or Destiny{i}", type="chanceordestiny"))
            elif i in [19]: 
                properties.append(Property(f"Emergency {i}", type="emergency"))#直接去醫院
            elif i in [22]: 
                properties.append(Property(f"Fat->killed {i}", type="fattokilled"))
            elif i in [13]: 
                properties.append(Property(f"Hospital {i}", type="hospital"))
            elif i in [10]: 
                properties.append(Property(f"Magic Card {i}", type="magiccard"))
            elif i in [9]: 
                properties.append(Property(f"Jail {i}", type="jail"))
            elif i in [25]: 
                properties.append(Property(f"媽媽的愛 {i}", 4500))
            elif i in [24]: 
                properties.append(Property(f"A5和牛 {i}", 3000))
            elif i in [23]: 
                properties.append(Property(f"魚子醬 {i}", 1500))
            elif i in [21]: 
                properties.append(Property(f"鮑魚烏參佛跳牆 {i}", 2200))
            elif i in [20]: 
                properties.append(Property(f"威靈頓牛排 {i}", 2800))
            elif i in [18]: 
                properties.append(Property(f"龍蝦 {i}", 1000))
            elif i in [17]: 
                properties.append(Property(f"牛排 {i}", 500))
            elif i in [15]: 
                properties.append(Property(f"火鍋{i}", 350))
            elif i in [14]: 
                properties.append(Property(f"pizza {i}", 300))
            elif i in [12]: 
                properties.append(Property(f"義大利麵 {i}", 400))
            elif i in [11]: 
                properties.append(Property(f"燒烤 {i}", 800))
            elif i in [8]: 
                properties.append(Property(f"石鍋拌飯 {i}", 200))
            elif i in [7]: 
                properties.append(Property(f"牛肉麵 {i}", 250))
            elif i in [6]: 
                properties.append(Property(f"壽司 {i}", 350))
            elif i in [5]: 
                properties.append(Property(f"咖哩 {i}", 100))
            elif i in [3]: 
                properties.append(Property(f"韓式炸雞 {i}", 250))
            elif i in [2]: 
                properties.append(Property(f"新竹人❤麥當勞 {i}", 150))
            elif i in [1]: 
                properties.append(Property(f"便當 {i}", 80))
            elif i in [0]: 
                properties.append(Property(f"Start {i}", 0))
        #return []
        return properties

    def add_player(self, player):
        self.players.append(player)
        self.ui.create_player_piece(player)
    def next_turn(self):  
        if not self.players:
            messagebox.showerror("Error", "No players in the game.")
            return
        while self.players[self.current_turn].skip_turns > 0:
            current_player = self.players[self.current_turn]
            self.players[self.current_turn].skip_turns -= 1
            self.ui.update_status_label(f"{self.players[self.current_turn].name} is skipping this turn.")
            self.current_turn = (self.current_turn + 1) % len(self.players)
            self.ui.update_player_list()

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
                
        steps = 10 #self.roll_dice()
        current_player.move(steps, self.board_size,self.ui)
        self.ui.next_turn_button.config(state=tk.NORMAL)
        self.ui.update_status_label(f"{current_player.name} rolled a {steps} and moved to position {current_player.position}.")
        self.ui.update_player_piece_position(current_player)

        self.handle_space_action(current_player)
            
        self.ui.update_player_list()

        self.current_turn = (self.current_turn + 1) % len(self.players)

    def roll_dice(self):
        self.ui.next_turn_button.config(state=tk.DISABLED)
        animation_window = DiceAnimationWindow()
        result_container = [None]  # 使用列表来存储结果，以便在回调函数中修改它
        # 定义回调函数来获取结果并打印
        def callback(result):
            result_container[0] = result  # 存储结果到 result_container 中
        # 设置回调函数
        animation_window.set_callback(callback)
        # 开始骰子动画
        animation_window.roll_dice_animation()
        # 等待动画完成
        animation_window.root.wait_window()
        # 返回结果
        
        return result_container[0]

    def handle_space_action(self, player):
        if 0 <= player.position < len(self.properties):
            property = self.properties[player.position]
            if property.type == "chanceordestiny":
                self.ui.add_message(f"{player.name} landed on a Chance or Destiny space.")

                amount = random.choice([50,-50 ])
                if amount > 0:
                    self.draw_chance_card(player)
                else:
                    self.draw_destiny_card(player)

            elif property.type == "emergency" and player.position == 19:
                self.ui.add_message(f"{player.name}  landed on a Emergency space and moved to hospital.")
                player.is_emergency = True
                self.ui.root.update()
                time.sleep(0.5)
                player.position=13
                self.ui.update_player_piece_position(player)
            elif property.type == "fattokilled":
                self.ui.add_message(f"{player.name} landed on a Fat->killed space , you are so fat that you will get killed!!!")
            elif property.type == "hospital":
                self.ui.add_message(f"{player.name} landed on a Hospital space and stays for one turn.")
                player.in_hospital = True
            elif property.type == "magiccard":
                self.ui.add_message(f"{player.name} landed on a Magic Card space")
                self.draw_magic_card(player)
            elif property.type == "jail":
                    if player.has_jail_free_card:
                        player.has_jail_free_card = False
                        self.ui.add_message(f"{player.name} used a Get Out of Jail Free card and avoided jail.")
                    else:
                        self.ui.add_message(f"{player.name} landed on a Jail space and stays for one turn.")
                        player.in_jail = True
                #self.ui.update_player_list()

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
    
    def store(self):
        self.store_app = GotchaStore(self.store_window, self.players, self.current_turn)


    def draw_chance_card(self, player):
        def on_close(result):
            print(f"讀取到的卡牌結果: {result}")
            if result =="恭喜獲得 300 金幣!":
                amount=300
            elif  result =="恭喜獲得 500 金幣!!":
                amount=500
            elif  result =="恭喜要損失 300 金幣哈哈":
                amount=-300
            elif  result =="恭喜獲得 100 金幣!!":
                amount=100
            elif  result =="恭喜要損失 200 金幣哈哈":
                amount=-200
            elif  result =="恭喜獲得 700 金幣!!":
                amount=700
            elif  result =="恭喜要損失 100 金幣哈哈":
                amount=-100
            elif  result =="甚麼都沒有":
                return
            elif  result =="恭喜要損失 300 金幣哈":
                amount=-300
            elif  result =="恭喜獲得 300 金幣!!":
                amount=300
            elif  result =="恭喜要損失 200 金幣哈哈":
                amount=-200
            elif  result =="恭喜要損失 20 金幣哈哈":
                amount=-20
            elif  result =="莫名其妙獲得 100 金幣!!":
                amount=100
            elif  result =="恭喜要損失 50 金幣哈哈":
                amount=-50
            if player.money >= -amount:
                player.update_money(amount)
            else:
                self.ui.add_message(f"{player.name} does not have enough money to pay rent and is bankrupt.")
                messagebox.showinfo("Bankrupt", f"{player.name} does not have enough money  and is bankrupt.")
                self.end_game()
                self.ui.game_over() 
            #player.update_money(amount)
            #self.ui.add_message(f"{player.name} drew a Destiny card and the result was: {result}")
            self.ui.update_player_list()
        self.chance_fate_ui_instance = ChanceUI(self.ui.root, on_close)
        
    def draw_destiny_card(self, player):
        current_player = self.players[self.current_turn]
        def on_close(result):
            print(f"讀取到的卡牌結果: {result}")
            if result =="說不定是明智的選擇[損失500金幣]":
                amount=-500
            elif  result =="乖乖秀秀痛痛飛走[損失10金幣]":
                amount=-10
            elif  result =="土地公顯靈[增加600金幣]":
                amount=600
            elif  result =="恭喜獲得不會做菜的廚師[損失300金幣]":
                amount=-300
            elif  result =="放屁有益身體健康[獲得200金幣]":
                amount=200
            elif  result =="聽君一席話，如聽一席話":
                return
            elif  result =="上帝可能比較忙[損失100金幣]":
                amount=-100
            elif  result =="衝動是不好的行為[損失100金幣]":
                amount=-100
            elif  result =="逆轉乾坤 倒立人生":
                return
            elif  result =="想偷懶不是這樣的[損失200金幣]":
                amount=-200
            elif result =="退後不一定是壞事[後退五格]":
                if player.position == 4:
                    self.ui.root.update()
                    time.sleep(0.5)
                    player.position=25
                    self.ui.update_player_piece_position(player)
                    self.ui.update_player_list()
                    self.current_turn = (self.current_turn + 1) % len(self.players)
                elif player.position == 16:
                    self.ui.root.update()
                    time.sleep(0.5)
                    player.position=11
                    self.ui.update_player_piece_position(player)
                    self.ui.update_player_list()
                    self.current_turn = (self.current_turn + 1) % len(self.players)
                return
            elif result =="在馬桶上安頓好再走[停止兩回合]":
                current_player.skip_turns = 2
                self.ui.update_status_label(f"{current_player.name}  skips this turn.")
                self.ui.update_player_list()
                #self.current_turn = (self.current_turn + 1) % len(self.players)
                return
            elif result =="這樣算賄賂嗎[獲得一次免進監獄牌（保留此張牌直到使用完）]":
                current_player.has_jail_free_card = True
                self.ui.update_status_label(f"{current_player.name} obtained a Get Out of Jail Free card.")
                self.ui.update_player_list()
                #self.next_turn()  # 立即進入下一個玩家的回合
                return
            if player.money >= -amount:
                player.update_money(amount)
            else:
                self.ui.add_message(f"{player.name} does not have enough money to pay rent and is bankrupt.")
                messagebox.showinfo("Bankrupt", f"{player.name} does not have enough money  and is bankrupt.")
                self.end_game()
                self.ui.game_over() 
            #player.update_money(amount)
            #self.ui.add_message(f"{player.name} drew a Destiny card and the result was: {result}")
            self.ui.update_player_list()
        self.chance_fate_ui_instance = FateUI(self.ui.root, on_close)

    def draw_magic_card(self, player):
        amount = random.choice([1000,100])
        player.update_money(amount)
        self.ui.add_message(f"{player.name} drew a Magic card and received ${amount}.")
                
class ChanceUI:
    def __init__(self,parent, on_close_callback):
        self.drawn_card_result = None  # 在 __init__ 方法中添加這行
        #self.win = tk.Tk()
        self.on_close_callback = on_close_callback
        self.win = tk.Toplevel(parent)
        self.win.title("Flashing Button Example")
        self.win.geometry("1050x550")
        self.win.resizable(0, 0)
        self.win.config(bg="#f0f0f0")

        screen_width = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()
        x = int((screen_width - 1050) / 2)
        y = int((screen_height - 580) / 2)
        self.win.geometry(f"+{x}+{y}")

        self.card_function_label = tk.Label(self.win, text="", font=("Helvetica", 16), bg="white")
        self.card_function_label.grid(row=10, columnspan=5)

        image_path = "chance/CHANCE_COVER.png"
        image_paths_new = [
            "chance/chance_1.png",
            "chance/chance_2.png",
            "chance/chance_3.png",
            "chance/chance_4.png",
            "chance/chance_5.png",
            "chance/chance_6.png",
            "chance/chance_7.png",
            "chance/chance_8.png",
            "chance/chance_9.png",
            "chance/chance_10.png",
            "chance/chance_11.png",
            "chance/chance_12.png",
            "chance/chance_13.png",
            "chance/chance_14.png",
        ]

        original_image = Image.open(image_path)
        original_width, original_height = original_image.size
        target_width = int(original_width * 0.19)
        target_height = int(original_height * 0.19)
        resized_image = original_image.resize((target_width, target_height))

        self.img_normal = ImageTk.PhotoImage(resized_image)
        self.img_blank = ImageTk.PhotoImage(Image.new('RGBA', (target_width, target_height), (0, 0, 0, 0)))

        resized_images_new = [{'path': path, 'image': ImageTk.PhotoImage(Image.open(path).resize((target_width, target_height)))} for path in image_paths_new]
        self.imgs_new = [img for img in resized_images_new]

        self.image_to_message = {
            "chance/chance_1.png": "恭喜獲得 300 金幣!",
            "chance/chance_2.png": "恭喜獲得 500 金幣!!",
            "chance/chance_3.png": "恭喜要損失 300 金幣哈哈",
            "chance/chance_4.png": "恭喜獲得 100 金幣!!",
            "chance/chance_5.png": "恭喜要損失 200 金幣哈哈",
            "chance/chance_6.png": "恭喜獲得 700 金幣!!",
            "chance/chance_7.png": "恭喜要損失 100 金幣哈哈",
            "chance/chance_8.png": "甚麼都沒有",
            "chance/chance_9.png": "恭喜要損失 300 金幣哈哈",
            "chance/chance_10.png": "恭喜獲得 300 金幣!!",
            "chance/chance_11.png": "恭喜要損失 200 金幣哈哈",
            "chance/chance_12.png": "恭喜要損失 20 金幣哈哈",
            "chance/chance_13.png": "莫名其妙獲得 100 金幣!!",
            "chance/chance_14.png": "恭喜要損失 50 金幣哈哈",
        }

        gif_path = "chance/drawCard.gif"
        gif = Image.open(gif_path)
        scale_factor = 0.7
        original_width, original_height = gif.size
        target_width = int(original_width * scale_factor)
        target_height = int(original_height * scale_factor)

        self.update_frame_index = 0  # 增加这一行来跟踪帧索引
        # 确保frames不会被垃圾回收
        self.frames = []
        try:
            while True:
                for frame in ImageSequence.Iterator(gif):
                    gif.seek(len(self.frames))
                    frame = gif.copy().convert('RGBA').resize((target_width, target_height))
                    self.frames.append(ImageTk.PhotoImage(frame))
        except EOFError:
            pass

        self.gif_label = tk.Label(self.win)
        self.gif_label.grid(row=0, column=0, columnspan=5, pady=20)
        self.animate_gif()
        #self.animate_gif(self.gif_label,self.frames, delay=100)
        self.win.after(3600, self.show_cards)
        self.win.grid_columnconfigure(0, weight=1)
        self.win.grid_columnconfigure(1, weight=1)
        self.win.grid_columnconfigure(2, weight=1)
        self.win.grid_columnconfigure(3, weight=1)
        self.win.grid_columnconfigure(4, weight=1)
        self.win.grid_rowconfigure(0, weight=1)
        self.gif_label.grid(row=0, column=0, columnspan=8)

        self.win.protocol("WM_DELETE_WINDOW", self.on_close)


    def button_clicked(self, card):
        print("你選擇了此張命運卡牌!")
        self.flash_button(card, 0)

    def flash_button(self, card, count):
        if count < 7:
            if count % 2 == 0:
                card.config(image=self.img_normal)
            else:
                card.config(image=self.img_blank)
            count += 1
            card.after(150, self.flash_button, card, count)
        else:
            new_image = random.choice(self.imgs_new)
            card.config(image=new_image['image'])
            card.image = new_image['image']
            self.win.after(1000, lambda: self.handle_draw_card_result(self.draw_card(new_image['path'])))

    def handle_draw_card_result(self, result):
        self.drawn_card_result = result  # 保存抽到的卡牌結果
        print(f"卡牌結果已設置: {result}")  # 添加调试信息
        self.on_close()
        
    def get_drawn_card_result(self):
        return self.drawn_card_result

    def draw_card(self, image_path):
        message = self.image_to_message.get(image_path, "未知卡牌")
        for widget in self.win.winfo_children():
            widget.grid_remove()

        original_image = Image.open(image_path)
        original_width, original_height = original_image.size
        target_width = int(original_width * 0.3)
        target_height = int(original_height * 0.3)
        resized_image = original_image.resize((target_width, target_height))
        card_image = ImageTk.PhotoImage(resized_image)
        card_image_label = tk.Label(self.win, image=card_image)
        card_image_label.image = card_image
        card_image_label.grid(row=9, columnspan=5, pady=(50, 30))
        self.card_function_label.config(text=message, bg="#f0f0f0")
        self.card_function_label.grid(row=10, columnspan=5)
        confirm_button = tk.Button(self.win, text="確認", font=("Helvetica", 17), command=self.win.destroy)
        #confirm_button = tk.Button(self.win, text="確認", font=("Helvetica", 17), command=self.on_close)
        confirm_button.grid(row=11, columnspan=5, pady=(10, 60))
        print(message)
        return message
        

    def show_cards(self):
        self.gif_label.grid_remove()
        buttons = []
        for i in range(10):
            button = tk.Button(self.win, image=self.img_normal, bd=0, highlightthickness=0)
            button.bind("<Enter>", self.on_enter)
            button.bind("<Leave>", self.on_leave)
            row = i // 5
            col = i % 5
            button.grid(row=row, column=col, padx=10, pady=10)
            button.config(command=lambda b=button: self.button_clicked(b))
            buttons.append(button)

    def on_leave(self, event):
        event.widget.config(borderwidth=0, relief="flat")

    def on_enter(self, event):
        if isinstance(event.widget, tk.Button):
            event.widget.config(borderwidth=2, relief="solid")

    def animate_gif(self):
        def update_frame():
            frame = self.frames[self.update_frame_index]
            self.gif_label.config(image=frame)
            self.update_frame_index = (self.update_frame_index + 1) % len(self.frames)
            self.win.after(100, update_frame)  # 调整延迟时间以控制动画速度
        update_frame()
        
    def on_close(self):
        if self.on_close_callback:
            self.on_close_callback(self.drawn_card_result)
        #self.win.destroy()
    
class FateUI:
    def __init__(self,parent, on_close_callback):
        self.drawn_card_result = None  # 在 __init__ 方法中添加這行
        #self.win = tk.Tk()
        self.on_close_callback = on_close_callback
        self.win = tk.Toplevel(parent)
        self.win.title("Flashing Button Example")
        self.win.geometry("1050x550")
        self.win.resizable(0, 0)
        self.win.config(bg="#f0f0f0")

        screen_width = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()
        x = int((screen_width - 1050) / 2)
        y = int((screen_height - 580) / 2)
        self.win.geometry(f"+{x}+{y}")

        self.card_function_label = tk.Label(self.win, text="", font=("Helvetica", 16), bg="white")
        self.card_function_label.grid(row=10, columnspan=5)

        image_path = "fate/FATE_COVER.png"
        image_paths_new = [
            "fate/fate_1.png",
            "fate/fate_2.png",
            "fate/fate_3.png",
            "fate/fate_4.png",
            "fate/fate_5.png",
            "fate/fate_6.png",
            "fate/fate_7.png",
            "fate/fate_8.png",
            "fate/fate_11.png",
            "fate/fate_12.png",
            "fate/fate_13.png",
            "fate/fate_15.png",
            "fate/fate_17.png"
        ]

        original_image = Image.open(image_path)
        original_width, original_height = original_image.size
        target_width = int(original_width * 0.19)
        target_height = int(original_height * 0.19)
        resized_image = original_image.resize((target_width, target_height))

        self.img_normal = ImageTk.PhotoImage(resized_image)
        self.img_blank = ImageTk.PhotoImage(Image.new('RGBA', (target_width, target_height), (0, 0, 0, 0)))

        resized_images_new = [{'path': path, 'image': ImageTk.PhotoImage(Image.open(path).resize((target_width, target_height)))} for path in image_paths_new]
        self.imgs_new = [img for img in resized_images_new]

        self.image_to_message = {
            "fate/fate_1.png": "說不定是明智的選擇[損失500金幣]",
            "fate/fate_2.png": "乖乖秀秀痛痛飛走[損失10金幣]",
            "fate/fate_3.png": "退後不一定是壞事[後退五格]",
            "fate/fate_4.png": "土地公顯靈[增加600金幣]",
            "fate/fate_5.png": "恭喜獲得不會做菜的廚師[損失300金幣]",
            "fate/fate_6.png": "放屁有益身體健康[獲得200金幣]",
            "fate/fate_7.png": "在馬桶上安頓好再走[停止兩回合]",
            "fate/fate_8.png": "聽君一席話，如聽一席話",
            "fate/fate_11.png": "上帝可能比較忙[損失100金幣]",
            "fate/fate_12.png": "衝動是不好的行為[損失100金幣]",
            "fate/fate_13.png": "逆轉乾坤 倒立人生",
            "fate/fate_15.png": "這樣算賄賂嗎[獲得一次免進監獄牌（保留此張牌直到使用完）]",
            "fate/fate_17.png": "想偷懶不是這樣的[損失200金幣]"
        }

        gif_path = "fate/drawFateCard.gif"
        gif = Image.open(gif_path)
        scale_factor = 0.7
        original_width, original_height = gif.size
        target_width = int(original_width * scale_factor)
        target_height = int(original_height * scale_factor)

        self.update_frame_index = 0  # 增加这一行来跟踪帧索引
        # 确保frames不会被垃圾回收
        self.frames = []
        try:
            while True:
                for frame in ImageSequence.Iterator(gif):
                    gif.seek(len(self.frames))
                    frame = gif.copy().convert('RGBA').resize((target_width, target_height))
                    self.frames.append(ImageTk.PhotoImage(frame))
        except EOFError:
            pass

        self.gif_label = tk.Label(self.win)
        self.gif_label.grid(row=0, column=0, columnspan=5, pady=20)
        self.animate_gif()
        #self.animate_gif(self.gif_label,self.frames, delay=100)
        self.win.after(3600, self.show_cards)
        self.win.grid_columnconfigure(0, weight=1)
        self.win.grid_columnconfigure(1, weight=1)
        self.win.grid_columnconfigure(2, weight=1)
        self.win.grid_columnconfigure(3, weight=1)
        self.win.grid_columnconfigure(4, weight=1)
        self.win.grid_rowconfigure(0, weight=1)
        self.gif_label.grid(row=0, column=0, columnspan=8)

        self.win.protocol("WM_DELETE_WINDOW", self.on_close)


    def button_clicked(self, card):
        print("你選擇了此張命運卡牌!")
        self.flash_button(card, 0)

    def flash_button(self, card, count):
        if count < 7:
            if count % 2 == 0:
                card.config(image=self.img_normal)
            else:
                card.config(image=self.img_blank)
            count += 1
            card.after(150, self.flash_button, card, count)
        else:
            new_image = random.choice(self.imgs_new)
            card.config(image=new_image['image'])
            card.image = new_image['image']
            self.win.after(1000, lambda: self.handle_draw_card_result(self.draw_card(new_image['path'])))

    def handle_draw_card_result(self, result):
        self.drawn_card_result = result  # 保存抽到的卡牌結果
        print(f"卡牌結果已設置: {result}")  # 添加调试信息
        self.on_close()

        
    def get_drawn_card_result(self):
        return self.drawn_card_result

    def draw_card(self, image_path):
        message = self.image_to_message.get(image_path, "未知卡牌")
        for widget in self.win.winfo_children():
            widget.grid_remove()

        original_image = Image.open(image_path)
        original_width, original_height = original_image.size
        target_width = int(original_width * 0.3)
        target_height = int(original_height * 0.3)
        resized_image = original_image.resize((target_width, target_height))
        card_image = ImageTk.PhotoImage(resized_image)
        card_image_label = tk.Label(self.win, image=card_image)
        card_image_label.image = card_image
        card_image_label.grid(row=9, columnspan=5, pady=(50, 30))
        self.card_function_label.config(text=message, bg="#f0f0f0")
        self.card_function_label.grid(row=10, columnspan=5)
        confirm_button = tk.Button(self.win, text="確認", font=("Helvetica", 17), command=self.win.destroy)
        #confirm_button = tk.Button(self.win, text="確認", font=("Helvetica", 17), command=self.on_close)
        confirm_button.grid(row=11, columnspan=5, pady=(10, 60))
        print(message)
        return message
        

    def show_cards(self):
        self.gif_label.grid_remove()
        buttons = []
        for i in range(10):
            button = tk.Button(self.win, image=self.img_normal, bd=0, highlightthickness=0)
            button.bind("<Enter>", self.on_enter)
            button.bind("<Leave>", self.on_leave)
            row = i // 5
            col = i % 5
            button.grid(row=row, column=col, padx=10, pady=10)
            button.config(command=lambda b=button: self.button_clicked(b))
            buttons.append(button)

    def on_leave(self, event):
        event.widget.config(borderwidth=0, relief="flat")

    def on_enter(self, event):
        if isinstance(event.widget, tk.Button):
            event.widget.config(borderwidth=2, relief="solid")

    def animate_gif(self):
        def update_frame():
            frame = self.frames[self.update_frame_index]
            self.gif_label.config(image=frame)
            self.update_frame_index = (self.update_frame_index + 1) % len(self.frames)
            self.win.after(100, update_frame)  # 调整延迟时间以控制动画速度
        update_frame()
        
    def on_close(self):
        if self.on_close_callback:
            self.on_close_callback(self.drawn_card_result)
        #self.win.destroy()

class GameMenuApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("遊戲菜單")

        # 創建遊戲菜單框架
        self.game_menu_frame = tk.Frame(self.root)
        self.game_menu_frame.pack()

        # 添加按鈕到遊戲菜單框架
        self.new_game_button = tk.Button(self.game_menu_frame, text="開始新遊戲", command=self.start_new_game)
        self.new_game_button.pack(side=tk.TOP, padx=10, pady=(35,10))

        self.exit_button = tk.Button(self.game_menu_frame, text="退出此遊戲", command=self.exit_game)
        self.exit_button.pack(side=tk.TOP, padx=10, pady=10)

        self.exit_button = tk.Button(self.game_menu_frame, text="繼續此遊戲", command=self.root.destroy)
        self.exit_button.pack(side=tk.TOP, padx=10, pady=10)

        window_width = 300
        window_height = 200
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def start_new_game(self):
        self.root.quit()
        self.root.destroy() 
        root.destroy() 
        subprocess.call(["python", "choose.py"])

    def exit_game(self):
        self.root.destroy() 
        root.destroy() 

    def run(self):
        self.root.mainloop()

class MonopolyUI:
    def __init__(self, root):
        self.root = root
        self.root.title("大富翁遊戲")

        # 獲取屏幕寬高
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # 根據屏幕尺寸調整窗口大小
        window_width = int(screen_width * 1)
        window_height = int(screen_height * 1)
        self.root.geometry(f"{window_width}x{window_height}")

        #self.chance_fate_ui = ChanceFateUI()  # 創建ChanceFateUI的實例
        self.game = MonopolyGame(self)
        #self.game = MonopolyGame(self,self.chance_fate_ui)
        self.image_labels = {}
        self.player_pieces = {}
        self.cell_colors = {}  # Dictionary to store the color of each cell
        self.colors = ["red", "blue", "green", "orange"]  # Colors for players

        #GotchaStore((self, root, player))
        self.player ={}
        
        
        # 假定棋盤格子名稱
        self.cell_names = [
            "Start", "便當", "新竹人的❤️麥當勞","韓式炸雞", "Chance or Destiny","咖哩飯","壽司","牛肉麵","石鍋拌飯","jail",
            "媽媽的愛","","","","","","","","","Magic Card",
            "A5和牛","","","","", "","","","","燒烤",
            "魚子醬","","", "","","","","","","義大利麵",
            "Fat->killed", "鮑魚烏參佛跳牆","Beef Wellington","too much delicacy","lobster","steak","Chance or Destiny","hotpot","pizza", "Hospital"
        ]
        
        self.list_names = [
            "Start", "便當", "新竹人的\n❤️\n麥當勞","韓式炸雞", "Chance or\nDestiny","咖哩飯","壽司","牛肉麵","石鍋拌飯","jail",
            "媽媽的愛","","","","","","","","","Magic Card",
            "A5和牛","","","","", "","","","","燒烤",
            "魚子醬","","", "","","","","","","義大利麵",
            "Fat->killed", "鮑魚烏參\n佛跳牆","Beef\nWellington","too much\ndelicacy","lobster","steak","Chance or\nDestiny","hotpot","pizza", "Hospital"
        ]
        
        self.cost_list =[
            "Not for sale", "80", "150","250", "Not for sale","100","350","250","200","Not for sale",
            "4500","","","","","","","","","Not for sale",
            "3000","","","","", "","","","","800",
            "1500","","", "","","","","","","400",
            "Not for sale", "2200","2800","Not for sale","1000","500","Not for sale","500","300", "Not for sale"
        ]
        
        # 自定義映射字典，將格子的實際編號映射到屬性索引
        self.cell_to_property_index = {
            0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 
            10: 10, 19: 11, 20: 12, 29: 13, 30: 14, 39: 15, 40: 16, 41: 17, 42: 18, 43: 19, 
            44: 20, 45: 21, 46: 22, 47: 23, 48: 24, 49: 25
        }

        self.cell_to_property_index2 = {
            0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 
            10: 11, 11:13, 12:15, 13:25, 14:24, 15:23, 16:22, 17:21, 18:20, 19:19,
            20:18, 21:17, 22:16, 23:14, 24:12, 25:10
        }

        # 主框架設置
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 使視窗全屏並隱藏窗口管理工具欄
        self.root.attributes('-fullscreen', True)
        self.root.overrideredirect(True)

        # 在主框架中添加畫布來畫棋盤
        self.board_canvas = tk.Canvas(self.main_frame, width=1000, height=500, bg='white')
        # 使用place方法將畫布置中
        self.board_canvas.place(relx=0.5, rely=0.5, anchor='center')
        self.draw_board()

        # 創建遊戲選單按鈕
        self.game_menu_button = tk.Button(self.root, text="遊戲菜單", command=self.open_game_menu)
        self.game_menu_button.place(relx=0.8, rely=0.68, anchor='se')

        # 創建商城按鈕
        self.store_button = tk.Button(self.root, text="商店", command=self.open_store)
        self.store_button.place(relx=0.235, rely=0.68, anchor='se')
    

        # 創建四個玩家信息顯示 Text 組件，放置在界面的四個角落
        self.player_texts = []
        self.player_images = []  # 初始化 player_images 列表
        positions = [(0.01, 0.5), (0.99, 0.5), (0.01, 0.5), (0.99, 0.5)]

        anchors = [ 'sw', 'se','nw', 'ne']
        
        for i in range(Globals.players):
            pos = positions[i]
            anchor = anchors[i]
            frame = tk.Frame(self.main_frame, width=200, height=400)
            frame.place(relx=pos[0], rely=pos[1], anchor=anchor)
            name = str(Globals.selected_characters[i+1])
            player_image_path = "character/" + name + ".png"
            print(player_image_path)
            if name:
                player = Player(name)
                self.game.add_player(player)
            else:
                messagebox.showerror("Error", "Player name cannot be empty.")
            image = Image.open(player_image_path)
            image = image.resize((80, 104), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            label = tk.Label(frame, image=photo)
            label.image = photo  # 保存對象引用，防止被垃圾回收
            label.pack(side=tk.TOP)
            self.player_images.append(label)
            text_widget = tk.Text(frame, height=15, width=17, font=('Arial', 10))
            text_widget.pack(fill=tk.BOTH, expand=True)
            self.player_texts.append(text_widget)
        self.update_player_list()
        # 控制元件，包括按鈕在內的 Frame
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.place(relx=0.7, rely=0.4, anchor='center')

        self.player_name_var = tk.StringVar()
        self.player_name_entry = tk.Entry(self.main_frame, textvariable=self.player_name_var)
        self.player_name_entry.place(relx=0.5, rely=0.4, anchor='center')

        

        self.next_turn_button = tk.Button(self.button_frame, text="丟骰子", command=self.next_turn)
        self.next_turn_button.pack(side=tk.TOP, pady=5)

        self.status_label = tk.Label(self.main_frame, text="遊戲狀態")
        self.status_label.place(relx=0.5, rely=0.35, anchor='center')

        # 提升消息框的高度
        self.message_listbox = tk.Listbox(self.main_frame, height=10,width=70)
        # 在這裡添加 padx 和 pady 以增加邊距
        self.message_listbox.place(relx=0.5, rely=0.55, anchor='center')
    """   
    def wait_window(self, win):
        self.root.wait_window(win)
    """ 
    def open_store(self):
        current_player = self.game.players[self.game.current_turn]

        self.store_app = GotchaStore( current_player, self.game.current_turn)

    def draw_board(self):
        food_image_paths = [
            "character/start.png",
            "character/bento.png",
            "character/mcdonal's.png",
            "character/korean_fried_chicken.png",
            "character/chance.png",
            "character/curry.png",
            "character/sushi.png",
            "character/beef_noodle.png",
            "character/korean_meal.png",
            "character/prison.png",
            "character/mom_love.png",
            "character/magic_card.png",
            "character/a5.png",
            "character/barbecue.png",
            "character/fish.png",
            "character/pasta.png",
            "character/eat_too_much.png",
            "character/chinese_dish.png",
            "character/advanced_steak.png",#威
            "character/too_many_delicy.png",
            "character/lobster.png",
            "character/steak.png",#威
            "character/chance.png",
            "character/hotpot.png",#hotpot
            "character/pizza.png",#pizza
            "character/hospital.png"
            
            # Add more food image paths as needed
        ]
        
                
        food_image_pic=0
        rows, cols = 5, 10
        # 确保格子为正方形
        cell_size = min(1000 / cols, 500 / rows)

        cell_index = 0
        for row in range(rows):
            for col in range(cols):
                if (row == 0 or row == rows - 1) or (col == 0 or col == cols - 1):
                    x1 = col * cell_size
                    y1 = row * cell_size
                    x2 = x1 + cell_size
                    y2 = y1 + cell_size
                
                    property_index = self.cell_to_property_index[cell_index]
                    # 计算格子的索引，假设每个格子都有一个名字存储在 self.cell_names 列表中
                    #cell_index = row * cols + col
                    if property_index is not None:
                        cell_name = self.cell_names[cell_index]  # 循环使用名字列表
                        list_index = row * cols + col
                        list_name=self.list_names[list_index]  # 循环使用名字列表
                        cost_index = row * cols + col
                        cost_name=self.cost_list[cost_index]  # 循环使用名字列表
                        outline_color = 'black' if (row == 0 or row == rows - 1 or col == 0 or col == cols - 1) else ''
                    
                    rect = self.board_canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline=outline_color)
                    # Store the rectangle ID
                    #for index in cell_indices:

                    #self.cell_colors[cell_index] = rect
                    self.cell_colors[property_index] = rect
                    self.board_canvas.tag_bind(rect, '<Button-1>', lambda event, name=cell_name, cost=cost_name, image_path=food_image_paths[food_image_pic]: self.show_cell_name_picture(name, cost, image_path))
                    #print(property_index,rect)
                    self.board_canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=list_name, fill="black", font=("Arial", 12, "bold"))
                    food_image_pic += 1
                    
                #key+=1
                cell_index += 1
                    
    def make_callback(self, name, cost,image_path):
        return lambda event: self.show_cell_name_picture(name, cost,image_path)
                    
    def show_cell_name_picture(self, name,cost ,image_path):
        top = tk.Toplevel(self.root)
        top.title(f"{name}詳細資訊")
        
        img = Image.open(image_path)
        img = img.resize((250, 250))  # Resize if needed
        photo = ImageTk.PhotoImage(img)

        label = tk.Label(top, image=photo,width=300,height=300)
        label.image = photo
        label.pack()
       
        tk.Label(top, text=f"地點: {name}\n價格: {cost}").pack()

        window_width = 300
        window_height = 350
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        x_pos = (screen_width - window_width) // 2
        y_pos = (screen_height - window_height) // 2

        top.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

        label.image = photo
    
    def create_player_piece(self, player):
        colors = ['red', 'blue', 'green', 'orange']
        color = colors[len(self.player_pieces) % len(colors)]
        x,y = self.get_position_coordinates(player.position, len(self.game.players)-1)
        piece = self.board_canvas.create_oval(x-10, y-10, x+10, y+10, fill=color)
        self.player_pieces[player] = piece

    def update_player_piece_position(self,player):
        x,y = self.get_position_coordinates(player.position, list(self.player_pieces.keys()).index(player))
        self.board_canvas.coords(self.player_pieces[player], x-10, y-10, x+10, y+10)

    def get_position_coordinates(self, position, player_index):
        cell_size = min(1000 / 10, 500 / 5)
        offset_x = (player_index % 2) * cell_size / 2        
        offset_y = (player_index // 2) * cell_size / 2 
        if position < 10:
            x = position * cell_size + offset_x + cell_size / 4
            y = cell_size / 4 + offset_y
        elif position < 13:
            x = 9 * cell_size + offset_x + cell_size / 4
            y = (position - 9) * cell_size + offset_y + cell_size / 4
        elif position < 23:
            x = (22 - position)* cell_size + offset_x + cell_size / 4
            y = cell_size * 4 + offset_y + cell_size / 4
        else:
            x = 0 + offset_x +cell_size / 4
            y = (26 - position) * cell_size + offset_y + cell_size / 4
        return x,y

    def next_turn(self):
        self.game.next_turn()
        self.update_player_list()

    def update_player_list(self):
        colors = ["red", "blue", "green", "orange"]
        for i, player in enumerate(self.game.players):
            if i < len(self.player_texts):
                print(i)
                text_widget = self.player_texts[i]
                text_widget.delete('1.0', tk.END)  # 清空文本框
                player_info = f"{player.name}\nPosition🚩: {player.position}\nMoney💰: ${player.money}\nCuisines🍽:\n"
                player_properties = '\n'.join(player.properties)
                player_info += player_properties

                text_widget.insert(tk.END, player_info)  # 插入新的玩家資訊
                
                # 设置玩家颜色
                color = colors[i % len(colors)]
                text_widget.tag_configure(f"player_color_{i}", foreground=color)
                text_widget.tag_add(f"player_color_{i}", '1.0', tk.END)

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
                
                self.update_property_color(player, property)
                
            else:
                messagebox.showerror("Error", "Not enough money to buy this property.")
                
    def update_property_color(self, player, property):
        food_image_paths = [
            "character/start.png",
            "character/bento.png",
            "character/mcdonal's.png",
            "character/korean_fried_chicken.png",
            "character/chance.png",
            "character/curry.png",
            "character/sushi.png",
            "character/beef_noodle.png",
            "character/korean_meal.png",
            "character/prison.png",
            "character/mom_love.png",
            "character/magic_card.png",
            "character/a5.png",
            "character/barbecue.png",
            "character/fish.png",
            "character/pasta.png",
            "character/eat_too_much.png",
            "character/chinese_dish.png",
            "character/advanced_steak.png",#威
            "character/too_many_delicy.png",
            "character/lobster.png",
            "character/steak.png",#威
            "character/chance.png",
            "character/hotpot.png",#hotpot
            "character/pizza.png",#pizza
            "character/hospital.png"
            
            # Add more food image paths as needed
        ]
        
        property_index = self.game.properties.index(property)
        property_index = self.cell_to_property_index2[property_index]

        '''
        property_index = self.get_key(self.cell_to_property_index,property_index)
        
        '''
        print(f"pro :{property_index }") 
    
        
        #cell_index = self.cell_to_property_index.get(property_index)
        if property_index is None:
            print(f"Warning: Cell index None not found in cell_colors.")
            return

        color = self.colors[self.game.players.index(player) % len(self.colors)]
        if property_index in self.cell_colors:
            self.board_canvas.itemconfig(self.cell_colors[property_index], fill=color)
            self.board_canvas.tag_bind(self.cell_colors[property_index], '<Button-1>', lambda event, name=property.name, cost=property.cost, image_path=food_image_paths[property_index]: self.show_cell_name_picture(name, cost, image_path))
        else:
            print(f"Warning: Cell index {property_index} not found in cell_colors.")

    def get_key(self,dict, value):
        return [k for k, v in dict.items() if v==value]
    
    
    def disable_buttons(self):
        self.next_turn_button.config(state=tk.DISABLED)
    
    def game_over(self):
        response = messagebox.askyesno("Game Over", "A player has gone bankrupt. Do you want to play another round?")
        if response:
            self.reset_game()
        else:
            self.root.quit()
            self.root.destroy() 
            #self.reset_game()  # 關閉遊戲視窗

    def reset_game(self):
        self.root.quit()
        self.root.destroy() 
        subprocess.call(["python", "choose.py"])




    def open_game_menu(self):
        game_menu_app = GameMenuApp()
        game_menu_app.run()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    Globals.load_from_file('globals_data.pkl')
    root = tk.Tk()
    app = MonopolyUI(root)
    root.mainloop()