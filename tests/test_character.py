"""제출 기능의 이동, 상태, 입력 및 종료 동작 검증."""

import unittest
from types import SimpleNamespace
from unittest.mock import patch

import move_character as game
import move_character_with_key as key_game


class CharacterTests(unittest.TestCase):
    def setUp(self):
        self.game = game

    def test_four_directions_and_vertical_facing(self):
        for dx, dy in ((-1, 0), (1, 0), (0, 1), (0, -1)):
            with self.subTest(direction=(dx, dy)):
                c = self.game.Character()
                c.update(0.1, dx, dy)
                self.assertEqual((c.x, c.y), (500 + dx * 10, 400 + dy * 10))
                self.assertEqual(c.action, self.game.RUN_LEFT if dx < 0 else self.game.RUN_RIGHT)
        c = self.game.Character()
        c.update(0.1, -1, 0)
        for dy in (1, -1):
            c.update(0.1, 0, dy)
            self.assertEqual(c.action, self.game.RUN_LEFT)
        c.update(0.1, 0, 0)
        self.assertEqual(c.action, self.game.IDLE_LEFT)

    def test_all_edges_and_corners(self):
        for x, y in ((50, 50), (50, 750), (950, 50), (950, 750)):
            for dx, dy in ((-1, 0), (1, 0), (0, 1), (0, -1)):
                with self.subTest(start=(x, y), direction=(dx, dy)):
                    c = self.game.Character()
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
            c = self.game.Character()
            c.x, c.y = x, y
            c.update(0.1, dx, dy)
            self.assertEqual((c.x, c.y), (x, y))
            self.assertIn(c.action, (self.game.IDLE_LEFT, self.game.IDLE_RIGHT))
            c.update(0.1, -dx, -dy)
            self.assertIn(c.action, (self.game.RUN_LEFT, self.game.RUN_RIGHT))

    def test_idle_run_loop_and_state_reset(self):
        c = self.game.Character()
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
        self.assertEqual((c.action, c.frame), (self.game.RUN_LEFT, 0))
        c.update(0.05, 0, 0)
        self.assertEqual((c.action, c.frame), (self.game.IDLE_LEFT, 0))

    def test_time_based_speed(self):
        a, b = self.game.Character(), self.game.Character()
        for _ in range(10):
            a.update(0.01, 0, 1)
        b.update(0.1, 0, 1)
        self.assertAlmostEqual(a.y, b.y)

    def test_last_pressed_priority_and_release(self):
        p = self.game.pico
        keys = []
        events = [
            SimpleNamespace(type=p.SDL_KEYDOWN, key=p.SDLK_LEFT),
            SimpleNamespace(type=p.SDL_KEYDOWN, key=p.SDLK_UP),
            SimpleNamespace(type=p.SDL_KEYDOWN, key=p.SDLK_LEFT),
        ]
        with patch.object(p, "get_events", return_value=events):
            self.assertTrue(self.game.handle_events(keys))
        self.assertEqual(keys, [p.SDLK_LEFT, p.SDLK_UP])
        self.assertEqual(self.game.DIRECTIONS[keys[-1]], (0, 1))
        with patch.object(p, "get_events", return_value=[
            SimpleNamespace(type=p.SDL_KEYUP, key=p.SDLK_UP)
        ]):
            self.assertTrue(self.game.handle_events(keys))
        self.assertEqual(self.game.DIRECTIONS[keys[-1]], (-1, 0))
        with patch.object(p, "get_events", return_value=[
            SimpleNamespace(type=p.SDL_KEYDOWN, key=p.SDLK_RIGHT)
        ]):
            self.game.handle_events(keys)
        self.assertEqual(self.game.DIRECTIONS[keys[-1]], (1, 0))

    def test_mouse_target_clamp_and_vertical_facing(self):
        c = self.game.Character()
        c.move_to(-100, 2000, 0.05)
        self.assertEqual((c.x, c.y, c.action), (50, 750, self.game.RUN_LEFT))
        c.move_to(-100, 2000, 0.05)
        self.assertEqual(c.action, self.game.IDLE_LEFT)
        c.move_to(50, 400, 0.05)
        self.assertEqual(c.action, self.game.RUN_LEFT)

    def test_escape_and_quit(self):
        for event in (
            SimpleNamespace(type=self.game.pico.SDL_KEYDOWN, key=self.game.pico.SDLK_ESCAPE),
            SimpleNamespace(type=self.game.pico.SDL_QUIT),
        ):
            with patch.object(self.game.pico, "get_events", return_value=[event]):
                self.assertFalse(self.game.handle_events([]))


class KeyCharacterTests(CharacterTests):
    def setUp(self):
        self.game = key_game


if __name__ == "__main__":
    unittest.main()
