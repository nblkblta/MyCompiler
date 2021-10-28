from my_token import Token
from my_error import LexerException
from my_type import LexemType

class Lexer:
    coord: [2]
    curr_token: Token
    curr_symbol: bytes
    keywords = {'begin', 'var', 'function', 'end', 'integer', 'real', 'if', 'else', 'then', 'else', 'array', 'case',
                'const', 'downto', 'file', 'for', 'goto', 'label', 'of', 'packed', 'procedure', 'program', 'record',
                'repeat', 'set', 'to', 'type', 'until', 'while', 'with'}
    separators = {'(', ')', ':', ',', '..', ';'}
    operations = {'+', '@', '^', '.', 'in', '-', '/', '*', '=', '>', '<', 'div', '<=', '>=', '<>', 'and', ':=', 'not',
                  'or', 'shl', 'shr', 'xor', 'mod'}

    def __init__(self, filestream):
        self.filestream = filestream
        self.coord = [0, 0]
        self.get_symbol()

    def error(self, message):
        raise LexerException(f'{self.coord} {message} {self.curr_token.src}')

    def set_token_value(self):
        if self.curr_token.type == LexemType.REAL:
            self.curr_token.value = float(self.curr_token.src)
            if self.curr_token.value > 1.7e308:
                self.error("too big real number")
        elif self.curr_token.type == LexemType.INT:
            self.curr_token.value = int(self.curr_token.src)
            if self.curr_token.value > 32767:
                self.error('integer number value error')
        elif self.curr_token.type == LexemType.INT16:
            self.curr_token.value = int(self.curr_token.src[1:], 16)
            self.curr_token.type = LexemType.INT
            if self.curr_token.value > 32767:
                self.error('integer number value error')
        elif self.curr_token.type == LexemType.INT8:
            self.curr_token.value = int(self.curr_token.src[1:], 8)
            self.curr_token.type = LexemType.INT
            if self.curr_token.value > 32767:
                self.error('integer number value error')
        elif self.curr_token.type == LexemType.INT2:
            self.curr_token.value = int(self.curr_token.src[1:], 2)
            self.curr_token.type = LexemType.INT
            if self.curr_token.value > 32767:
                self.error('integer number value error')
        elif self.curr_token.type == LexemType.IDENTF:
            self.curr_token.value = self.curr_token.src.lower()
        elif self.curr_token.type == LexemType.STRING:
            pass
        else:
            self.curr_token.value = self.curr_token.src

    def get_next(self):
        self.lexer_analyse()
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
        self.curr_token.src += self.get_curr_sym()
        self.curr_token.type = LexemType.IDENTF
        self.get_symbol()
        while self.get_curr_sym().isalnum() or self.get_curr_sym() == '_':
            self.curr_token.src += self.get_curr_sym()
            self.get_symbol()
        if self.curr_token.src in self.keywords:
            self.curr_token.type = LexemType.KEYWORD
        elif self.curr_token.src in self.operations:
            self.curr_token.type = LexemType.OPERATOR
        elif len(self.curr_token.src) > 64:
            self.error("too long identificator size")

    def get_new_line(self):
        self.get_symbol()
        self.get_symbol()
        self.coord[0] += 1
        self.coord[1] = 1

    def get_real_number(self):
        e_flag = False
        point_flag = False
        sign_flag = False
        self.curr_token.type = LexemType.REAL
        while self.get_curr_sym().isnumeric( ) or self.get_curr_sym().lower() == 'e' \
                or self.get_curr_sym() in {'.', '-', '+'}:
            if self.get_curr_sym().lower() == 'e':
                if e_flag:
                    self.error("Lexical error real number e ")
                e_flag = True
                self.curr_token.src += self.get_curr_sym()
                self.get_symbol()
                if self.get_curr_sym() not in {"+", "-"} and not self.get_curr_sym().isnumeric():
                    self.error("Lexical error real number +- ")
            elif self.get_curr_sym() == '.':
                if point_flag or e_flag:
                    self.error("Lexical error real number point")
                point_flag = True
            elif self.get_curr_sym() in {'+', '-'}:
                if not e_flag:
                    break
                if sign_flag:
                    self.error("unexpected sign")
                sign_flag = True
            self.curr_token.src += self.get_curr_sym()
            self.get_symbol()
        if self.get_curr_sym().isalpha():
            self.error('Unexpected alpha after number')
        return

    def get_number(self):
        self.curr_token.type = LexemType.INT
        while self.get_curr_sym().isnumeric():
            self.curr_token.src += self.get_curr_sym()
            self.get_symbol()
            if self.get_curr_sym() == 'e' or self.get_curr_sym() == '.':
                self.get_real_number()
                return
        if self.get_curr_sym().isalpha():
            self.error("Unexpected symbol")
        return

    def get_ctrl_symbol(self):
        self.curr_token.src += self.get_curr_sym()
        self.curr_token.type = LexemType.STRING
        buf = ''
        self.get_symbol()
        while self.get_curr_sym().isnumeric():
            self.curr_token.src += self.get_curr_sym()
            buf += self.get_curr_sym()
            self.get_symbol()
        if len(buf) == 0:
            self.error('Empty control symbol')
        self.curr_token.value += chr(int(buf))
        if self.curr_symbol == b'\r':
            return
        elif self.get_curr_sym() == '#':
            self.get_ctrl_symbol()
            return
        elif self.get_curr_sym() == "'":
            self.get_string()
            return
        else:
            self.error('Unexpected symbol')

    def get_string(self):
        self.curr_token.type = LexemType.STRING
        self.curr_token.src += self.get_curr_sym()
        self.get_symbol()
        while self.get_curr_sym() != "'":
            if self.curr_symbol == b'\r':
                self.error('Unexpected end of line')
            self.curr_token.src += self.get_curr_sym()
            self.curr_token.value += self.get_curr_sym()
            self.get_symbol()
        self.curr_token.src += self.get_curr_sym()
        self.get_symbol()
        if self.get_curr_sym() == '#':
            self.get_ctrl_symbol()

    def get_curr_sym(self):
        return str(self.curr_symbol)[2]

    def get_int16(self):
        self.curr_token.type = LexemType.INT16
        self.curr_token.src += self.get_curr_sym()
        self.get_symbol()
        while self.get_curr_sym().isnumeric() or ("a" <= self.get_curr_sym().lower() <= "f"):
            self.curr_token.src += self.get_curr_sym()
            self.get_symbol()
        if self.get_curr_sym() > "f":
            self.error("Unexpected numeric symbol")

    def get_int8(self):
        self.curr_token.type = LexemType.INT8
        self.curr_token.src += self.get_curr_sym()
        self.get_symbol()
        while self.get_curr_sym().isnumeric():
            if int(self.get_curr_sym()) > 7:
                self.error("Unexpected numeric symbol")
            self.curr_token.src += self.get_curr_sym()
            self.get_symbol()
        if self.get_curr_sym().isalpha():
            self.error("Unexpected numeric symbol")

    def get_int2(self):
        self.curr_token.type = LexemType.INT2
        self.curr_token.src += self.get_curr_sym()
        self.get_symbol()
        while self.get_curr_sym() in {'0', '1'}:
            self.curr_token.src += self.get_curr_sym()
            self.get_symbol()
        if self.get_curr_sym().isalpha():
            self.error("Unexpected numeric symbol")

    def get_separator(self):
        self.curr_token.type = LexemType.SEPARATOR
        self.curr_token.src += self.get_curr_sym()
        self.get_symbol()

    def get_multiline_comment(self):
        while self.get_curr_sym() != "}":
            self.get_symbol()
            while self.curr_symbol == b'\r' or self.curr_symbol == b'\n':
                self.get_new_line()
            if self.curr_symbol == b'':
                self.error("Unexpected EOF")
        self.get_symbol()

    def lexer_analyse(self):
        while True:
            if self.get_curr_sym() == ' ':
                self.get_symbol()
                while self.get_curr_sym() == ' ':
                    self.get_symbol()

            while self.curr_symbol == b'\r' or self.curr_symbol == b'\n':
                self.get_new_line()

            if self.get_curr_sym() == "{":
                self.get_multiline_comment()

            self.curr_token = Token(self.coord.copy(), '', '', '')

            if self.get_curr_sym() == '/':
                self.curr_token.type = "operator"
                self.curr_token.src += self.get_curr_sym()
                self.get_symbol()
                if self.get_curr_sym() == '/':
                    while self.curr_symbol != b'\r':
                        self.get_symbol()
                    self.get_new_line()

            if self.curr_symbol == b'':
                self.curr_token.type = 'EOF'
                self.get_symbol()
                break

            if self.get_curr_sym().isalpha():
                self.get_identf()
                break

            if self.get_curr_sym().isnumeric():
                self.get_number()
                break

            if self.get_curr_sym() == "&":
                self.get_int8()
                break

            if self.get_curr_sym() == "%":
                self.get_int2()
                break

            if self.get_curr_sym() == "$":
                self.get_int16()
                break

            if self.get_curr_sym() in {'<', '>'}:
                self.curr_token.type = LexemType.OPERATOR
                self.curr_token.src += self.get_curr_sym()
                self.get_symbol()
                if self.get_curr_sym() == '=':
                    self.curr_token.src += self.get_curr_sym()
                    self.get_symbol()
                    break
                elif self.get_curr_sym() == '>':
                    self.curr_token.src += self.get_curr_sym()
                    self.get_symbol()
                    break
                break

            if self.get_curr_sym() == ':':
                self.curr_token.src += self.get_curr_sym()
                self.curr_token.type = LexemType.SEPARATOR
                self.get_symbol()
                if self.get_curr_sym() == '=':
                    self.curr_token.type = LexemType.OPERATOR
                    self.curr_token.src += self.get_curr_sym()
                    self.get_symbol()
                    break
                else:
                    break

            if self.get_curr_sym() in self.separators:
                self.get_separator()
                break

            if self.get_curr_sym() in self.operations:
                self.curr_token.type = LexemType.OPERATOR
                self.curr_token.src += self.get_curr_sym()
                self.get_symbol()
                break

            if self.get_curr_sym() == "'":
                self.get_string()
                break

            if self.get_curr_sym() == "#":
                self.get_ctrl_symbol()
                break
