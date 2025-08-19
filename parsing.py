import re

# Tokenize the string
def tokenize(code):
    #tokens = re.findall(r'[()]|\\|λ|\.|[a-zA-Z_][a-zA-Z0-9_]*', code)
    #return tokens
    return re.findall(r'[()]|\\|λ|\.|\d+|[a-zA-Z_][a-zA-Z0-9_]*', code)

# Parser class
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self, expected=None):
        tok = self.peek()
        if expected and tok != expected:
            raise SyntaxError(f"Expected {expected} but got {tok}")
        self.pos += 1
        return tok

    def parse(self):
        return self.parse_expr()

    def parse_expr(self):
        # Handle abstraction or application
        if self.peek() in ['\\', 'λ']:
            return self.parse_lambda()
        else:
            return self.parse_application()

    def parse_lambda(self):
        self.consume()  # consume '\' or 'λ'
        var = self.consume()  # get variable name
        self.consume('.')     # consume the '.'
        body = self.parse_expr()
        return ('lambda', var, body)

    def parse_application(self):
        expr = self.parse_atom()
        while self.peek() not in [None, ')']:
            next_expr = self.parse_atom()
            expr = ('app', expr, next_expr)
        return expr

    def parse_atom(self):
        tok = self.peek()
        if tok is None:
        	raise SyntaxError("Unexpected end of input in atom")
        if tok == '(':
            self.consume('(')
            expr = self.parse_expr()
            self.consume(')')
            return expr
        elif re.match(r'[a-zA-Z_][a-zA-Z0-9_]*', tok):
            return ('var', self.consume())
        elif tok.isdigit():
        	return ('var', self.consume())
        else:
            raise SyntaxError(f"Unexpected token: {tok}")


if __name__=="__main__":
	code = r'(\x. x) y'
	tokens = tokenize(code)
	parser = Parser(tokens)
	ast = parser.parse()
	print(ast)
