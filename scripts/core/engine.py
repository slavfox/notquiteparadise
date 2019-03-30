import logging
import pygame

from scripts.core.constants import GameStates
from scripts.core.global_data import world_manager, game_manager, entity_manager, turn_manager, ui_manager, \
    debug_manager
from scripts.core.input import get_input, handle_input
from scripts.core.intialisers import initialise_game

# Project Wide to do list...
# TODO *NEXT* add basic attack skill
# TODO - swap out nose for pytest
# TODO - setup README, setup.py and requirements.txt
# TODO - move json data to a dictionary on load; create reload/refresh function
# TODO - create global tooltip method
# TODO - skill activation events (so that animation can listen and play)
# TODO - effect activation events (so that world can update)
# TODO - text wrapping, especially in message log
# TODO - all UI functionality to watch events and update UI in response

def main():
    """
    The container for the game initialisation and game loop
    """
    initialise_game()
    game_loop()

    # we've left the game loop so now leave the game
    logging.shutdown() # clear logging resources
    pygame.quit()  # clean up pygame resources
    raise SystemExit  # exit window and python


def game_loop():
    """
    The core game loop, handling input, rendering and logic.
    """
    while not game_manager.game_state == GameStates.EXIT_GAME:

        # limit frames
        game_manager.internal_clock.tick(60)

        # HANDLE INPUT
        # determine the action to take from the input with the context of the game state
        input_values = get_input()
        handle_input(input_values)

        if game_manager.game_state == GameStates.ENEMY_TURN:
            turn_manager.turn_holder.ai.take_turn()

        # HANDLE UPDATE
        game_manager.update()
        debug_manager.update()
        world_manager.update()
        entity_manager.update(world_manager.game_map)

        # DRAW
        ui_manager.draw_game(world_manager.game_map, entity_manager.entities, debug_manager.visible)


if __name__ == "__main__":  # prevents being run from other modules
    main()
