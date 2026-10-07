from pathlib import Path

from pico2d import *


SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
FRAME_SIZE = 100
FRAME_DELAY = 0.05
IMAGE_DIR = Path(__file__).resolve().parent

running = True
x, y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2


def handle_events():
    global running
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


def draw(background, character):
    clear_canvas()
    background.draw(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                    SCREEN_WIDTH, SCREEN_HEIGHT)
    character.clip_draw(0, 300, FRAME_SIZE, FRAME_SIZE, x, y)
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
            draw(background, character)
            delay(FRAME_DELAY)
    finally:
        close_canvas()


if __name__ == '__main__':
    main()
