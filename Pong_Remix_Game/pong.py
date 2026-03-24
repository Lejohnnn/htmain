"""
╔══════════════════════════════════════════════════╗
║         N E O N   P O N G   A R E N A           ║
║   2–4 Players | Power-Ups | Classic Arcade       ║
╚══════════════════════════════════════════════════╝

Controls:
  Player 1 (Left):   W / S
  Player 2 (Right):  UP / DOWN arrow
  Player 3 (Bottom): A / D   (3-4 player mode)
  Player 4 (Top):    LEFT / RIGHT arrow  (4 player mode)

Power-ups (GREEN):  bigger paddle | multi-ball | speed slow
Power-downs (RED):  smaller paddle | speed boost

First to 7 points wins!
"""

import pygame
import sys
import math
import random

# ── Constants ─────────────────────────────────────────────────────────────────

WIDTH, HEIGHT = 800, 800
FPS = 60
WINNING_SCORE = 7

PADDLE_THICKNESS = 14
PADDLE_LENGTH_DEFAULT = 110
PADDLE_SPEED = 6
BALL_SPEED_INIT = 5.5
BALL_RADIUS = 9

POWERUP_RADIUS = 14
POWERUP_SPAWN_INTERVAL = 420   # frames (~7 s)
POWERUP_LIFETIME = 360         # frames before it vanishes
POWERUP_DURATION = 360         # frames the effect lasts

# ── Neon colour palette ────────────────────────────────────────────────────────

BLACK   = (0,   0,   0)
WHITE   = (255, 255, 255)
CYAN    = (0,   240, 255)
MAGENTA = (255, 0,   200)
YELLOW  = (255, 220, 0)
GREEN   = (0,   255, 100)
RED     = (255, 40,  40)
ORANGE  = (255, 140, 0)
PURPLE  = (180, 0,   255)
GREY    = (50,  50,  60)

PLAYER_COLORS = [CYAN, MAGENTA, YELLOW, ORANGE]

# ── Helpers ───────────────────────────────────────────────────────────────────

def glow_rect(surf, color, rect, radius=6):
    """Draw a rectangle with a simple neon-glow effect."""
    glow_surf = pygame.Surface((rect.width + radius*4, rect.height + radius*4), pygame.SRCALPHA)
    for i in range(radius, 0, -1):
        alpha = int(80 * (i / radius))
        col = (*color, alpha)
        pygame.draw.rect(glow_surf, col,
                         (radius*2 - i, radius*2 - i,
                          rect.width + i*2, rect.height + i*2),
                         border_radius=4)
    surf.blit(glow_surf, (rect.x - radius*2, rect.y - radius*2))
    pygame.draw.rect(surf, color, rect, border_radius=4)

def glow_circle(surf, color, pos, r, radius=6):
    """Draw a circle with neon-glow effect."""
    glow_surf = pygame.Surface(((r + radius)*2 + 4, (r + radius)*2 + 4), pygame.SRCALPHA)
    cx = cy = r + radius + 2
    for i in range(radius, 0, -1):
        alpha = int(100 * (i / radius))
        col = (*color, alpha)
        pygame.draw.circle(glow_surf, col, (cx, cy), r + i)
    surf.blit(glow_surf, (pos[0] - cx, pos[1] - cy))
    pygame.draw.circle(surf, color, pos, r)

def glow_line(surf, color, p1, p2, width=2, radius=4):
    for i in range(radius, 0, -1):
        alpha = int(60 * (i / radius))
        col = (*color, alpha)
        s = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
        pygame.draw.line(s, col, p1, p2, width + i*2)
        surf.blit(s, (0, 0))
    pygame.draw.line(surf, color, p1, p2, width)

# ── Power-Up / Power-Down definitions ─────────────────────────────────────────

POWERUP_TYPES = [
    # (id,            label,           color,   is_good)
    ("bigger",       "+PADDLE",        GREEN,   True),
    ("smaller",      "-PADDLE",        RED,     False),
    ("multiball",    "MULTI-BALL",     PURPLE,  True),
    ("slow",         "SLOW BALL",      CYAN,    True),
    ("fast",         "FAST BALL",      RED,     False),
]

# ── Ball ──────────────────────────────────────────────────────────────────────

