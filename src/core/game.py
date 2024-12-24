from pygame.locals import SCALED, FULLSCREEN, KEYDOWN, KEYUP, QUIT
from src.core.scene import Scene
from src.game.settings import *
from src.game.scenes import *
from src.core.util import *
from typing import cast
import pygame

class AbortScene(Exception):
    def __str__(self):
        return "Scene aborted but not caught with a try/except block."

class AbortGame(Exception):
    def __str__(self):
        return "Game aborted but not caught with a try/except block."

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.size = self.width, self.height = self.w, self.h = WIDTH, HEIGHT
        self.screen = pygame.display.set_mode(self.size, SCALED | FULLSCREEN * (not Debug.on()))
        self.clock = pygame.time.Clock()

        self.dt = self.clock.tick(0) / 1000
        self.scene = MainScene(self)

    def run(self) -> None:
        while True:
            try:
                self.update()
                if not Debug.paused():
                    self.scene.update(self.dt)
            except AbortScene:
                continue
            except AbortGame:
                break

            self.scene.draw(self.screen)
            Debug.draw(self)
            pygame.display.flip()

            pygame.display.set_caption(f"FPS: {self.clock.get_fps():.0f}")

            self.dt = self.clock.tick(0) / 1000

        pygame.quit()

    def update(self) -> None:
        self.events = {event.type: event for event in pygame.event.get()}
        self.key_down = -1
        if KEYDOWN in self.events:
            self.key_down = cast(pygame.event.Event, self.events[KEYDOWN]).key
        self.key_up = -1
        if KEYUP in self.events:
            self.key_up = cast(pygame.event.Event, self.events[KEYUP]).key

        if QUIT in self.events:
            raise AbortGame

        if KEYDOWN in self.events and Debug.on():
            match self.events[KEYDOWN].key:
                case pygame.K_F1:
                    Debug.toggle_paused()
                case pygame.K_F3:
                    Debug.toggle_visibility()

        Profile.update(self.key_down)

    def change_scene(self, scene: Scene) -> None:
        self.scene = scene
        raise AbortScene
