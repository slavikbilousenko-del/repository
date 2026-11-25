import random
import tkinter as tk

W, H = 800, 300
GROUND = 250
BASE_SPEED = 7.0
MAX_SPEED = 18.0
TIME_ACCEL = 0.004  # Прирост скорости за каждый кадр (~0.25 в секунду)

root = tk.Tk()
root.title("Динозаврик")
canvas = tk.Canvas(root, width=W, height=H, bg="white")
canvas.pack()

dino = canvas.create_rectangle(80, 200, 120, 250, fill="#329632")
cactus = canvas.create_rectangle(800, 210, 825, 250, fill="#c83232")
bird = canvas.create_rectangle(-100, 175, -60, 195, fill="#3264c8")

canvas.create_line(0, GROUND, W, GROUND, width=2)
score_txt = canvas.create_text(60, 25, text="Счёт: 0", font=("Arial", 16, "bold"))
speed_txt = canvas.create_text(W - 85, 25, text="Скорость: 1.0x", font=("Arial", 13, "bold"))

vel_y = 0.0
jumping = False
ducking = False
game_over = False
speed = BASE_SPEED
score = 0
over_txt = None
active_obstacle = "cactus"

def update_speed_label():
    mult = speed / BASE_SPEED
    canvas.itemconfigure(speed_txt, text=f"Скорость: {mult:.1f}x")

def spawn_next():
    global active_obstacle
    if score >= 3 and random.choice([True, False]):
        active_obstacle = "bird"
        bird_y = random.choice([175, 215])
        canvas.coords(bird, W + 20, bird_y, W + 60, bird_y + 20)
        canvas.coords(cactus, -100, 210, -75, 250)
    else:
        active_obstacle = "cactus"
        canvas.coords(cactus, W + 20, 210, W + 45, 250)
        canvas.coords(bird, -100, 175, -60, 195)

def reset():
    global vel_y, jumping, ducking, game_over, speed, score, over_txt
    vel_y = 0.0
    jumping = False
    ducking = False
    game_over = False
    speed = BASE_SPEED
    score = 0
    canvas.coords(dino, 80, 200, 120, 250)
    canvas.itemconfigure(score_txt, text="Счёт: 0")
    update_speed_label()
    if over_txt:
        canvas.delete(over_txt)
        over_txt = None
    spawn_next()

def on_space(event):
    global vel_y, jumping, ducking
    if game_over:
        reset()
    elif not jumping:
        ducking = False
        vel_y = -15.0
        jumping = True

def on_down_press(event):
    global ducking
    if not jumping and not game_over:
        ducking = True
        canvas.coords(dino, 80, 225, 130, 250)

def on_down_release(event):
    global ducking
    if ducking and not game_over:
        ducking = False
        canvas.coords(dino, 80, 200, 120, 250)

root.bind("<space>", on_space)
root.bind("<Down>", on_down_press)
root.bind("<KeyRelease-Down>", on_down_release)

def loop():
    global vel_y, jumping, game_over, speed, score, over_txt
    if not game_over:
        # Плавное ускорение со временем до лимита MAX_SPEED
        if speed < MAX_SPEED:
            speed = min(MAX_SPEED, speed + TIME_ACCEL)
            update_speed_label()

        if jumping:
            canvas.move(dino, 0, vel_y)
            vel_y += 0.8
            x1, y1, x2, y2 = canvas.coords(dino)
            if y2 >= GROUND:
                canvas.coords(dino, 80, 200, 120, GROUND)
                vel_y = 0.0
                jumping = False

        obs = cactus if active_obstacle == "cactus" else bird
        canvas.move(obs, -speed, 0)
        ox1, oy1, ox2, oy2 = canvas.coords(obs)

        if ox2 < 0:
            score += 1
            speed = min(MAX_SPEED, speed + 0.15)
            canvas.itemconfigure(score_txt, text=f"Счёт: {score}")
            update_speed_label()
            spawn_next()

        dx1, dy1, dx2, dy2 = canvas.coords(dino)
        if dx1 < ox2 and dx2 > ox1 and dy1 < oy2 and dy2 > oy1:
            game_over = True
            over_txt = canvas.create_text(
                W // 2, 120, text="ИГРА ОКОНЧЕНА! Пробел — заново",
                fill="#c80000", font=("Arial", 18, "bold")
            )

    root.after(16, loop)

loop()
root.mainloop()
