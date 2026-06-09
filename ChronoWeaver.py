import sys
import math
import random
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QDialog,  
    QVBoxLayout, QHBoxLayout, QStackedWidget,
    QLabel, QPushButton, QComboBox
)
from PyQt6.QtCore import (Qt, QTimer, QPointF, QRectF, pyqtSignal, QObject,
                           QPropertyAnimation, QEasingCurve, QSize)
from PyQt6.QtGui import (QPainter, QColor, QPen, QBrush, QFont, QLinearGradient,
                          QRadialGradient, QPainterPath, QPixmap, QFontMetrics,
                          QKeyEvent, QPalette)


# ─── Translations ────────────────────────────────────────────────────────────
TRANSLATIONS = {
    "en": {
        "title": "ChronoWeaver",
        "subtitle": "Weave Time, Bend Reality",
        "play": "Play",
        "settings": "Settings",
        "quit": "Quit",
        "language": "Language",
        "theme": "Theme",
        "light": "Light",
        "dark": "Dark",
        "back": "Back",
        "energy": "Time Energy",
        "score": "Score",
        "level": "Level",
        "time_threads": "Time Threads",
        "knots": "Knots",
        "pause": "Pause",
        "resume": "Resume",
        "restart": "Restart",
        "main_menu": "Main Menu",
        "game_over": "Game Over",
        "level_complete": "Level Complete!",
        "controls": "Controls",
        "move": "Move: A/D or ←/→",
        "jump": "Jump: W or ↑ or Space",
        "time_view": "Time View: Q",
        "weave": "Weave Knot: E",
        "pause_key": "Pause: Esc",
        "tutorial_1": "Collect Time Crystals to gain energy",
        "tutorial_2": "Press Q to see your time trails",
        "tutorial_3": "Press E near trails to create knots",
        "tutorial_4": "Past versions help solve puzzles",
        "enemies": "Enemies",
        "crystals": "Crystals",
        "platforms": "Platforms",
        "boss": "TIME BOSS",
        "health": "HP",
        "wave": "Wave",
    },
    "zh": {
        "title": "时间编织者",
        "subtitle": "编织时间，弯曲现实",
        "play": "开始游戏",
        "settings": "设置",
        "quit": "退出",
        "language": "语言",
        "theme": "主题",
        "light": "浅色",
        "dark": "深色",
        "back": "返回",
        "energy": "时间能量",
        "score": "分数",
        "level": "关卡",
        "time_threads": "时间线",
        "knots": "结点",
        "pause": "暂停",
        "resume": "继续",
        "restart": "重新开始",
        "main_menu": "主菜单",
        "game_over": "游戏结束",
        "level_complete": "关卡完成！",
        "controls": "控制",
        "move": "移动: A/D 或 ←/→",
        "jump": "跳跃: W 或 ↑ 或 空格",
        "time_view": "时间视图: Q",
        "weave": "编织结点: E",
        "pause_key": "暂停: Esc",
        "tutorial_1": "收集时间水晶获得能量",
        "tutorial_2": "按Q查看时间轨迹",
        "tutorial_3": "在轨迹附近按E创建结点",
        "tutorial_4": "过去的版本帮助解决谜题",
        "enemies": "敌人",
        "crystals": "水晶",
        "platforms": "平台",
        "boss": "时间首领",
        "health": "生命",
        "wave": "波次",
    },
    "fa": {
        "title": "بافنده‌ی زمان",
        "subtitle": "زمان را ببافید، واقعیت را خم کنید",
        "play": "بازی",
        "settings": "تنظیمات",
        "quit": "خروج",
        "language": "زبان",
        "theme": "پوسته",
        "light": "روشن",
        "dark": "تاریک",
        "back": "بازگشت",
        "energy": "انرژی زمان",
        "score": "امتیاز",
        "level": "مرحله",
        "time_threads": "نخ‌های زمان",
        "knots": "گره‌ها",
        "pause": "توقف",
        "resume": "ادامه",
        "restart": "شروع مجدد",
        "main_menu": "منوی اصلی",
        "game_over": "بازی تمام شد",
        "level_complete": "مرحله کامل شد!",
        "controls": "کنترل‌ها",
        "move": "حرکت: A/D یا ←/→",
        "jump": "پرش: W یا ↑ یا Space",
        "time_view": "دید زمان: Q",
        "weave": "بافت گره: E",
        "pause_key": "توقف: Esc",
        "tutorial_1": "کریستال‌های زمان جمع کنید",
        "tutorial_2": "Q را فشار دهید تا ردهای زمانی ببینید",
        "tutorial_3": "نزدیک ردها E را فشار دهید",
        "tutorial_4": "نسخه‌های گذشته به حل پازل کمک می‌کنند",
        "enemies": "دشمنان",
        "crystals": "کریستال‌ها",
        "platforms": "سکوها",
        "boss": "باس زمان",
        "health": "سلامت",
        "wave": "موج",
    }
}

# ─── Theme Colors ─────────────────────────────────────────────────────────────
THEMES = {
    "dark": {
        "bg": QColor(8, 8, 20),
        "bg2": QColor(15, 15, 35),
        "panel": QColor(20, 20, 45),
        "panel2": QColor(30, 30, 60),
        "accent": QColor(80, 200, 255),
        "accent2": QColor(150, 80, 255),
        "accent3": QColor(255, 150, 50),
        "text": QColor(220, 230, 255),
        "text2": QColor(150, 160, 200),
        "border": QColor(60, 80, 140),
        "player": QColor(100, 220, 255),
        "trail": QColor(80, 180, 255, 120),
        "knot": QColor(200, 100, 255),
        "platform": QColor(40, 60, 100),
        "platform_top": QColor(60, 100, 160),
        "enemy": QColor(255, 80, 80),
        "crystal": QColor(100, 255, 200),
        "ghost": QColor(150, 200, 255, 80),
        "button_bg": QColor(25, 35, 70),
        "button_hover": QColor(40, 60, 120),
        "button_border": QColor(80, 120, 200),
        "hud_bg": QColor(10, 15, 35, 200),
        "energy_bar": QColor(80, 200, 255),
        "health_bar": QColor(80, 255, 120),
        "boss_bar": QColor(255, 80, 80),
        "star": QColor(200, 210, 255, 150),
    },
    "light": {
        "bg": QColor(200, 215, 240),
        "bg2": QColor(215, 228, 250),
        "panel": QColor(230, 238, 255),
        "panel2": QColor(245, 248, 255),
        "accent": QColor(30, 120, 200),
        "accent2": QColor(100, 30, 180),
        "accent3": QColor(200, 100, 20),
        "text": QColor(20, 30, 70),
        "text2": QColor(60, 80, 130),
        "border": QColor(120, 150, 210),
        "player": QColor(20, 100, 200),
        "trail": QColor(30, 120, 220, 100),
        "knot": QColor(140, 40, 200),
        "platform": QColor(100, 130, 180),
        "platform_top": QColor(80, 120, 200),
        "enemy": QColor(200, 40, 40),
        "crystal": QColor(20, 180, 130),
        "ghost": QColor(60, 120, 200, 80),
        "button_bg": QColor(210, 225, 255),
        "button_hover": QColor(180, 200, 240),
        "button_border": QColor(80, 120, 200),
        "hud_bg": QColor(200, 215, 240, 200),
        "energy_bar": QColor(30, 120, 200),
        "health_bar": QColor(30, 180, 80),
        "boss_bar": QColor(200, 40, 40),
        "star": QColor(100, 120, 180, 100),
    }
}

