from parse_expr.parser_expr_node.expr_node import ExprNode
from my_token import Token


class IdentfNode(ExprNode):
    def __init__(self, token):
        self.token = token

    def get_value(self):
        return self.token.get_value() if isinstance(self.token, Token) else self.token.print()

    def print(self, priority=1):
        return str(self.token.get_value() if isinstance(self.token, Token) else self.token.print(priority))