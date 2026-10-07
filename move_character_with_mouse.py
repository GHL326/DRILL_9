"""마우스 이동 예제: 캠퍼스 배경, RUN/IDLE 및 화면 경계."""

import pico2d as pico

from move_character import ASSET_DIR, HEIGHT, WIDTH, Character


def main():
    pico.open_canvas(WIDTH, HEIGHT)
    background = sheet = None
    try:
        pico.hide_cursor()
        background = pico.load_image(str(ASSET_DIR / "TUK_GROUND.png"))
        sheet = pico.load_image(str(ASSET_DIR / "animation_sheet.png"))
        character = Character()
        last_time = pico.get_time()
        running = True

        while running:
            target_x, target_y = character.x, character.y
            for event in pico.get_events():
                if event.type == pico.SDL_QUIT:
                    running = False
                elif event.type == pico.SDL_KEYDOWN and event.key == pico.SDLK_ESCAPE:
                    running = False
                elif event.type == pico.SDL_MOUSEMOTION:
                    target_x, target_y = event.x, HEIGHT - 1 - event.y
            if not running:
                break

            now = pico.get_time()
            dt = min(max(now - last_time, 0.0), 0.1)
            last_time = now
            character.move_to(target_x, target_y, dt)
            pico.clear_canvas()
            background.draw(WIDTH / 2, HEIGHT / 2, WIDTH, HEIGHT)
            character.draw(sheet)
            pico.update_canvas()
            pico.delay(0.01)
    finally:
        sheet = background = None
        pico.show_cursor()
        pico.close_canvas()


if __name__ == "__main__":
    main()
