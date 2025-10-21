import pygame


class Assets:
    player: list[pygame.Surface] = []
    ground: list[pygame.Surface] = []
    gun: list[pygame.Surface] = []
    shot_sound: pygame.mixer.Sound | None = None
    mob_death_sound: pygame.mixer.Sound | None = None
    hearts: list[pygame.Surface] = []
    beetles: list[pygame.Surface] = []
    ground_tiles: list[pygame.Surface] = []
    totem: list[pygame.Surface] = []

    def load(self):
        self.player = self._load_spritesheet("assets/player.png", 32, 32)
        self.gun = self._load_spritesheet("assets/gun.png", 32, 32)
        self.ground = self._load_spritesheet("assets/ground.png", 32, 32)
        self.shot_sound = pygame.mixer.Sound("assets/shot_sound.mp3")
        self.mob_death_sound = pygame.mixer.Sound("assets/mob_death.wav")
        self.hearts = self._load_spritesheet("assets/hearts.png", 16, 16)
        self.beetles = self._load_spritesheet("assets/beetle.png", 32, 32)
        self.ground_tiles = self._load_spritesheet("assets/ground_tiles1.png", 32, 32)
        self.totem = self._load_spritesheet("assets/totem.png", 32, 64)

    def _load_spritesheet(
        self, path: str, tile_w: int, tile_h: int
    ) -> list[pygame.Surface]:
        image = pygame.image.load(path).convert_alpha()
        img_w, img_h = image.get_size()
        tiles: list[pygame.Surface] = []

        for y in range(0, img_h, tile_h):
            for x in range(0, img_w, tile_w):
                rect = pygame.Rect(x, y, tile_w, tile_h)
                tile = image.subsurface(rect).copy()
                tiles.append(tile)

        return tiles
