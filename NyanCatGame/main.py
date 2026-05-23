import pygame
import random
import os
import sys

# Инициализация модулей pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Настройка окна игры и шрифта
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nyan Cat")
FONT = "Arial"

# Таймер FPS
clock = pygame.time.Clock()

# Цвета интерфейса
DARK_BLUE = (5, 5, 40)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (120, 120, 120)
BLACK = (0, 0, 0)

# ЗАГРУЗКА ИЗОБРАЖЕНИЙ

# Путь к папке проекта
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))


NYAN_FRAMES = []

# Загрузка кадров анимации персонажа
for i in range(6):
    frame_path = os.path.join(PROJECT_PATH, "images", "cat", f"{i}.png")
    frame = pygame.image.load(frame_path).convert_alpha()
    frame = pygame.transform.scale(frame, (120, 70))
    NYAN_FRAMES.append(frame)

GOOD_IMAGES = []

# Загрузка изображений "хорошей" еды
good_path = os.path.join(PROJECT_PATH, "images", "good")
for filename in os.listdir(good_path):
    img_path = os.path.join(good_path, filename)
    img = pygame.image.load(img_path).convert_alpha()
    img = pygame.transform.scale(img, (48, 48))
    GOOD_IMAGES.append(img)

BAD_IMAGES = []

# Загрузка изображений "плохой" еды
bad_path = os.path.join(PROJECT_PATH, "images", "bad")
for filename in os.listdir(bad_path):
    img_path = os.path.join(bad_path, filename)
    img = pygame.image.load(img_path).convert_alpha()
    img = pygame.transform.scale(img, (48, 48))
    BAD_IMAGES.append(img)

# Загрузка иконки "жизни"
heart_path = os.path.join(PROJECT_PATH, "menu", "ui", "heart.png")
HEART_IMAGE = pygame.image.load(heart_path).convert_alpha()
HEART_IMAGE = pygame.transform.scale(HEART_IMAGE, (48, 48))

# Загрузка кнопки настроек
settings_path = os.path.join(PROJECT_PATH, "images", "picture", "setting_button.png")
SETTINGS_ICON = pygame.image.load(settings_path).convert_alpha()
SETTINGS_ICON = pygame.transform.scale(SETTINGS_ICON, (64, 64))
SETTINGS_ICON.fill(WHITE, special_flags=pygame.BLEND_RGB_MAX)

# ЗАГРУЗКА ЗВУКОВ
SOUND_EAT_GOOD = pygame.mixer.Sound(
    os.path.join(PROJECT_PATH, "sounds", "eat_good.wav")
)
SOUND_EAT_BAD = pygame.mixer.Sound(os.path.join(PROJECT_PATH, "sounds", "eat_bad.wav"))
SOUND_HAPPINESS_STAR = pygame.mixer.Sound(
    os.path.join(PROJECT_PATH, "sounds", "happiness_star.wav")
)
SOUND_GAME_OVER = pygame.mixer.Sound(
    os.path.join(PROJECT_PATH, "sounds", "game_over.mp3")
)
SOUND_BG_MUSIC = pygame.mixer.Sound(
    os.path.join(PROJECT_PATH, "sounds", "background_music.mp3")
)
SOUND_LEVEL_COMPLETE = pygame.mixer.Sound(
    os.path.join(PROJECT_PATH, "sounds", "level_complete.mp3")
)
FINISH_GAME = pygame.mixer.Sound(
    os.path.join(PROJECT_PATH, "sounds", "finish_game.mp3")
)
SOUND_SPACE = pygame.mixer.Sound(os.path.join(PROJECT_PATH, "sounds", "fon_music.mp3"))
SOUND_MENU = pygame.mixer.Sound(os.path.join(PROJECT_PATH, "sounds", "menu_music.mp3"))

# Установка громкости звуков
SOUND_MENU.set_volume(0.15)
SOUND_SPACE.set_volume(0.03)
SOUND_BG_MUSIC.set_volume(0.1)
SOUND_EAT_GOOD.set_volume(0.2)
SOUND_LEVEL_COMPLETE.set_volume(0.4)
FINISH_GAME.set_volume(0.3)

