from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox


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
