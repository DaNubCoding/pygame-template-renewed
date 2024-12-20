from src.utils import pathof

import pygame

def load_image(file: str, scale: int = 1) -> pygame.SurfaceType:
    return pygame.transform.scale_by(pygame.image.load(pathof(f"res/images/{file}")).convert_alpha(), scale)

class SpriteSheet(list):
    def __init__(self, path: str, height: int, scale: int = 1) -> None:
        self.image = load_image(path, scale)
        for i in range(self.image.get_height() // height):
            self.append(self.image.subsurface((0, i * height, self.image.get_width(), height)))

pygame.display.set_mode((1, 1), pygame.NOFRAME)

test = load_image("test.png")

pygame.display.quit()