# Настройки уровней
LEVELS = {
    # Легкий
    1: {"name": "ЛЁГКИЙ", "goal": 30, "spawn": 1.25, "speed": 4},
    # Средний
    2: {"name": "СРЕДНИЙ", "goal": 60, "spawn": 1.0, "speed": 6},
    # Сложный
    3: {"name": "СЛОЖНЫЙ", "goal": 100, "spawn": 0.65, "speed": 8},
}


# КЛАСС ИГРОВОГО ПЕРСОНАЖА
class Cat:
    # Создание
    def __init__(self):
        self.width = 100
        self.height = 64
        self.x = 50
        self.y = HEIGHT // 2 - self.height // 2
        self.speed = 6
        self.animation_speed = 0.2
        self.frames = NYAN_FRAMES
        self.current_frame = 0
        self.image = self.frames[0]
        self.rect = pygame.Rect(self.x, self.y, 30, 30)

    # Анимация
    def animate(self):
        self.current_frame += self.animation_speed

        if self.current_frame >= len(self.frames):
            self.current_frame = 0

        self.image = self.frames[int(self.current_frame)]

        return self.image

    # Отрисовка
    def draw(self, surface):
        surface.blit(self.animate(), (self.x, self.y))

    # Управление вверх, вниз
    def update(self, keys):
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.y > 0:
            self.y -= self.speed

        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.y < HEIGHT - self.height:
            self.y += self.speed

        self.rect.topleft = (self.x, self.y)


# КЛАСС ЕДЫ
class Food:
    # Создание
    def __init__(self, difficulty_level, eaten_food):
        self.kind = random.choice(["good", "bad"])

        if self.kind == "good":
            self.image = random.choice(GOOD_IMAGES)
        else:
            self.image = random.choice(BAD_IMAGES)

        self.x = WIDTH + 50
        self.y = random.randint(50, HEIGHT - 50)

        base_speed = LEVELS[difficulty_level]["speed"]
        dynamic_bonus = (eaten_food // 10) * 2

        self.speed = base_speed + dynamic_bonus
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    # Движение еды
    def move(self):
        self.x -= self.speed
        self.rect.x = self.x

    # Отрисовка еды
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


# КЛАСС ЗВЕЗД
class Star:
    # Создание
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed = random.uniform(1, 5)
        self.size = random.randint(1, 3)

    # Движение звезд
    def move(self):
        self.x -= self.speed

        if self.x < 0:
            self.x = WIDTH
            self.y = random.randint(0, HEIGHT)

    # Отрисовка звезд
    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.size)


# КЛАСС СЧАСТЛИВЫХ ЗВЕЗД
class HappinessStar:
    # Создание
    def __init__(self):
        self.x = WIDTH + 50
        self.y = random.randint(50, HEIGHT - 50)
        self.speed = 10
        self.size = 15
        self.rect = pygame.Rect(self.x, self.y, self.size * 2, self.size * 2)

    # Движение звезды
    def move(self):
        self.x -= self.speed
        self.rect.x = self.x

    # Отрисовка звезды
    def draw(self, surface):
        pygame.draw.circle(
            surface,
            YELLOW,
            (int(self.x + self.size), int(self.y + self.size)),
            self.size,
        )
        pygame.draw.circle(
            surface,
            WHITE,
            (int(self.x + self.size), int(self.y + self.size)),
            self.size // 2,
        )


# СБРОС ИГРЫ
def reset_game():
    global score
    global happiness
    global eaten_food
    global foods
    global food_timer
    global game_over
    global paused
    global cat
    global stars
    global happiness_stars
    global last_happiness_star

    score = 0
    happiness = 3
    eaten_food = 0
    foods = []
    food_timer = 0
    game_over = False
    paused = False

    cat = Cat()

    stars = [Star() for _ in range(100)]
    happiness_stars = []
    last_happiness_star = pygame.time.get_ticks()


# Запуск музыки менюш
SOUND_MENU.play(-1)


# ИГРОВЫЕ СОСТОЯНИЯ
game = True
menu = True
level_menu = False
paused = False
game_over = False
level_complete = False
game_finished = False
settings_menu = False
controls_menu = False
rules_menu = False

