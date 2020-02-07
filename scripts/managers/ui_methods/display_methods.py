
from typing import Tuple
from scripts.core.constants import VisualInfo
import pygame


class DisplayMethods:
    """
    Methods for handling display

    Attributes:
        manager ():
    """

    def __init__(self, manager):
        from scripts.managers.ui_manager import UIManager
        self._manager = manager  # type: UIManager

        self.init_pygame()

        self.desired_width = VisualInfo.BASE_WINDOW_WIDTH
        self.desired_height = VisualInfo.BASE_WINDOW_HEIGHT
        # TODO - allow for selection by player but only multiples of base (16:9)
        self.screen_scaling_mod_x = self.desired_width // VisualInfo.BASE_WINDOW_WIDTH
        self.screen_scaling_mod_y = self.desired_height // VisualInfo.BASE_WINDOW_HEIGHT
        self.window = pygame.display.set_mode((self.desired_width, self.desired_height))
        self.main_surface = pygame.Surface((VisualInfo.BASE_WINDOW_WIDTH, VisualInfo.BASE_WINDOW_HEIGHT),
                                           pygame.SRCALPHA)

        self.init_display_config()

    def init_pygame(self):
        """
        Init pygame
        """
        pygame.init()

    def init_display_config(self):
        """
        Initialise display settings.
        """
        pygame.display.set_caption("Not Quite Paradise")
        # pygame.display.set_icon() # TODO - add window icon

    def get_screen_scaling_mod(self):
        """
        Get the screen scaling modifier

        Returns:
            Tuple[int,int]
        """
        return self.screen_scaling_mod_x, self.screen_scaling_mod_y

    def get_main_surface(self):
        """
        Get the main surface where all draws eventually go.

        Returns:
            pygame.Surface:
        """
        return self.main_surface

    def get_desired_resolution(self):
        """
        Get the desired resolution

        Returns:
            Tuple[int, int]: (width, height)
        """
        return self.desired_width, self.desired_height

    def get_window(self):
        """
        Get the window

        Returns:

        """
        return self.window