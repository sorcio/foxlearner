"""
options.py: provides extra options for the controllers
"""

class FoxgameOption(object):
    """
    A FoxgameOption provides some attributes useful for
    parsing and configuring some specific constants on the game.
    """

    def __init__(self,
                 name,
                 type='string',
                 description=''):
        """
        Set up FoxgameOption attributes.
        """
        self.name = name
        self.description = description
        self._parse_clstype(type)

    def __repr__(self):
        return '<FoxgameOption object name=\'%s\', type=\'%s\'>' % (
               self.name, self.factory.__name__)

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
        elif sfactory == 'bool':
            self.factory = lambda x: 'true'.startswith(x.lower())
        elif sfactory == 'function':
            self.factory = lambda x: lambda *x: eval(*x)
        # elif sfactory == 'vector':
        #     self.factory = Vector
        # elif sfactory == 'direction':
        #     self.factory = Direction
        else:
            raise TypeError('Unknown type.')

    @property
    def doc(self):
        return self.description



