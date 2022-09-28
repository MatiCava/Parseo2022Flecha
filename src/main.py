from sys import argv

from .lexer import FlechaLexer
from .parser import FlechaParser

if __name__ == '__main__':

    try:
        if len(argv) < 2:
            raise Exception("")

        inputFile = argv[1]
        with open(inputFile, 'r') as inputContent:
            inputData = inputContent.read()

        lexer = FlechaLexer()
        parser = FlechaParser()
        tokenized = lexer.tokenize(inputData)
        parsed = parser.parse(tokenized)
        ast = parsed.toAST()
    except Exception as e:
        print(e)