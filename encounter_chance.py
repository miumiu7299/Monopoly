import tkinter as tk
from PIL import Image, ImageTk
import random

def button_clicked(card):
    print("你選擇了此張機會卡牌!") 
    
    # 卡牌閃爍
    flash_button(card, 0)

def flash_button(card, count):
    if count < 7:  
        if count % 2 == 0:
            card.config(image=img_normal) 
        else:
            card.config(image=img_blank) 
        count += 1
        card.after(150, flash_button, card, count)  
    else:
        new_image = random.choice(imgs_new)  # 隨機選擇一張卡牌
        card.config(image=new_image['image'])
        card.image = new_image['image']

        draw_card(new_image['path'])

def draw_card(image_path):
    # 根據抽取的卡牌設置相應的訊息
    message = image_to_message.get(image_path, "未知卡牌")
    
    # 顯示卡牌功能或訊息
    card_function_label.config(text=message)
    print(message) 
    
    # 在 3 秒後關閉窗口
    win.after(3000, win.destroy)  

# 主視窗
win = tk.Tk()
win.title("Flashing Button Example")

# 視窗大小
win.geometry("1050x550")
win.resizable(0, 0)

# 取得螢幕寬度和高度
screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()

# 計算視窗的 X 和 Y 座標，使其置中
x = int((screen_width - 1050) / 2)
y = int((screen_height - 630) / 2)

# 設定視窗的幾何位置
win.geometry(f"+{x}+{y}")

win.config(bg="white")

# 卡牌介面
card_function_label = tk.Label(win, text="", font=("Helvetica", 16), bg="white")
card_function_label.grid(row=10, columnspan=5)

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
    "chance/chance_10.png"
]

original_image = Image.open(image_path)
original_width, original_height = original_image.size

# 調整卡片大小
target_width = int(original_width * 0.9)
target_height = int(original_height * 0.9)
resized_image = original_image.resize((target_width, target_height))

# 轉換卡片格式
img_normal = ImageTk.PhotoImage(resized_image)
img_blank = ImageTk.PhotoImage(Image.new('RGBA', (target_width, target_height), (0, 0, 0, 0)))

# 轉換新的圖片
resized_images_new = [{'path': path, 'image': ImageTk.PhotoImage(Image.open(path).resize((target_width, target_height)))} for path in image_paths_new]
imgs_new = [img for img in resized_images_new]

# 創建圖片路徑到訊息的映射
image_to_message = {
    "chance/chance_1.png": "恭喜獲得 300 金幣!",
    "chance/chance_2.png": "恭喜獲得 500 金幣!!",
    "chance/chance_3.png": "恭喜要損失 300 金幣哈哈",
    "chance/chance_4.png": "恭喜獲得 100 金幣!!",
    "chance/chance_5.png": "恭喜要損失 200 金幣哈哈",
    "chance/chance_6.png": "恭喜獲得 700 金幣!!",
    "chance/chance_7.png": "恭喜要損失 300 金幣哈哈",
    "chance/chance_8.png": "甚麼都沒有",
    "chance/chance_9.png": "恭喜要損失 300 金幣哈哈",
    "chance/chance_10.png": "恭喜獲得 300 金幣!!"
}

# 創建 10 張卡牌
buttons = []
for i in range(10):  
    button = tk.Button(win, image=img_normal, bd=0, highlightthickness=0)
    row = i // 5  
    col = i % 5   
    button.grid(row=row, column=col, padx=20, pady=20)  
    button.config(command=lambda b=button: button_clicked(b))
    buttons.append(button)

# 將整體佈局置中
win.grid_columnconfigure((0,1,2,3,4), weight=1)
win.grid_rowconfigure(0, weight=1)

win.mainloop()