import math
from collections import deque

# a map of operators to their precedence
p = {"+": 1, "-": 1, "*": 2, "/": 2, "_": 3, "log": 3}

def isnumber(s):
    """
    helper function to determine if string represents a number"
    """
    try:
        float(s)
        return True
    except ValueError:
        return False

def isoperator(s):
    return isunary(s) or isbinary(s)

def isunary(s):
    return s == "_" or s == "log"

def isbinary(s):
    return s == "+" or s == "-" or s == "*" or s == "/"

def tokenize(expr):
    """
    expr: a string representing a mathematical expression in infix notation

    returns: a list of strings where each string represents a token of the 
    mathematical expression
    """
    tokens = []
    parens = 0
    i = 0

    while i < len(expr):
        c = expr[i]
        if c == "(" or c == ")":
            if c == "(":
                parens += 1
            else:
                parens -= 1
                if parens < 0:
                    raise Exception, "Unbalanced parentheses"
            tokens.append(c)
            i += 1
        elif c == "+" or c == "*" or c == "/":
            if len(tokens) > 0 and (tokens[-1] == ")" or isnumber(tokens[-1])):
                tokens.append(c)
                i += 1
            else:
                raise Exception, "missing left operand"
        elif c == "l": # what about number right before log?
            if i <= len(expr) - 3 and expr[i:i+3] == "log":
                tokens.append(expr[i:i+3])
                i += 3
            else:
                raise Exception, "expected log"
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
                elif prev == ")" or isnumber(prev):
                    tokens.append("-")
                    i += 1
                else: # don't think will need this
                    raise Exception, "invalid -"
        elif expr[i].isspace():
            while i < len(expr) and expr[i].isspace():
                i += 1
        elif c == "." or c.isdigit():
            haspoint = c == "."
            num = [c]
            i += 1
            while i < len(expr):
                if expr[i].isdigit():
                    num.append(expr[i])
                    i += 1
                elif not haspoint and expr[i] == ".":
                    haspoint = True
                    num.append(".")
                    i += 1
                else:
                    break

            strnum = ''.join(num)

            if strnum == ".":
                raise Exception, "single dot"

            if len(tokens) > 0 and (tokens[-1] == ")" or isnumber(tokens[-1])):
                raise Exception, "missing operator"

            tokens.append(strnum)
        else:
            raise Exception, "Unrecognized character"

    if parens != 0:
        raise Exception, "Unbalanced parentheses"

    if len(tokens) > 0 and isoperator(tokens[-1]):
        raise Exception, "Ended in " + tokens[-1]

    return tokens


def topostfix(tokens):
    """
    tokens: a list of strings which represent the tokens of a valid 
    mathematical expression in infix notation

    returns: a queue of strings that represent the tokens of a mathematical 
    expression in postfix notation
    """
    stack = []
    queue = deque([])

    for token in tokens:
        if isnumber(token):
            queue.append(token)
        elif token == "(" or isunary(token):
            stack.append(token)
        elif isbinary(token):
            while len(stack) > 0 and stack[-1] != "(" and \
                p[token] <= p[stack[-1]]:
                queue.append(stack.pop())

            stack.append(token)
        elif token == ")":
            while stack[-1] != "(":
                queue.append(stack.pop())

            stack.pop()

    while len(stack) > 0:
        queue.append(stack.pop())

    return queue

def eval(tokens):
    """
    tokens: a queue of strings that represent the tokens of a valid 
    mathematical expression in postfix notation

    returns: a floating number that is the result of evaluating the
    mathematical expression
    """
    stack = []
    for token in tokens:
        if isnumber(token):
            stack.append(float(token))
        elif token == "_":
            val = -stack.pop()
            stack.append(val)
        elif token == "log":
            val = math.log(stack.pop())
            stack.append(val)
        elif token == "+":
            right = stack.pop()
            left = stack.pop()
            stack.append(left + right)
        elif token == "-":
            right = stack.pop()
            left = stack.pop()
            stack.append(left - right)
        elif token == "*":
            right = stack.pop()
            left = stack.pop()
            stack.append(left * right)
        else:
            right = stack.pop()
            left = stack.pop()
            stack.append(left / right)

    return stack[-1]

def calc(s):
    tokens = tokenize(s)
    postfix = topostfix(tokens)
    return eval(postfix)