class Ball:
    def __init__(self, x, y, speed=BALL_SPEED_INIT):
        self.x = float(x)
        self.y = float(y)
        angle = random.uniform(-math.pi/4, math.pi/4)
        if random.random() < 0.5:
            angle += math.pi
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.speed = speed
        self.trail = []   # (x, y) history for trail effect

    def update(self):
        self.trail.append((self.x, self.y))
        if len(self.trail) > 12:
            self.trail.pop(0)
        self.x += self.vx
        self.y += self.vy

    def draw(self, surf):
        # trail
        for i, (tx, ty) in enumerate(self.trail):
            alpha = int(200 * (i / len(self.trail)))
            r = max(2, int(BALL_RADIUS * i / len(self.trail)))
            s = pygame.Surface((r*2+1, r*2+1), pygame.SRCALPHA)
            pygame.draw.circle(s, (*WHITE, alpha), (r, r), r)
            surf.blit(s, (tx - r, ty - r))
        glow_circle(surf, WHITE, (int(self.x), int(self.y)), BALL_RADIUS)

    def rect(self):
        return pygame.Rect(self.x - BALL_RADIUS, self.y - BALL_RADIUS,
                           BALL_RADIUS*2, BALL_RADIUS*2)

# ── Paddle ────────────────────────────────────────────────────────────────────

class Paddle:
    """
    side: 'left' | 'right' | 'top' | 'bottom'
    """
    def __init__(self, side, player_index, num_players):
        self.side = side
        self.index = player_index
        self.color = PLAYER_COLORS[player_index]
        self.length = PADDLE_LENGTH_DEFAULT
        self.pos = 0.0          # centre along the wall (x for left/right, y for top/bottom)
        self.effects = {}       # effect_id -> frames_remaining
        self._place(num_players)

    def _place(self, num_players):
        if self.side in ('left', 'right'):
            self.pos = HEIGHT / 2
        else:
            self.pos = WIDTH / 2

    # Returns the paddle Rect for drawing & collision
    def get_rect(self):
        half = self.length // 2
        t = PADDLE_THICKNESS
        if self.side == 'left':
            return pygame.Rect(8, self.pos - half, t, self.length)
        elif self.side == 'right':
            return pygame.Rect(WIDTH - 8 - t, self.pos - half, t, self.length)
        elif self.side == 'top':
            return pygame.Rect(self.pos - half, 8, self.length, t)
        else:  # bottom
            return pygame.Rect(self.pos - half, HEIGHT - 8 - t, self.length, t)

    def move(self, direction):
        """direction: -1 or +1"""
        speed = PADDLE_SPEED
        if self.side in ('left', 'right'):
            half = self.length // 2
            self.pos = max(half + 10, min(HEIGHT - half - 10,
                                          self.pos + direction * speed))
        else:
            half = self.length // 2
            self.pos = max(half + 10, min(WIDTH - half - 10,
                                          self.pos + direction * speed))

    def apply_effect(self, eid):
        if eid == 'bigger':
            self.length = min(220, self.length + 50)
            self.effects['bigger'] = POWERUP_DURATION
        elif eid == 'smaller':
            self.length = max(40, self.length - 50)
            self.effects['smaller'] = POWERUP_DURATION

    def tick_effects(self):
        expired = []
        for eid, frames in list(self.effects.items()):
            self.effects[eid] = frames - 1
            if self.effects[eid] <= 0:
                expired.append(eid)
        for eid in expired:
            del self.effects[eid]
            if eid == 'bigger':
                self.length = max(PADDLE_LENGTH_DEFAULT, self.length - 50)
            elif eid == 'smaller':
                self.length = min(PADDLE_LENGTH_DEFAULT, self.length + 50)

    def draw(self, surf):
        r = self.get_rect()
        glow_rect(surf, self.color, r, radius=8)

# ── Power-up Pickup ───────────────────────────────────────────────────────────

