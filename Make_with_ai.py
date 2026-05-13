import pygame, sys, math, random

pygame.init()

# ── Window & Settings ────────────────────────────────────────
W, H = 1000, 650
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Number Quest")
clock = pygame.time.Clock()

# ── Colors (Cool Neon Palette) ──────────────────────────────
BLACK    = (10, 10, 15)
N_BLUE   = (0, 255, 255)   # Cyan Neon
N_PINK   = (255, 0, 255)   # Pink Neon
N_PURPLE = (150, 0, 255)  # Purple Glow
WHITE    = (240, 240, 255)
GOLD     = (255, 215, 0)

# ── Font System ──────────────────────────────────────────────
def get_f(size, bold=True):
    return pygame.font.SysFont("Segoe UI", size, bold=bold)

f_title = get_f(85)
f_main  = get_f(38)
f_input = get_f(50)
f_small = get_f(24)

# ── Visual Effects ───────────────────────────────────────────
class Star:
    def __init__(self):
        self.reset()
    def reset(self):
        self.x = random.randint(0, W)
        self.y = random.randint(0, H)
        self.size = random.uniform(1, 3)
        self.speed = random.uniform(0.5, 1.5)
    def update(self):
        self.y += self.speed
        if self.y > H: self.reset(); self.y = 0
    def draw(self, surf):
        pygame.draw.circle(surf, (200, 200, 255), (int(self.x), int(self.y)), int(self.size))

def draw_neon_rect(surf, rect, color, width=3, glow=True):
    if glow:
        for i in range(1, 10):
            alpha = 100 // i
            s = pygame.Surface((rect[2] + i*2, rect[3] + i*2), pygame.SRCALPHA)
            pygame.draw.rect(s, (*color, alpha), (0, 0, rect[2]+i*2, rect[3]+i*2), border_radius=18, width=width)
            surf.blit(s, (rect[0]-i, rect[1]-i))
    pygame.draw.rect(surf, color, rect, border_radius=18, width=width)

def draw_text(surf, text, font, col, x, y, shadow=True):
    if shadow:
        s = font.render(str(text), True, (0, 0, 0))
        surf.blit(s, s.get_rect(center=(x+3, y+3)))
    t = font.render(str(text), True, col)
    surf.blit(t, t.get_rect(center=(x, y)))

