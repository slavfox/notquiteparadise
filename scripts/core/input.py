import pygame

from scripts.core.constants import GameStates, TILE_SIZE
from scripts.core.global_data import entity_manager, game_manager, ui_manager, world_manager, debug_manager
from scripts.events.entity_events import UseSkillEvent
from scripts.events.game_events import ExitEvent


def get_input():
    """
    Get the pygame event, update the input_values dictionary and return input_values.

    Returns:
        Dict[] : `input_values` containing True for all appropriate inputs, and Tuple[int,int] for the `mouse_xy`.

    """
    # gets mouse and key input as list of events
    input_events = pygame.event.get()

    # init input values
    input_values = {
        "left_click": False,
        "right_click": False,
        "middle_click": False,
        "mouse_xy": (0, 0),
        "up": False,
        "down": False,
        "left": False,
        "right": False,
        "up_right": False,
        "up_left": False,
        "down_right": False,
        "down_left": False,
        "wait": False,
        "interact": False,
        "inventory": False,
        "drop": False,
        "character": False,
        "fullscreen": False,
        "cancel": False,
        "new_game": False,
        "load_game": False,
        "debug_toggle": False

    }

    # check all input events
    for input in input_events:

        # update MOUSE input values based on input
        # TODO: move each set of event typ eto its own function
        if input.type == pygame.MOUSEBUTTONDOWN:
            check_mouse_input(input_values)

        # is a key pressed?
        if input.type == pygame.KEYDOWN:

            # update OTHER input values based on input
            if input.key == pygame.K_UP or input.key == pygame.K_KP8 or input.key == pygame.K_k:
                input_values["up"] = True
            elif input.key == pygame.K_DOWN or input.key == pygame.K_KP2 or input.key == pygame.K_j:
                input_values["down"] = True
            elif input.key == pygame.K_LEFT or input.key == pygame.K_KP4 or input.key == pygame.K_h:
                input_values["left"] = True
            elif input.key == pygame.K_RIGHT or input.key == pygame.K_KP6 or input.key == pygame.K_l:
                input_values["right"] = True
            elif input.key == pygame.K_KP7 or input.key == pygame.K_y:
                input_values["up_left"] = True
            elif input.key == pygame.K_KP9 or input.key == pygame.K_u:
                input_values["up_right"] = True
            elif input.key == pygame.K_KP1 or input.key == pygame.K_b:
                input_values["down_left"] = True
            elif input.key == pygame.K_KP3 or input.key == pygame.K_n:
                input_values["down_right"] = True
            elif input.key == pygame.K_z or input.key == pygame.K_KP5:
                input_values["wait"] = True
            elif input.key == pygame.K_i:
                input_values["inventory"] = True
            elif input.key == pygame.K_d:
                input_values["drop"] = True
            elif input.key == pygame.K_RETURN:
                input_values["interact"] = True
            elif input.key == pygame.K_c:
                input_values["character"] = True
            elif input.key == pygame.K_RETURN and pygame.K_LALT:
                # Alt+Enter: toggle full screen
                input_values["fullscreen"] = True
            elif input.key == pygame.K_ESCAPE:
                input_values["cancel"] = True
            elif input.key == pygame.K_a:
                # TODO remove this legacy when menu's can use kb+m
                input_values["new_game"] = True
            elif input.key == pygame.K_b:
                # TODO remove this legacy when menu's can use kb+m
                input_values["load_game"] = True
            elif input.key == pygame.K_TAB:
                input_values["debug_toggle"] = True

    return input_values


def handle_input(values):
    """
    Process the user input into game action by interpreting the value in relation to the `GameState`.

    Args:
        values (Dict[]): User input events.

    """
    game_state = game_manager.game_state
    player = entity_manager.player

    # game state agnostic
    if game_state:
        if values["debug_toggle"]:
            if debug_manager.visible:
                debug_manager.set_visibility(False)
            else:
                debug_manager.set_visibility(True)

    if game_state == GameStates.PLAYER_TURN:

        if values["right_click"]:
            pos = values["mouse_xy"]
            for key, rect in ui_manager.visible_panels.items():
                if rect.collidepoint(pos):
                    clicked_rect = key

            # right clicked on the map so give the selected tile to the ui manager to display info
            if clicked_rect == "game_map":
                tile_pos = ui_manager.get_relative_scaled_mouse_pos(clicked_rect)
                tile_x = tile_pos[0] // TILE_SIZE
                tile_y = tile_pos[1] // TILE_SIZE
                entity = entity_manager.query.get_entity_in_fov_at_tile((tile_x, tile_y))

                if entity:
                    ui_manager.entity_info.set_selected_entity(entity)


        dx = 0
        dy = 0

        if values["up"]:
            dx = 0
            dy = -1
        elif values["down"]:
            dx = 0
            dy = 1
        elif values["left"]:
            dx = -1
            dy = 0
        elif values["right"]:
            dx = 1
            dy = 0
        elif values["up_left"]:
            dx = -1
            dy = -1
        elif values["up_right"]:
            dx = 1
            dy = -1
        elif values["down_left"]:
            dx = -1
            dy = 1
        elif values["down_right"]:
            dx = 1
            dy = 1

        # if destination isn't 0 then we need to move an entity
        if dx != 0 or dy != 0:
            target_tile = (dx, dy)
            game_manager.create_event(UseSkillEvent(player, target_tile, "move"))

        if values["wait"]:
            return {"wait": True}
        elif values["inventory"]:
            return {"show_inventory": True}
        elif values["drop"]:
            return {"drop_inventory": True}
        elif values["interact"]:
            # TODO check if item on same tile
            return {"pickup": True}
            # TODO check if stairs on same tile
            return {"take_stairs": True}
        elif values["character"]:
            return {"show_character_screen": True}
        elif values["fullscreen"]:
            return {"fullscreen": True}
        elif values["cancel"]:
            game_manager.create_event(ExitEvent())

    if game_state == GameStates.TARGETING:
        if values["cancel"]:
            return {"exit": True}

    if game_state == GameStates.PLAYER_DEAD:
        if values["inventory"]:
            return {"show_inventory": True}
        elif values["fullscreen"]:
            return {"fullscreen": True}
        elif values["cancel"]:
            return {"exit": True}

    if game_state == GameStates.SHOW_INVENTORY:
        # TODO add mouse and keyboard input
        # TODO change to generic Menu state; will need a var to hold which menu
        if values["fullscreen"]:
            return {"fullscreen": True}
        elif values["cancel"]:
            return {"exit": True}

    if game_state == GameStates.MAIN_MENU:
        pass
    # if values["new_game"]:
    # 	create_event(event_hub, Event(GameEventTypes.NEW_GAME, EventTopics.GAME, []))
    # elif values["load_game"]:
    # 	return {"load_game": True}
    # elif values["cancel"]:
    # 	create_event(event_hub, Event(GameEventTypes.EXIT, EventTopics.GAME, []))


def check_mouse_input(input_values):
        """

        Args:
            input_values:
        """

        if pygame.mouse.get_pressed()[0]:
            input_values["left_click"] = True
        elif pygame.mouse.get_pressed()[1]:
            input_values["middle_click"] = True
        elif pygame.mouse.get_pressed()[2]:
            input_values["right_click"] = True

        input_values["mouse_xy"] = ui_manager.get_scaled_mouse_pos()