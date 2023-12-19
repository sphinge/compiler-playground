## Parser - Project Blue

### project setup

- Run `make setup` to create a venv and insall all the needed dependencies.
- Run `make test` to run our tests.

### project structure

![A picture describing our current scheme.](scheme.png)

This project is written in python and uses pytest to test the lexer. The
different stages of our compiler are seperated into python modules:

The lexer in `lexer` uses an input to generate a token stream. The tokens are
defined in `TokenTypes.py`.

### UML diagram

Our UML diagram can be opened and edited using
[drawio](https://app.diagrams.net/).

### [Language Spec](docs/language-spec)
