from my_token import Token
from my_error import LexerException


class Lexer:
    coord: [2]
    curr_token: Token
    curr_symbol: bytes
    keywords = {'begin', 'var', 'function', 'end', 'integer', 'real', 'if', 'else', 'then', 'else', 'array', 'case',
                'const', 'downto', 'file', 'for', 'goto', 'label', 'of', 'packed', 'procedure', 'program', 'record',
                'repeat', 'set', 'to', 'type', 'until', 'while', 'with'}
    separators = {'(', ')', ':', '.', ',', '..', ';'}
    operations = {'+', '@', '^', '.', 'in', '()', '[]'}
    binOperations = {'-', '/', '*', '=', '>', '<', 'div', '<=', '>=', '<>', 'and', ':=', 'not', 'or', 'shl', 'shr',
                     'xor', 'mod'}

    def __init__(self, filestream):
        self.filestream = filestream
        self.coord = [0, 0]
        self.get_symbol()

    def set_token_value(self):
        if self.curr_token.type == 'real':
            self.curr_token.value = float(self.curr_token.src)
            if self.curr_token.value > 1.7e308:
                raise LexerException(self.coord.__str__() + 'real number value error')
        elif self.curr_token.type == 'integer':
            self.curr_token.value = int(self.curr_token.src)
        elif self.curr_token.type == 'identf':
            self.curr_token.value = self.curr_token.src.lower()
        else:
            self.curr_token.value = self.curr_token.src

    def get_next(self) -> Token:
        self.lexer_analize()
        self.set_token_value()
        self.curr_token.coord[1] -= 1
        return self.curr_token

    def get_curr_token(self):
        return self.curr_token

    def get_symbol(self):
        self.coord[1] += 1
        self.curr_symbol = self.filestream.read(1)
        return self.curr_symbol

    def get_identf(self):
        self.curr_token.src += str(self.curr_symbol)[2]
        self.curr_token.type = 'identf'
        self.get_symbol()
        while str(self.curr_symbol)[2].isalnum() or str(self.curr_symbol)[2] == '_':
            self.curr_token.src += str(self.curr_symbol)[2]
            self.get_symbol()
        if self.curr_token.src in self.keywords:
            self.curr_token.type = 'keyword'
        elif self.curr_token.src in self.operations:
            self.curr_token.type = 'operator'
        elif len(self.curr_token.src) > 64:
            self.curr_token.type = 'error'
            raise LexerException(self.coord.__str__() + " too long identificator size")

    def get_new_line(self):
        self.get_symbol()
        self.get_symbol()
        self.coord[0] += 1
        self.coord[1] = 1

    def get_number(self):
        e_flag = False
        point_flag = False
        op_flag = False
        self.curr_token.type = 'integer'
        while str(self.curr_symbol)[2].isnumeric() or str(self.curr_symbol)[2] == '.' \
                or str(self.curr_symbol)[2].lower() == 'e' or str(self.curr_symbol)[2] == '-'\
                or str(self.curr_symbol)[2] == '+':
            self.curr_token.src += str(self.curr_symbol)[2]
            if str(self.curr_symbol)[2] == 'e':
                if e_flag:
                    self.curr_token.type = 'error'
                    raise LexerException(self.coord.__str__() +" Lexical error " + self.curr_token.src)
                self.curr_token.type = 'real'
                e_flag = True
            if str(self.curr_symbol)[2] == '.':
                if point_flag or e_flag:
                    self.curr_token.type = 'error'
                    raise LexerException(self.coord.__str__() +" Lexical error " + self.curr_token.src)
                self.curr_token.type = 'real'
                point_flag = True
            if str(self.curr_symbol)[2] == '-' or str(self.curr_symbol)[2] == '+':
                if e_flag and not op_flag:
                    op_flag = True
                else:
                    self.curr_token.type = 'error'
                    raise LexerException(self.coord.__str__() +" Lexical error " + self.curr_token.src)
            self.get_symbol()
        else:
            if str(self.curr_symbol)[2].isalpha():
                self.curr_token.type = 'error'
            return

    def lexer_analize(self):
        if self.curr_symbol == b'':
            self.curr_token.type = 'EOF'
            self.get_symbol()
            return

        if str(self.curr_symbol)[2] == "{":
            while str(self.curr_symbol)[2] != "}":
                self.get_symbol()
                if self.curr_symbol == b'':
                    raise LexerException(self.coord.__str__() + "Unexpected EOF")
            self.get_symbol()

        while self.curr_symbol == b'\r' or self.curr_symbol == b'\n':
            self.get_new_line()

        self.curr_token = Token(self.coord.copy(), '', '', '')

        if str(self.curr_symbol)[2].isalpha():
            self.get_identf()
            return

        if str(self.curr_symbol)[2].isnumeric():
            self.get_number()
            return

        if str(self.curr_symbol)[2] in self.separators:
            self.curr_token.type = 'separator'
            self.curr_token.src += str(self.curr_symbol)[2]
            self.get_symbol()
            return

        if str(self.curr_symbol)[2] in self.operations or str(self.curr_symbol)[2] in self.binOperations:
            self.curr_token.type = 'operator'
            self.curr_token.src += str(self.curr_symbol)[2]
            self.get_symbol()
            return

        if str(self.curr_symbol)[2] == ' ':
            self.curr_token.type = 'space'
            self.curr_token.src += str(self.curr_symbol)[2]
            self.get_symbol()
            while str(self.curr_symbol)[2] == ' ':
                self.curr_token.src += str(self.curr_symbol)[2]
                self.get_symbol()
            return

        if str(self.curr_symbol)[2] == "'":
            self.curr_token.type = 'string literal'
            self.curr_token.src += str(self.curr_symbol)[2]
            self.get_symbol()
            while str(self.curr_symbol)[2] != "'":
                self.curr_token.src += str(self.curr_symbol)[2]
                self.get_symbol()
            self.curr_token.src += str(self.curr_symbol)[2]
            self.get_symbol()
            return

