import random
import tkinter as tk

W, H = 800, 300
GROUND = 250

root = tk.Tk()
root.title("Динозаврик")
canvas = tk.Canvas(root, width=W, height=H, bg="white")
canvas.pack()

dino = canvas.create_rectangle(80, 200, 120, 250, fill="#329632")
cactus = canvas.create_rectangle(800, 210, 825, 250, fill="#c83232")
canvas.create_line(0, GROUND, W, GROUND, width=2)
score_txt = canvas.create_text(60, 25, text="Счёт: 0", font=("Arial", 16, "bold"))

vel_y = 0.0
jumping = False
game_over = False
speed = 7.0
score = 0
over_txt = None

def reset():
    global vel_y, jumping, game_over, speed, score, over_txt
    vel_y = 0.0
    jumping = False
    game_over = False
    speed = 7.0
    score = 0
    canvas.coords(dino, 80, 200, 120, 250)
    canvas.coords(cactus, 800, 210, 825, 250)
    canvas.itemconfigure(score_txt, text="Счёт: 0")
    if over_txt:
        canvas.delete(over_txt)
        over_txt = None

def on_space(event):
    global vel_y, jumping
    if game_over:
        reset()
    elif not jumping:
        vel_y = -15.0
        jumping = True

root.bind("<space>", on_space)

def loop():
    global vel_y, jumping, game_over, speed, score, over_txt
    if not game_over:
        canvas.move(dino, 0, vel_y)
        vel_y += 0.8
        x1, y1, x2, y2 = canvas.coords(dino)
        if y2 >= GROUND:
            canvas.coords(dino, x1, GROUND - 50, x2, GROUND)
            vel_y = 0.0
            jumping = False

        canvas.move(cactus, -speed, 0)
        cx1, cy1, cx2, cy2 = canvas.coords(cactus)
        if cx2 < 0:
            nx = W + random.randint(0, 250)
            canvas.coords(cactus, nx, 210, nx + 25, 250)
            score += 1
            speed += 0.2
            canvas.itemconfigure(score_txt, text=f"Счёт: {score}")

        dx1, dy1, dx2, dy2 = canvas.coords(dino)
        cx1, cy1, cx2, cy2 = canvas.coords(cactus)
        if dx1 < cx2 and dx2 > cx1 and dy1 < cy2 and dy2 > cy1:
            game_over = True
            over_txt = canvas.create_text(
                W // 2, 120, text="ИГРА ОКОНЧЕНА! Пробел — заново",
                fill="#c80000", font=("Arial", 18, "bold")
            )

    root.after(16, loop)

loop()
root.mainloop()