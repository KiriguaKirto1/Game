import os
import sys
import pygame
import zipfile

pygame.init()

WIDTH, HEIGHT = 960, 540
FPS = 60

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aventura Pixel")
CLOCK = pygame.time.Clock()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp")

PLAYER_HEIGHT = 88
ENEMY_HEIGHT = 62
SPIKE_HEIGHT = 42
DECOR_HEIGHT = 76
FLAG_HEIGHT = 105
PLATFORM_HEIGHT = 64

GRAVITY = 0.65
PLAYER_SPEED = 4.6
PLAYER_JUMP_FORCE = -13.5

BLACK = (15, 15, 20)
WHITE = (255, 255, 255)


def error(message):
    # print(f"[ERRO] {message}")  # Silenced for cleaner console
    pass


def asset_path(*parts):
    return os.path.join(ASSETS_DIR, *parts)


def folder_exists(folder):
    if not os.path.isdir(folder):
        error(f"Pasta não encontrada: {folder}")
        return False
    return True


def file_exists(file_path):
    if not os.path.isfile(file_path):
        error(f"Arquivo não encontrado: {file_path}")
        return False
    return True


def list_images(folder):
    if not folder_exists(folder):
        return []

    files = [
        os.path.join(folder, file)
        for file in sorted(os.listdir(folder))
        if file.lower().endswith(IMAGE_EXTENSIONS)
    ]

    if not files:
        error(f"Nenhuma imagem encontrada em: {folder}")

    return files


def find_first_image(folder):
    images = list_images(folder)
    return images[0] if images else None


def find_image_by_names(folder, possible_names):
    if not folder_exists(folder):
        return None

    files = os.listdir(folder)

    for name in possible_names:
        for file in files:
            base, ext = os.path.splitext(file)
            if base.lower() == name.lower() and ext.lower() in IMAGE_EXTENSIONS:
                return os.path.join(folder, file)

    for file in files:
        if file.lower().endswith(IMAGE_EXTENSIONS):
            return os.path.join(folder, file)

    error(f"Nenhuma imagem encontrada em: {folder}")
    return None


def load_image(file_path, width=None, height=None):
    if not file_exists(file_path):
        surface = pygame.Surface((50, 50), pygame.SRCALPHA)
        surface.fill((255, 0, 255, 180))
        return surface

    image = pygame.image.load(file_path).convert_alpha()

    if width is not None or height is not None:
        original_w, original_h = image.get_size()

        if width is None:
            scale = height / original_h
            width = int(original_w * scale)

        if height is None:
            scale = width / original_w
            height = int(original_h * scale)

        image = pygame.transform.smoothscale(image, (int(width), int(height)))

    return image


def load_frames(folder, height, fallback_folder=None):
    files = list_images(folder)

    if not files and fallback_folder:
        files = list_images(fallback_folder)

    frames = [load_image(file, height=height) for file in files]

    if not frames:
        surface = pygame.Surface((50, height), pygame.SRCALPHA)
        surface.fill((255, 0, 255, 180))
        frames = [surface]

    return frames


def flip_frames(frames):
    return [pygame.transform.flip(frame, True, False) for frame in frames]


