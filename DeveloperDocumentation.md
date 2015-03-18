# Tools #

Each developer should use these tools to check for errors/bad style:
  * [pylint](http://www.logilab.org/857)
  * [trial](http://twistedmatrix.com/) or [py.test](http://codespeak.net/py/dist/test/)


# Before Commit #
  * DISCUSS: if your patch is really important(i.e. change a function often used in the code), ensure that the rest of the developers is informed about it;
  * TEST: ensure that at least the same number of tests in the previous commit passes;
  * REVIEW: use pylint to test the file, and ensure that its rate is > 6.4

# Commit #
  * avoid nonsensical commit messages;
  * keep patches simple: better split them and provide a description for each one;
  * always submit with a short but comprehensive description;
  * you should use your real name instead of your nick;
  * Commit ;)