import unittest
import calc

class TokenizeValidInput(unittest.TestCase):
    valid_expr = (
        ("", []),
        ("()", ["(", ")"]),
        ("(())", ["(", "(", ")", ")"]),
        ("()()", ["(", ")", "(", ")"]),
        ("1", ["1"]),
        ("5.84", ["5.84"]),
        ("-1", ["_", "1"]), # unary negation is represented as _
        ("log 14", ["log", "14"]),
        ("log(3)", ["log", "(", "3", ")"]),
        ("log(-1)", ["log", "(", "_", "1", ")"]),
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
        "1.2.",
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

if __name__ == "__main__":
    unittest.main()
