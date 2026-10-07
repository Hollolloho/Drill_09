"""실행: python test_drill_09.py"""
from types import SimpleNamespace
from unittest.mock import patch

import Drill_09_2023180036 as game


def send_event(event_type, key=None):
    original = game.get_events
    try:
        game.get_events = lambda: [SimpleNamespace(type=event_type, key=key)]
        game.handle_events()
    finally:
        game.get_events = original


def check():
    for key, offset in [(game.SDLK_RIGHT, (5, 0)),
                        (game.SDLK_LEFT, (-5, 0)),
                        (game.SDLK_UP, (0, 5)),
                        (game.SDLK_DOWN, (0, -5))]:
        game.x, game.y = 600, 400
        game.pressed_keys.clear()
        send_event(game.SDL_KEYDOWN, key)
        send_event(game.SDL_KEYDOWN, key)
        game.update()
        assert (game.x, game.y) == (600 + offset[0], 400 + offset[1])
        send_event(game.SDL_KEYUP, key)
        game.update()
        assert (game.x, game.y) == (600 + offset[0], 400 + offset[1])

    game.x, game.y = 600, 400
    send_event(game.SDL_KEYDOWN, game.SDLK_LEFT)
    send_event(game.SDL_KEYDOWN, game.SDLK_RIGHT)
    game.update()
    assert (game.x, game.y) == (600, 400)
    send_event(game.SDL_KEYDOWN, game.SDLK_UP)
    send_event(game.SDL_KEYUP, game.SDLK_LEFT)
    game.update()
    assert (game.x, game.y) == (605, 405)
    game.pressed_keys.clear()

    for horizontal, expected in [(game.SDLK_LEFT, -1), (game.SDLK_RIGHT, 1)]:
        game.pressed_keys = {horizontal}
        game.update()
        assert game.facing == expected
        for vertical in (game.SDLK_UP, game.SDLK_DOWN):
            game.pressed_keys = {vertical}
            game.update()
            assert game.facing == expected
        game.pressed_keys.clear()
        game.update()
        assert game.facing == expected

    game.pressed_keys.clear()
    game.frame = 0
    frames = []
    for _ in range(8):
        game.update()
        frames.append(game.frame)
        assert not game.moving
    assert frames == [1, 2, 3, 4, 5, 6, 7, 0]

    game.pressed_keys = {game.SDLK_UP}
    game.update()
    assert game.moving
    game.pressed_keys.clear()
    game.update()
    assert not game.moving

    background = SimpleNamespace(draw=lambda *args: None)
    calls = []
    character = SimpleNamespace(clip_draw=lambda *args: calls.append(args))
    with patch.object(game, 'clear_canvas'), patch.object(game, 'update_canvas'):
        for moving, facing, row in [(True, -1, 0), (True, 1, 100),
                                   (False, -1, 200), (False, 1, 300)]:
            game.moving, game.facing = moving, facing
            game.draw(background, character)
            assert calls[-1][:4] == (game.frame * 100, row, 100, 100)

    for key, start, expected in [
        (game.SDLK_LEFT, (51, 400), (50, 400)),
        (game.SDLK_RIGHT, (1149, 400), (1150, 400)),
        (game.SDLK_DOWN, (600, 51), (600, 50)),
        (game.SDLK_UP, (600, 749), (600, 750)),
    ]:
        game.x, game.y = start
        game.pressed_keys = {key}
        game.update()
        assert (game.x, game.y) == expected and game.moving
        game.update()
        assert (game.x, game.y) == expected and not game.moving

    for horizontal, edge_x, inward_x in [(game.SDLK_LEFT, 50, game.SDLK_RIGHT),
                                         (game.SDLK_RIGHT, 1150, game.SDLK_LEFT)]:
        for vertical, edge_y, inward_y in [(game.SDLK_DOWN, 50, game.SDLK_UP),
                                          (game.SDLK_UP, 750, game.SDLK_DOWN)]:
            game.x, game.y = edge_x, edge_y
            game.pressed_keys = {horizontal, vertical}
            for _ in range(10):
                game.update()
                assert (game.x, game.y) == (edge_x, edge_y) and not game.moving
            game.pressed_keys = {inward_x, inward_y}
            game.update()
            assert 50 < game.x < 1150 and 50 < game.y < 750 and game.moving

    game.x, game.y = 50, 400
    game.pressed_keys = {game.SDLK_LEFT, game.SDLK_UP}
    game.update()
    assert (game.x, game.y) == (50, 405) and game.moving

    game.running = True
    send_event(game.SDL_KEYDOWN, game.SDLK_ESCAPE)
    assert not game.running
    game.running = True
    send_event(game.SDL_QUIT)
    assert not game.running
    print('PASS: input, facing, animation, four edges, four corners, edge sliding, exit')


if __name__ == '__main__':
    check()
