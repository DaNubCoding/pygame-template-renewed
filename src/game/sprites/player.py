from src.core import *

class Player(Sprite):
    def __init__(self, scene: MainScene) -> None:
        super().__init__(scene, scene.Layer.DEFAULT)
        self.pos = Vec(0, 0)
        self.image = Image.get("player")
        self.angle = 0
        self.timer = LoopTimer(2.5, max_loops=3)

    def update(self, dt: float) -> None:
        self.pos = self.game.mouse_pos + Vec(20, 0) * self.timer.loops
        if self.game.mouse_pressed[0]:
            self.angle += 90 * dt
        else:
            self.angle -= 90 * dt

        if self.game.key_down == pygame.K_SPACE:
            self.timer.toggle()

    def draw(self, screen: pygame.Surface) -> None:
        self.image = pygame.transform.rotate(Image.get("player"), self.angle)
        screen.blit(self.image, self.pos - Vec(self.image.size) / 2)
