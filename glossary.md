### Game logic (GL) ###
In the software architecture, this is the component which fully implements the
logic of the game. It should include definition of the game, game rules, game
mechanics, pawns. It should not include user interface or controller code.
It should provide a class Game, which should be the abstraction for a running
game.

Main implementation: `gamecore.py`

### User interface (UI) ###
In the software architecture, this is the component which runs the main loop,
gets input from the user and displays a user interface.

Main implementations:
  1. `bubbles/`   - Pygame interface.
  1. `simulator.py` - Void. interface. Useful for testing.

### Game ###
The Game cass provides basics for the game logic: it keeps track of pawns (carrots included), time elapsed, ...


### Controller (ctl) ###
TODO

## Brain ##
TODO

### PostFilter ###
TODO