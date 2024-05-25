import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk
import os
from tkinter import PhotoImage

#file_path = os.path.join("Users", "yejiayu", "Desktop", "python", "map.png")
#self.image = Image.open(file_path)


class Player:
    def __init__(self, name, position=0, money=4000):
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
        self.board_size = 26 #共30格
        self.properties = self.create_properties()
        self.ui = ui

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
                properties.append(Property(f"新竹人的❤️ 麥當勞 {i}", 150))
            elif i in [1]: 
                properties.append(Property(f"便當 {i}", 80))
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
                player.position=13
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
        self.image_labels = {}
        self.cell_colors = {}  # Dictionary to store the color of each cell
        self.colors = ["red", "blue", "green", "orange"]  # Colors for players
        # 假定棋盤格子名稱
        self.cell_names = [
            "Start", "便當", "新竹人的❤️麥當勞","韓式炸雞", "Chance or Destiny","咖哩飯","壽司","牛肉麵","石鍋拌飯","jail",
            "媽媽的愛","","","","","","","","","Magic Card",
            "A5和牛","","","","", "","","","","燒烤",
            "魚子醬","","", "","","","","","","義大利麵",
            "Fat->killed", "鮑魚烏參佛跳牆","Beef Wellington","too much delicacy","lobster","steak","Chance or Destiny","hotpot","pizza", "Hospital"
        ]
        
        self.list_names = [
            "Start", "便當", "新竹人的❤️\n麥當勞","韓式炸雞", "Chance or\nDestiny","咖哩飯","壽司","牛肉麵","石鍋拌飯","jail",
            "媽媽的愛","","","","","","","","","Magic Card",
            "A5和牛","","","","", "","","","","燒烤",
            "魚子醬","","", "","","","","","","義大利麵",
            "Fat->killed", "鮑魚烏參佛跳牆","Beef Wellington","too much\ndelicacy","lobster","steak","Chance or\nDestiny","hotpot","pizza", "Hospital"
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

        # 主框架設置
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 在主框架中添加畫布來畫棋盤
        self.board_canvas = tk.Canvas(self.main_frame, width=1000, height=500, bg='white')
        # 使用place方法將畫布置中
        self.board_canvas.place(relx=0.5, rely=0.5, anchor='center')
        self.draw_board()

        # 創建四個玩家信息顯示 Text 組件，放置在界面的四個角落
        self.player_texts = []
        self.player_images = []  # 初始化 player_images 列表
        positions = [(0.01, 0.5), (0.99, 0.5), (0.01, 0.5), (0.99, 0.5)]

        anchors = [ 'sw', 'se','nw', 'ne']
        
        for i, (pos, anchor) in enumerate(zip(positions, anchors)):
            """
            frame = tk.Frame(self.main_frame, width=200, height=100)
            frame.place(relx=pos[0], rely=pos[1], anchor=anchor)
            text_widget = tk.Text(frame, height=15, width=25, font=('Arial', 12))
            text_widget.pack(fill=tk.BOTH, expand=True)
            self.player_texts.append(text_widget)
            """
            frame = tk.Frame(self.main_frame, width=200, height=400)
            frame.place(relx=pos[0], rely=pos[1], anchor=anchor)
            player_image_path = "character/馬力歐.png"
            image = Image.open(player_image_path)
            #image = Image.open(f"player_{i+1}.png")  # 假定圖片命名為 player_1.png, player_2.png 等
            image = image.resize((100, 130), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            label = tk.Label(frame, image=photo)
            label.image = photo  # 保存對象引用，防止被垃圾回收
            label.pack(side=tk.TOP)
            self.player_images.append(label)
            text_widget = tk.Text(frame, height=15, width=25, font=('Arial', 12))
            text_widget.pack(fill=tk.BOTH, expand=True)
            self.player_texts.append(text_widget)
            

        # 控制元件，包括按鈕在內的 Frame
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.place(relx=0.7, rely=0.4, anchor='center')

        self.player_name_var = tk.StringVar()
        self.player_name_entry = tk.Entry(self.main_frame, textvariable=self.player_name_var)
        self.player_name_entry.place(relx=0.5, rely=0.4, anchor='center')

        self.add_player_button = tk.Button(self.button_frame, text="添加玩家", command=self.add_player)
        self.add_player_button.pack(side=tk.TOP, pady=5)

        self.next_turn_button = tk.Button(self.button_frame, text="丟骰子", command=self.next_turn)
        self.next_turn_button.pack(side=tk.TOP, pady=5)

        self.status_label = tk.Label(self.main_frame, text="遊戲狀態")
        self.status_label.place(relx=0.5, rely=0.35, anchor='center')

        # 提升消息框的高度
        self.message_listbox = tk.Listbox(self.main_frame, height=10,width=50)
        # 在這裡添加 padx 和 pady 以增加邊距
        self.message_listbox.place(relx=0.5, rely=0.55, anchor='center')
        
        
        

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
        
        # 自定義映射字典，將格子的實際編號映射到屬性索引
        self.cell_to_property_index = {
            0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 
            10: 10, 19: 11, 20: 12, 29: 13, 30: 14, 39: 15, 40: 16, 41: 17, 42: 18, 43: 19, 
            44: 20, 45: 21, 46: 22, 47: 23, 48: 24, 49: 25
        }

        
        food_image_pic=0
        rows, cols = 5, 10
        # 确保格子为正方形
        cell_size = min(1000 / cols, 500 / rows)
        cell_indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 19, 20, 29, 30, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49]
        cell_index = 0
        for row in range(rows):
            for col in range(cols):
                if (row == 0 or row == rows - 1) or (col == 0 or col == cols - 1):

                    x1 = col * cell_size
                    y1 = row * cell_size
                    x2 = x1 + cell_size
                    y2 = y1 + cell_size
                    
                    # 计算格子的索引，假设每个格子都有一个名字存储在 self.cell_names 列表中
                    cell_index = row * cols + col
                    cell_name = self.cell_names[cell_index % len(self.cell_names)]  # 循环使用名字列表
                    list_index = row * cols + col
                    list_name=self.list_names[list_index % len(self.list_names)]  # 循环使用名字列表
                    cost_index = row * cols + col
                    cost_name=self.cost_list[cost_index % len(self.cost_list)]  # 循环使用名字列表
                    outline_color = 'black' if (row == 0 or row == rows - 1 or col == 0 or col == cols - 1) else ''
                    
                    rect = self.board_canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline=outline_color)
                    # Store the rectangle ID
                    #for index in cell_indices:
                    """
                    for key, value in self.cell_to_property_index.items():
                        self.cell_colors[value] = rect
                    """
                    """
                    for index in cell_indices:
                        self.cell_colors[index] = rect
                    """
                    self.cell_colors[cell_index] = rect
                    self.board_canvas.tag_bind(rect, '<Button-1>', self.make_callback(cell_name, cost_name, food_image_paths[food_image_pic]))
                    self.board_canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=list_name, fill="black", font=("Arial", 12, "bold"))
                    food_image_pic += 1
                #index+=1
                #key+=1
                cell_index += 1
                    
                """
                    rect = self.board_canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline=outline_color)
                    #self.cell_colors[0,1,2,3,4,5,6,7,8,9,10,19,20,29,30,39,40,41,42,43,44,45,46,47,49] = rect  # Store the rectangle ID
                    self.cell_colors[cell_index] = rect 
                    self.board_canvas.tag_bind(rect, '<Button-1>', self.make_callback(cell_name, cost_name, food_image_paths[food_image_pic]))
                    self.board_canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=list_name, fill="black", font=("Arial", 12, "bold"))
                    food_image_pic += 1 
                cell_index+=1
                """
                """
                    # 畫出格子背景
                    self.board_canvas.create_rectangle(x1, y1, x2, y2, outline=outline_color)
                    
                    # 在格子內放入文字
                    #self.board_canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=cell_name, fill="black")
                    
                    # 加载并显示图片
                    image_path = food_image_paths[food_image_pic]  # 替换为你的图片路径
                    rect = self.board_canvas.create_rectangle(x1, y1, x2, y2,fill='white' ,outline=outline_color)
                    self.board_canvas.tag_bind(rect, '<Button-1>', self.make_callback(cell_name, cost_name,image_path))
                    #self.board_canvas.tag_bind(rect, '<Button-1>', self.make_callback(cell_name, food_image_paths[food_image_pic % len(food_image_paths)]))
                    
                    # 在格子內放入文字
                    self.board_canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=list_name, fill="black", font=("Arial", 12,"bold"))
                    food_image_pic+=1 
                    """
                    
                    
    def make_callback(self, name, cost,image_path):
        return lambda event: self.show_cell_name_picture(name, cost,image_path)
                    
    def show_cell_name_picture(self, name,cost ,image_path):
        top = tk.Toplevel(self.root)
        top.title(f"您點擊了：{name}")
        
        img = Image.open(image_path)
        img = img.resize((250, 250))  # Resize if needed
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(top, image=photo,width=300,height=300)
        label.image = photo
    
        label.pack()
        tk.Label(top, text=f"地點: {name}\n價格: {cost}").pack()
        
        #tk.Label(top, text=f"物業信息: {name}").pack()
        #messagebox.showinfo("物業信息", f"您點擊了：{name}")

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
        colors = ["red", "blue", "green", "orange"]
        for i, player in enumerate(self.game.players):
            if i < len(self.player_texts):
                text_widget = self.player_texts[i]
                text_widget.delete('1.0', tk.END)  # 清空文本框
                player_info = f"{player.name}\nPosition🚩: {player.position}\nMoney💰: ${player.money}\nCuisines🍽️: {', '.join(player.properties)}"
                
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
        index = self.game.properties.index(property)
        color = self.colors[self.game.players.index(player) % len(self.colors)]

        if index in self.cell_colors:
            self.board_canvas.itemconfig(self.cell_colors[index], fill=color)
        else:
            print(f"Warning: Property index {index} not found in cell_colors.")
        #self.board_canvas.itemconfig(self.cell_colors[index], fill=color)

    
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
        #self.disable_buttons()  # 重新啟用按鈕等可能在遊戲中變更的UI元件

if __name__ == "__main__":
    root = tk.Tk()
    app = MonopolyUI(root)
    root.mainloop()