def scale_background(image, target_width, target_height):
    img_w, img_h = image.get_size()
    scale = max(target_width / img_w, target_height / img_h)

    new_w = int(img_w * scale)
    new_h = int(img_h * scale)

    image = pygame.transform.smoothscale(image, (new_w, new_h))

    cropped = pygame.Surface((target_width, target_height)).convert()
    cropped.blit(image, ((target_width - new_w) // 2, (target_height - new_h) // 2))

    return cropped


class Animation:
    def __init__(self, frames, frame_duration=140, loop=True):
        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop
        self.current_frame = 0
        self.timer = 0
        self.finished = False

    def reset(self):
        self.current_frame = 0
        self.timer = 0
        self.finished = False

    def update(self, dt):
        if self.finished or len(self.frames) <= 1:
            return

        self.timer += dt

        while self.timer >= self.frame_duration:
            self.timer -= self.frame_duration
            self.current_frame += 1

            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.finished = True
                    break

    def image(self):
        return self.frames[self.current_frame]


class Camera:
    def __init__(self, world_width):
        self.x = 0
        self.world_width = world_width

    def update(self, target):
        desired_x = target.centerx - WIDTH // 2
        self.x += (desired_x - self.x) * 0.08
        self.x = max(0, min(self.x, self.world_width - WIDTH))

    def apply_rect(self, rect):
        return rect.move(-int(self.x), 0)

    def apply_pos(self, x, y):
        return x - int(self.x), y


class Platform:
    def __init__(self, x, y, width, image):
        self.image = image
        self.tile_width = image.get_width()
        self.tile_height = image.get_height()
        self.rect = pygame.Rect(x, y, width, self.tile_height)

        self.hitbox = pygame.Rect(
            x,
            y + int(self.tile_height * 0.18),
            width,
            int(self.tile_height * 0.58),
        )

    def draw(self, surface, camera):
        draw_rect = camera.apply_rect(self.rect)
        start_x = draw_rect.left

        while start_x < draw_rect.right:
            surface.blit(self.image, (start_x, draw_rect.y))
            start_x += self.tile_width


class Decoration:
    def __init__(self, x, ground_y, image):
        self.image = image
        self.rect = self.image.get_rect(midbottom=(x, ground_y))

    def draw(self, surface, camera):
        surface.blit(self.image, camera.apply_rect(self.rect))


class Hazard:
    def __init__(self, x, ground_y, image):
        self.image = image
        self.rect = self.image.get_rect(midbottom=(x, ground_y))

        self.hitbox = self.rect.inflate(
            -int(self.rect.width * 0.35),
            -int(self.rect.height * 0.45),
        )

        self.hitbox.y += int(self.rect.height * 0.12)

    def draw(self, surface, camera):
        surface.blit(self.image, camera.apply_rect(self.rect))


class Player:
    def __init__(self, x, y):
        self.animations_right = {
            "idle": Animation(
                load_frames(asset_path("player", "idle"), PLAYER_HEIGHT),
                frame_duration=220,
                loop=True,
            ),
            "run": Animation(
                load_frames(asset_path("player", "run"), PLAYER_HEIGHT),
                frame_duration=165,
                loop=True,
            ),
            "jump": Animation(
                load_frames(
                    asset_path("player", "jump"),
                    PLAYER_HEIGHT,
                    fallback_folder=asset_path("player", "idle"),
                ),
                frame_duration=220,
                loop=True,
            ),
            "hurt": Animation(
                load_frames(
                    asset_path("player", "hurt"),
                    PLAYER_HEIGHT,
                    fallback_folder=asset_path("player", "idle"),
                ),
                frame_duration=160,
                loop=False,
            ),
        }

        self.animations_left = {
            name: Animation(
                flip_frames(animation.frames),
                frame_duration=animation.frame_duration,
                loop=animation.loop,
            )
            for name, animation in self.animations_right.items()
        }

        self.state = "idle"
        self.facing = 1

        self.rect = pygame.Rect(x, y, 36, 76)
        self.velocity = pygame.Vector2(0, 0)

        self.on_ground = False
        self.lives = 3
        self.invincible_timer = 0
        self.dead = False

    def animation_set(self):
        return self.animations_right if self.facing == 1 else self.animations_left

    def current_animation(self):
        return self.animation_set()[self.state]

    def set_state(self, new_state):
        if new_state != self.state:
            self.state = new_state
            self.current_animation().reset()

    def hurt(self):
        if self.dead or self.invincible_timer > 0:
            return

        self.lives -= 1
        
        # Respawn on hurt
        self.rect.topleft = (80, 260)
        self.velocity = pygame.Vector2(0, 0)
        
        self.invincible_timer = 1000
        self.velocity.y = -8
        self.set_state("hurt")

        if self.lives <= 0:
            self.dead = True

    def update(self, dt, keys, platforms):
        if self.invincible_timer > 0:
            self.invincible_timer -= dt

        if not self.dead:
            direction = 0

            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                direction -= 1

            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                direction += 1

            self.velocity.x = direction * PLAYER_SPEED

            if direction != 0:
                self.facing = 1 if direction > 0 else -1

            jump_pressed = (
                keys[pygame.K_SPACE]
                or keys[pygame.K_w]
                or keys[pygame.K_UP]
            )

            if jump_pressed and self.on_ground:
                self.velocity.y = PLAYER_JUMP_FORCE
                self.on_ground = False
        else:
            self.velocity.x = 0

        self.velocity.y += GRAVITY
        self.velocity.y = min(self.velocity.y, 15)

        self.rect.x += int(self.velocity.x)
        self.collide(platforms, axis="x")

        self.rect.y += int(self.velocity.y)
        self.on_ground = False
        self.collide(platforms, axis="y")

        if self.rect.top > HEIGHT + 300:
            self.hurt()
            self.rect.topleft = (80, 260)
            self.velocity.update(0, 0)

        if self.dead:
            self.set_state("hurt")
        elif self.invincible_timer > 700:
            self.set_state("hurt")
        elif not self.on_ground:
            self.set_state("jump")
        elif abs(self.velocity.x) > 0.1:
            self.set_state("run")
        else:
            self.set_state("idle")

        self.current_animation().update(dt)

    def collide(self, platforms, axis):
        for platform in platforms:
            if self.rect.colliderect(platform.hitbox):
                if axis == "x":
                    if self.velocity.x > 0:
                        self.rect.right = platform.hitbox.left
                    elif self.velocity.x < 0:
                        self.rect.left = platform.hitbox.right

                elif axis == "y":
                    if self.velocity.y > 0:
                        self.rect.bottom = platform.hitbox.top
                        self.velocity.y = 0
                        self.on_ground = True

                    elif self.velocity.y < 0:
                        self.rect.top = platform.hitbox.bottom
                        self.velocity.y = 0

    def draw(self, surface, camera):
        if self.invincible_timer > 0 and int(self.invincible_timer / 90) % 2 == 0:
            return

        image = self.current_animation().image()
        draw_rect = image.get_rect(midbottom=(self.rect.centerx, self.rect.bottom + 4))
        surface.blit(image, camera.apply_rect(draw_rect))


class Enemy:
    def __init__(self, x, ground_y, left_limit, right_limit):
        self.walk_right = load_frames(asset_path("enemy", "walk"), ENEMY_HEIGHT)
        self.walk_left = flip_frames(self.walk_right)

        hurt_folder = asset_path("enemy", "hurt")
        self.hurt_frames = load_frames(
            hurt_folder,
            ENEMY_HEIGHT,
            fallback_folder=asset_path("enemy", "walk"),
        )

        self.walk_animation = Animation(self.walk_left, frame_duration=170, loop=True)
        self.death_animation = Animation(self.hurt_frames, frame_duration=180, loop=False)

        self.rect = pygame.Rect(0, 0, 48, 44)
        self.rect.midbottom = (x, ground_y)

        self.left_limit = left_limit
        self.right_limit = right_limit

        self.direction = -1
        self.speed = 1.25

        self.alive = True
        self.remove = False

    def stomp(self):
        if not self.alive:
            return

        self.alive = False
        self.death_animation.reset()

    def update(self, dt):
        if not self.alive:
            self.death_animation.update(dt)

            if self.death_animation.finished:
                self.remove = True

            return

        self.rect.x += int(self.direction * self.speed)

        if self.rect.left <= self.left_limit:
            self.rect.left = self.left_limit
            self.direction = 1

        elif self.rect.right >= self.right_limit:
            self.rect.right = self.right_limit
            self.direction = -1

        self.walk_animation.frames = self.walk_right if self.direction == 1 else self.walk_left
        self.walk_animation.update(dt)

    def draw(self, surface, camera):
        image = self.death_animation.image() if not self.alive else self.walk_animation.image()
        draw_rect = image.get_rect(midbottom=(self.rect.centerx, self.rect.bottom + 6))
        surface.blit(image, camera.apply_rect(draw_rect))


class Game:
    def __init__(self):
        self.world_width = 2600
        self.camera = Camera(self.world_width)

        self.font = pygame.font.SysFont("arial", 19, bold=True)
        self.big_font = pygame.font.SysFont("arial", 54, bold=True)

        # Auto-unpack assets if incomplete
        if os.path.exists('assets.zip'):
            idle_dir = asset_path('player', 'idle')
            if not os.path.exists(idle_dir) or not os.listdir(idle_dir):
                print("Unpacking assets.zip...")
                with zipfile.ZipFile('assets.zip', 'r') as zf:
                    zf.extractall('.')
                print("Assets unpacked!")

        self.load_assets()
        self.reset()

    def load_assets(self):
        # Procedural gradient sky background (no missing folder error)
        self.background = pygame.Surface((WIDTH, HEIGHT)).convert()
        for y in range(HEIGHT):
            r = max(50, 120 - y // 4)
            g = max(140, 190 - y // 5)
            b = max(200, 255 - y // 6)
            color = (r, g, b)
            pygame.draw.line(self.background, color, (0, y), (WIDTH, y))

        platform_file = find_image_by_names(
            asset_path("platforms"),
            [
                "grass_large",
                "grass",
                "platform",
                "ground",
                "tile",
            ],
        )

        self.platform_image = load_image(platform_file, height=PLATFORM_HEIGHT)

        spike_file = find_image_by_names(
            asset_path("objects"),
            [
                "spikes_small",
                "spikes",
                "spike",
                "espinho",
            ],
        )

        flag_file = find_image_by_names(
            asset_path("objects"),
            [
                "flag",
                "bandeira",
                "finish",
            ],
        )

        cactus_file = find_image_by_names(
            asset_path("objects"),
            [
                "cactus",
                "cacto",
            ],
        )

        rock_file = find_image_by_names(
            asset_path("objects"),
            [
                "rock",
                "pedra",
                "stone",
            ],
        )

        box_file = find_image_by_names(
            asset_path("objects"),
            [
                "wood_box",
                "box",
                "caixa",
            ],
        )

        self.spike_image = load_image(spike_file, height=SPIKE_HEIGHT)
        self.flag_image = load_image(flag_file, height=FLAG_HEIGHT)
        self.cactus_image = load_image(cactus_file, height=DECOR_HEIGHT)
        self.rock_image = load_image(rock_file, height=58)
        self.box_image = load_image(box_file, height=54)

    def reset(self):
        ground_y = 454

        self.player = Player(90, 260)
        self.player.lives = 3

        self.platforms = [
            Platform(0, ground_y, 620, self.platform_image),
            Platform(720, ground_y, 640, self.platform_image),
            Platform(1460, ground_y, 520, self.platform_image),
            Platform(2060, ground_y, 540, self.platform_image),

            Platform(520, 340, 240, self.platform_image),
            Platform(1080, 325, 240, self.platform_image),
            Platform(1690, 330, 260, self.platform_image),
        ]

        self.hazards = [
            Hazard(670, ground_y, self.spike_image),
            Hazard(1410, ground_y, self.spike_image),
            Hazard(2025, ground_y, self.spike_image),
        ]

        self.decorations = [
            Decoration(250, ground_y, self.cactus_image),
            Decoration(930, ground_y, self.rock_image),
            Decoration(1550, ground_y, self.box_image),
        ]

        self.enemies = [
            Enemy(950, ground_y, 780, 1280),
            Enemy(1725, ground_y, 1500, 1940),
            Enemy(2260, ground_y, 2100, 2520),
        ]

        self.flag = Decoration(2520, ground_y, self.flag_image)

        self.won = False

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_r]:
            self.reset()
            return

        if self.won or self.player.dead:
            return

        self.player.update(dt, keys, self.platforms)

        for enemy in self.enemies:
            enemy.update(dt)

            if enemy.alive and self.player.rect.colliderect(enemy.rect):
                player_is_falling = self.player.velocity.y > 1
                player_above_enemy = self.player.rect.bottom <= enemy.rect.centery + 18

                if player_is_falling and player_above_enemy:
                    enemy.stomp()
                    self.player.velocity.y = -9.5
                else:
                    self.player.hurt()

        self.enemies = [enemy for enemy in self.enemies if not enemy.remove]

        for hazard in self.hazards:
            if self.player.rect.colliderect(hazard.hitbox):
                self.player.hurt()

        if self.player.rect.colliderect(self.flag.rect.inflate(-25, -15)):
            self.won = True

        self.camera.update(self.player.rect)

    def draw_hud(self):
        text = self.font.render(
            f"Vidas: {self.player.lives}   A/D ou setas: mover   Espaço: pular   R: reiniciar",
            True,
            BLACK,
        )

        bg = pygame.Rect(12, 10, text.get_width() + 18, text.get_height() + 10)
        pygame.draw.rect(SCREEN, (255, 255, 255), bg, border_radius=8)
        pygame.draw.rect(SCREEN, BLACK, bg, 2, border_radius=8)

        SCREEN.blit(text, (21, 15))

    def draw_center_message(self, title, subtitle):
        box = pygame.Rect(0, 0, 620, 150)
        box.center = (WIDTH // 2, HEIGHT // 2)

        pygame.draw.rect(SCREEN, WHITE, box, border_radius=18)
        pygame.draw.rect(SCREEN, BLACK, box, 4, border_radius=18)

        title_surface = self.big_font.render(title, True, BLACK)
        subtitle_surface = self.font.render(subtitle, True, BLACK)

        SCREEN.blit(
            title_surface,
            title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30)),
        )

        SCREEN.blit(
            subtitle_surface,
            subtitle_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 35)),
        )

    def draw(self):
        SCREEN.blit(self.background, (0, 0))

        for decoration in self.decorations:
            decoration.draw(SCREEN, self.camera)

        self.flag.draw(SCREEN, self.camera)

        for platform in self.platforms:
            platform.draw(SCREEN, self.camera)

        for hazard in self.hazards:
            hazard.draw(SCREEN, self.camera)

        for enemy in self.enemies:
            enemy.draw(SCREEN, self.camera)

        self.player.draw(SCREEN, self.camera)

        self.draw_hud()

        if self.won:
            self.draw_center_message("VOCÊ VENCEU!", "Pressione R para jogar novamente")

        elif self.player.dead:
            self.draw_center_message("FIM DE JOGO", "Pressione R para reiniciar")

        pygame.display.flip()

    def run(self):
        while True:
            dt = CLOCK.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()

            self.update(dt)
            self.draw()


if __name__ == "__main__":
    Game().run()