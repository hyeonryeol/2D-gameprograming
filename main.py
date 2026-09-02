"""2D Game Programming - LEC00 sample program.

Checks that the whole toolchain works: Python + pico2d + VSCode + Claude Code.

Controls:
    Left / Right arrow  move the character
    Space               jump
    ESC                 quit
"""
import os

from pico2d import (SDLK_ESCAPE, SDLK_LEFT, SDLK_RIGHT, SDLK_SPACE, SDL_KEYDOWN,
                    SDL_KEYUP, SDL_QUIT, clear_canvas, close_canvas, get_events,
                    get_time, load_font, load_image, open_canvas, update_canvas)

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

GROUND_Y = 150          # y of the character's feet when standing
MOVE_SPEED = 260.0      # pixels per second
JUMP_SPEED = 520.0      # initial upward speed, pixels per second
GRAVITY = 1400.0        # pixels per second squared

FRAME_W = 64            # one frame inside res/character.png
FRAME_H = 64
FRAME_COUNT = 4
FRAMES_PER_SECOND = 10

RES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res')


def ensure_resources():
    """Generate res/*.png on first run so the sample never needs a download."""
    background = os.path.join(RES_DIR, 'background.png')
    character = os.path.join(RES_DIR, 'character.png')
    if not (os.path.exists(background) and os.path.exists(character)):
        import runpy
        generator = os.path.join(os.path.dirname(RES_DIR), 'tools', 'make_assets.py')
        runpy.run_path(generator, run_name='__main__')
    return background, character


def load_ui_font(size=20):
    """Use a system font when one is available; text is optional decoration."""
    for path in (r'C:\Windows\Fonts\consola.ttf', r'C:\Windows\Fonts\arial.ttf',
                 '/System/Library/Fonts/Supplemental/Arial.ttf',
                 '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'):
        if os.path.exists(path):
            try:
                return load_font(path, size)
            except Exception:
                pass
    return None


class Character:
    def __init__(self, image):
        self.image = image
        self.x = CANVAS_WIDTH // 2
        self.y = GROUND_Y
        self.dir = 0            # -1 left, 0 idle, +1 right
        self.face = 1           # last non-zero direction
        self.velocity_y = 0.0
        self.on_ground = True
        self.frame_time = 0.0

    def handle_key_down(self, key):
        if key == SDLK_LEFT:
            self.dir -= 1
        elif key == SDLK_RIGHT:
            self.dir += 1
        elif key == SDLK_SPACE and self.on_ground:
            self.velocity_y = JUMP_SPEED
            self.on_ground = False

    def handle_key_up(self, key):
        if key == SDLK_LEFT:
            self.dir += 1
        elif key == SDLK_RIGHT:
            self.dir -= 1

    def update(self, delta_time):
        if self.dir != 0:
            self.face = 1 if self.dir > 0 else -1
        self.x += self.dir * MOVE_SPEED * delta_time

        half = FRAME_W // 2
        self.x = max(half, min(CANVAS_WIDTH - half, self.x))

        if not self.on_ground:
            self.velocity_y -= GRAVITY * delta_time
            self.y += self.velocity_y * delta_time
            if self.y <= GROUND_Y:
                self.y = GROUND_Y
                self.velocity_y = 0.0
                self.on_ground = True

        moving = self.dir != 0 or not self.on_ground
        self.frame_time = self.frame_time + delta_time * FRAMES_PER_SECOND if moving else 0.0

    def draw(self):
        frame = int(self.frame_time) % FRAME_COUNT
        left = frame * FRAME_W
        if self.face >= 0:
            self.image.clip_draw(left, 0, FRAME_W, FRAME_H, self.x, self.y)
        else:
            self.image.clip_composite_draw(left, 0, FRAME_W, FRAME_H,
                                           0, 'h', self.x, self.y)


def main():
    background_path, character_path = ensure_resources()

    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    background = load_image(background_path)
    character = Character(load_image(character_path))
    font = load_ui_font()

    running = True
    last_time = get_time()

    while running:
        for event in get_events():
            if event.type == SDL_QUIT:
                running = False
            elif event.type == SDL_KEYDOWN:
                if event.key == SDLK_ESCAPE:
                    running = False
                else:
                    character.handle_key_down(event.key)
            elif event.type == SDL_KEYUP:
                character.handle_key_up(event.key)

        now = get_time()
        delta_time = min(now - last_time, 0.05)   # clamp so a stall cannot teleport
        last_time = now

        character.update(delta_time)

        clear_canvas()
        background.draw(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)
        character.draw()
        if font is not None:
            font.draw(20, CANVAS_HEIGHT - 30,
                      'pico2d sample - Arrow keys: move, Space: jump, ESC: quit',
                      (255, 255, 255))
        update_canvas()

    close_canvas()


if __name__ == '__main__':
    main()
