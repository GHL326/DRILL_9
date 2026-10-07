"""자동 달리기 예제: 오른쪽 경계에서 IDLE, ESC로 종료."""

import pico2d as pico

from move_character import ASSET_DIR, FRAME_SIZE, HEIGHT, WIDTH, Character


def main():
    pico.open_canvas(WIDTH, HEIGHT)
    background = sheet = None
    try:
        background = pico.load_image(str(ASSET_DIR / "TUK_GROUND.png"))
        sheet = pico.load_image(str(ASSET_DIR / "animation_sheet.png"))
        character = Character()
        character.x = FRAME_SIZE / 2
        last_time = pico.get_time()
        running = True

        while running:
            for event in pico.get_events():
                if event.type == pico.SDL_QUIT:
                    running = False
                elif event.type == pico.SDL_KEYDOWN and event.key == pico.SDLK_ESCAPE:
                    running = False
            if not running:
                break

            now = pico.get_time()
            dt = min(max(now - last_time, 0.0), 0.1)
            last_time = now
            character.update(dt, 1, 0)
            pico.clear_canvas()
            background.draw(WIDTH / 2, HEIGHT / 2, WIDTH, HEIGHT)
            character.draw(sheet)
            pico.update_canvas()
            pico.delay(0.01)
    finally:
        sheet = background = None
        pico.close_canvas()


if __name__ == "__main__":
    main()
