import pygame
import time
import random
from sys import exit

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1200, 800
P_WIDTH, P_HEIGHT, P_VEL = 40, 60, 10
BLOCK_WIDTH, BLOCK_HEIGHT, BLOCK_VEL = 50, 50, 2
FONT = pygame.font.SysFont("comicsans", 30)
OPERATIONS_LIST = ["+", "-"]

class EquationRaceGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("The Equation Race")
        self.home_screen = pygame.transform.scale(pygame.image.load("assets/landscape.jpg"), (WIDTH, HEIGHT))
        self.start_screen_image = pygame.transform.scale(pygame.image.load("assets/math_wallpaper.jpg"), (WIDTH, HEIGHT))
        self.difficulty = None
        pygame.mixer.init()

    def start_screen(self):
        pygame.mixer.music.load("assets/home_screen_music.wav")
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)
        self.screen.blit(self.start_screen_image, (0, 0))
        title_font = pygame.font.SysFont("comicsans", 60)
        title_text = title_font.render("The Equation Race!", 1, "white")
        tutorial_text = FONT.render("Don't hit the blocks with the wrong answer!", 1, "red")
        difficulty_text = FONT.render("Choose your difficulty:", 1, "white")
        self.screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//4 - 100))
        self.screen.blit(difficulty_text, (WIDTH//2 - difficulty_text.get_width()//2, HEIGHT//4 + 70))
        self.screen.blit(tutorial_text, (WIDTH//2 - tutorial_text.get_width()//2, HEIGHT//4))
        button_width, button_height = 200, 50
        
        pygame.display.update()
        
        easy_rect = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//2 - 70, button_width, button_height)
        medium_rect = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//2, button_width, button_height)
        hard_rect = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//2 + 70, button_width, button_height)
        
        pygame.draw.rect(self.screen, "white", easy_rect)
        pygame.draw.rect(self.screen, "white", medium_rect)
        pygame.draw.rect(self.screen, "white", hard_rect)
        easy_text = FONT.render("Easy", 1, "black")
        medium_text = FONT.render("Medium", 1, "black")
        hard_text = FONT.render("Hard", 1, "black")
        
        self.screen.blit(easy_text, (easy_rect.x + easy_rect.width//2 - easy_text.get_width()//2,
                                     easy_rect.y + easy_rect.height//2 - easy_text.get_height()//2))
        self.screen.blit(medium_text, (medium_rect.x + medium_rect.width//2 - medium_text.get_width()//2,
                                       medium_rect.y + medium_rect.height//2 - medium_text.get_height()//2))
        self.screen.blit(hard_text, (hard_rect.x + hard_rect.width//2 - hard_text.get_width()//2,
                                     hard_rect.y + hard_rect.height//2 - hard_text.get_height()//2))
        
        quit_rect = pygame.Rect(WIDTH - button_width - 20, 0 + 20, button_width, button_height)
        pygame.draw.rect(self.screen, "white", quit_rect)
        quit_text = FONT.render("Quit", 1, "black")
        self.screen.blit(quit_text, (quit_rect.x + quit_rect.width//2 - quit_text.get_width()//2,
                                     quit_rect.y + quit_rect.height//2 - quit_text.get_height()//2))
        pygame.display.update()
        waiting = True
        chosen_difficulty = None
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if easy_rect.collidepoint(pos):
                        chosen_difficulty = "Easy"
                        waiting = False
                    elif medium_rect.collidepoint(pos):
                        chosen_difficulty = "Medium"
                        waiting = False
                    elif hard_rect.collidepoint(pos):
                        chosen_difficulty = "Hard"
                        waiting = False
                    elif quit_rect.collidepoint(pos):
                        pygame.quit()
                        exit()
        pygame.time.delay(200)
        pygame.mixer.music.stop()  
        self.difficulty = chosen_difficulty
        return chosen_difficulty

    def draw_game_screen(self, player, elapsed_time, blocks, blocks_text, heart_list, equation, score):
        self.screen.blit(self.home_screen, (0, 0))
        time_text = FONT.render(f"Time: {round(max(0, 60 - elapsed_time))}s", 1, "white")
        live_text = FONT.render("Lives:", 1, "white")
        bar = pygame.Rect(0,0, WIDTH, 60)
        pygame.draw.rect(self.screen, "black", bar)
        self.screen.blit(live_text, (900, 10))
        self.screen.blit(time_text, (10, 10))
        pygame.draw.rect(self.screen, "red", player)
        
        for i, block in enumerate(blocks):
            pygame.draw.rect(self.screen, "white", block)
            text_surface = FONT.render(blocks_text[i], 1, "black")
            text_x = block.x + (BLOCK_WIDTH // 2 - text_surface.get_width() // 2)
            text_y = block.y + (BLOCK_HEIGHT // 2 - text_surface.get_height() // 2)
            self.screen.blit(text_surface, (text_x, text_y))
        
        for i, heart in enumerate(heart_list):
            self.screen.blit(heart, (i*60 + 960, 10))
        font_equation = FONT.render(equation, 1, "white")
        self.screen.blit(font_equation, (WIDTH//2 - font_equation.get_width()//2, 10))
        self.draw_score(score)
        pygame.display.update()
    
    def draw_score(self, score):
        font_score = FONT.render(f"Score: {score}", 1, "white")
        self.screen.blit(font_score, (200, 10))
    
    def handle_player_movement(self, keys, player):
        if keys[pygame.K_LEFT] and player.x - P_VEL >= 0:
            player.x -= P_VEL
        if keys[pygame.K_RIGHT] and player.x + P_VEL + player.width <= WIDTH:
            player.x += P_VEL
        if keys[pygame.K_UP] and player.y - P_VEL >= 60:
            player.y -= P_VEL
        if keys[pygame.K_DOWN] and player.y + P_VEL + player.height <= HEIGHT:
            player.y += P_VEL

    def spawn_blocks(self, blocks, blocks_text, block_add_increment, total, equation_start):
        correct_block_index = None
        if 5 < time.time() - equation_start < 7:
            correct_block_index = random.randint(0, 2)
        for i in range(3):
            while True:
                block_x = random.randint(0, WIDTH - BLOCK_WIDTH)
                if all(abs(block_x - block.x) > BLOCK_WIDTH + 5 for block in blocks):
                    break
            block = pygame.Rect(block_x, -BLOCK_HEIGHT + 90, BLOCK_WIDTH, BLOCK_HEIGHT)
            block_text = str(total) if i == correct_block_index else str(random.randint(max(total - 10, 0), total + 10))
            blocks_text.append(block_text)
            blocks.append(block)
        return max(300, block_add_increment - 25)
    
    def update_blocks(self, blocks, blocks_text, player, total):
        hit = False
        correct = False
        block_remove = []
        for i in range(len(blocks)):
            blocks[i].y += BLOCK_VEL
            if blocks[i].y > HEIGHT:
                block_remove.append(i)
            elif blocks[i].colliderect(player):
                if int(blocks_text[i]) == total:
                    correct = True
                block_remove.append(i)
                hit = True
                break
        for idx in block_remove[::-1]:
            del blocks[idx]
            del blocks_text[idx]
        return hit, correct

    def display_game_over(self, score, elapsed_time):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 150))
        self.screen.blit(overlay, (0, 0))
        stat_text = FONT.render(f"You survived {int(elapsed_time)} seconds with a score of {score}", 1, "black")
        game_over_text = FONT.render("Press R to play again, E to exit", 1, "black")
        button_width, button_height = 150, 50
        home_button = pygame.Rect(WIDTH//2 - button_width - 10, (HEIGHT//2) + 170, button_width, button_height)
        pygame.draw.rect(self.screen, "blue", home_button)
        home_text = FONT.render("Home", 1, "white")
        self.screen.blit(home_text, (home_button.x + home_button.width//2 - home_text.get_width()//2,
                                     home_button.y + home_button.height//2 - home_text.get_height()//2))
        quit_button = pygame.Rect(WIDTH//2 + 10, (HEIGHT//2) + 170, button_width, button_height)
        pygame.draw.rect(self.screen, "grey", quit_button)
        quit_text = FONT.render("Quit", 1, "white")
        self.screen.blit(quit_text, (quit_button.x + quit_button.width//2 - quit_text.get_width()//2,
                                     quit_button.y + quit_button.height//2 - quit_text.get_height()//2))
        self.screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, (HEIGHT//2) + 100))
        self.screen.blit(stat_text, (WIDTH//2 - stat_text.get_width()//2, (HEIGHT//2) - 100))
        pygame.display.update()
        return home_button, quit_button

    def restart_quit(self, buttons):
        home_button, quit_button = buttons
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return self.difficulty
                    if event.key == pygame.K_e:
                        pygame.quit()
                        exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if home_button.collidepoint(pos):
                        self.difficulty = self.start_screen()
                        return self.difficulty
                    if quit_button.collidepoint(pos):
                        pygame.quit()
                        exit()

    def new_equation(self):
        if self.difficulty == "Easy":
            low, high = 0, 20
        elif self.difficulty == "Medium":
            low, high = 21, 50
        elif self.difficulty == "Hard":
            low, high = 51, 99
        rand_num1 = random.randint(low, high)
        rand_num2 = random.randint(low, high)
        operation = OPERATIONS_LIST[random.randint(0,1)]
        if operation == "+":
            equation = f"{rand_num1} + {rand_num2}"
            total = rand_num1 + rand_num2
        else:
            if rand_num1 < rand_num2:
                rand_num1, rand_num2 = rand_num2, rand_num1
            equation = f"{rand_num1} - {rand_num2}"
            total = rand_num1 - rand_num2
        return equation, total

    def run(self):
        while True:
            player = pygame.Rect(200, HEIGHT - P_HEIGHT, P_WIDTH, P_HEIGHT)
            clock = pygame.time.Clock()
            start_time = time.time()
            elapsed_time = 0
            block_add_increment = 2000
            block_count = 0
            blocks, blocks_text = [], []
            heart = pygame.image.load("assets/heart.png")
            heart_scaled = pygame.transform.scale(heart, (100, 50))
            heart_list = [heart_scaled for _ in range(3)]
            music = pygame.mixer.Sound("assets/game song.wav")
            music_channel = pygame.mixer.Channel(0)
            music_channel.play(music, loops=-1)
            music_channel.set_volume(0.25)
            equation, total = self.new_equation()
            equation_start = time.time()
            score = 0
            run = True
            while run:
                block_count += clock.tick(90)
                elapsed_time = time.time() - start_time
                if block_count > block_add_increment:
                    block_add_increment = self.spawn_blocks(blocks, blocks_text, block_add_increment, total, equation_start)
                    block_count = 0
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
                        exit()
                keys = pygame.key.get_pressed()
                self.handle_player_movement(keys, player)
                hit, correct = self.update_blocks(blocks, blocks_text, player, total)
                if hit and correct:
                    correct_sound = pygame.mixer.Sound("assets/hit_correct.mp3")
                    sfx_channel = pygame.mixer.Channel(2)
                    sfx_channel.play(correct_sound)
                    sfx_channel.set_volume(1.0)
                    score += total
                    equation, total = self.new_equation()
                    equation_start = time.time()
                    self.draw_score(score)
                    self.draw_game_screen(player, elapsed_time, blocks, blocks_text, heart_list, equation, score)
                    pygame.display.update() 
                    pygame.time.delay(200)
                elif hit and not correct:
                    if len(heart_list) > 1:
                        incorrect_sound = pygame.mixer.Sound("assets/incorrect.mp3")
                        inc_channel = pygame.mixer.Channel(1)
                        inc_channel.play(incorrect_sound)
                        inc_channel.set_volume(1.0)
                    heart_list.pop()
                    self.draw_game_screen(player, elapsed_time, blocks, blocks_text, heart_list, equation, score)
                    pygame.display.update() 
                    pygame.time.delay(200)
                if len(heart_list) == 0:
                    lost_sound = pygame.mixer.Sound("assets/lost_sound.mp3")
                    lost_channel = pygame.mixer.Channel(3)
                    lost_channel.play(lost_sound)
                    lost_channel.set_volume(1.0)
                    music_channel.stop()
                    buttons = self.display_game_over(score, elapsed_time)
                    self.difficulty = self.restart_quit(buttons)
                    run = False
                if elapsed_time >= 60:
                    finished_sound = pygame.mixer.Sound("assets/finished_sound.mp3")
                    finished_channel = pygame.mixer.Channel(4)
                    finished_channel.play(finished_sound)
                    finished_channel.set_volume(1.0)
                    music_channel.stop()
                    buttons = self.display_game_over(score, elapsed_time)
                    self.difficulty = self.restart_quit(buttons)
                    run = False
                self.draw_game_screen(player, elapsed_time, blocks, blocks_text, heart_list, equation, score)
            pygame.time.delay(500)