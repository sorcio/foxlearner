"""
void.py: Brains useful for testing.
"""

from foxgame.controller import Brain
from foxgame.structures import Direction

class FoxBrain(Brain):

    def update(self):
        """
        Always return Direction.NULL.
        """

        return Direction(Direction.NULL)


class HareBrain(Brain):
    # threshold = 80

    def update(self):
        """
        Alwaysreturn Direction.NULL
        """
        return Direction(Direction.NULL)
