from pathlib import Path

from pico2d import *


SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
FRAME_SIZE = 100
FRAME_COUNT = 8
FRAME_DELAY = 0.05
MOVE_STEP = 5
ARROW_KEYS = {SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN}
IMAGE_DIR = Path(__file__).resolve().parent

pressed_keys = set()
running = True
moving = False
frame = 0
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
    global x, y, facing, moving, frame
    previous_position = x, y
    dx = (SDLK_RIGHT in pressed_keys) - (SDLK_LEFT in pressed_keys)
    dy = (SDLK_UP in pressed_keys) - (SDLK_DOWN in pressed_keys)
    if dx:
        facing = dx
    x = clamp(FRAME_SIZE // 2, x + dx * MOVE_STEP,
              SCREEN_WIDTH - FRAME_SIZE // 2)
    y += dy * MOVE_STEP
    moving = (x, y) != previous_position
    frame = (frame + 1) % FRAME_COUNT


def draw(background, character):
    clear_canvas()
    background.draw(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                    SCREEN_WIDTH, SCREEN_HEIGHT)
    row = 100 if facing == 1 else 0
    if not moving:
        row += 200
    character.clip_draw(frame * FRAME_SIZE, row, FRAME_SIZE, FRAME_SIZE, x, y)
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
