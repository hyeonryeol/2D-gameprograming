"""Non-interactive check that the pico2d environment is fully working.

Opens the canvas, loads the sample resources, renders a few hundred frames and
closes by itself, so it can be run from a terminal or from CI without anyone
pressing a key.

Run:  python tools/smoke_test.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pico2d import (clear_canvas, close_canvas, get_events, get_time,  # noqa: E402
                    load_image, open_canvas, update_canvas)

import main  # noqa: E402

FRAMES = 180


def run():
    background_path, character_path = main.ensure_resources()
    print('resources ok:', os.path.basename(background_path),
          os.path.basename(character_path))

    open_canvas(main.CANVAS_WIDTH, main.CANVAS_HEIGHT)
    background = load_image(background_path)
    character = main.Character(load_image(character_path))
    font = main.load_ui_font()
    print('canvas ok: %dx%d' % (main.CANVAS_WIDTH, main.CANVAS_HEIGHT))
    print('font ok:', font is not None)

    character.handle_key_down(main.SDLK_RIGHT)
    character.handle_key_down(main.SDLK_SPACE)

    start = get_time()
    last_time = start
    for i in range(FRAMES):
        get_events()
        now = get_time()
        delta_time = min(now - last_time, 0.05)
        last_time = now

        character.update(delta_time)

        clear_canvas()
        background.draw(main.CANVAS_WIDTH // 2, main.CANVAS_HEIGHT // 2)
        character.draw()
        if font is not None:
            font.draw(20, main.CANVAS_HEIGHT - 30, 'smoke test frame %d' % i,
                      (255, 255, 255))
        update_canvas()

    elapsed = get_time() - start
    print('rendered %d frames in %.2fs (%.1f fps)' % (FRAMES, elapsed, FRAMES / elapsed))
    print('character x=%.1f y=%.1f on_ground=%s' % (character.x, character.y,
                                                    character.on_ground))
    close_canvas()
    print('SMOKE TEST PASSED')


if __name__ == '__main__':
    run()
