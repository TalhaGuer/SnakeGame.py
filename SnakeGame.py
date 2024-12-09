import pygame
import random
import customtkinter as ctk
import json
from datetime import datetime


pygame.init()

WIDTH, HEIGHT = 800, 600
snake_block = 20
FPS = 10


BUFFS = {
    "Hız artışı sağlar": {"color": (255, 0, 0), "effect": ""},
    "Hızı yavaşlatır": {"color": (0, 0, 255), "effect": ""},
    "Ekstra puan verir": {"color": (0, 255, 0), "effect": ""},
}


snake_list = []
snake_length = 1
direction = "RIGHT"
score = 0


def rgb_to_hex(rgb):
   
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def save_score(score):
    
    try:
        with open("scores.json", "r") as f:
            scores = json.load(f)
    except FileNotFoundError:
        scores = []

    scores.append({
        "score": score,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "attempt": len(scores) + 1
    })

    with open("scores.json", "w") as f:
        json.dump(scores, f, indent=4)


def run_game():
 
    global snake_list, snake_length, direction, score

   
    snake_list = [[WIDTH // 2, HEIGHT // 2]]
    snake_length = 1
    direction = "RIGHT"
    score = 0

    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Yılan Oyunu")

    food_pos = [random.randrange(1, WIDTH // snake_block) * snake_block,
                random.randrange(1, HEIGHT // snake_block) * snake_block]
    food_color = random.choice(list(BUFFS.values()))["color"]

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_score(score)  
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

        
        head_x, head_y = snake_list[-1]
        if direction == "UP":
            head_y -= snake_block
        elif direction == "DOWN":
            head_y += snake_block
        elif direction == "LEFT":
            head_x -= snake_block
        elif direction == "RIGHT":
            head_x += snake_block

       
        head_x %= WIDTH
        head_y %= HEIGHT

      
        snake_list.append([head_x, head_y])

     
        if [head_x, head_y] == food_pos:
            food_pos = [random.randrange(1, WIDTH // snake_block) * snake_block,
                        random.randrange(1, HEIGHT // snake_block) * snake_block]
            food_color = random.choice(list(BUFFS.values()))["color"]
            snake_length += 1
            score += 10
        else:
            while len(snake_list) > snake_length:
                snake_list.pop(0)

       
        if [head_x, head_y] in snake_list[:-1]:
            save_score(score) 
            running = False
            show_game_over_screen(score)  

       
        screen.fill((0, 0, 0))

        for segment in snake_list:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(segment[0], segment[1], snake_block, snake_block))
        pygame.draw.rect(screen, food_color, pygame.Rect(food_pos[0], food_pos[1], snake_block, snake_block))

        
        font = pygame.font.Font(None, 24)
        score_text = font.render(f"Skor: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


def show_game_over_screen(score):
  
    app = ctk.CTk()
    app.title("Oyun Bitti")
    app.geometry("400x200")

    label = ctk.CTkLabel(app, text=f"Oyun Bitti! Skorunuz: {score}", font=("Arial", 20, "bold"))
    label.pack(pady=20)

    restart_button = ctk.CTkButton(app, text="Yeniden Başla", command=lambda: [app.destroy(), start_game()])
    restart_button.pack(pady=10)

    app.mainloop()


def start_game():
    
    run_game()


def main_menu():
    
    app = ctk.CTk()
    app.title("Yılan Oyunu")
    app.geometry("400x400")

    label = ctk.CTkLabel(app, text="Yılan Oyunu", font=("Arial", 24, "bold"))
    label.pack(pady=20)

    for buff, details in BUFFS.items():
        frame = ctk.CTkFrame(app)
        frame.pack(pady=10, padx=10, fill="x")

        color_label = ctk.CTkLabel(frame, width=20, height=20, fg_color=rgb_to_hex(details["color"]), corner_radius=5)
        color_label.pack(side="left", padx=5)

        text_label = ctk.CTkLabel(frame, text=f"{buff}: {details['effect']}", font=("Arial", 14))
        text_label.pack(side="left", padx=10)

    start_button = ctk.CTkButton(app, text="Oyunu Başlat", command=lambda: [app.destroy(), start_game()])
    start_button.pack(pady=20)

    app.mainloop()


if __name__ == "__main__":
    main_menu()
