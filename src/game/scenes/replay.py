from __future__ import annotations
from src.core import *
from src.game.sprites import *

class Replay(Scene):
    def __init__(self, game: Game, timestamp: int) -> None:
        super().__init__(game)
        self.previous_caption = pygame.display.get_caption()
        pygame.display.set_caption(f"{self.previous_caption[0]} - REPLAY")

        self.previous_scene = game.scene
        self.original_timestamp = timestamp
        self.timestamp = timestamp - 1 # The current frame hasn't been snapshot yet
        while self.game.replayer.get_snapshot(self.timestamp) is None:
            self.timestamp -= 1
        self.replay_view = pygame.Surface(SIZE)

        Replayer._start_time = game.time

        # Whether the replay is paused, this acts the same as the pause in game
        # except that this will retain game-based debug information like game.time
        self.paused = False

        Log.info(f"Replay started at timestamp {self.timestamp}.")

    def update(self, dt: float) -> None:
        if pygame.KEYDOWN in self.game.events:
            match self.game.events[pygame.KEYDOWN].key:
                case pygame.K_ESCAPE:
                    self.quit()
                case pygame.K_F1 | pygame.K_SPACE:
                    self.pause()
                case pygame.K_LEFT:
                    self.seek_previous_snapshot()
                case pygame.K_RIGHT:
                    self.seek_next_snapshot()
                case pygame.K_PERIOD:
                    self.step_forward()

        self.update_replay()
        if not self.paused:
            self.timestamp += 1

        self.sprite_manager.update(dt)

    def update_replay(self) -> None:
        try:
            self.frame = self.game.replayer.get_frame(self.timestamp)
        except KeyError:
            self.paused = True

        scene = self.frame.apply()
        if scene is not None:
            self.replay_scene = scene
        if not self.paused:
            self.replay_scene.update(self.frame.dt)
        self.replay_scene.draw(self.replay_view)

    def step_forward(self) -> None:
        self.timestamp += 1
        if self.timestamp > self.game.replayer.newest_frame:
            self.timestamp = self.game.replayer.newest_frame
            return

        frame = self.game.replayer.get_frame(self.timestamp)
        if frame is None:
            self.paused = True
        else:
            self.frame = frame
        scene = self.frame.apply()
        if scene is not None:
            self.replay_scene = scene
        self.replay_scene.update(self.frame.dt)
        self.replay_scene.draw(self.replay_view)

    def seek_previous_snapshot(self) -> None:
        self.timestamp -= 1
        try:
            while self.game.replayer.get_snapshot(self.timestamp) is None:
                self.timestamp -= 1
                if self.timestamp < 0:
                    self.timestamp = 0
                    break
        except KeyError:
            self.timestamp = 0
        self.update_replay()
        self.paused = True

    def seek_next_snapshot(self) -> None:
        self.timestamp += 1
        while self.game.replayer.get_snapshot(self.timestamp) is None:
            self.timestamp += 1
            if self.timestamp > self.game.replayer.newest_frame:
                self.seek_previous_snapshot()
                return
        self.update_replay()
        self.paused = True

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.replay_view, (0, 0))

        self.sprite_manager.draw(screen)

    def pause(self) -> None:
        self.paused = not self.paused

    def quit(self) -> None:
        self.game.replaying = False
        pygame.display.set_caption(*self.previous_caption)
        self.game.replayer.snapshot_timer.force_end()
        Replayer._time += self.game.time - Replayer._start_time
        self.game.timestamp = self.original_timestamp
        self.game.set_scene(self.previous_scene)
