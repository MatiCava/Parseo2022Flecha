from sys import argv
from json import dumps
from .Lexer import FlechaLexer
from .Parser import FlechaParser

if __name__ == '__main__':

    inputFile  = 'no_input.txt'
    if len(argv) >= 2:
        inputFile = argv[1]
    with open(inputFile,'r') as inputContent:
        data = inputContent.read()

    try:

        lexer = FlechaLexer()
        parser = FlechaParser()
        tokenized = lexer.tokenize(data)
        parsed = parser.parse(tokenized)
        ast = parsed.toAST()
        print(ast)
        jsonResult = dumps(ast, indent=3)
        print('jsonResult: ' + jsonResult)
    except Exception as e:
        print(e)