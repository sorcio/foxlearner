"""
void.py: Brains useful for testing.
"""

from foxgame.controller import Brain
from foxgame.structures import Direction

class FoxBrain(Brain):

    def update(self, time):
        """
        Always return Direction.NULL.
        """

        return Direction(Direction.NULL)


class HareBrain(Brain):
    # threshold = 80

    def update(self, time):
        """
        Alwaysreturn Direction.NULL
        """
        return Direction(Direction.NULL)
