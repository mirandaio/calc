# Define exceptions
class InvalidExpressionError(Exception):
    pass

class NotStringError(Exception):
    pass

class NotListError(Exception):
    pass

class NotQueueError(Exception):
    pass

def tokenize(expr):
    """
    expr: a string representing a mathematical expression in infix notation

    returns: a list of strings where each string represents a token of the 
    mathematical expression
    """
    tokens = []
    i = 0

    while i < len(expr):
        c = expr[i]
        if c == "(" or c == ")" or c == "+" or c == "*" or c == "/":
            tokens.append(c)
            i += 1
        elif c == "l": # what about number right before log?
            if i <= len(expr) - 3 and expr[i:i+3] == "log":
                tokens.append(expr[i:i+3])
                i += 3
            else:
                raise InvalidExpressionError, "expected log"
        elif c == "-":
            if len(tokens) == 0:
                tokens.append("_")
                i += 1
            else:
                prev = tokens[-1] # previous token
                if prev == "(" or prev == "+" or prev == "-" or \
                    prev == "_" or prev == "*" or prev == "/" or \
                    prev == "log":
                    tokens.append("_")
                    i += 1
                elif prev == ")" or prev[-1] == "." or prev[-1].isdigit():
                    tokens.append("-")
                    i += 1
                else: # don't think will need this
                    raise InvalidExpressionError, "invalid -"
        elif expr[i].isspace():
            # skip white space
            while i < len(expr) and expr[i].isspace():
                i += 1
        elif c == "." or c.isdigit():
            haspoint = c == "."
            num = c
            i += 1
            while i < len(expr):
                if expr[i].isdigit():
                    num += expr[i]
                    i += 1
                elif not haspoint and expr[i] == ".":
                    num += "."
                    i += 1
                else:
                    break

            if num == ".":
                raise InvalidExpressionError, "single dot"

            tokens.append(num)
        else:
            raise InvalidExpressionError, "Unrecognized character"

    return tokens

def topostfix(tokens):
    """
    tokens: a list of strings which represent the tokens of a mathematical 
    expression in infix notation

    returns: a queue of strings that represent the tokens of a mathematical 
    expression in postfix notation
    """
    pass

def eval(token):
    """
    tokens: a queue of strings that represent the tokens of a mathematical
    expression in postfix notation

    returns: a floating number that is the result of evaluating the
    mathematical expression
    """
    pass
