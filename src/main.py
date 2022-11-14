from sys import argv
from json import dumps
from Lexer import FlechaLexer
from Parser import FlechaParser
from Interprete import FlechaInterprete, EntornoVacio, EntornoExtendido
import os

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
        inter = FlechaInterprete({}, EntornoVacio())
        inter.evaluar(ast)
        ##jsonResult = dumps(ast, indent=3)
        ##dirResult = ".\\test_results\\" + os.path.basename(inputFile).split('.')[0] + '.result'
        ##with open(dirResult, 'w') as f:
        ##    f.write(jsonResult)
        
    except Exception as e:
        print(e)