# ─── Game State ───────────────────────────────────────────────────────────────
class GameState:
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    LEVEL_COMPLETE = "level_complete"
    SETTINGS = "settings"

# ─── Platform ─────────────────────────────────────────────────────────────────
class Platform:
    def __init__(self, x, y, w, h, moving=False, move_range=0, move_speed=1):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.moving = moving
        self.move_range = move_range
        self.move_speed = move_speed
        self.start_x = x
        self.move_dir = 1
        self.move_t = 0

    def update(self, dt):
        if self.moving:
            self.move_t += dt * self.move_speed
            self.x = self.start_x + math.sin(self.move_t) * self.move_range

    def rect(self):
        return QRectF(self.x, self.y, self.w, self.h)

# ─── Crystal ──────────────────────────────────────────────────────────────────
class Crystal:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collected = False
        self.anim = 0.0
        self.size = 12

    def update(self, dt):
        self.anim += dt * 2.0

    def rect(self):
        return QRectF(self.x - self.size/2, self.y - self.size/2, self.size, self.size)

# ─── Enemy ────────────────────────────────────────────────────────────────────
class Enemy:
    TYPE_TRAIL = "trail"    # follows trails
    TYPE_PRESENT = "present"  # attacks current player
    TYPE_KNOT = "knot"      # destroys knots

    def __init__(self, x, y, etype=TYPE_PRESENT, patrol_range=80):
        self.x = x
        self.y = y
        self.w = 24
        self.h = 28
        self.etype = etype
        self.patrol_range = patrol_range
        self.start_x = x
        self.vx = 1.5
        self.vy = 0
        self.on_ground = False
        self.health = 3
        self.anim = 0.0
        self.alert = False
        self.alert_timer = 0

    def update(self, dt, platforms, player_x, player_y, trails):
        self.anim += dt * 3.0
        self.alert_timer = max(0, self.alert_timer - dt)

        if self.etype == self.TYPE_PRESENT:
            dx = player_x - self.x
            if abs(dx) < 200:
                self.alert = True
                self.alert_timer = 1.0
                self.vx = 2.0 * (1 if dx > 0 else -1)
            else:
                self.alert = False
                if abs(self.x - self.start_x) > self.patrol_range:
                    self.vx *= -1
        elif self.etype == self.TYPE_TRAIL:
            if trails:
                nearest = min(trails, key=lambda t: math.hypot(t[0]-self.x, t[1]-self.y))
                dx = nearest[0] - self.x
                self.vx = 1.8 * (1 if dx > 0 else -1)
                self.alert = True
            else:
                if abs(self.x - self.start_x) > self.patrol_range:
                    self.vx *= -1
        else:
            if abs(self.x - self.start_x) > self.patrol_range:
                self.vx *= -1

        self.vy += 600 * dt
        self.x += self.vx * 60 * dt
        self.y += self.vy * dt

        self.on_ground = False
        for p in platforms:
            pr = p.rect()
            if (self.x + self.w > pr.x() and self.x < pr.x() + pr.width() and
                    self.y + self.h > pr.y() and self.y + self.h < pr.y() + pr.height() + 20 and
                    self.vy >= 0):
                self.y = pr.y() - self.h
                self.vy = 0
                self.on_ground = True

    def rect(self):
        return QRectF(self.x, self.y, self.w, self.h)

# ─── Ghost (past version) ─────────────────────────────────────────────────────
class Ghost:
    def __init__(self, history):
        self.history = list(history)
        self.index = 0
        self.x = history[0][0] if history else 0
        self.y = history[0][1] if history else 0
        self.active = True
        self.loop = True
        self.w = 20
        self.h = 28

    def update(self, dt):
        if not self.active or not self.history:
            return
        self.index = (self.index + 1) % len(self.history)
        self.x = self.history[self.index][0]
        self.y = self.history[self.index][1]

    def rect(self):
        return QRectF(self.x, self.y, self.w, self.h)

# ─── Time Knot ────────────────────────────────────────────────────────────────
class TimeKnot:
    def __init__(self, x, y, ktype="ghost"):
        self.x = x
        self.y = y
        self.ktype = ktype  # "ghost", "platform", "field"
        self.active = True
        self.anim = 0.0
        self.duration = 8.0
        self.timer = 0.0
        self.w = 60
        self.h = 12

    def update(self, dt):
        self.anim += dt * 2.0
        self.timer += dt
        if self.timer >= self.duration:
            self.active = False

    def rect(self):
        if self.ktype == "platform":
            return QRectF(self.x - self.w/2, self.y, self.w, self.h)
        return QRectF(self.x - 20, self.y - 20, 40, 40)

# ─── Player ───────────────────────────────────────────────────────────────────
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 20
        self.h = 28
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.health = 5
        self.max_health = 5
        self.energy = 100.0
        self.max_energy = 100.0
        self.score = 0
        self.facing = 1
        self.anim = 0.0
        self.invincible = 0.0
        self.history = []
        self.max_history = 300
        self.time_view = False
        self.knots = []
        self.ghosts = []
        self.jump_count = 0
        self.max_jumps = 2

    def update(self, dt, keys, platforms):
        self.anim += dt * 4.0
        self.invincible = max(0, self.invincible - dt)

        speed = 180
        accel = 800
        friction = 600

        target_vx = 0
        if keys.get(Qt.Key.Key_A) or keys.get(Qt.Key.Key_Left):
            target_vx = -speed
            self.facing = -1
        if keys.get(Qt.Key.Key_D) or keys.get(Qt.Key.Key_Right):
            target_vx = speed
            self.facing = 1

        if target_vx != 0:
            self.vx += (target_vx - self.vx) * min(1.0, accel * dt / speed)
        else:
            sign = 1 if self.vx > 0 else -1
            self.vx -= sign * min(abs(self.vx), friction * dt)

        self.vy += 600 * dt
        self.vy = min(self.vy, 800)

        self.x += self.vx * dt
        self.y += self.vy * dt

        self.on_ground = False
        for p in platforms:
            pr = p.rect()
            if (self.x + self.w > pr.x() and self.x < pr.x() + pr.width()):
                if (self.vy >= 0 and self.y + self.h > pr.y() and
                        self.y + self.h < pr.y() + pr.height() + 30):
                    self.y = pr.y() - self.h
                    self.vy = 0
                    self.on_ground = True
                    self.jump_count = 0

        if self.on_ground or self.jump_count < self.max_jumps:
            pass

        # Record history
        self.history.append((self.x, self.y, self.facing))
        if len(self.history) > self.max_history:
            self.history.pop(0)

        # Update knots
        for k in self.knots:
            k.update(dt)
        self.knots = [k for k in self.knots if k.active]

        # Update ghosts
        for g in self.ghosts:
            g.update(dt)

        # Energy regen
        self.energy = min(self.max_energy, self.energy + 3 * dt)

    def jump(self):
        if self.on_ground:
            self.vy = -380
            self.on_ground = False
            self.jump_count = 1
        elif self.jump_count < self.max_jumps:
            self.vy = -320
            self.jump_count += 1

    def create_knot(self):
        if self.energy >= 20 and len(self.history) > 30:
            self.energy -= 20
            ktype = random.choice(["ghost", "platform", "field"])
            knot = TimeKnot(self.x, self.y - 20, ktype)
            self.knots.append(knot)
            if ktype == "ghost" and len(self.history) > 60:
                ghost = Ghost(self.history[-60:])
                self.ghosts.append(ghost)
                if len(self.ghosts) > 3:
                    self.ghosts.pop(0)
            return True
        return False

    def rect(self):
        return QRectF(self.x, self.y, self.w, self.h)

    def take_damage(self, amount=1):
        if self.invincible <= 0:
            self.health -= amount
            self.invincible = 1.5

