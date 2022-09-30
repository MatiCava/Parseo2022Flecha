from sly import Lexer


class FlechaLexer(Lexer):
    # Set of token names preguntar si podemos usar MINUS para dos cosas distintas
    
    tokens = { 
                LOWERID,
                UPPERID, 
                NUMBER, 
                CHAR,
                STRING,
                DEF,
                IF,
                THEN,
                ELIF,
                ELSE,
                CASE,
                LET,
                IN,
                EQ,
                DEFEQ,
                SEMICOLON,
                LPAREN,
                RPAREN,
                LAMBDA,
                PIPE,
                ARROW,
                AND,
                OR,
                NOT,
                NE,
                GE,
                LE,
                GT,
                LT,
                PLUS,
                MINUS,
                DIV,
                MOD,
                TIMES,
                UMINUS
            }

    # String containing ignored characters between tokens
    ignore_tab = '\t'
    ignore_whitespace = '\s'
    ignore_newline = '\n'
    ignore_return = '\r'
    ignore_comments = r'(--.*)' #aca quizas hay que frenar el regex con \n creo

    # Regular expression rules for tokens
    LOWERID = r'[a-z][_a-zA-Z0-9_]*'
    UPPERID = r'[A-Z][_a-zA-Z0-9_]*'
    NUMBER  = r'\d+'
    CHAR    = r'\'(\t|\n|\r|\\.|.|\")\''
    STRING  = r'\"(?:[^\"\\]|\t|\n|\r|\\.|\")*\"'
    EQ      = r'=='
    DEFEQ   = r'='
    SEMICOLON = r';'
    LPAREN  = r'\('
    RPAREN  = r'\)'
    LAMBDA  = r'\\'
    OR      = r'\|\|'
    PIPE    = r'\|'
    ARROW   = r'->'
    AND     = r'&&'
    NE      = r'!='
    NOT     = r'!'
    GE      = r'>='
    LE      = r'<='
    GT      = r'>'
    LT      = r'<'
    PLUS    = r'\+'
    MINUS   = r'-'
    UMINUS  = r'-'
    DIV     = r'\/'
    MOD     = r'%'
    TIMES   = r'\*'

    # Special cases
    LOWERID['def']  = DEF
    LOWERID['if']   = IF
    LOWERID['then'] = THEN
    LOWERID['elif'] = ELIF
    LOWERID['else'] = ELSE
    LOWERID['case'] = CASE
    LOWERID['let']  = LET
    LOWERID['in']   = IN

    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1
    
    def tokenize(self, s: str) -> Lexer.tokenize:
        return super().tokenize(s)