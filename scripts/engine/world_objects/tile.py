from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pygame  # type: ignore


class Tile:
    """
    A Tile on the GameMap.

    Attributes:
        x(int): tile_x
        y(int): tile_y
        is_visible(bool): if tile is visible to player
        sprite(pygame.Surface): the sprite of the floor.
    """

    def __init__(self, x: int, y: int, sprite: pygame.Surface, blocks_sight: bool = False, blocks_movement: bool =
    False):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.is_visible = False
        self.blocks_sight = blocks_sight
        self.blocks_movement = blocks_movement



