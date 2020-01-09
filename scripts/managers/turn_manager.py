import logging
from typing import Dict, Tuple

from scripts.events.game_events import EndRoundEvent
from scripts.core.event_hub import publisher
from scripts.managers.world_manager import world
from scripts.world.components import Resources, Identity, IsTurnHolder
from scripts.world.entity import Entity


class TurnManager:
    """
    Manager of turns functions.
    """
    # TODO What do we need from the turn queue?
    #  Add all entities that are within X range of the player;
    #  Add new entities to the queue as they get into range;
    #  Amend an entities position in the queue;
    #  Keep track of rounds;

    def __init__(self):
        self.turn_queue = {}  # type: Dict[Tuple[int, int]] # (entity, time)
        self.round = 0  # count of the round
        self.time = 0  # total time of actions taken
        self.time_of_last_turn = 0
        self.time_in_round = 100  # time units in a round
        self.round_time = 0  # tracker of time progressed in current round

        logging.info(f"TurnManager initialised.")

    def build_new_turn_queue(self):
        """
        Build a new turn queue for all entities
        """
        logging.debug(f"Building a new turn queue...")

        # create a turn queue from the entities list
        for entity, resource in world.World.get_component(Resources):
            self.turn_queue[entity] = resource.time_spent

        # remove turn holder component from existing turn holder
        old_turn_holder = world.Entity.get_entity(IsTurnHolder)
        world.World.remove_component(old_turn_holder, IsTurnHolder)

        # get the next entity in the queue
        new_turn_holder = min(self.turn_queue, key=self.turn_queue.get)
        world.World.add_component(new_turn_holder, IsTurnHolder)

        # log result
        queue = []
        for entity, time in self.turn_queue.items():
            if world.World.has_component(entity, Identity):
                identity = world.World.component_for_entity(entity, Identity)
                queue.append((identity.name, time))

        logging.debug(f"-> Queue built. {queue}")

    def end_turn(self, spent_time):
        """
        End the current turn and apply time spent

        Args:
            spent_time:
        """
        # get turn holder
        turn_holder = world.Entity.get_entity(IsTurnHolder)

        #  update turn holder`s time spent
        world.Entity.spend_time(spent_time)

        # update turn holders time in queue
        resources = world.Entity.get_entitys_component(turn_holder, Resources)
        self.turn_queue[turn_holder] = resources.time_spent

        # remove turn holder component
        world.World.remove_component(turn_holder, IsTurnHolder)

        # log result
        identity = world.Entity.get_entitys_component(turn_holder, Identity)
        logging.debug(f"Ended '{identity.name}'`s turn.")

    def next_turn(self):
        """
        Proceed to the next turn, setting the next entity to act as the turn holder.
        """
        logging.debug(f"Moving to the next turn...")

        if not self.turn_queue:
            self.build_new_turn_queue()

        # get the next entity in the queue
        new_turn_holder = min(self.turn_queue, key=self.turn_queue.get)

        # update time using last action and when new turn holder can act
        resources = world.Entity.get_entitys_component(new_turn_holder, Resources)
        time_progressed = resources.time_spent - self.time_of_last_turn
        self.time += time_progressed
        self.time_of_last_turn = self.time

        # check if we need to set new round
        if self.round_time + time_progressed > self.time_in_round:
            self.next_round(time_progressed)
        else:
            self.round_time += time_progressed

        # log result
        identity = world.Entity.get_entitys_component(new_turn_holder, Identity)
        logging.debug(f"-> It is now '{identity.name}'`s turn.")

    def next_round(self, time_progressed):
        """
        Move to the next round and trigger end of round events

        Args:
            time_progressed (int):
        """
        # trigger end of round actions
        publisher.publish(EndRoundEvent())

        # add progressed time and minus time_in_round to keep the remaining time
        self.round_time = (self.round_time + time_progressed) - self.time_in_round

        # increment rounds
        self.round += 1

        logging.info(f"It is now round {self.round}.")


turn = TurnManager()