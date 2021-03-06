from parse_expr.parser_expr_node.expr_node import ExprNode


class UnOpNode(ExprNode):
    def __init__(self, operation, operand):
        self.operation = operation
        self.operand = operand

    def print(self, priority=None):
        return f"{self.operation.get_value()}{self.operand.get_value()}"

    def get_value(self):
        pass