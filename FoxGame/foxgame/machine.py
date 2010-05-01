
class StateMachine(object):
    """
    Simple finite state machine with stateful methods.
    """

    def __init__(self):
        # Registered states
        self.states = dict()

        # Current state
        self.state = None

        # Registered stateful methods
        self.statefuls = ['enter', 'exit']

    def do_nothing(self, *args, **kwargs):
        """
        Placeholder method used when state specifies no other.
        """
        pass

    def register_state(self, name):
        methods = dict(('state_' + meth_name,
                       getattr(self, '%s_%s' % (name, meth_name),
                               self.do_nothing))
                       for meth_name in self.statefuls)

        getattr(self, name + '_init', self.do_nothing)()

        self.states[name] = methods

    def goto_state(self, name):
        new_state = self.states[name]

        # Call previous state exit
        if self.state:
            self.state_exit(name)

        # Set new state
        self.state = name

        # Update statefuls to new state
        self.__dict__.update(new_state)

        # Enter the new state
        self.state_enter()
