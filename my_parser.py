from my_lexer import Lexer
from parse_expr.parser_expr_node.bin_operation_node import BinOpNode
from parse_expr.parser_expr_node.int_node import IntNode
from parse_expr.parser_expr_node.real_node import RealNode
from parse_expr.parser_expr_node.un_operation_node import UnOpNode
from parse_expr.parser_expr_node.identf_node import IdentfNode
from my_error import CompilerException


class ParserExpr:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer

    bin_operations = {'-', '/', '*', '=', '>', '<', 'div', '<=', '>=', '<>', 'and', ':=', 'not', 'or', 'shl', 'shr',
                     'xor', 'mod'}
    def parseExpr(self):
        token = self.lexer.get_curr_token()
        if not token.get_type() != "EOF" or token.get_value() == ';':
            raise CompilerException(f"{token.get_coord()} Expected expression")
        left = self.parseTerm()
        operation = self.lexer.get_curr_token()
        while operation.get_value() == "+" or operation.get_value() == "-":
            self.lexer.get_next()
            right = self.parseTerm()
            left = BinOpNode(operation, left, right)
            operation = self.lexer.get_curr_token()
        return left

    def parseTerm(self):
        left = self.parseFactor()
        operation = self.lexer.get_curr_token()
        while operation.get_value() in self.bin_operations:
            self.lexer.get_next()
            right = self.parseFactor()
            left = BinOpNode(operation, left, right)
            operation = self.lexer.get_curr_token()
        return left

    def parseFactor(self):
        token = self.lexer.get_curr_token()
        self.lexer.get_next()
        if token.get_type() == "identf":
            return IdentfNode(token)
        if token.get_type() == 'integer':
            return IntNode(token)
        if token.get_type() == 'real':
            return RealNode(token)
        if token.get_value() == "+" or token.get_value() == "-":
            operand = self.parseFactor()
            return UnOpNode(token, operand)
        if token.get_value() == "(":
            left = self.parseExpr()
            token = self.lexer.get_curr_token()
            if token.get_value() != ")":
                raise CompilerException(f"{token.getCoordinates()}')' was expected")
            self.lexer.get_next()
            return left
        raise CompilerException(f'{token.getCoordinates()} Unexpected "{token.getCode()}"')
