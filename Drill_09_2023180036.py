from pathlib import Path

from pico2d import *


SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
FRAME_SIZE = 100
FRAME_COUNT = 8
FRAME_DELAY = 0.05  # 애니메이션 프레임 간격
FRAME_INTERVAL = 1.0 / 60
MOVE_STEP = 5
MOVE_SPEED = MOVE_STEP / FRAME_DELAY
ARROW_KEYS = {
    SDLK_LEFT: SDL_SCANCODE_LEFT, SDLK_RIGHT: SDL_SCANCODE_RIGHT,
    SDLK_UP: SDL_SCANCODE_UP, SDLK_DOWN: SDL_SCANCODE_DOWN,
}
IMAGE_DIR = Path(__file__).resolve().parent

pressed_keys = set()
running = True
moving = False
frame = 0
animation_time = 0.0
x, y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
facing = 1  # 1: 오른쪽, -1: 왼쪽


def handle_events():
    global running
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

    # 과거 이벤트를 누적하지 않고, 이벤트 처리 후의 현재 키 상태를 읽는다.
    pressed_keys.clear()
    if SDL_GetKeyboardFocus():
        keyboard = SDL_GetKeyboardState(None)
        pressed_keys.update(key for key, scancode in ARROW_KEYS.items()
                            if keyboard[scancode])


def update(delta_time=FRAME_DELAY):
    global x, y, facing, moving, frame, animation_time
    # 창 이동이나 일시 정지 뒤 지난 시간만큼 한꺼번에 이동하지 않는다.
    delta_time = max(0.0, min(delta_time, FRAME_DELAY))
    previous_position = x, y
    dx = (SDLK_RIGHT in pressed_keys) - (SDLK_LEFT in pressed_keys)
    dy = (SDLK_UP in pressed_keys) - (SDLK_DOWN in pressed_keys)
    if dx:
        facing = dx
    distance = MOVE_SPEED * delta_time
    x = clamp(FRAME_SIZE // 2, x + dx * distance,
              SCREEN_WIDTH - FRAME_SIZE // 2)
    y = clamp(FRAME_SIZE // 2, y + dy * distance,
              SCREEN_HEIGHT - FRAME_SIZE // 2)
    moving = (x, y) != previous_position
    animation_time += delta_time
    frame_steps = int((animation_time + 1e-9) / FRAME_DELAY)
    frame = (frame + frame_steps) % FRAME_COUNT
    animation_time = max(0.0, animation_time - frame_steps * FRAME_DELAY)

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
        previous_time = get_time() - FRAME_INTERVAL
        while running:
            frame_start = get_time()
            delta_time = frame_start - previous_time
            previous_time = frame_start
            handle_events()
            if not running:
                break
            update(delta_time)
            draw(background, character)
            delay(max(0.0, FRAME_INTERVAL - (get_time() - frame_start)))
    finally:
        close_canvas()


if __name__ == '__main__':
    main()
