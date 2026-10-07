"""제출 기능의 이동, 상태, 입력 및 종료 동작 검증."""

import unittest
from types import SimpleNamespace
from unittest.mock import patch

import move_character_with_key as game


class CharacterTests(unittest.TestCase):
    def test_four_directions_and_vertical_facing(self):
        for dx, dy in ((-1, 0), (1, 0), (0, 1), (0, -1)):
            with self.subTest(direction=(dx, dy)):
                c = game.Character()
                c.update(0.1, dx, dy)
                self.assertEqual((c.x, c.y), (500 + dx * 10, 400 + dy * 10))
                self.assertEqual(c.action, game.RUN_LEFT if dx < 0 else game.RUN_RIGHT)
        c = game.Character()
        c.update(0.1, -1, 0)
        for dy in (1, -1):
            c.update(0.1, 0, dy)
            self.assertEqual(c.action, game.RUN_LEFT)
        c.update(0.1, 0, 0)
        self.assertEqual(c.action, game.IDLE_LEFT)

    def test_all_edges_and_corners(self):
        for x, y in ((50, 50), (50, 750), (950, 50), (950, 750)):
            for dx, dy in ((-1, 0), (1, 0), (0, 1), (0, -1)):
                with self.subTest(start=(x, y), direction=(dx, dy)):
                    c = game.Character()
                    c.x, c.y = x, y
                    c.update(100, dx, dy)
                    self.assertGreaterEqual(c.x, 50)
                    self.assertLessEqual(c.x, 950)
                    self.assertGreaterEqual(c.y, 50)
                    self.assertLessEqual(c.y, 750)
        for x, y, dx, dy in (
            (50, 400, -1, 0), (950, 400, 1, 0),
            (500, 50, 0, -1), (500, 750, 0, 1),
        ):
            c = game.Character()
            c.x, c.y = x, y
            c.update(0.1, dx, dy)
            self.assertEqual((c.x, c.y), (x, y))
            self.assertIn(c.action, (game.IDLE_LEFT, game.IDLE_RIGHT))
            c.update(0.1, -dx, -dy)
            self.assertIn(c.action, (game.RUN_LEFT, game.RUN_RIGHT))

    def test_idle_run_loop_and_state_reset(self):
        c = game.Character()
        frames = [c.frame]
        for _ in range(8):
            c.update(0.05, 0, 0)
            frames.append(c.frame)
        self.assertEqual(frames, list(range(8)) + [0])
        c.update(0.05, 1, 0)
        self.assertEqual(c.frame, 0)
        frames = [c.frame]
        for _ in range(8):
            c.update(0.05, 1, 0)
            frames.append(c.frame)
        self.assertEqual(frames, list(range(8)) + [0])
        c.update(0.05, -1, 0)
        self.assertEqual((c.action, c.frame), (game.RUN_LEFT, 0))
        c.update(0.05, 0, 0)
        self.assertEqual((c.action, c.frame), (game.IDLE_LEFT, 0))

    def test_time_based_speed(self):
        a, b = game.Character(), game.Character()
        for _ in range(10):
            a.update(0.01, 0, 1)
        b.update(0.1, 0, 1)
        self.assertAlmostEqual(a.y, b.y)

    def test_last_pressed_priority_and_release(self):
        p = game.pico
        keys = []
        events = [
            SimpleNamespace(type=p.SDL_KEYDOWN, key=p.SDLK_LEFT),
            SimpleNamespace(type=p.SDL_KEYDOWN, key=p.SDLK_UP),
            SimpleNamespace(type=p.SDL_KEYDOWN, key=p.SDLK_LEFT),
        ]
        with patch.object(p, "get_events", return_value=events):
            self.assertTrue(game.handle_events(keys))
        self.assertEqual(keys, [p.SDLK_LEFT, p.SDLK_UP])
        self.assertEqual(game.DIRECTIONS[keys[-1]], (0, 1))
        with patch.object(p, "get_events", return_value=[
            SimpleNamespace(type=p.SDL_KEYUP, key=p.SDLK_UP)
        ]):
            self.assertTrue(game.handle_events(keys))
        self.assertEqual(game.DIRECTIONS[keys[-1]], (-1, 0))
        with patch.object(p, "get_events", return_value=[
            SimpleNamespace(type=p.SDL_KEYDOWN, key=p.SDLK_RIGHT)
        ]):
            game.handle_events(keys)
        self.assertEqual(game.DIRECTIONS[keys[-1]], (1, 0))

    def test_escape_and_quit(self):
        for event in (
            SimpleNamespace(type=game.pico.SDL_KEYDOWN, key=game.pico.SDLK_ESCAPE),
            SimpleNamespace(type=game.pico.SDL_QUIT),
        ):
            with patch.object(game.pico, "get_events", return_value=[event]):
                self.assertFalse(game.handle_events([]))


if __name__ == "__main__":
    unittest.main()