# ── Main Game Logic ──────────────────────────────────────────
class NeonGame:
    def __init__(self):
        self.stars = [Star() for _ in range(80)]
        self.reset_full()

    def reset_full(self):
        
        self.scene = "name_input"
        self.names = {1: "", 2: ""}
        self.current_typing = 1
        self.secrets = {1: random.randint(1, 100), 2: random.randint(1, 100)}
        self.guesses = {1: 0, 2: 0}
        self.active_p = 1
        self.input_val = ""
        self.feedback = "Guess 1-100"
        self.fb_col = WHITE

    def update(self):
        for s in self.stars: s.update()

    def draw(self, surf):
        surf.fill(BLACK)
        for s in self.stars: s.draw(surf)
        
        # Bottom Pulsing Wave
        t = pygame.time.get_ticks() * 0.003
        pts = [(0, H)]
        for x in range(0, W + 40, 40):
            y = H - 40 + math.sin(x * 0.008 + t) * 20
            pts.append((x, y))
        pts.append((W, H))
        pygame.draw.polygon(surf, (15, 5, 30), pts)
        pygame.draw.lines(surf, N_PURPLE, False, pts[1:-1], 4)

        if self.scene == "name_input": self.draw_name_input(surf)
        elif self.scene == "game": self.draw_gameplay(surf)
        elif self.scene == "result": self.draw_result(surf)

    def draw_name_input(self, surf):
        draw_text(surf, "WHO IS PLAYING?", f_title, GOLD, W//2, H//5)
        
        for p in [1, 2]:
            y_pos = H//2 - 40 if p == 1 else H//2 + 90
            is_active = (self.current_typing == p)
            col = N_BLUE if p == 1 else N_PINK
            
            # Box highlighting
            box_col = col if is_active else (60, 60, 70)
            draw_neon_rect(surf, (W//2 - 220, y_pos, 440, 70), box_col, glow=is_active)
            
            txt = f"P{p} Name: {self.names[p]}"
            if is_active and (pygame.time.get_ticks() // 500) % 2:
                txt += "_"
            draw_text(surf, txt, f_main, WHITE, W//2, y_pos + 35)
        
        draw_text(surf, "Press ENTER to lock name", f_small, (180, 180, 180), W//2, H - 80)

    def draw_gameplay(self, surf):
        p = self.active_p
        theme = N_BLUE if p == 1 else N_PINK
        
        # Float effect
        bob = math.sin(pygame.time.get_ticks() * 0.005) * 12
        
        # Display Player Name Header
        draw_text(surf, f"{self.names[p]}'s TURN", f_main, theme, W//2, H//2 - 240)
        
        # Gameplay Card
        rect = (W//2 - 220, H//2 - 170 + bob, 440, 380)
        draw_neon_rect(surf, rect, theme, glow=True)
        
        draw_text(surf, self.feedback, f_small, self.fb_col, W//2, H//2 - 130 + bob)
        
        # Input Box inside card
        draw_neon_rect(surf, (W//2 - 90, H//2 - 20 + bob, 180, 90), WHITE, width=2)
        draw_text(surf, self.input_val, f_input, WHITE, W//2, H//2 + 25 + bob)
        
        draw_text(surf, f"Guesses: {self.guesses[p]}", f_small, (200, 200, 200), W//2, H//2 + 150 + bob)

    def draw_result(self, surf):
        draw_text(surf, "GAMEOVER", f_title, GOLD, W//2, H//4)
        p1, p2 = self.guesses[1], self.guesses[2]
        
        if p1 < p2: winner_txt = f"🏆 {self.names[1]} WINS!"
        elif p2 < p1: winner_txt = f"🏆 {self.names[2]} WINS!"
        else: winner_txt = "🤝 IT'S A TIE!"
        
        draw_text(surf, winner_txt, f_main, N_BLUE, W//2, H//2)
        draw_text(surf, f"Final Scores -> {self.names[1]}: {p1} | {self.names[2]}: {p2}", f_small, WHITE, W//2, H//2 + 70)
        draw_text(surf, "Press 'R' to start fresh with names", f_small, N_PINK, W//2, H - 120)

    def handle_keys(self, key, uni):
        if self.scene == "name_input":
            if key == pygame.K_RETURN:
                if self.current_typing == 1: self.current_typing = 2
                else:
                    for i in [1,2]: 
                        if not self.names[i].strip(): self.names[i] = f"Player {i}"
                    self.scene = "game"
            elif key == pygame.K_BACKSPACE:
                self.names[self.current_typing] = self.names[self.current_typing][:-1]
            elif len(self.names[self.current_typing]) < 12 and uni.isprintable():
                self.names[self.current_typing] += uni

        elif self.scene == "game":
            if key == pygame.K_RETURN and self.input_val:
                val = int(self.input_val)
                self.guesses[self.active_p] += 1
                target = self.secrets[self.active_p]
                
                if val < target: self.feedback = "AIM HIGHER! ⬆️"; self.fb_col = N_BLUE
                elif val > target: self.feedback = "AIM LOWER! ⬇️"; self.fb_col = N_PINK
                else:
                    if self.active_p == 1:
                        self.active_p = 2
                        self.feedback = "BULLSEYE! Player 2, your turn."
                        self.fb_col = GOLD
                    else:
                        self.scene = "result"
                self.input_val = ""
            elif key == pygame.K_BACKSPACE:
                self.input_val = self.input_val[:-1]
            elif uni.isdigit() and len(self.input_val) < 3:
                self.input_val += uni

# ── Main Loop ────────────────────────────────────────────────
def main():
    game = NeonGame()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                # 'R' চাপলে এখন reset_full() কল হবে যা নাম সেট করার স্ক্রিনে নিয়ে যাবে
                if event.key == pygame.K_r and game.scene == "result":
                    game.reset_full()
                else:
                    game.handle_keys(event.key, event.unicode)

        game.update()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()