from __future__ import annotations

import logging
import esper

from typing import TYPE_CHECKING
from scripts.managers.world_manager.entity_methods import EntityMethods
from scripts.managers.world_manager.fov_methods import FOVMethods
from scripts.managers.world_manager.map_methods import MapMethods
from scripts.managers.world_manager.skill_methods import SkillMethods
from scripts.managers.world_manager.turn_methods import TurnMethods

if TYPE_CHECKING:
    pass


class WorldManager:
    """
    Contains all world related functionality
    """
    def __init__(self):

        self.World = esper.World()
        self.Entity = EntityMethods(self)
        self.Skill = SkillMethods(self)
        self.Map = MapMethods(self)
        self.FOV = FOVMethods(self)
        self.Turn = TurnMethods(self)

        logging.info(f"WorldManager initialised.")

    def update(self, delta_time: float):
        """
        Update real-time timers on entities
        """
        self.Entity.process_aesthetic_update(delta_time)


world = WorldManager()