# ─── Level Data ───────────────────────────────────────────────────────────────
def create_level(level_num, world_w, world_h):
    platforms = []
    crystals = []
    enemies = []

    # Ground
    platforms.append(Platform(0, world_h - 40, world_w, 40))

    if level_num == 1:
        platforms += [
            Platform(100, world_h - 140, 120, 16),
            Platform(280, world_h - 200, 100, 16),
            Platform(440, world_h - 160, 140, 16),
            Platform(640, world_h - 240, 100, 16),
            Platform(800, world_h - 180, 120, 16),
            Platform(200, world_h - 300, 80, 16),
            Platform(500, world_h - 320, 100, 16),
        ]
        crystals = [Crystal(160, world_h-160), Crystal(330, world_h-220),
                    Crystal(510, world_h-180), Crystal(690, world_h-260),
                    Crystal(240, world_h-320)]
        enemies = [Enemy(400, world_h-68, Enemy.TYPE_PRESENT, 100),
                   Enemy(700, world_h-68, Enemy.TYPE_TRAIL, 80)]

    elif level_num == 2:
        platforms += [
            Platform(80, world_h-160, 100, 16, True, 60, 0.8),
            Platform(260, world_h-220, 90, 16),
            Platform(420, world_h-180, 110, 16, True, 40, 1.2),
            Platform(600, world_h-260, 100, 16),
            Platform(760, world_h-200, 120, 16),
            Platform(180, world_h-320, 80, 16),
            Platform(480, world_h-340, 90, 16, True, 50, 0.9),
            Platform(700, world_h-360, 80, 16),
        ]
        crystals = [Crystal(130, world_h-180), Crystal(305, world_h-240),
                    Crystal(475, world_h-200), Crystal(650, world_h-280),
                    Crystal(220, world_h-340), Crystal(800, world_h-220)]
        enemies = [Enemy(350, world_h-68, Enemy.TYPE_PRESENT, 120),
                   Enemy(600, world_h-68, Enemy.TYPE_KNOT, 90),
                   Enemy(800, world_h-68, Enemy.TYPE_TRAIL, 100)]

    else:
        platforms += [
            Platform(60, world_h-160, 90, 16, True, 80, 1.0),
            Platform(220, world_h-240, 80, 16),
            Platform(380, world_h-200, 100, 16, True, 60, 1.5),
            Platform(560, world_h-280, 90, 16),
            Platform(720, world_h-220, 110, 16, True, 70, 1.2),
            Platform(160, world_h-360, 80, 16),
            Platform(400, world_h-380, 90, 16, True, 50, 1.0),
            Platform(640, world_h-400, 80, 16),
            Platform(300, world_h-460, 100, 16),
        ]
        crystals = [Crystal(105, world_h-180), Crystal(260, world_h-260),
                    Crystal(430, world_h-220), Crystal(605, world_h-300),
                    Crystal(775, world_h-240), Crystal(200, world_h-380),
                    Crystal(445, world_h-400), Crystal(680, world_h-420)]
        enemies = [Enemy(300, world_h-68, Enemy.TYPE_PRESENT, 100),
                   Enemy(550, world_h-68, Enemy.TYPE_KNOT, 80),
                   Enemy(750, world_h-68, Enemy.TYPE_TRAIL, 120),
                   Enemy(450, world_h-68, Enemy.TYPE_PRESENT, 90)]

    return platforms, crystals, enemies

