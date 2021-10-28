from parse_expr.parser_expr_node.expr_node import ExprNode


class RealNode(ExprNode):
    def __init__(self, token):
        self.token = token

    def get_value(self):
        return self.token.get_value()

    def print(self, priority=None):
        return str(self.token.get_value())
