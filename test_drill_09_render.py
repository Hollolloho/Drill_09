"""실행: python test_drill_09_render.py [--portable | --capture 폴더]"""
import ctypes
import hashlib
import os
from pathlib import Path
import sys

# 실제 SDL 이벤트 큐와 렌더링을 검사하고 현재 키 상태는 명시적으로 모의한다.
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import Drill_09_2023180036 as game
import pico2d.pico2d as pico
from sdl2 import (SDL_CreateRenderer, SDL_CreateRGBSurfaceWithFormat, SDL_Event,
                  SDL_FreeSurface, SDL_GetRendererOutputSize, SDL_KEYDOWN, SDL_KEYUP,
                  SDL_PIXELFORMAT_RGBA32, SDL_PushEvent, SDL_RENDERER_SOFTWARE,
                  SDL_RenderReadPixels)
from sdl2.sdlimage import IMG_SavePNG


def check(capture_dir=None):
    steps = [
        (set(), (600, 400), 1, False, 'idle_right'),
        (set(), (600, 400), 1, False, 'idle_right_next'),
        ({game.SDLK_RIGHT}, (605, 400), 1, True, 'run_right'),
        ({game.SDLK_RIGHT}, (610, 400), 1, True, 'run_right_next'),
        ({game.SDLK_UP}, (610, 405), 1, True, 'up_right'),
        ({game.SDLK_LEFT}, (605, 405), -1, True, 'run_left'),
        ({game.SDLK_UP}, (605, 410), -1, True, 'up_left'),
        (set(), (605, 410), -1, False, 'idle_left'),
        (set(), (605, 410), -1, False, 'idle_left_next'),
        ({game.SDLK_LEFT, game.SDLK_DOWN}, (50, 50), -1, True, 'corner'),
        ({game.SDLK_LEFT, game.SDLK_DOWN}, (50, 50), -1, False, 'corner_idle'),
        ({game.SDLK_RIGHT, game.SDLK_UP}, (55, 55), 1, True, 'corner_return'),
    ]
    index = 0
    held_keys = set()
    keyboard_state = (ctypes.c_uint8 * 512)()
    digests = []
    original_open, original_draw, original_delay = game.open_canvas, game.draw, game.delay
    original_keyboard, original_focus = game.SDL_GetKeyboardState, game.SDL_GetKeyboardFocus

    def push_key(event_type, key):
        event = SDL_Event()
        event.type = event_type
        event.key.keysym.sym = key
        assert SDL_PushEvent(ctypes.byref(event)) == 1

    def queue_keys(keys):
        nonlocal held_keys
        for key in held_keys - keys:
            push_key(SDL_KEYUP, key)
        for key in keys - held_keys:
            push_key(SDL_KEYDOWN, key)
        held_keys = keys
        for key, scancode in game.ARROW_KEYS.items():
            keyboard_state[scancode] = key in keys

    def software_canvas(*args):
        original_open(*args)
        # pico2d의 dummy 드라이버에서 null 포인터를 놓치는 경우를 보완한다.
        if not pico.renderer:
            pico.renderer = SDL_CreateRenderer(pico.window, -1, SDL_RENDERER_SOFTWARE)
        assert pico.renderer
        queue_keys(steps[0][0])

    def checked_draw(background, character):
        nonlocal index
        _, position, facing, moving, name = steps[index]
        assert (game.x, game.y) == position, (name, game.x, game.y)
        assert game.facing == facing and game.moving == moving, name
        assert game.frame == (index + 1) % game.FRAME_COUNT
        original_draw(background, character)
        width, height = ctypes.c_int(), ctypes.c_int()
        assert SDL_GetRendererOutputSize(pico.renderer, ctypes.byref(width),
                                        ctypes.byref(height)) == 0
        assert (width.value, height.value) == (1200, 800)
        surface = SDL_CreateRGBSurfaceWithFormat(0, 1200, 800, 32, SDL_PIXELFORMAT_RGBA32)
        assert surface
        try:
            assert SDL_RenderReadPixels(pico.renderer, None, SDL_PIXELFORMAT_RGBA32,
                                       surface.contents.pixels, surface.contents.pitch) == 0
            pixels = ctypes.string_at(surface.contents.pixels, surface.contents.pitch * 800)
            digests.append(hashlib.sha256(pixels).digest())
            if capture_dir:
                path = capture_dir / (name + '.png')
                assert IMG_SavePNG(surface, str(path).encode('utf8')) == 0
        finally:
            SDL_FreeSurface(surface)
        index += 1

    def next_step(seconds):
        if index == len(steps):
            push_key(SDL_KEYDOWN, game.SDLK_ESCAPE)
        else:
            if index == 9:
                game.x, game.y = 51, 51
            queue_keys(steps[index][0])

    if capture_dir:
        capture_dir.mkdir(parents=True, exist_ok=True)
    game.running, game.frame = True, 0
    game.x, game.y, game.facing, game.moving = 600, 400, 1, False
    game.pressed_keys.clear()
    game.open_canvas, game.draw, game.delay = software_canvas, checked_draw, next_step
    game.SDL_GetKeyboardState = lambda count: keyboard_state
    game.SDL_GetKeyboardFocus = lambda: True
    try:
        game.main()
    finally:
        game.open_canvas, game.draw, game.delay = original_open, original_draw, original_delay
        game.SDL_GetKeyboardState, game.SDL_GetKeyboardFocus = original_keyboard, original_focus
    assert index == len(steps) and not game.running
    assert digests[0] != digests[1], 'Right IDLE frames must render differently'
    assert digests[7] != digests[8], 'Left IDLE frames must render differently'
    print('PASS: SDL event queue, simulated key state, rendered animation, movement, corner, ESC')



def check_portability():
    import shutil
    import subprocess
    import tempfile

    temp_base = Path(tempfile.gettempdir()).resolve()
    with tempfile.TemporaryDirectory(prefix='drill09-', dir=temp_base) as directory:
        temporary = Path(directory).resolve()
        assert temporary.parent == temp_base
        project = temporary / '옮긴 프로젝트'
        working = temporary / '다른 작업 폴더'
        project.mkdir()
        working.mkdir()
        for name in ('Drill_09_2023180036.py', 'animation_sheet.png',
                     'TUK_GROUND.png', Path(__file__).name):
            shutil.copy2(game.IMAGE_DIR / name, project / name)
        subprocess.run([sys.executable, str(project / Path(__file__).name)],
                       cwd=working, check=True)
    print('PASS: relocated project, Korean path with spaces, alternate working directory')

if __name__ == '__main__':
    capture_dir = Path(sys.argv[2]).resolve() if len(sys.argv) == 3 and sys.argv[1] == '--capture' else None
    check(capture_dir)
    if '--portable' in sys.argv:
        check_portability()