# ─── Game Canvas ──────────────────────────────────────────────────────────────
class GameCanvas(QWidget):
    score_changed = pyqtSignal(int)
    health_changed = pyqtSignal(int, int)
    energy_changed = pyqtSignal(float, float)
    knots_changed = pyqtSignal(int)
    state_changed = pyqtSignal(str)

    def __init__(self, theme, lang):
        super().__init__()
        self.theme_name = theme
        self.lang = lang
        self.T = THEMES[theme]
        self.tr = TRANSLATIONS[lang]
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setMinimumSize(600, 400)

        self.world_w = 1000
        self.world_h = 600
        self.camera_x = 0
        self.camera_y = 0

        self.keys = {}
        self.jump_pressed = False
        self.weave_pressed = False

        self.state = GameState.PLAYING
        self.level_num = 1
        self.max_levels = 3
        self.boss_health = 20
        self.boss_max_health = 20
        self.boss_active = False
        self.boss_x = 500
        self.boss_y = 100
        self.boss_vx = 2
        self.boss_anim = 0.0
        self.wave = 1

        self.particles = []
        self.bg_stars = [(random.randint(0, 1000), random.randint(0, 600),
                          random.random() * 2 + 0.5) for _ in range(80)]

        self._init_level()

        self.timer = QTimer()
        self.timer.timeout.connect(self._tick)
        self.timer.start(16)

        self.last_time = 0
        self._dt = 0.016

    def _init_level(self):
        self.player = Player(60, self.world_h - 100)
        self.platforms, self.crystals, self.enemies = create_level(
            self.level_num, self.world_w, self.world_h)
        self.boss_active = (self.level_num == self.max_levels)
        self.boss_health = self.boss_max_health
        self.goal_x = self.world_w - 80
        self.goal_y = self.world_h - 80

    def set_theme(self, theme):
        self.theme_name = theme
        self.T = THEMES[theme]
        self.update()

    def set_lang(self, lang):
        self.lang = lang
        self.tr = TRANSLATIONS[lang]
        self.update()

    def _tick(self):
        if self.state != GameState.PLAYING:
            self.update()
            return

        dt = self._dt

        # Update platforms
        for p in self.platforms:
            p.update(dt)

        # Update player
        self.player.update(dt, self.keys, self.platforms)

        # Update crystals
        for c in self.crystals:
            c.update(dt)
            if not c.collected and self.player.rect().intersects(c.rect()):
                c.collected = True
                self.player.energy = min(self.player.max_energy, self.player.energy + 25)
                self.player.score += 50
                self._spawn_particles(c.x, c.y, self.T["crystal"], 8)
                self.score_changed.emit(self.player.score)
                self.energy_changed.emit(self.player.energy, self.player.max_energy)

        # Update enemies
        trail_points = [(h[0], h[1]) for h in self.player.history[::5]]
        for e in self.enemies:
            e.update(dt, self.platforms, self.player.x, self.player.y, trail_points)
            if e.rect().intersects(self.player.rect()):
                self.player.take_damage()
                self.health_changed.emit(self.player.health, self.player.max_health)
                if self.player.health <= 0:
                    self.state = GameState.GAME_OVER
                    self.state_changed.emit(GameState.GAME_OVER)

        # Boss
        if self.boss_active:
            self._update_boss(dt)

        # Update particles
        for p in self.particles:
            p[0] += p[2] * dt
            p[1] += p[3] * dt
            p[3] += 200 * dt
            p[4] -= dt
        self.particles = [p for p in self.particles if p[4] > 0]

        # Camera
        target_cx = self.player.x - self.width() / 2
        target_cy = self.player.y - self.height() / 2
        self.camera_x += (target_cx - self.camera_x) * 0.1
        self.camera_y += (target_cy - self.camera_y) * 0.1
        self.camera_x = max(0, min(self.camera_x, self.world_w - self.width()))
        self.camera_y = max(0, min(self.camera_y, self.world_h - self.height()))

        # Check goal
        goal_rect = QRectF(self.goal_x, self.goal_y, 40, 40)
        if self.player.rect().intersects(goal_rect):
            if self.level_num < self.max_levels:
                self.level_num += 1
                self._init_level()
                self.state_changed.emit(GameState.LEVEL_COMPLETE)
            else:
                self.state = GameState.LEVEL_COMPLETE
                self.state_changed.emit(GameState.LEVEL_COMPLETE)

        self.knots_changed.emit(len(self.player.knots))
        self.update()

    def _update_boss(self, dt):
        self.boss_anim += dt * 2.0
        self.boss_x += self.boss_vx * 60 * dt
        if self.boss_x < 100 or self.boss_x > self.world_w - 100:
            self.boss_vx *= -1

        # Boss attacks player
        dx = self.player.x - self.boss_x
        dy = self.player.y - self.boss_y
        dist = math.hypot(dx, dy)
        if dist < 60:
            self.player.take_damage()
            self.health_changed.emit(self.player.health, self.player.max_health)

        # Boss destroys knots
        for k in self.player.knots:
            if math.hypot(k.x - self.boss_x, k.y - self.boss_y) < 80:
                k.active = False

        # Player knots damage boss
        for k in self.player.knots:
            if math.hypot(k.x - self.boss_x, k.y - self.boss_y) < 50:
                self.boss_health -= dt * 2
                self._spawn_particles(self.boss_x, self.boss_y, self.T["knot"], 3)

        if self.boss_health <= 0:
            self.boss_active = False
            self.player.score += 500
            self.score_changed.emit(self.player.score)
            self._spawn_particles(self.boss_x, self.boss_y, self.T["accent3"], 30)

    def _spawn_particles(self, x, y, color, count):
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(50, 200)
            life = random.uniform(0.3, 0.8)
            self.particles.append([x, y, math.cos(angle)*speed,
                                    math.sin(angle)*speed, life, color])

    def keyPressEvent(self, event):
        self.keys[event.key()] = True
        if event.key() in (Qt.Key.Key_W, Qt.Key.Key_Up, Qt.Key.Key_Space):
            if self.state == GameState.PLAYING:
                self.player.jump()
        if event.key() == Qt.Key.Key_Q:
            self.player.time_view = not self.player.time_view
        if event.key() == Qt.Key.Key_E:
            if self.state == GameState.PLAYING:
                if self.player.create_knot():
                    self._spawn_particles(self.player.x, self.player.y, self.T["knot"], 6)
                    self.energy_changed.emit(self.player.energy, self.player.max_energy)
                    self.knots_changed.emit(len(self.player.knots))
        if event.key() == Qt.Key.Key_Escape:
            if self.state == GameState.PLAYING:
                self.state = GameState.PAUSED
                self.state_changed.emit(GameState.PAUSED)
            elif self.state == GameState.PAUSED:
                self.state = GameState.PLAYING
                self.state_changed.emit(GameState.PLAYING)

    def keyReleaseEvent(self, event):
        self.keys[event.key()] = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()

        # Scale factor for responsiveness
        scale_x = w / 1000
        scale_y = h / 600
        scale = min(scale_x, scale_y)

        self._draw_background(painter, w, h)
        painter.save()
        painter.translate(-self.camera_x, -self.camera_y)
        self._draw_world(painter)
        painter.restore()
        self._draw_hud(painter, w, h)

        if self.state == GameState.PAUSED:
            self._draw_overlay(painter, w, h, self.tr["pause"])
        elif self.state == GameState.GAME_OVER:
            self._draw_overlay(painter, w, h, self.tr["game_over"])
        elif self.state == GameState.LEVEL_COMPLETE:
            self._draw_overlay(painter, w, h, self.tr["level_complete"])

        painter.end()

    def _draw_background(self, painter, w, h):
        grad = QLinearGradient(0, 0, 0, h)
        grad.setColorAt(0, self.T["bg"])
        grad.setColorAt(1, self.T["bg2"])
        painter.fillRect(0, 0, w, h, grad)

        # Stars
        for sx, sy, size in self.bg_stars:
            rx = (sx - self.camera_x * 0.3) % w
            ry = (sy - self.camera_y * 0.2) % h
            c = QColor(self.T["star"])
            painter.setPen(QPen(c, size))
            painter.drawPoint(int(rx), int(ry))

    def _draw_world(self, painter):
        # Draw platforms
        for p in self.platforms:
            pr = p.rect()
            grad = QLinearGradient(pr.x(), pr.y(), pr.x(), pr.y() + pr.height())
            grad.setColorAt(0, self.T["platform_top"])
            grad.setColorAt(1, self.T["platform"])
            painter.fillRect(pr, grad)
            painter.setPen(QPen(self.T["border"], 1))
            painter.drawRect(pr)

        # Draw time trails
        if self.player.time_view and len(self.player.history) > 2:
            path = QPainterPath()
            path.moveTo(self.player.history[0][0] + 10, self.player.history[0][1] + 14)
            for hx, hy, _ in self.player.history[1:]:
                path.lineTo(hx + 10, hy + 14)
            pen = QPen(self.T["trail"], 2)
            pen.setStyle(Qt.PenStyle.DashLine)
            painter.setPen(pen)
            painter.drawPath(path)

            # Trail dots
            for i, (hx, hy, _) in enumerate(self.player.history[::10]):
                alpha = int(80 * i / (len(self.player.history) // 10 + 1))
                c = QColor(self.T["accent"])
                c.setAlpha(alpha)
                painter.setPen(QPen(c, 3))
                painter.drawPoint(int(hx + 10), int(hy + 14))

        # Draw knots
        for k in self.player.knots:
            self._draw_knot(painter, k)

        # Draw ghosts
        for g in self.player.ghosts:
            if g.active:
                self._draw_ghost(painter, g)

        # Draw crystals
        for c in self.crystals:
            if not c.collected:
                self._draw_crystal(painter, c)

        # Draw enemies
        for e in self.enemies:
            self._draw_enemy(painter, e)

        # Draw boss
        if self.boss_active:
            self._draw_boss(painter)

        # Draw goal
        self._draw_goal(painter)

        # Draw player
        self._draw_player(painter)

        # Draw particles
        for p in self.particles:
            c = QColor(p[5])
            c.setAlpha(int(255 * p[4] / 0.8))
            painter.setPen(QPen(c, 3))
            painter.drawPoint(int(p[0]), int(p[1]))

    def _draw_player(self, painter):
        p = self.player
        x, y = int(p.x), int(p.y)
        bob = math.sin(p.anim) * 2 if p.on_ground else 0

        # Glow
        if p.invincible > 0:
            glow = QRadialGradient(x + p.w//2, y + p.h//2 + bob, 30)
            glow.setColorAt(0, QColor(255, 200, 100, 80))
            glow.setColorAt(1, QColor(255, 200, 100, 0))
            painter.fillRect(x-20, y-20+int(bob), p.w+40, p.h+40, glow)

        # Body
        body_color = self.T["player"]
        painter.setBrush(QBrush(body_color))
        painter.setPen(QPen(self.T["accent"], 1.5))
        painter.drawRoundedRect(x, y + int(bob), p.w, p.h, 4, 4)

        # Eyes
        eye_x = x + (12 if p.facing > 0 else 4)
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(eye_x, y + 6 + int(bob), 5, 5)
        painter.setBrush(QBrush(QColor(20, 20, 60)))
        painter.drawEllipse(eye_x + (1 if p.facing > 0 else 0), y + 7 + int(bob), 3, 3)

        # Time energy aura
        if p.time_view:
            aura = QRadialGradient(x + p.w//2, y + p.h//2, 40)
            aura.setColorAt(0, QColor(self.T["accent"].red(),
                                      self.T["accent"].green(),
                                      self.T["accent"].blue(), 40))
            aura.setColorAt(1, QColor(self.T["accent"].red(),
                                      self.T["accent"].green(),
                                      self.T["accent"].blue(), 0))
            painter.fillRect(x-30, y-30, p.w+60, p.h+60, aura)

    def _draw_ghost(self, painter, g):
        x, y = int(g.x), int(g.y)
        c = QColor(self.T["ghost"])
        painter.setBrush(QBrush(c))
        painter.setPen(QPen(self.T["accent"], 1))
        painter.setOpacity(0.5)
        painter.drawRoundedRect(x, y, g.w, g.h, 4, 4)
        painter.setOpacity(1.0)

    def _draw_knot(self, painter, k):
        x, y = int(k.x), int(k.y)
        pulse = math.sin(k.anim) * 0.3 + 0.7
        life_ratio = 1.0 - k.timer / k.duration

        if k.ktype == "platform":
            c = QColor(self.T["knot"])
            c.setAlpha(int(200 * life_ratio))
            painter.setBrush(QBrush(c))
            painter.setPen(QPen(self.T["accent2"], 2))
            painter.drawRoundedRect(int(x - k.w//2), y, k.w, k.h, 3, 3)
            # Glow
            glow_c = QColor(self.T["knot"])
            glow_c.setAlpha(int(60 * life_ratio * pulse))
            painter.setBrush(QBrush(glow_c))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(int(x - k.w//2 - 4), y - 4, k.w + 8, k.h + 8, 5, 5)

        elif k.ktype == "field":
            c = QColor(self.T["accent3"])
            c.setAlpha(int(100 * life_ratio * pulse))
            painter.setBrush(QBrush(c))
            painter.setPen(QPen(self.T["accent3"], 1))
            painter.drawEllipse(x - 30, y - 30, 60, 60)

        else:  # ghost knot
            c = QColor(self.T["accent2"])
            c.setAlpha(int(150 * life_ratio * pulse))
            painter.setBrush(QBrush(c))
            painter.setPen(QPen(self.T["knot"], 2))
            size = int(20 * pulse)
            painter.drawEllipse(x - size//2, y - size//2, size, size)
            # Orbiting dots
            for i in range(4):
                angle = k.anim + i * math.pi / 2
                ox = x + int(math.cos(angle) * 18)
                oy = y + int(math.sin(angle) * 18)
                painter.setPen(QPen(self.T["knot"], 3))
                painter.drawPoint(ox, oy)

    def _draw_crystal(self, painter, c):
        x, y = int(c.x), int(c.y)
        bob = int(math.sin(c.anim) * 4)
        size = c.size

        # Glow
        glow = QRadialGradient(x, y + bob, size * 2)
        glow.setColorAt(0, QColor(self.T["crystal"].red(),
                                   self.T["crystal"].green(),
                                   self.T["crystal"].blue(), 80))
        glow.setColorAt(1, QColor(0, 0, 0, 0))
        painter.fillRect(x - size*2, y - size*2 + bob, size*4, size*4, glow)

        # Diamond shape
        path = QPainterPath()
        path.moveTo(x, y - size + bob)
        path.lineTo(x + size * 0.6, y + bob)
        path.lineTo(x, y + size * 0.7 + bob)
        path.lineTo(x - size * 0.6, y + bob)
        path.closeSubpath()
        painter.setBrush(QBrush(self.T["crystal"]))
        painter.setPen(QPen(QColor(200, 255, 240), 1))
        painter.drawPath(path)

    def _draw_enemy(self, painter, e):
        x, y = int(e.x), int(e.y)
        bob = int(math.sin(e.anim) * 2)

        color_map = {
            Enemy.TYPE_PRESENT: self.T["enemy"],
            Enemy.TYPE_TRAIL: QColor(255, 150, 50),
            Enemy.TYPE_KNOT: QColor(200, 50, 200),
        }
        c = color_map.get(e.etype, self.T["enemy"])

        if e.alert:
            glow = QRadialGradient(x + e.w//2, y + e.h//2, 35)
            glow.setColorAt(0, QColor(c.red(), c.green(), c.blue(), 60))
            glow.setColorAt(1, QColor(0, 0, 0, 0))
            painter.fillRect(x-20, y-20, e.w+40, e.h+40, glow)

        painter.setBrush(QBrush(c))
        painter.setPen(QPen(QColor(255, 200, 200), 1.5))
        painter.drawRoundedRect(x, y + bob, e.w, e.h, 5, 5)

        # Eyes (angry)
        painter.setBrush(QBrush(QColor(255, 50, 50)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(x + 4, y + 6 + bob, 5, 5)
        painter.drawEllipse(x + 14, y + 6 + bob, 5, 5)

        # Health bar
        bar_w = e.w
        painter.fillRect(x, y - 8 + bob, bar_w, 4, QColor(60, 20, 20))
        hp_w = int(bar_w * e.health / 3)
        painter.fillRect(x, y - 8 + bob, hp_w, 4, self.T["health_bar"])

    def _draw_boss(self, painter):
        x, y = int(self.boss_x), int(self.boss_y)
        pulse = math.sin(self.boss_anim) * 0.2 + 1.0
        size = int(50 * pulse)

        # Glow
        glow = QRadialGradient(x, y, 80)
        glow.setColorAt(0, QColor(255, 50, 50, 80))
        glow.setColorAt(1, QColor(0, 0, 0, 0))
        painter.fillRect(x - 80, y - 80, 160, 160, glow)

        # Body
        painter.setBrush(QBrush(QColor(180, 20, 20)))
        painter.setPen(QPen(QColor(255, 100, 100), 2))
        painter.drawEllipse(x - size//2, y - size//2, size, size)

        # Orbiting rings
        for i in range(3):
            angle = self.boss_anim + i * math.pi * 2 / 3
            rx = x + int(math.cos(angle) * 40)
            ry = y + int(math.sin(angle) * 20)
            painter.setBrush(QBrush(QColor(255, 100, 50, 180)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(rx - 8, ry - 8, 16, 16)

        # Eyes
        painter.setBrush(QBrush(QColor(255, 255, 100)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(x - 12, y - 8, 10, 10)
        painter.drawEllipse(x + 2, y - 8, 10, 10)

    def _draw_goal(self, painter):
        x, y = int(self.goal_x), int(self.goal_y)
        t = self.player.anim
        pulse = math.sin(t * 1.5) * 0.15 + 1.0

        glow = QRadialGradient(x + 20, y + 20, 50)
        glow.setColorAt(0, QColor(self.T["accent3"].red(),
                                   self.T["accent3"].green(),
                                   self.T["accent3"].blue(), 100))
        glow.setColorAt(1, QColor(0, 0, 0, 0))
        painter.fillRect(x - 30, y - 30, 100, 100, glow)

        size = int(40 * pulse)
        painter.setBrush(QBrush(self.T["accent3"]))
        painter.setPen(QPen(QColor(255, 220, 100), 2))
        painter.drawRoundedRect(x + (40 - size)//2, y + (40 - size)//2, size, size, 8, 8)

        # Portal swirl
        for i in range(6):
            angle = t + i * math.pi / 3
            px = x + 20 + int(math.cos(angle) * 15)
            py = y + 20 + int(math.sin(angle) * 15)
            painter.setPen(QPen(QColor(255, 255, 150, 180), 2))
            painter.drawPoint(px, py)

    def _draw_hud(self, painter, w, h):
        hud_h = max(50, int(h * 0.1))
        painter.fillRect(0, 0, w, hud_h, self.T["hud_bg"])
        painter.setPen(QPen(self.T["border"], 1))
        painter.drawLine(0, hud_h, w, hud_h)

        font_size = max(9, int(h * 0.022))
        font = QFont("Arial", font_size, QFont.Weight.Bold)
        painter.setFont(font)

        pad = int(w * 0.015)
        bar_h = max(8, int(hud_h * 0.25))
        bar_y = int(hud_h * 0.55)
        bar_w = int(w * 0.14)

        # Health bar
        painter.setPen(QPen(self.T["text2"], 1))
        painter.drawText(pad, int(hud_h * 0.38), self.tr["health"])
        painter.fillRect(pad, bar_y, bar_w, bar_h, QColor(40, 20, 20))
        hp_w = int(bar_w * self.player.health / self.player.max_health)
        painter.fillRect(pad, bar_y, hp_w, bar_h, self.T["health_bar"])
        painter.setPen(QPen(self.T["border"], 1))
        painter.drawRect(pad, bar_y, bar_w, bar_h)

        # Energy bar
        e_x = pad + bar_w + pad
        painter.setPen(QPen(self.T["text2"], 1))
        painter.drawText(e_x, int(hud_h * 0.38), self.tr["energy"])
        painter.fillRect(e_x, bar_y, bar_w, bar_h, QColor(20, 20, 40))
        en_w = int(bar_w * self.player.energy / self.player.max_energy)
        painter.fillRect(e_x, bar_y, en_w, bar_h, self.T["energy_bar"])
        painter.setPen(QPen(self.T["border"], 1))
        painter.drawRect(e_x, bar_y, bar_w, bar_h)

        # Score
        score_x = int(w * 0.42)
        painter.setPen(QPen(self.T["text"], 1))
        painter.drawText(score_x, int(hud_h * 0.65),
                         f"{self.tr['score']}: {self.player.score}")

        # Level
        lv_x = int(w * 0.58)
        painter.drawText(lv_x, int(hud_h * 0.65),
                         f"{self.tr['level']}: {self.level_num}")

        # Knots
        kn_x = int(w * 0.72)
        painter.drawText(kn_x, int(hud_h * 0.65),
                         f"{self.tr['knots']}: {len(self.player.knots)}")

        # Boss health bar
        if self.boss_active:
            bw = int(w * 0.4)
            bx = (w - bw) // 2
            by = hud_h + 8
            painter.fillRect(bx, by, bw, 14, QColor(40, 10, 10))
            boss_w = int(bw * max(0, self.boss_health) / self.boss_max_health)
            painter.fillRect(bx, by, boss_w, 14, self.T["boss_bar"])
            painter.setPen(QPen(self.T["border"], 1))
            painter.drawRect(bx, by, bw, 14)
            painter.setPen(QPen(self.T["text"], 1))
            painter.setFont(QFont("Arial", max(8, font_size - 1)))
            painter.drawText(bx + bw//2 - 30, by + 11, self.tr["boss"])

        # Controls hint
        hint_font = QFont("Arial", max(7, font_size - 3))
        painter.setFont(hint_font)
        painter.setPen(QPen(self.T["text2"], 1))
        hints = "Q: Time View  |  E: Weave Knot  |  Esc: Pause"
        painter.drawText(w - int(w * 0.42), int(hud_h * 0.65), hints)

    def _draw_overlay(self, painter, w, h, text):
        painter.fillRect(0, 0, w, h, QColor(0, 0, 0, 140))
        font_size = max(20, int(h * 0.06))
        painter.setFont(QFont("Arial", font_size, QFont.Weight.Bold))
        painter.setPen(QPen(self.T["accent"], 2))
        fm = QFontMetrics(painter.font())
        tw = fm.horizontalAdvance(text)
        painter.drawText((w - tw) // 2, h // 2, text)

    def restart(self):
        self.level_num = 1
        self._init_level()
        self.state = GameState.PLAYING
        self.particles.clear()

    def toggle_pause(self):
        if self.state == GameState.PLAYING:
            self.state = GameState.PAUSED
        elif self.state == GameState.PAUSED:
            self.state = GameState.PLAYING


# ─── Styled Button ────────────────────────────────────────────────────────────
class ChronoButton(QPushButton):
    def __init__(self, text, theme, parent=None):
        super().__init__(text, parent)
        self.theme_name = theme
        self.T = THEMES[theme]
        self._hovered = False
        self.setMinimumHeight(44)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._apply_style()

    def set_theme(self, theme):
        self.theme_name = theme
        self.T = THEMES[theme]
        self._apply_style()

    def _apply_style(self):
        bg = self.T["button_bg"]
        hover = self.T["button_hover"]
        border = self.T["button_border"]
        text = self.T["text"]
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba({bg.red()},{bg.green()},{bg.blue()},220);
                color: rgb({text.red()},{text.green()},{text.blue()});
                border: 1.5px solid rgb({border.red()},{border.green()},{border.blue()});
                border-radius: 8px;
                padding: 8px 20px;
                font-size: 14px;
                font-weight: bold;
                letter-spacing: 1px;
            }}
            QPushButton:hover {{
                background-color: rgba({hover.red()},{hover.green()},{hover.blue()},240);
                border: 2px solid rgb({border.red()},{border.green()},{border.blue()});
            }}
            QPushButton:pressed {{
                background-color: rgba({border.red()},{border.green()},{border.blue()},180);
            }}
        """)


# ─── Main Menu ────────────────────────────────────────────────────────────────
class MainMenu(QWidget):
    play_clicked = pyqtSignal()
    settings_clicked = pyqtSignal()
    quit_clicked = pyqtSignal()

    def __init__(self, theme, lang):
        super().__init__()
        self.theme_name = theme
        self.lang = lang
        self.T = THEMES[theme]
        self.tr = TRANSLATIONS[lang]
        self.anim_t = 0.0
        self._build_ui()
        self._start_animation()

    def _build_ui(self):
        # Canvas به عنوان background کامل
        self.canvas = MenuCanvas(self.theme_name)
        self.canvas.setParent(self)

        # Container مرکزی روی canvas
        self.container = QWidget(self)
        self.container.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        vbox = QVBoxLayout(self.container)
        vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox.setSpacing(18)
        vbox.setContentsMargins(40, 40, 40, 40)

        self.title_label = QLabel(self.tr["title"])
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._style_title()
        vbox.addWidget(self.title_label)

        self.sub_label = QLabel(self.tr["subtitle"])
        self.sub_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._style_subtitle()
        vbox.addWidget(self.sub_label)

        vbox.addSpacing(20)

        self.btn_play = ChronoButton(self.tr["play"], self.theme_name)
        self.btn_play.setFixedWidth(220)
        self.btn_play.clicked.connect(self.play_clicked)
        vbox.addWidget(self.btn_play, alignment=Qt.AlignmentFlag.AlignCenter)

        self.btn_settings = ChronoButton(self.tr["settings"], self.theme_name)
        self.btn_settings.setFixedWidth(220)
        self.btn_settings.clicked.connect(self.settings_clicked)
        vbox.addWidget(self.btn_settings, alignment=Qt.AlignmentFlag.AlignCenter)

        self.btn_quit = ChronoButton(self.tr["quit"], self.theme_name)
        self.btn_quit.setFixedWidth(220)
        self.btn_quit.clicked.connect(self.quit_clicked)
        vbox.addWidget(self.btn_quit, alignment=Qt.AlignmentFlag.AlignCenter)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # canvas همیشه کل widget رو بپوشونه
        self.canvas.setGeometry(0, 0, self.width(), self.height())
        # container وسط باشه
        cw, ch = 320, 400
        self.container.setGeometry(
            (self.width() - cw) // 2,
            (self.height() - ch) // 2,
            cw, ch
        )

    def _start_animation(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)
        self.timer.start(16)

    def _animate(self):
        self.anim_t += 0.03
        self.canvas.anim_t = self.anim_t
        self.canvas.update()

    def _style_title(self):
        c = self.T["accent"]
        self.title_label.setStyleSheet(f"""
            color: rgb({c.red()},{c.green()},{c.blue()});
            font-size: 38px;
            font-weight: bold;
            letter-spacing: 4px;
            background: transparent;
        """)

    def _style_subtitle(self):
        c = self.T["text2"]
        self.sub_label.setStyleSheet(f"""
            color: rgb({c.red()},{c.green()},{c.blue()});
            font-size: 15px;
            letter-spacing: 2px;
            background: transparent;
        """)

    def apply_theme(self, theme):
        self.theme_name = theme
        self.T = THEMES[theme]
        self.canvas.set_theme(theme)
        self._style_title()
        self._style_subtitle()
        self.btn_play.set_theme(theme)
        self.btn_settings.set_theme(theme)
        self.btn_quit.set_theme(theme)

    def apply_lang(self, lang):
        self.lang = lang
        self.tr = TRANSLATIONS[lang]
        self.title_label.setText(self.tr["title"])
        self.sub_label.setText(self.tr["subtitle"])
        self.btn_play.setText(self.tr["play"])
        self.btn_settings.setText(self.tr["settings"])
        self.btn_quit.setText(self.tr["quit"])


# ─── Menu Canvas (animated background) ───────────────────────────────────────
class MenuCanvas(QWidget):
    def __init__(self, theme):
        super().__init__()
        self.theme_name = theme
        self.T = THEMES[theme]
        self.anim_t = 0.0
        self.stars = [(random.randint(0, 1200), random.randint(0, 800),
                       random.uniform(1, 3)) for _ in range(120)]
        self.orbs = [(random.uniform(0.1, 0.9), random.uniform(0.2, 0.8),
                      random.uniform(0.5, 1.5), random.uniform(0, math.pi * 2))
                     for _ in range(6)]

    def set_theme(self, theme):
        self.theme_name = theme
        self.T = THEMES[theme]
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()

        # Background gradient
        grad = QLinearGradient(0, 0, 0, h)
        grad.setColorAt(0, self.T["bg"])
        grad.setColorAt(1, self.T["bg2"])
        painter.fillRect(0, 0, w, h, grad)

        # Stars
        for sx, sy, size in self.stars:
            twinkle = math.sin(self.anim_t * 2 + sx * 0.01) * 0.4 + 0.6
            c = QColor(self.T["star"])
            c.setAlpha(int(180 * twinkle))
            painter.setPen(QPen(c, size))
            painter.drawPoint(sx % w, sy % h)

        # Floating orbs
        for ox, oy, speed, phase in self.orbs:
            cx = int(ox * w + math.sin(self.anim_t * speed + phase) * 40)
            cy = int(oy * h + math.cos(self.anim_t * speed * 0.7 + phase) * 25)
            r = int(30 + math.sin(self.anim_t + phase) * 8)
            glow = QRadialGradient(cx, cy, r * 2)
            ac = self.T["accent"]
            glow.setColorAt(0, QColor(ac.red(), ac.green(), ac.blue(), 50))
            glow.setColorAt(1, QColor(ac.red(), ac.green(), ac.blue(), 0))
            painter.fillRect(cx - r*2, cy - r*2, r*4, r*4, glow)
            c = QColor(self.T["accent2"])
            c.setAlpha(60)
            painter.setBrush(QBrush(c))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(cx - r//2, cy - r//2, r, r)

        # Time trail decoration
        path = QPainterPath()
        path.moveTo(0, h * 0.6)
        for i in range(0, w + 20, 20):
            wave_y = h * 0.6 + math.sin(self.anim_t + i * 0.015) * 30
            path.lineTo(i, wave_y)
        pen = QPen(self.T["trail"], 1.5)
        pen.setStyle(Qt.PenStyle.DashLine)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(path)

        painter.end()


# ─── Settings Dialog ──────────────────────────────────────────────────────────
class SettingsDialog(QDialog):
    theme_changed = pyqtSignal(str)
    lang_changed = pyqtSignal(str)

    def __init__(self, theme, lang, parent=None):
        super().__init__(parent)
        self.theme_name = theme
        self.lang = lang
        self.T = THEMES[theme]
        self.tr = TRANSLATIONS[lang]
        self.setWindowTitle(self.tr["settings"])
        self.setMinimumWidth(340)
        self.setModal(True)
        self._build_ui()
        self._apply_dialog_style()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(18)
        layout.setContentsMargins(30, 30, 30, 30)

        # Theme selector
        theme_label = QLabel(self.tr["theme"])
        theme_label.setObjectName("setting_label")
        layout.addWidget(theme_label)

        self.theme_combo = QComboBox()
        self.theme_combo.addItem(self.tr["dark"], "dark")
        self.theme_combo.addItem(self.tr["light"], "light")
        self.theme_combo.setCurrentIndex(0 if self.theme_name == "dark" else 1)
        self.theme_combo.currentIndexChanged.connect(self._on_theme_change)
        layout.addWidget(self.theme_combo)

        # Language selector
        lang_label = QLabel(self.tr["language"])
        lang_label.setObjectName("setting_label")
        layout.addWidget(lang_label)

        self.lang_combo = QComboBox()
        self.lang_combo.addItem("English", "en")
        self.lang_combo.addItem("فارسی", "fa")
        self.lang_combo.addItem("中文", "zh")
        idx = {"en": 0, "fa": 1, "zh": 2}.get(self.lang, 0)
        self.lang_combo.setCurrentIndex(idx)
        self.lang_combo.currentIndexChanged.connect(self._on_lang_change)
        layout.addWidget(self.lang_combo)

        layout.addSpacing(10)

        btn_close = ChronoButton(self.tr["close"], self.theme_name)
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)

    def _apply_dialog_style(self):
        bg = self.T["bg"]
        text = self.T["text"]
        border = self.T["border"]
        combo_bg = self.T["button_bg"]
        self.setStyleSheet(f"""
            QDialog {{
                background-color: rgb({bg.red()},{bg.green()},{bg.blue()});
            }}
            QLabel#setting_label {{
                color: rgb({text.red()},{text.green()},{text.blue()});
                font-size: 13px;
                font-weight: bold;
            }}
            QComboBox {{
                background-color: rgb({combo_bg.red()},{combo_bg.green()},{combo_bg.blue()});
                color: rgb({text.red()},{text.green()},{text.blue()});
                border: 1px solid rgb({border.red()},{border.green()},{border.blue()});
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 13px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox QAbstractItemView {{
                background-color: rgb({bg.red()},{bg.green()},{bg.blue()});
                color: rgb({text.red()},{text.green()},{text.blue()});
                selection-background-color: rgb({border.red()},{border.green()},{border.blue()});
            }}
        """)

    def _on_theme_change(self, idx):
        theme = self.theme_combo.itemData(idx)
        self.theme_name = theme
        self.T = THEMES[theme]
        self._apply_dialog_style()
        self.theme_changed.emit(theme)

    def _on_lang_change(self, idx):
        lang = self.lang_combo.itemData(idx)
        self.lang = lang
        self.lang_changed.emit(lang)


# ─── Main Window ──────────────────────────────────────────────────────────────
class ChronoWeaverWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.theme = "dark"
        self.lang = "en"
        self.setWindowTitle("ChronoWeaver")
        self.setMinimumSize(800, 500)
        self.resize(1100, 680)
        self._build_ui()

    def _build_ui(self):
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.menu = MainMenu(self.theme, self.lang)
        self.menu.play_clicked.connect(self._start_game)
        self.menu.settings_clicked.connect(self._open_settings)
        self.menu.quit_clicked.connect(self.close)
        self.stack.addWidget(self.menu)

        self.game_widget = QWidget()
        self._build_game_ui()
        self.stack.addWidget(self.game_widget)

        self.stack.setCurrentWidget(self.menu)

    def _build_game_ui(self):
        layout = QVBoxLayout(self.game_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.canvas = GameCanvas(self.theme, self.lang)
        self.canvas.state_changed.connect(self._on_state_change)
        self.canvas.health_changed.connect(self._on_health)
        self.canvas.energy_changed.connect(self._on_energy)
        self.canvas.score_changed.connect(self._on_score)
        self.canvas.knots_changed.connect(self._on_knots)
        layout.addWidget(self.canvas)

        # Bottom bar
        self.bottom_bar = QWidget()
        self.bottom_bar.setFixedHeight(36)
        bar_layout = QHBoxLayout(self.bottom_bar)
        bar_layout.setContentsMargins(12, 4, 12, 4)
        bar_layout.setSpacing(10)

        self.btn_menu = ChronoButton("◀ Menu", self.theme)
        self.btn_menu.setFixedHeight(28)
        self.btn_menu.clicked.connect(self._back_to_menu)
        bar_layout.addWidget(self.btn_menu)

        self.btn_restart = ChronoButton("↺ Restart", self.theme)
        self.btn_restart.setFixedHeight(28)
        self.btn_restart.clicked.connect(self._restart_game)
        bar_layout.addWidget(self.btn_restart)

        bar_layout.addStretch()

        self.btn_settings2 = ChronoButton("⚙ Settings", self.theme)
        self.btn_settings2.setFixedHeight(28)
        self.btn_settings2.clicked.connect(self._open_settings)
        bar_layout.addWidget(self.btn_settings2)

        layout.addWidget(self.bottom_bar)
        self._apply_bar_style()

    def _apply_bar_style(self):
        T = THEMES[self.theme]
        bg = T["hud_bg"]
        border = T["border"]
        self.bottom_bar.setStyleSheet(f"""
            QWidget {{
                background-color: rgba({bg.red()},{bg.green()},{bg.blue()},230);
                border-top: 1px solid rgb({border.red()},{border.green()},{border.blue()});
            }}
        """)

    def _start_game(self):
        self.canvas.restart()
        self.stack.setCurrentWidget(self.game_widget)
        self.canvas.setFocus()

    def _back_to_menu(self):
        self.canvas.state = GameState.PAUSED
        self.stack.setCurrentWidget(self.menu)

    def _restart_game(self):
        self.canvas.restart()
        self.canvas.setFocus()

    def _open_settings(self):
        dlg = SettingsDialog(self.theme, self.lang, self)
        dlg.theme_changed.connect(self._apply_theme)
        dlg.lang_changed.connect(self._apply_lang)
        dlg.exec()

    def _apply_theme(self, theme):
        self.theme = theme
        self.menu.apply_theme(theme)
        self.canvas.set_theme(theme)
        self.btn_menu.set_theme(theme)
        self.btn_restart.set_theme(theme)
        self.btn_settings2.set_theme(theme)
        self._apply_bar_style()

    def _apply_lang(self, lang):
        self.lang = lang
        self.menu.apply_lang(lang)
        self.canvas.set_lang(lang)

    def _on_state_change(self, state):
        pass  # HUD handles display; extend here for extra UI reactions

    def _on_health(self, hp, max_hp):
        pass

    def _on_energy(self, en, max_en):
        pass

    def _on_score(self, score):
        pass

    def _on_knots(self, count):
        pass

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.canvas.update()


# ─── Entry Point ──────────────────────────────────────────────────────────────
def main():
    app = QApplication(sys.argv)
    app.setApplicationName("ChronoWeaver")
    app.setStyle("Fusion")

    # Base dark palette for Fusion
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(18, 18, 30))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(220, 220, 240))
    palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 40))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(35, 35, 55))
    palette.setColor(QPalette.ColorRole.Text, QColor(220, 220, 240))
    palette.setColor(QPalette.ColorRole.Button, QColor(40, 40, 65))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(220, 220, 240))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(80, 120, 220))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)

    window = ChronoWeaverWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
