from src.scenes.main_scene import MainScene
from src.core.scene import Scene
from pygame.locals import *
from src.util import *
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
        self.screen = pygame.display.set_mode((960, 540), SCALED | FULLSCREEN * (not Debug.on()))
        self.clock = pygame.time.Clock()

        self.dt = self.clock.tick(0) / 1000
        self.scene = MainScene(self)

    def run(self) -> None:
        while True:
            try:
                self.update()
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
        self.key_down: int = self.events.get(KEYDOWN).key if KEYDOWN in self.events else -1
        self.key_up: int = self.events.get(KEYUP).key if KEYUP in self.events else -1

        if QUIT in self.events:
            raise AbortGame

        Profiler.update(self.key_down)

    def change_scene(self, scene: Scene) -> None:
        self.scene = scene