class PowerUp:
    def __init__(self, arena_rect):
        ptype = random.choice(POWERUP_TYPES)
        self.id, self.label, self.color, self.is_good = ptype
        margin = 80
        self.x = random.randint(arena_rect.left + margin, arena_rect.right - margin)
        self.y = random.randint(arena_rect.top + margin, arena_rect.bottom - margin)
        self.lifetime = POWERUP_LIFETIME
        self.angle = 0.0

    def update(self):
        self.lifetime -= 1
        self.angle += 2

    def draw(self, surf, font_small):
        if self.lifetime <= 0:
            return
        alpha_factor = min(1.0, self.lifetime / 60)
        col = tuple(int(c * alpha_factor) for c in self.color)
        glow_circle(surf, col, (self.x, self.y), POWERUP_RADIUS, radius=10)
        # rotating inner symbol
        symb_surf = font_small.render("★" if self.is_good else "▼", True, col)
        symb_surf = pygame.transform.rotate(symb_surf, self.angle)
        surf.blit(symb_surf, symb_surf.get_rect(center=(self.x, self.y)))

    def rect(self):
        return pygame.Rect(self.x - POWERUP_RADIUS, self.y - POWERUP_RADIUS,
                           POWERUP_RADIUS*2, POWERUP_RADIUS*2)

# ── Notification ──────────────────────────────────────────────────────────────

class Notification:
    def __init__(self, text, color, duration=120):
        self.text = text
        self.color = color
        self.timer = duration
        self.duration = duration

    def draw(self, surf, font, y_offset=0):
        alpha = int(255 * min(1.0, self.timer / 40))
        scale = 1.0 + 0.15 * math.sin(self.timer * 0.15)
        txt = font.render(self.text, True, self.color)
        txt = pygame.transform.rotozoom(txt, 0, scale)
        x = WIDTH // 2 - txt.get_width() // 2
        y = HEIGHT // 2 - 40 + y_offset
        s = pygame.Surface(txt.get_size(), pygame.SRCALPHA)
        s.blit(txt, (0, 0))
        s.set_alpha(alpha)
        surf.blit(s, (x, y))

# ── Game ──────────────────────────────────────────────────────────────────────

