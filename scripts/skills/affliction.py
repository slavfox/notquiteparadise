
from scripts.core.constants import AfflictionCategory, AfflictionTypes, AfflictionTriggers, LoggingEventTypes
from scripts.data_loaders.getters import get_value_from_afflictions_json
from scripts.events.logging_events import LoggingEvent
from scripts.global_instances.event_hub import publisher
from scripts.skills.affliction_effects.affliction_effect import AfflictionEffect
from scripts.world.entity import Entity


class Affliction:
    """
    Affliction, either Bane or Boon. Applies a periodic effect to an Entity, dictated by its AfflictionTrigger.

    Attributes:
        name (str):  string name of the Affliction
        description (str): description of the Affliction
        icon (pygame.Image): pygame image to symbolise the Affliction
        affliction_category (AfflictionCategory): Bane or Boon
        affliction_type (AfflictionTypes): the Enum value of the Affliction Name
        duration (int): amount of applications before expiry
        trigger_event (AfflictionTriggers): the event that triggers the Affliction to activate
        affected_entity (Entity): the Entity being impacted by the Affliction
        affliction_effects (list(AfflictionEffect)): list of AfflictionEffects
    """

    def __init__(self, name, duration, affected_entity):
        from scripts.global_instances.managers import game_manager
        action = game_manager.affliction_action
        values = get_value_from_afflictions_json(name)
        self.name = name
        self.description = values["description"]
        self.icon = values["icon"]
        self.affliction_category = action.get_affliction_category_from_string(values["category"])
        self.affliction_type = action.get_affliction_type_from_string(name)
        self.duration = duration
        self.trigger_event = action.get_trigger_event_from_string(values["trigger_event"])
        self.affected_entity = affected_entity  # set at time of allocation to an entity
        self.affliction_effects = []

        # get the affliction skill_effects
        affliction_effects_values = values["affliction_effects"]

        # unpack all affliction_effects
        for effect in affliction_effects_values:
            created_effect = None
            effect_name = effect["name"]

            if effect_name == "damage":
                created_effect = game_manager.affliction_action.create_damage_effect(self, effect)

            # if we have an effect add it to internal list
            if created_effect:
                self.affliction_effects.append(created_effect)

    def trigger(self):
        """
        Trigger all affliction effects and decrement duration by 1
        """
        log_string = f"Triggering effects in {self.name}"
        publisher.publish(LoggingEvent(LoggingEventTypes.INFO, log_string))

        for effect in self.affliction_effects:
            effect.trigger(self.affected_entity)

        # reduce duration on all effects other than Passive
        if self.trigger_event != AfflictionTriggers.PASSIVE:
            self.duration -= 1
            log_string = f"Duration reduced to: {self.duration}"
            publisher.publish(LoggingEvent(LoggingEventTypes.DEBUG, log_string))

