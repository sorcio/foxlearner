class FakeGame(object):
    """
    A simple class used to test GameObject and MovingPawn class
    providing all necessary attributes, so without using the __real__
    game class.
    """
    def __init__(self, size):
        """
        Set up fake attributes.
        """
        self.size = size


class FakeController(object):
    """
    A simple class used to test Game class providinf all necessary attributes,
    so without the __real__ game class.
    """
    def __init__(self, pawn, brain, *postfilters):
        """
        Set up fake attributes.
        """
        self.brain = brain
        self.postfitlers = postfilters
        self.pawn = pawn


