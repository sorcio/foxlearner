"""
options.py: provides extra options for the controllers
"""
from foxgame.gamecore import FoxGameError
from foxgame.structures import Direction, Vector
from functools import wraps

class FoxgameOption(object):
    """
    A FoxgameOption provides some attributes useful for
    parsing and configuring some specific constants on the game.
    """

    def __init__(self,
                 name,
                 type='string',
                 choices=None,
                 description=''):
        """
        Set up FoxgameOption attributes.
        """
        self.name = name
        self.description = description
        self.choices = choices
        if self.choices is not None:
            self.factory = self._parse_choice
        else:
            self._parse_clstype(type)

    def __repr__(self):
        return '<FoxgameOption object name=\'%s\', type=\'%s\'>' % (
               self.name, self.factory.__name__)

    def __str__(self):
        return '(%s) %s' % (self.factory.__name__, self.name)

    def __eq__(self, other):
        """
        Compare self.name with another string.
        """
        return self.name == other

    def __ne__(self, other):
        return not self == other

    def __call__(self, value):
        """
        Return a new object according to the type given.
        """
        return self.factory(value)

    def _parse_clstype(self, sfactory):
        if sfactory == 'string':
            self.factory = str
        elif sfactory == 'int':
            self.factory = int
        elif sfactory == 'float':
            self.factory = float
        elif sfactory == 'bool':
            self.factory = self._factory_bool
        elif sfactory == 'vector':
            self.factory = self._factory_vector
        elif sfactory == 'direction':
             self.factory = Direction.from_string
        else:
            raise TypeError('Unknown type.')

    def _parse_choice(self, x):
        return self.choices[x]

    @staticmethod
    def _factory_bool(x):
        if x.lower() in ('yes', 'on', 'true', '1'):
            return True
        elif x.lower() in ('no', 'off', 'false', '0'):
            return False
        else:
            raise FoxgameError('FoxgameOption', 'invalid bool string %s' % x)

    @staticmethod
    def _factory_vector(x):
        x = x.strip('( )')
        x = (float(x.strip()) for x in x.split(','))
        return Vector(*x)

    @property
    def doc(self):
        return self.description


def task(task_func):
    """
    A task is.. XXX.
    """
    # TODO
    # ensure task_func is a task? (func_name.startswith('task_'), ...)
    return staticmethod(task_func)

