import unittest
import calc

class TokenizeBadInput(unittest.TestCase):
    invalid_expr = (
        "1 1",         # consecutive numbers without operator in middle
        "+",           # binary operator missing both operands
        "3 * ",        # binary operator missing right operand
        " + 2",        # binary operator missing left operand
        "1 + log",     # unary operator missing operand
        "1 / 0",       # divide by zero
        "1 & 2",       # invalid operator
        "(",           # unbalanced parentheses
        ")",           # unbalanced parentheses
        "())",         # unbalanced parentheses
        "(1 + 2 * 3",  # unbalanced parentheses
        "1 + 2) * 3") # unbalanced parentheses

    def test_invalid_expression(self):
        for expr in self.invalid_expr:
            self.assertRaises(calc.InvalidExpression, calc.tokenize, expr)

if __name__ == "__main__":
    unittest.main()
