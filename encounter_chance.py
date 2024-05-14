import tkinter as tk
from PIL import Image, ImageTk

def button_clicked(btn):
    print(f"選擇卡牌!")  # 在按鈕被點擊時顯示訊息
    
    # 按鈕閃爍效果
    flash_button(btn, 0)

def flash_button(btn, count):
    if count < 7:  
        if count % 2 == 0:
            btn.config(image=img_normal) 
        else:
            btn.config(image=img_blank) 
        count += 1
        btn.after(150, flash_button, btn, count)  
    else:
        btn.config(image=img_new)

# 主視窗
win = tk.Tk()
win.title("Flashing Button Example")

# 視窗大小
win.geometry("1050x550")
win.resizable(0, 0)

image_path = "CHANCE_COVER.png"
image_path_new = "chance_1.png"

original_image = Image.open(image_path)
original_image_new = Image.open(image_path_new)

original_width, original_height = original_image.size

target_width = int(original_width * 0.65)
target_height = int(original_height * 0.65)
resized_image = original_image.resize((target_width, target_height))
resized_image_new = original_image_new.resize((target_width, target_height))

img_normal = ImageTk.PhotoImage(resized_image)
img_blank = ImageTk.PhotoImage(Image.new('RGBA', (target_width, target_height), (0, 0, 0, 0)))  # 空白圖片
img_new = ImageTk.PhotoImage(resized_image_new)

buttons = []
for i in range(10):  # 創建 10 張卡牌
    button = tk.Button(win, image=img_normal, bd=0, highlightthickness=0)
    row = i // 5  
    col = i % 5   
    button.grid(row=row, column=col, padx=20, pady=20)  
    button.config(command=lambda b=button: button_clicked(b))  
    buttons.append(button)

win.mainloop()
