from my_lexer import Lexer
import my_error
import sys


# -l
# -p

def lexer_test(quantity):
    i = 1
    while i <= quantity:
        print("Тест №" + str(i))
        test_name = 'tests/test_' + i.__str__() + '.txt'
        answer_name = 'tests/answer_' + i.__str__() + '.txt'
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


if __name__ == "__main__":
    for param in sys.argv:
        if param == '-l':
            lexer_test(5)
