import unittest
import calc
from collections import deque

class TokenizeValidInput(unittest.TestCase):
    valid_expr = (
        ("", []),
        ("()", ["(", ")"]),
        ("(())", ["(", "(", ")", ")"]),
        ("()()", ["(", ")", "(", ")"]),
        ("1", ["1"]),
        ("5.84", ["5.84"]),
        ("-1", ["_", "1"]), # unary negation is represented as _
        ("--2", ["_", "_", "2"]),
        ("log 14", ["log", "14"]),
        ("log(3)", ["log", "(", "3", ")"]),
        ("log(-1)", ["log", "(", "_", "1", ")"]),
        ("log -4", ["log", "_", "4"]),
        ("(2)", ["(", "2", ")"]),
        ("1 + 2", ["1", "+", "2"]),
        ("1/0", ["1", "/", "0"]),
        ("2.3+1", ["2.3", "+", "1"]),
        ("4.5 + 1 * 4.9", ["4.5", "+", "1", "*", "4.9"]),
        ("(23 + 5) * 5", ["(", "23", "+", "5", ")", "*", "5"]),
        ("12*(56+4)", ["12", "*", "(", "56", "+", "4", ")"]),
        ("log3+1", ["log", "3", "+", "1"]),
        ("log(4.1 + 2)", ["log", "(", "4.1", "+", "2", ")"]),
        ("log(1 + 7) + 4", ["log", "(", "1", "+", "7", ")", "+", "4"]))

    def test_valid_expr(self):
        for expr, tokens in self.valid_expr:
            result = calc.tokenize(expr)
            self.assertEqual(tokens, result)

class TokenizeBadInput(unittest.TestCase):
    invalid_expr = (
        "1 1",         # consecutive numbers without operator in the middle
        "1.2.3",       # consecutive numbers without operator in the middle
        "1.2 + 3.2.4", # consecutive numbers without operator in middle
        "1.2.",        # extra dot
        "+",           # binary operator missing both operands
        "3 * ",        # binary operator missing right operand
        " + 2",        # binary operator missing left operand
        "1 + log",     # unary operator missing operand
        "1 & 2",       # invalid operator
        "(",           # unbalanced parentheses
        ")",           # unbalanced parentheses
        "())",         # unbalanced parentheses
        "(1 + 2 * 3",  # unbalanced parentheses
        "1 + 2) * 3")  # unbalanced parentheses

    def test_invalid_expr(self):
        for expr in self.invalid_expr:
            self.assertRaises(calc.InvalidExpressionError, calc.tokenize, expr)

class ToPostFix(unittest.TestCase):
    exprmap = (
        (["1"], deque(["1"])),
        (["_", "1"], deque(["1", "_"])),
        (["_", "_", "2"], deque(["2", "_", "_"])),
        (["log", "2"], deque(["2", "log"])),
        (["log", "_", "3"], deque(["3", "_", "log"])),
        (["log", "(", "_", "5", ")"], deque(["5", "_", "log"])),
        (["log", "(", "1", "+", "2", ")"], deque(["1", "2", "+", "log"])),
        (["log", "_", "1", "+", "2"], deque(["1", "_", "log", "2", "+"])),
        (["1", "/", "2"], deque(["1", "2", "/"])),
        (["2", "*", "3", "-", "1"], deque(["2", "3", "*", "1", "-"])),
        (["1", "+", "2", "*", "3"], deque(["1", "2", "3", "*", "+"])),
        (["2", "*", "3", "/", "4"], deque(["2", "3", "*", "4", "/"])),
        (["(", "2", "*", "3", ")"], deque(["2", "3", "*"])),
        (["log", "(", "2", "*", "3", "+", "7", ")"], deque(["2", "3", "*", "7",
        "+", "log"])))

    def test_postfix(self):
        for infix, postfix in self.exprmap:
            result = calc.topostfix(infix)
            self.assertEqual(postfix, result)

class Eval(unittest.TestCase):
    exprtoval = (
    (deque(["1"]), 1),
    (deque(["2", "_"]), -2),
    (deque(["3", "2", "*"]), 6),
    (deque(["4", ".5", "*"]), 2),
    (deque(["1", "0.5", "/"]), 2),
    (deque(["2", "1", "log", "+"]), 2))

    def test_eval(self):
        for postfix, val in self.exprtoval:
            result = calc.eval(postfix)
            self.assertEqual(val, result)

class Calc(unittest.TestCase):
    exprtoval = (
    ("2", 2),
    ("-7", -7),
    ("log1", 0),
    ("1 + 2", 3),
    ("4.3 * 3.2", 13.76),
    ("7 / 2", 3.5),
    ("log1 + 3", 3),
    ("5*log1", 0),
    ("-log1", 0),
    ("2 + 4 - 1 * 7", -1),
    ("3.5 * 4 / 2", 7),
    ("(1+2)/6", 0.5),
    ("15/(-4 + 7)", 5))

    def test_calc(self):
        for expr, val in self.exprtoval:
            result = calc.calc(expr)
            self.assertEqual(val, result)

if __name__ == "__main__":
    unittest.main()
