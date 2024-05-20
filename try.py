import tkinter as tk
from tkinter import messagebox

class MapApp:
    def __init__(self, master):
        self.master = master
        self.master.title("地圖應用程式")
        
        # 創建Canvas元件
        self.canvas = tk.Canvas(self.master, width=400, height=400, bg="white")
        self.canvas.pack()
        
        # 地圖參數
        self.grid_size = 40  # 方格大小
        self.map_width = 10  # 地圖寬度
        self.map_height = 10  # 地圖高度
        
        # 繪製地圖
        self.draw_map()
        
        # 綁定點擊事件
        self.canvas.bind("<Button-1>", self.on_map_click)
        
    def draw_map(self):
        # 繪製方格
        for y in range(self.map_height):
            for x in range(self.map_width):
                if x == 0 or x == self.map_width - 1 or y == 0 or y == self.map_height - 1:
                    x0 = x * self.grid_size
                    y0 = y * self.grid_size
                    x1 = x0 + self.grid_size
                    y1 = y0 + self.grid_size
                    self.canvas.create_rectangle(x0, y0, x1, y1, outline="black")
        
    def on_map_click(self, event):
        # 獲取點擊位置的坐標
        x = event.x // self.grid_size
        y = event.y // self.grid_size
        
        # 判斷是否點擊了外圍的格子
        if x == 0 or x == self.map_width - 1 or y == 0 or y == self.map_height - 1:
            # 顯示是第幾格
            index = y * self.map_width + x + 1
            messagebox.showinfo("Info", "You clicked on grid: {}".format(index))
        

def main():
    root = tk.Tk()
    app = MapApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
