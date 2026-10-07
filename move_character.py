"""Drill 09 제출용: 상하좌우 이동, 방향 유지, RUN/IDLE, 화면 경계."""

from pathlib import Path

import pico2d as pico


WIDTH, HEIGHT = 1000, 800
FRAME_SIZE = 100
FRAME_COUNT = 8
ANIMATION_FPS = 20
MOVE_SPEED = 100
RUN_LEFT, RUN_RIGHT = 0, 1
IDLE_LEFT, IDLE_RIGHT = 2, 3
ASSET_DIR = Path(__file__).resolve().parent
DIRECTIONS = {
    pico.SDLK_LEFT: (-1, 0),
    pico.SDLK_RIGHT: (1, 0),
    pico.SDLK_UP: (0, 1),
    pico.SDLK_DOWN: (0, -1),
}


class Character:
    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.facing = 1
        self.action = IDLE_RIGHT
        self.animation_time = 0.0

    @property
    def frame(self):
        return int(self.animation_time * ANIMATION_FPS + 1e-9) % FRAME_COUNT

    def update(self, dt, dx, dy):
        # 세로 이동은 마지막 좌우 시선을 유지한다.
        if dx:
            self.facing = dx
        self.move_to(
            self.x + dx * MOVE_SPEED * dt,
            self.y + dy * MOVE_SPEED * dt,
            dt,
        )

    def move_to(self, x, y, dt):
        old_x, old_y = self.x, self.y
        half = FRAME_SIZE / 2
        self.x = pico.clamp(half, x, WIDTH - half)
        self.y = pico.clamp(half, y, HEIGHT - half)
        if self.x != old_x:
            self.facing = 1 if self.x > old_x else -1
        moving = self.x != old_x or self.y != old_y
        if moving:
            next_action = RUN_RIGHT if self.facing > 0 else RUN_LEFT
        else:
            next_action = IDLE_RIGHT if self.facing > 0 else IDLE_LEFT

        if next_action != self.action:
            self.action = next_action
            self.animation_time = 0.0
        else:
            self.animation_time = (
                self.animation_time + dt
            ) % (FRAME_COUNT / ANIMATION_FPS)

    def draw(self, sheet):
        sheet.clip_draw(
            self.frame * FRAME_SIZE, self.action * FRAME_SIZE,
            FRAME_SIZE, FRAME_SIZE, self.x, self.y,
        )


def handle_events(pressed_keys):
    """누른 순서를 보존하고 ESC 또는 창 닫기는 False를 반환한다."""
    for event in pico.get_events():
        key = getattr(event, "key", None)
        if event.type == pico.SDL_QUIT:
            return False
        if event.type == pico.SDL_KEYDOWN:
            if key == pico.SDLK_ESCAPE:
                return False
            if key in DIRECTIONS and key not in pressed_keys:
                pressed_keys.append(key)
        elif event.type == pico.SDL_KEYUP and key in pressed_keys:
            pressed_keys.remove(key)
    return True


def main():
    pico.open_canvas(WIDTH, HEIGHT)
    background = sheet = None
    try:
        background = pico.load_image(str(ASSET_DIR / "TUK_GROUND.png"))
        sheet = pico.load_image(str(ASSET_DIR / "animation_sheet.png"))
        character = Character()
        pressed_keys = []
        last_time = pico.get_time()

        while handle_events(pressed_keys):
            now = pico.get_time()
            # 창 이동 등으로 지연되어도 한 번에 크게 뛰지 않도록 제한한다.
            dt = min(max(now - last_time, 0.0), 0.1)
            last_time = now
            dx, dy = DIRECTIONS[pressed_keys[-1]] if pressed_keys else (0, 0)
            character.update(dt, dx, dy)

            pico.clear_canvas()
            background.draw(WIDTH / 2, HEIGHT / 2, WIDTH, HEIGHT)
            character.draw(sheet)
            pico.update_canvas()
            pico.delay(0.01)
    finally:
        # 텍스처를 먼저 해제한 뒤 캔버스를 닫는다.
        sheet = background = None
        pico.close_canvas()


if __name__ == "__main__":
    main()