class Game:
    def __init__(self, num_players):
        self.num_players = num_players
        self.arena = pygame.Rect(30, 30, WIDTH - 60, HEIGHT - 60)
        self._build_paddles()
        self.balls = [Ball(WIDTH//2, HEIGHT//2)]
        self.scores = [0] * num_players
        self.powerups = []
        self.spawn_timer = POWERUP_SPAWN_INTERVAL
        self.notifications = []
        self.ball_speed_modifier = 1.0
        self.speed_timer = 0
        self.winner = None
        self.flash = 0   # screen flash frames on score

    def _build_paddles(self):
        sides = {
            1: ['left'],           # shouldn't happen but safe
            2: ['left', 'right'],
            3: ['left', 'right', 'bottom'],
            4: ['left', 'right', 'bottom', 'top'],
        }[self.num_players]
        self.paddles = [Paddle(s, i, self.num_players) for i, s in enumerate(sides)]

    # ── Input map ─────────────────────────────────────────────────────────────
    # Returns (paddle_index, direction) tuples for pressed keys
    KEYMAPS = {
        # P1 left
        pygame.K_w:     (0, -1),
        pygame.K_s:     (0, +1),
        # P2 right
        pygame.K_UP:    (1, -1),
        pygame.K_DOWN:  (1, +1),
        # P3 bottom  (left/right on its wall = left/right keys for us)
        pygame.K_a:     (2, -1),
        pygame.K_d:     (2, +1),
        # P4 top
        pygame.K_LEFT:  (3, -1),
        pygame.K_RIGHT: (3, +1),
    }

    def handle_input(self, keys):
        for key, (pidx, direction) in self.KEYMAPS.items():
            if pidx < self.num_players and keys[key]:
                self.paddles[pidx].move(direction)

    # ── Update ────────────────────────────────────────────────────────────────

    def update(self):
        if self.winner:
            return

        # Tick effects
        for p in self.paddles:
            p.tick_effects()

        # Speed modifier timer
        if self.speed_timer > 0:
            self.speed_timer -= 1
            if self.speed_timer == 0:
                self.ball_speed_modifier = 1.0
                for b in self.balls:
                    spd = math.hypot(b.vx, b.vy)
                    scale = BALL_SPEED_INIT / spd
                    b.vx *= scale; b.vy *= scale

        # Move balls
        dead_balls = []
        for ball in self.balls:
            ball.vx *= self.ball_speed_modifier ** (1/FPS * 0.5)  # smooth apply
            ball.update()
            result = self._check_ball(ball)
            if result == 'dead':
                dead_balls.append(ball)

        for b in dead_balls:
            self.balls.remove(b)

        if not self.balls:
            self.balls.append(Ball(WIDTH//2, HEIGHT//2,
                                   BALL_SPEED_INIT * self.ball_speed_modifier))

        # Limit multi-ball
        if len(self.balls) > 4:
            self.balls = self.balls[:4]

        # Power-ups
        self.spawn_timer -= 1
        if self.spawn_timer <= 0:
            self.powerups.append(PowerUp(self.arena))
            self.spawn_timer = POWERUP_SPAWN_INTERVAL

        for pu in list(self.powerups):
            pu.update()
            if pu.lifetime <= 0:
                self.powerups.remove(pu)
                continue
            for ball in self.balls:
                if pu.rect().colliderect(ball.rect()):
                    self._apply_powerup(pu)
                    self.powerups.remove(pu)
                    break

        # Notifications
        for n in list(self.notifications):
            n.timer -= 1
            if n.timer <= 0:
                self.notifications.remove(n)

        if self.flash > 0:
            self.flash -= 1

    def _check_ball(self, ball):
        """Bounce off walls & paddles. Return 'dead' if ball exits."""
        ar = self.arena

        # --- Paddle collisions ---
        for pad in self.paddles:
            pr = pad.get_rect()
            if ball.rect().colliderect(pr):
                self._bounce_off_paddle(ball, pad, pr)
                return None

        # --- Wall / goal logic ---
        scored = False
        # Left wall
        if ball.x - BALL_RADIUS < ar.left:
            if self.num_players >= 2 and self.paddles[0].side == 'left':
                # Left paddle missed → everyone else gets a point
                self._score_against(0)
                return 'dead'
            else:
                ball.vx = abs(ball.vx)
        # Right wall
        if ball.x + BALL_RADIUS > ar.right:
            pad_right = next((p for p in self.paddles if p.side == 'right'), None)
            if pad_right:
                self._score_against(pad_right.index)
                return 'dead'
            else:
                ball.vx = -abs(ball.vx)
        # Top wall
        if ball.y - BALL_RADIUS < ar.top:
            pad_top = next((p for p in self.paddles if p.side == 'top'), None)
            if pad_top:
                self._score_against(pad_top.index)
                return 'dead'
            else:
                ball.vy = abs(ball.vy)
        # Bottom wall
        if ball.y + BALL_RADIUS > ar.bottom:
            pad_bot = next((p for p in self.paddles if p.side == 'bottom'), None)
            if pad_bot:
                self._score_against(pad_bot.index)
                return 'dead'
            else:
                ball.vy = -abs(ball.vy)

        return None

    def _bounce_off_paddle(self, ball, pad, pr):
        offset_ratio = 0.0
        if pad.side == 'left':
            ball.vx = abs(ball.vx) * 1.03
            ball.x = pr.right + BALL_RADIUS + 1
            offset_ratio = (ball.y - pr.centery) / (pr.height / 2)
            ball.vy = offset_ratio * abs(ball.vx) * 1.2
        elif pad.side == 'right':
            ball.vx = -abs(ball.vx) * 1.03
            ball.x = pr.left - BALL_RADIUS - 1
            offset_ratio = (ball.y - pr.centery) / (pr.height / 2)
            ball.vy = offset_ratio * abs(ball.vx) * 1.2
        elif pad.side == 'top':
            ball.vy = abs(ball.vy) * 1.03
            ball.y = pr.bottom + BALL_RADIUS + 1
            offset_ratio = (ball.x - pr.centerx) / (pr.width / 2)
            ball.vx = offset_ratio * abs(ball.vy) * 1.2
        elif pad.side == 'bottom':
            ball.vy = -abs(ball.vy) * 1.03
            ball.y = pr.top - BALL_RADIUS - 1
            offset_ratio = (ball.x - pr.centerx) / (pr.width / 2)
            ball.vx = offset_ratio * abs(ball.vy) * 1.2

        # Cap speed
        spd = math.hypot(ball.vx, ball.vy)
        max_spd = BALL_SPEED_INIT * 2.2 * self.ball_speed_modifier
        if spd > max_spd:
            ball.vx *= max_spd / spd
            ball.vy *= max_spd / spd

    def _score_against(self, loser_index):
        """Give a point to every player except the loser."""
        for i in range(self.num_players):
            if i != loser_index:
                self.scores[i] += 1
        self.flash = 20
        self.notifications.append(Notification(
            f"P{loser_index+1} MISSED!", PLAYER_COLORS[loser_index], 100))
        for i, s in enumerate(self.scores):
            if s >= WINNING_SCORE:
                self.winner = i
                break

    def _apply_powerup(self, pu):
        self.notifications.append(Notification(pu.label, pu.color, 130))
        if pu.id == 'bigger':
            target = random.choice(self.paddles)
            target.apply_effect('bigger')
        elif pu.id == 'smaller':
            target = random.choice(self.paddles)
            target.apply_effect('smaller')
        elif pu.id == 'multiball':
            for _ in range(2):
                b = Ball(WIDTH//2, HEIGHT//2, BALL_SPEED_INIT * self.ball_speed_modifier)
                self.balls.append(b)
        elif pu.id == 'slow':
            self.ball_speed_modifier = 0.5
            self.speed_timer = POWERUP_DURATION
            for b in self.balls:
                spd = math.hypot(b.vx, b.vy)
                b.vx *= 0.5; b.vy *= 0.5
        elif pu.id == 'fast':
            self.ball_speed_modifier = 1.8
            self.speed_timer = POWERUP_DURATION
            for b in self.balls:
                spd = math.hypot(b.vx, b.vy)
                b.vx *= 1.8; b.vy *= 1.8

    # ── Draw ──────────────────────────────────────────────────────────────────

    def draw(self, surf, font, font_small, font_big):
        surf.fill(BLACK)

        # Screen flash on score
        if self.flash > 0:
            f_surf = pygame.Surface((WIDTH, HEIGHT))
            f_surf.fill(WHITE)
            f_surf.set_alpha(int(120 * (self.flash / 20)))
            surf.blit(f_surf, (0, 0))

        # Arena border
        ar = self.arena
        # Draw each wall with the colour of the player defending it (or grey if no player)
        sides_info = {p.side: p.color for p in self.paddles}
        wall_map = {
            'left':   (ar.left,   ar.top,    ar.left,   ar.bottom),
            'right':  (ar.right,  ar.top,    ar.right,  ar.bottom),
            'top':    (ar.left,   ar.top,    ar.right,  ar.top),
            'bottom': (ar.left,   ar.bottom, ar.right,  ar.bottom),
        }
        for side, pts in wall_map.items():
            col = sides_info.get(side, GREY)
            glow_line(surf, col, pts[:2], pts[2:], width=3, radius=5)

        # Centre cross-hair
        cx, cy = WIDTH//2, HEIGHT//2
        glow_line(surf, (30, 30, 40), (cx, ar.top), (cx, ar.bottom), width=1, radius=1)
        glow_line(surf, (30, 30, 40), (ar.left, cy), (ar.right, cy), width=1, radius=1)
        pygame.draw.circle(surf, (30, 30, 40), (cx, cy), 40, 1)

        # Power-ups
        for pu in self.powerups:
            pu.draw(surf, font_small)

        # Balls
        for ball in self.balls:
            ball.draw(surf)

        # Paddles
        for pad in self.paddles:
            pad.draw(surf)

        # Scores
        self._draw_scores(surf, font, font_small)

        # Notifications
        for i, n in enumerate(self.notifications):
            n.draw(surf, font, y_offset=i * 45)

        # Winner overlay
        if self.winner is not None:
            self._draw_winner(surf, font_big, font)

    def _draw_scores(self, surf, font, font_small):
        score_positions = {
            'left':   (60,       HEIGHT // 2),
            'right':  (WIDTH-60, HEIGHT // 2),
            'bottom': (WIDTH//2, HEIGHT - 55),
            'top':    (WIDTH//2, 50),
        }
        for pad in self.paddles:
            pos = score_positions[pad.side]
            txt = font.render(str(self.scores[pad.index]), True, pad.color)
            surf.blit(txt, txt.get_rect(center=pos))
            lbl = font_small.render(f"P{pad.index+1}", True,
                                    tuple(c//2 for c in pad.color))
            offset = {
                'left': (50, 0), 'right': (-50, 0),
                'bottom': (0, -25), 'top': (0, 25)
            }[pad.side]
            surf.blit(lbl, lbl.get_rect(center=(pos[0]+offset[0], pos[1]+offset[1])))

    def _draw_winner(self, surf, font_big, font):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        surf.blit(overlay, (0, 0))
        col = PLAYER_COLORS[self.winner]
        txt = font_big.render(f"PLAYER {self.winner+1} WINS!", True, col)
        surf.blit(txt, txt.get_rect(center=(WIDTH//2, HEIGHT//2 - 40)))
        sub = font.render("Press R to restart  |  Q to quit", True, WHITE)
        surf.blit(sub, sub.get_rect(center=(WIDTH//2, HEIGHT//2 + 30)))


# ── Menu ──────────────────────────────────────────────────────────────────────

def draw_menu(surf, font_big, font, font_small, tick):
    surf.fill(BLACK)

    # Animated title
    scale = 1.0 + 0.04 * math.sin(tick * 0.05)
    title = font_big.render("NEON PONG", True, CYAN)
    title = pygame.transform.rotozoom(title, 0, scale)
    surf.blit(title, title.get_rect(center=(WIDTH//2, 160)))

    sub = font_small.render("ARENA", True, MAGENTA)
    surf.blit(sub, sub.get_rect(center=(WIDTH//2, 220)))

    # Player selection prompt
    for i, (n, label) in enumerate([(2, "2 PLAYERS"), (3, "3 PLAYERS"), (4, "4 PLAYERS")]):
        col = [CYAN, YELLOW, MAGENTA][i]
        blink = int(255 * abs(math.sin(tick * 0.06 + i))) if True else 255
        t = font.render(f"Press {n}  →  {label}", True,
                        tuple(min(255, c + 40) for c in col))
        surf.blit(t, t.get_rect(center=(WIDTH//2, 320 + i * 60)))

    # Controls cheatsheet
    lines = [
        ("P1 (Left):", "W / S", CYAN),
        ("P2 (Right):", "↑ / ↓", MAGENTA),
        ("P3 (Bottom):", "A / D", YELLOW),
        ("P4 (Top):", "← / →", ORANGE),
    ]
    y0 = 530
    for label, keys, col in lines:
        lt = font_small.render(label, True, GREY)
        kt = font_small.render(keys, True, col)
        surf.blit(lt, (220, y0))
        surf.blit(kt, (420, y0))
        y0 += 36

    foot = font_small.render("First to 7 points wins!", True, (80, 80, 90))
    surf.blit(foot, foot.get_rect(center=(WIDTH//2, 740)))

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    pygame.init()
    surf = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Neon Pong Arena")
    clock = pygame.time.Clock()

    try:
        font_big   = pygame.font.SysFont("couriernew", 56, bold=True)
        font       = pygame.font.SysFont("couriernew", 34, bold=True)
        font_small = pygame.font.SysFont("couriernew", 20)
    except Exception:
        font_big   = pygame.font.SysFont(None, 60, bold=True)
        font       = pygame.font.SysFont(None, 38, bold=True)
        font_small = pygame.font.SysFont(None, 22)

    state = "menu"   # "menu" | "game"
    game = None
    tick = 0

    while True:
        clock.tick(FPS)
        tick += 1
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if state == "menu":
                    if event.key == pygame.K_2:
                        game = Game(2); state = "game"
                    elif event.key == pygame.K_3:
                        game = Game(3); state = "game"
                    elif event.key == pygame.K_4:
                        game = Game(4); state = "game"
                elif state == "game":
                    if event.key == pygame.K_r:
                        game = Game(game.num_players)
                    elif event.key == pygame.K_q:
                        state = "menu"
                    elif event.key == pygame.K_ESCAPE:
                        state = "menu"

        if state == "menu":
            draw_menu(surf, font_big, font, font_small, tick)
        elif state == "game":
            game.handle_input(keys)
            game.update()
            game.draw(surf, font, font_small, font_big)

            # ESC hint
            hint = font_small.render("ESC = menu  |  R = restart", True, (50, 50, 60))
            surf.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT - 22))

        pygame.display.flip()


if __name__ == "__main__":
    main()
