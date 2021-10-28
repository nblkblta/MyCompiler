from my_lexer import Lexer
import my_error
import sys
from my_parser import ParserExpr

# -l
# -p


def lexer_test(quantity):
    i = 1
    while i <= quantity:
        print(f"Тест № {i}")
        test_name = f'lexer_tests/test_{i}.txt'
        answer_name = f'lexer_tests/answer_{i}.txt'
        test = open(test_name, 'br')
        answer = open(answer_name, 'r')
        lexer = Lexer(test)
        answers = answer.read().split('\n')
        i += 1
        j = -1
        error_count = 0
        try:
            token = lexer.get_next()
            while token.type != 'EOF':
                j += 1
                if f'{token.get_str()}' != answers[j]:
                    print(f'ошибка -  {token.get_str()} {answers[j]}')
                    error_count += 1
                token = lexer.get_next()
        except my_error.LexerException as error:
            j += 1
            if f'{error}' != answers[j]:
                print(f'ошибка - {error} {answers[j]}')
                error_count += 1
        test.close()
        answer.close()


def parser_test(quantity):
    i = 1
    while i <= quantity:
        print(f"Тест № {i}")
        test_name = f'parser_tests/test_{i}.txt'
        answer_name = f'parser_tests/answer_{i}.txt'
        test = open(test_name, 'br')
        answer = open(answer_name, 'r')
        lexer = Lexer(test)
        lexer.get_next()
        parser = ParserExpr(lexer)
        i += 1
        try:
            out = parser.parseExpr().print()
            for sym in out:
                sym_answ = answer.read(1)
                if sym != sym_answ:
                    print(f"ошибка {sym} {sym_answ}")
                    print(out)
        except my_error.CompilerException as error:
            print(f'{error}')
        test.close()
        answer.close()


if __name__ == "__main__":
    for param in sys.argv:
        if param == '-l':
            lexer_test(9)
        if param == '-p':
            parser_test(3)
