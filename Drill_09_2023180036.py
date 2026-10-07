from pathlib import Path

from pico2d import *


SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
FRAME_SIZE = 100
FRAME_DELAY = 0.05
MOVE_STEP = 5
ARROW_KEYS = {SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN}
IMAGE_DIR = Path(__file__).resolve().parent

pressed_keys = set()
running = True
x, y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
facing = 1  # 1: 오른쪽, -1: 왼쪽


def handle_events():
    global running
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key in ARROW_KEYS:
                pressed_keys.add(event.key)
        elif event.type == SDL_KEYUP:
            pressed_keys.discard(event.key)


def update():
    global x, y, facing
    dx = (SDLK_RIGHT in pressed_keys) - (SDLK_LEFT in pressed_keys)
    dy = (SDLK_UP in pressed_keys) - (SDLK_DOWN in pressed_keys)
    if dx:
        facing = dx
    x += dx * MOVE_STEP
    y += dy * MOVE_STEP


def draw(background, character):
    clear_canvas()
    background.draw(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                    SCREEN_WIDTH, SCREEN_HEIGHT)
    row = 300 if facing == 1 else 200
    character.clip_draw(0, row, FRAME_SIZE, FRAME_SIZE, x, y)
    update_canvas()


def main():
    open_canvas(SCREEN_WIDTH, SCREEN_HEIGHT)
    try:
        background = load_image(str(IMAGE_DIR / 'TUK_GROUND.png'))
        character = load_image(str(IMAGE_DIR / 'animation_sheet.png'))
        while running:
            handle_events()
            if not running:
                break
            update()
            draw(background, character)
            delay(FRAME_DELAY)
    finally:
        close_canvas()


if __name__ == '__main__':
    main()
