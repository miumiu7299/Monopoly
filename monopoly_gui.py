import tkinter as tk

def start_game():
    # 在這裡加入遊戲開始的程式碼
    print("遊戲開始！")

def select_character():
    # 在這裡加入選角色的程式碼
    print("選擇角色畫面")

# 建立主視窗
root = tk.Tk()
root.title("大富翁遊戲")

# 載入背景圖片
bg_image = tk.PhotoImage(file='4.png')

# 建立Canvas
canvas = tk.Canvas(root, highlightthickness=0, width=960, height=480)
canvas.pack()

# 在Canvas上顯示背景圖片
canvas.create_image(480, 240, image=bg_image)

# 建立遊戲開始按鈕
start_button = tk.Button(root, text="開始遊戲", command=select_character, bg="blue", fg="white", font=("Arial", 12, "bold"), bd=3, relief=tk.RAISED)
start_button.place(x=450, y=350)
print()
# 執行主迴圈
root.mainloop()
