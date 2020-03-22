from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from snecs import Component
from snecs.types import EntityID

from scripts.engine import entity


if TYPE_CHECKING:
    from typing import Type

# TODO - show debug info
# TODO - approach to type commands to trigger actions e.g. spawn creature
# TODO - approach to show required info, e.g. rounds & time, FPS

########################  ###########################


# def set_visibility(self, visible: bool):
#     """
#     Set whether the debug info is visible
#     """


def log_component_not_found(ent: EntityID, component: Type[Component]):
    """
    Use if component not found. Log the error as a warning in the format "{ent} tried to get {component} but it was
    not found."
    """
    name = entity.get_name(ent)
    logging.warning(f"'{name}'({ent}) tried to get {component.__class__.__name__}, but it was not found.")


