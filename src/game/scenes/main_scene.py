from src.core import *
from src.game.sprites import *

class MainScene(Scene):
    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.player = Player(self)
        self.add(self.player)

    def update(self, dt: float) -> None:
        self.sprite_manager.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill((50, 50, 50))
        screen.blit(Image.get("test"), (0, 0))
        pygame.draw.circle(screen, (255, 0, 0), self.game.mouse_pos, 50)
        self.sprite_manager.draw(screen)