# Текущий уровень
current_level = 1

# Открытый уровень
unlocked_levels = 1

# Сброс игры
reset_game()

# КНОПКИ

easy_button = pygame.Rect(270, 250, 260, 70)
medium_button = pygame.Rect(270, 350, 260, 70)
hard_button = pygame.Rect(270, 450, 260, 70)
controls_button = pygame.Rect(250, 240, 300, 80)
rules_button = pygame.Rect(250, 360, 300, 80)
settings_button = SETTINGS_ICON.get_rect(topleft=(700, 20))


# ФРАЗЫ В МЕНЮ
menu_phrases = [
    "Нажми любую кнопку, чтобы начать",
    "Собирай вкусняшки вместе с Nyan Cat",
    "Избегай плохой еды",
    "Пройди все уровни сложности",
    "Космическое приключение начинается",
]
# Текущая фраза
current_phrase = 0

# Таймер смезы фраз
last_phrase_change = pygame.time.get_ticks()


# ГЛАВНЫЙ ЦИКЛ ИГРЫ
while game:

    # Текущее время
    current_time = pygame.time.get_ticks()

    # Ограничение игры до 60 FPS
    dt = clock.tick(60) / 1000

    # Заливка экрана
    screen.fill(DARK_BLUE)

    # Обработка событий
    for event in pygame.event.get():

        # Закрытие окна
        if event.type == pygame.QUIT:
            game = False

        # ГЛАВНОЕ МЕНЮ
        if menu:

            # Обработка нажатий клавишей и мыши
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:

                # Перезапуск музыки
                SOUND_MENU.stop()
                SOUND_BG_MUSIC.stop()
                SOUND_SPACE.stop()

                SOUND_BG_MUSIC.play(-1)
                SOUND_SPACE.play(-1)

                # Переход в меню уровней
                menu = False
                level_menu = True

        # МЕНЮ ВЫБОРА УРОВНЯ
        elif level_menu:

            # ОБРБОТКА КЛАВИАТУРЫ
            if event.type == pygame.KEYDOWN:

                # Легкий уровень
                if event.key == pygame.K_1:

                    # Перезапуск музыки
                    SOUND_BG_MUSIC.stop()
                    SOUND_SPACE.stop()

                    SOUND_BG_MUSIC.play(-1)
                    SOUND_SPACE.play(-1)

                    # Выбор уровня
                    current_level = 1

                    # Закрытие меню уровней
                    level_menu = False

                    # сброс игры
                    reset_game()

                # Средний уровень
                if event.key == pygame.K_1 and unlocked_levels >= 2:

                    # Перезапуск музыки
                    SOUND_BG_MUSIC.stop()
                    SOUND_SPACE.stop()

                    SOUND_BG_MUSIC.play(-1)
                    SOUND_SPACE.play(-1)

                    # Выбор уровня
                    current_level = 2

                    # Закрытие меню уровней
                    level_menu = False

                    # сброс игры
                    reset_game()

                # Сложный уровень
                if event.key == pygame.K_1 and unlocked_levels >= 3:

                    # Перезапуск музыки
                    SOUND_BG_MUSIC.stop()
                    SOUND_SPACE.stop()

                    SOUND_BG_MUSIC.play(-1)
                    SOUND_SPACE.play(-1)

                    # Выбор уровня
                    current_level = 3

                    # Закрытие меню уровней
                    level_menu = False

                    # сброс игры
                    reset_game()

            # Управление мышкой
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Получение позиции мыши
                mouse_pos = event.pos

                # Кнопка легкого уровня
                if easy_button.collidepoint(mouse_pos):
                    SOUND_BG_MUSIC.stop()
                    SOUND_SPACE.stop()

                    SOUND_BG_MUSIC.play(-1)
                    SOUND_SPACE.play(-1)

                    current_level = 1
                    level_menu = False
                    reset_game()

                # Кнопка среднего уровня
                if medium_button.collidepoint(mouse_pos) and unlocked_levels >= 2:
                    SOUND_BG_MUSIC.stop()
                    SOUND_SPACE.stop()

                    SOUND_BG_MUSIC.play(-1)
                    SOUND_SPACE.play(-1)

                    current_level = 2
                    level_menu = False
                    reset_game()

                # Кнопка сложного уровня
                if hard_button.collidepoint(mouse_pos) and unlocked_levels >= 3:
                    SOUND_BG_MUSIC.stop()
                    SOUND_SPACE.stop()

                    SOUND_BG_MUSIC.play(-1)
                    SOUND_SPACE.play(-1)

                    current_level = 3
                    level_menu = False
                    reset_game()

                # Кнопка настроек
                if settings_button.collidepoint(mouse_pos):

                    level_menu = False
                    settings_menu = True

        # ИГРА ПОЛНОСТЬЮ ПРОЙДЕНА
        elif game_finished:
            if event.type == pygame.KEYDOWN:

                # ENTER для выхода в меню
                if event.key == pygame.K_RETURN:

                    # Остановка финальной музыки
                    FINISH_GAME.stop()

                    # Перезапуск космического звука
                    SOUND_SPACE.stop()
                    SOUND_SPACE.play(-1)

                    # Возврат в меню
                    game_finished = False
                    level_menu = True

        # МЕНЮ НАСТРОЕК
        elif settings_menu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    settings_menu = False
                    level_menu = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                # Кнопка - управление
                if controls_button.collidepoint(mouse_pos):
                    settings_menu = False
                    controls_menu = True

                # Кнопка - правила
                if rules_button.collidepoint(mouse_pos):
                    settings_menu = False
                    rules_menu = True

        # Меню управления
        elif controls_menu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    controls_menu = False
                    settings_menu = True

        # Меню правил
        elif rules_menu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    rules_menu = False
                    settings_menu = True

        # Экран победы
        elif level_complete:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:

                    # Остановка победной музыки
                    SOUND_LEVEL_COMPLETE.stop()

                    # Перезапуск космического фона
                    SOUND_SPACE.stop()
                    SOUND_SPACE.play(-1)

                    # Возврат в меню уровней
                    level_complete = False
                    level_menu = True

        # Игра окончена
        elif game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:

                    # Возврат в меню уровней
                    level_menu = True
                    game_over = False

        # ОСНОВНАЯ ИГРА
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                if paused and event.key == pygame.K_RETURN:

                    # Отключение музыки игры
                    SOUND_BG_MUSIC.stop()
                    SOUND_SPACE.stop()

                    # Включение только космоса
                    SOUND_SPACE.play(-1)

                    # Выход в меню
                    paused = False
                    level_menu = True

    # ГЛАВНОЕ МЕНЮ
    if menu:

        # Движение звезд
        for star in stars:
            star.move()
            star.draw(screen)

        # Смена фраз каждые 2 секунды
        if current_time - last_phrase_change > 2000:
            current_phrase = (current_phrase + 1) % len(menu_phrases)
            last_phrase_change = current_time

        # Шрифты
        title_font = pygame.font.SysFont(FONT, 72, bold=True)
        subtitle_font = pygame.font.SysFont(FONT, 28, bold=True)
        dynamic_font = pygame.font.SysFont(FONT, 22, bold=True)

        # Текст
        title = title_font.render("NYAN CAT", True, YELLOW)
        subtitle = subtitle_font.render("Выбор уровня", True, WHITE)
        dynamic_text = dynamic_font.render(menu_phrases[current_phrase], True, GREEN)

        # Отрисовка текста
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 170))
        screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 270))
        screen.blit(dynamic_text, (WIDTH // 2 - dynamic_text.get_width() // 2, 370))

    # ВЫБОР УРОВНЯ
    elif level_menu:

        # Отрисовка звезд
        for star in stars:
            star.move()
            star.draw(screen)

        # Шрифты
        title_font = pygame.font.SysFont(FONT, 72, bold=True)
        button_font = pygame.font.SysFont(FONT, 20, bold=True)

        # Заголовки
        title = title_font.render("NYAN CAT", True, YELLOW)
        subtitle = button_font.render("Выбор уровня", True, WHITE)

        # Отрисовка текста
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 200))

        # Отрисовка кнопок
        pygame.draw.rect(screen, YELLOW, easy_button, border_radius=20)

        # Кнопка серая, если уровень закрыт
        if unlocked_levels >= 2:
            medium_color = YELLOW
        else:
            medium_color = GRAY

        if unlocked_levels >= 2:
            hard_color = YELLOW
        else:
            hard_color = GRAY

        pygame.draw.rect(screen, medium_color, medium_button, border_radius=15)
        pygame.draw.rect(screen, hard_color, hard_button, border_radius=15)

        # Текст кнопок
        easy_text = button_font.render("УРОВЕНЬ 1 - ЛЁГКИЙ", True, DARK_BLUE)
        medium_text = button_font.render("УРОВЕНЬ 2 - СРЕДНИЙ", True, DARK_BLUE)
        hard_text = button_font.render("УРОВЕНЬ 3 - СЛОЖНЫЙ", True, DARK_BLUE)

        # Отрисовка текста кнопок
        screen.blit(
            easy_text,
            (
                easy_button.centerx - easy_text.get_width() // 2,
                easy_button.centery - easy_text.get_height() // 2,
            ),
        )
        screen.blit(
            medium_text,
            (
                medium_button.centerx - medium_text.get_width() // 2,
                medium_button.centery - medium_text.get_height() // 2,
            ),
        )
        screen.blit(
            hard_text,
            (
                hard_button.centerx - hard_text.get_width() // 2,
                hard_button.centery - hard_text.get_height() // 2,
            ),
        )

        # Иконка настроек
        screen.blit(SETTINGS_ICON, settings_button)

    # ЭКРАН ПОЛНОГО ПРОХОЖДЕНИЯ ИГРЫ
    elif game_finished:

        # Отрисовка звезд
        for star in stars:
            star.move()
            star.draw(screen)

        # Шрифты
        big_font = pygame.font.SysFont(FONT, 56, bold=True)
        small_font = pygame.font.SysFont(FONT, 28)

        # Тексты
        finish_text = big_font.render("ИГРА ЗАВЕРШЕНА!", True, YELLOW)
        info1 = small_font.render(
            "Nyan Cat прошёл все космические испытания!", True, WHITE
        )
        info2 = small_font.render("Вы отлично справились", True, GREEN)
        info3 = small_font.render("ENTER - вернуться в меню", True, WHITE)

        # Отрисовка текста
        screen.blit(finish_text, (WIDTH // 2 - finish_text.get_width() // 2, 180))
        screen.blit(info1, (WIDTH // 2 - info1.get_width() // 2, 280))
        screen.blit(info2, (WIDTH // 2 - info2.get_width() // 2, 340))
        screen.blit(info3, (WIDTH // 2 - info3.get_width() // 2, 430))

    # ЭКРАН ПОБЕДЫ
    elif level_complete:

        # Отрисовка звезд
        for star in stars:
            star.move()
            star.draw(screen)

        # Шрифты
        big_font = pygame.font.SysFont(FONT, 56, bold=True)
        small_font = pygame.font.SysFont(FONT, 28)

        # Текст победы
        win_text = big_font.render(f"УРОВЕНЬ {current_level} ПРОЙДЕН!", True, YELLOW)
        info_text = small_font.render(
            "Поздравляем! Вы открыли следующий уровень!", True, WHITE
        )
        continue_text = small_font.render("ENTER - продолжить", True, GREEN)

        # Отрисовка текста
        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, 220))
        screen.blit(info_text, (WIDTH // 2 - info_text.get_width() // 2, 320))
        screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, 390))

    # МЕНЮ НАСТРОЕК
    elif settings_menu:

        # Движение звезд
        for star in stars:
            star.move()
            star.draw(screen)

        # Шрифты
        title_font = pygame.font.SysFont(FONT, 56, bold=True)
        button_font = pygame.font.SysFont(FONT, 30, bold=True)

        # Заголовки
        title = title_font.render("НАСТРОЙКИ", True, YELLOW)
        back = button_font.render("ENTER - назад", True, GREEN)

        # Отрисовка
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        screen.blit(back, (290, 520))

        # Создание кнопок
        pygame.draw.rect(screen, WHITE, controls_button, border_radius=20)
        pygame.draw.rect(screen, WHITE, rules_button, border_radius=20)

        # Текст кнопок
        controls_text = button_font.render("УПРАВЛЕНИЕ", True, DARK_BLUE)
        rules_text = button_font.render("ПРАВИЛА", True, DARK_BLUE)

        # Отрисовка текста кнопок
        screen.blit(
            controls_text,
            (
                controls_button.centerx - controls_text.get_width() // 2,
                controls_button.centery - controls_text.get_height() // 2,
            ),
        )
        screen.blit(
            rules_text,
            (
                rules_button.centerx - rules_text.get_width() // 2,
                rules_button.centery - rules_text.get_height() // 2,
            ),
        )

    # ЭКРАН УПРАВЛЕНИЯ
    elif controls_menu:

        # Движение звезд
        for star in stars:
            star.move()
            star.draw(screen)

        # Шрифты
        title_font = pygame.font.SysFont(FONT, 56, bold=True)
        text_font = pygame.font.SysFont(FONT, 30)

        # Загловок
        title = title_font.render("УПРАВЛЕНИЕ", True, YELLOW)

        # Информация по клавишам
        control1 = text_font.render("W / ↑  - вверх", True, WHITE)
        control2 = text_font.render("S / ↓  - вниз", True, WHITE)
        control3 = text_font.render("ESC - пауза", True, WHITE)
        back = text_font.render("ENTER - назад", True, GREEN)

        # Отрисовка текста
        screen.blit(title, (220, 100))
        screen.blit(control1, (290, 240))
        screen.blit(control2, (290, 310))
        screen.blit(control3, (290, 380))
        screen.blit(back, (290, 520))

    # ЭКРАН ПРАВИЛ
    elif rules_menu:

        # Движение звезд
        for star in stars:
            star.move()
            star.draw(screen)

        # Шрифты
        title_font = pygame.font.SysFont(FONT, 56, bold=True)
        text_font = pygame.font.SysFont(FONT, 28)

        # Заголовок
        title = title_font.render("ПРАВИЛА", True, YELLOW)

        # Правила игры
        rule1 = text_font.render("Собирайте хорошую еду", True, GREEN)
        rule2 = text_font.render("Избегайте плохой еды", True, RED)
        rule3 = text_font.render("Не потеряйте все три сердца", True, WHITE)
        rule4 = text_font.render("Пройдите все уровни игры", True, WHITE)
        back = text_font.render("ENTER - назад", True, GREEN)

        # Отрисовка текста
        screen.blit(title, (290, 100))
        screen.blit(rule1, (190, 230))
        screen.blit(rule2, (190, 300))
        screen.blit(rule3, (190, 370))
        screen.blit(rule4, (190, 440))
        screen.blit(back, (320, 520))

    # ПАУЗА
    elif paused:

        # Движение звезд
        for star in stars:
            star.move()
            star.draw(screen)

        # Затемнение экрана в черный
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        # Шрифты
        font = pygame.font.SysFont(FONT, 56, bold=True)
        small_font = pygame.font.SysFont(FONT, 28)

        # Тексты
        pause_text = font.render("ПАУЗА", True, YELLOW)
        continue_text = small_font.render("ESC - продолжить", True, WHITE)
        menu_text = small_font.render("ENTER - выйти в меню", True, WHITE)

        # Отрисовка текста
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, 220))
        screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, 320))
        screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, 370))

    # ИГРА ЗАКОНЧЕНА
    elif game_over:

        # Шрифты
        font1 = pygame.font.SysFont(FONT, 72)
        font2 = pygame.font.SysFont(FONT, 30)

        # Тексты
        text = font1.render("Игра окончена!", True, RED)
        score_text = font2.render(f"Ваш счёт: {score}", True, YELLOW)
        restart_text = font2.render("ENTER - меню уровней", True, WHITE)

        # Отрисовка текста
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 120))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        screen.blit(
            restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 70)
        )

    # ОСНОВНАЯ ИГРА
    else:

        # Движение звезд
        for star in stars:
            star.move()
            star.draw(screen)

        # УПРАВЛЕНИЕ ПЕРСОНАЖЕМ

        # Получаем список из нажатых клавиш
        keys = pygame.key.get_pressed()

        # Обновление положения персонажа
        cat.update(keys)

        # Отрисовка персонажа
        cat.draw(screen)

        # Цель уровня и скорость появление еды
        level_goal = LEVELS[current_level]["goal"]
        level_spawn = LEVELS[current_level]["spawn"]

        # Динамическая сокрость увеличения скорости еды
        dynamic_spawn = max(0.2, level_spawn - (eaten_food // 10) * 0.1)

        # Уменьшение таймера
        food_timer -= dt

        if food_timer <= 0:

            # Создание новой еды и таймера
            foods.append(Food(current_level, eaten_food))
            food_timer = random.uniform(dynamic_spawn, dynamic_spawn + 0.4)

        # Обработка еды
        for food in foods[:]:

            # Движение еды
            food.move()

            # Отрисовка еды
            food.draw(screen)

            # Проверка на столкновение с персонажем
            if food.rect.colliderect(cat.rect):

                # Если хорошая еда
                if food.kind == "good":
                    score += 1
                    eaten_food += 1

                    SOUND_EAT_GOOD.play()

                # Если плохая еда
                else:
                    happiness -= 1
                    SOUND_EAT_BAD.play()

                foods.remove(food)

            # Если еда улетела за экран
            elif food.x < -50:
                foods.remove(food)

        # ЗВЕЗДЫ СЧАСТЬЯ

        # Создание звезды раз в 30-40 секунд
        if current_time - last_happiness_star > random.randint(30000, 40000):

            # Создание звезды
            happiness_stars.append(HappinessStar())

            # Обновление таймера
            last_happiness_star = current_time

        # Обработка звезд счастья
        for star in happiness_stars[:]:

            # Движение звезды
            star.move()

            # Отрисовка звезды
            star.draw(screen)

            # Проверка на столкновение с персонажем
            if star.rect.colliderect(cat.rect):

                # Использование максимум 3х жизней
                happiness = min(3, happiness + 1)

                SOUND_HAPPINESS_STAR.play()

                happiness_stars.remove(star)

            # Если звезда улетела за экран
            elif star.x < -50:
                happiness_stars.remove(star)

        # ИНТЕРФЕЙС ИГРЫ

        # Шрифт
        ui_font = pygame.font.SysFont(FONT, 28)

        # Текст уровня
        level_text = ui_font.render(f"Уровень: {current_level}", True, WHITE)

        # Текст цели
        goal_text = ui_font.render(f"Цель: {eaten_food} / {level_goal}", True, YELLOW)

        # Отрисовка текста
        screen.blit(level_text, (20, 15))
        screen.blit(goal_text, (WIDTH // 2 - goal_text.get_width() // 2, 15))

        # Отрисовка сердец
        for i in range(happiness):
            screen.blit(HEART_IMAGE, (WIDTH - 50 - i * 50, 10))

        # ПРОХОЖДЕНИЕ УРОВНЯ

        # Если игрок собрал достаточно еды
        if eaten_food >= level_goal:

            # Пройден первый уровень
            if current_level == 1:
                SOUND_BG_MUSIC.stop()
                SOUND_SPACE.stop()

                SOUND_LEVEL_COMPLETE.play()

                unlocked_levels = max(unlocked_levels, 2)
                level_complete = True

            # Пройден второй уровень
            elif current_level == 2:
                SOUND_BG_MUSIC.stop()
                SOUND_SPACE.stop()

                SOUND_LEVEL_COMPLETE.play()

                unlocked_levels = max(unlocked_levels, 3)
                level_complete = True

            # Пройден третий уровень
            elif current_level == 3:
                SOUND_BG_MUSIC.stop()
                SOUND_SPACE.stop()

                FINISH_GAME.play()
                game_finished = True

        # ПРОИГРЫШ

        # Если очки меньше 0 или закончились жизни
        if score < 0 or happiness <= 0:
            game_over = True

            SOUND_BG_MUSIC.stop()
            SOUND_GAME_OVER.play()

    # Обновление экрана
    pygame.display.update()

# Завершение игры
pygame.quit()
sys.exit()
