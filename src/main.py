import sys

from lexer import Lexer


def main():
    # TODO: handle wrong inputs
    ezcFilePath = sys.argv[1]
    fileContent = open(ezcFilePath, "r").read()
    lexer = Lexer()
    lexer.run(input_string=fileContent)
    print(lexer.tokenList)


if __name__ == "__main__":
    main()
