from abc import ABC, abstractmethod
from parse_expr.parser_expr_node.node import Node


class ExprNode(Node, ABC):
    @abstractmethod
    def print(self):
        pass

    @abstractmethod
    def get_value(self):
        pass
