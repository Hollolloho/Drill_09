from pico2d import *
from pathlib import Path

image_dir = Path(__file__).resolve().parent

open_canvas()
grass = load_image(str(image_dir / 'grass.png'))
character = load_image(str(image_dir / 'animation_sheet.png'))


# fill here

running = True  #루프 컨트롤 변수

def handle_events():
    global running

    events = get_events()
    if events:
        for event in events:
            if event.type == SDL_QUIT:
                running = False

            if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                running = False
    pass


frame = 0
for x in range(0, 800, 5):

    clear_canvas()
    grass.draw(400, 30)
    character.clip_draw(frame * 100, 100, 100, 100, x, 90)
    update_canvas()

    # fill here

    handle_events()
    if not running:
        break

    frame = (frame + 1) % 8
    delay(0.05)


close_canvas()
