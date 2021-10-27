from my_lexer import Lexer
import my_error
import sys
from my_parser import ParserExpr

# -l
# -p


def lexer_test(quantity):
    i = 1
    while i <= quantity:
        print("Тест №" + str(i))
        test_name = 'lexer_tests/test_' + i.__str__() + '.txt'
        answer_name = 'lexer_tests/answer_' + i.__str__() + '.txt'
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
                if token.get_str() != answers[j]:
                    print('ошибка - ' + token.get_str() + ',' + answers[j])
                    error_count += 1
                token = lexer.get_next()
        except my_error.LexerException as error:
            j += 1
            if error.__str__() != answers[j]:
                print('ошибка - ' + error.__str__() + ',' + answers[j])
                error_count += 1
        test.close()
        answer.close()


def parser_test(quantity):
    i = 1
    while i <= quantity:
        print("Тест №" + str(i))
        test_name = 'parser_tests/test_' + i.__str__() + '.txt'
        answer_name = 'parser_tests/answer_' + i.__str__() + '.txt'
        test = open(test_name, 'br')
        answer = open(answer_name, 'r')
        lexer = Lexer(test)
        lexer.get_next()
        parser = ParserExpr(lexer)
        i += 1
        j = -1
        error_count = 0
        try:
            print(parser.parseExpr().print())
        except my_error.CompilerException as error:
            print(error.__str__())
        test.close()
        answer.close()


if __name__ == "__main__":
    for param in sys.argv:
        if param == '-l':
            lexer_test(6)
        if param == '-p':
            parser_test(1)
