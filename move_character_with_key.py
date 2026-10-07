from pico2d import *
from pathlib import Path

image_dir = Path(__file__).resolve().parent

open_canvas()
grass = load_image(str(image_dir / 'grass.png'))
character = load_image(str(image_dir / 'animation_sheet.png'))

def handle_events():
    global running, dir
    global x
    # fill here

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        # fill here
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                dir += 1
            elif event.key == SDLK_LEFT:
                dir -= 1
            elif event.key == SDLK_ESCAPE:
                running = False

        if event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dir -= 1
            elif event.key == SDLK_LEFT:
                dir += 1


running = True
x = 800 // 2
frame = 0
dir = 0

# fill here
while running:
    clear_canvas()
    grass.draw(400, 30)
    character.clip_draw(frame * 100, 100, 100, 100, x, 90)
    update_canvas()

    handle_events()

    frame = (frame + 1) % 8
    x += dir * 5
    delay(0.05)

close_canvas()

