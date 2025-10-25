import os
import json
from .map import Map

_here = os.path.dirname(__file__)

with open(os.path.join(_here, "level1.gg")) as f:
    data = json.load(f)  # pyright: ignore[reportAny]
map = Map()
map.tiles = data["map"]
