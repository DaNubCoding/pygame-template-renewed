from __future__ import annotations
from src.core import *

class Player(Sprite):
    def __init__(self, scene: MainScene) -> None:
        super().__init__(scene, Layer.DEFAULT)
        self.pos = Vec(0, 0)
        self.image = Images.player
        self.angle = 0
        self.timer = Timer(3)

    def update(self, dt: float) -> None:
        self.pos = self.game.mouse_pos + Vec(50, 50) * self.timer.done
        if self.game.mouse_pressed[0]:
            self.angle += 90 * dt
        else:
            self.angle -= 90 * dt

    def draw(self, screen: pygame.Surface) -> None:
        self.image = pygame.transform.rotate(Images.player, self.angle)
        screen.blit(self.image, self.pos - Vec(self.image.size) / 2)
