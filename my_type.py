from enum import Enum


class LexemType(Enum):
    IDENTF = "identf"
    INT = "integer"
    REAL = "real"
    STRING = "string"
    SEPARATOR = "separator"
    OPERATOR = "operator"
    EOF = "EOF"
    INT2 = "int2"
    INT8 = "int8"
    INT16 = "int15"
    KEYWORD = "keyword"
