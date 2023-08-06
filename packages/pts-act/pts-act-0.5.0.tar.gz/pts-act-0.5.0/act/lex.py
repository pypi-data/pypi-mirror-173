import re
from enum import Enum, auto


class LexError(Exception):
    pass


class Token(Enum):
    TNEWLINE = auto()
    TCOLON = auto()
    TSTRING = auto()
    TINTEGER = auto()
    TBLOCK = auto()
    TLBRACE = auto()
    TRBRACE = auto()
    TLPAREN = auto()
    TRPAREN = auto()
    TSTATEMENT = auto()
    TEQUALS = auto()
    TQUOTE = auto()


RE_LITERAL = re.compile(r'[^\n={} "]')
RE_TSTRING = re.compile(r'[^\n= "]+')
RE_TINTEGER = re.compile(r'[0-9]+')
RE_LINE = re.compile(r'[^\n]*')


class LexedToken:
    def __init__(self, token, value, line, column, rawline):
        self.token = token
        self.value = value
        self.line = line
        self.column = column
        self.rawline = rawline

    def __repr__(self):
        return '<LexedToken {} "{}" at {},{}>'.format(self.token, self.value, self.line, self.column)


def lex_act(data):
    """
    Lex the input act data into the tokens
    :param data: act file as string
    :return: generator that produces LexedToken instances
    """
    pointer = 0
    line = 1
    column = 0
    was_newline = False
    linebuf = None
    while True:
        if linebuf is None:
            linebuf = RE_LINE.match(data[pointer:])[0]
        if pointer == len(data):
            return
        if data[pointer] == ' ' or data[pointer] == '\t':
            pointer += 1
            column += 1
            continue
        elif data[pointer] == '\n':
            if not was_newline:
                yield LexedToken(Token.TNEWLINE, '', line, column, linebuf)
            was_newline = True
            column = 0
            line += 1
            pointer += 1
            linebuf = None
            continue
        if data[pointer] == ':':
            yield LexedToken(Token.TCOLON, ':', line, column, linebuf)
            column += 1
        elif data[pointer] == '{':
            yield LexedToken(Token.TLBRACE, '{', line, column, linebuf)
        elif data[pointer] == '}':
            yield LexedToken(Token.TRBRACE, '}', line, column, linebuf)
        elif data[pointer] == '(':
            yield LexedToken(Token.TLPAREN, "(", line, column, linebuf)
        elif data[pointer] == ')':
            yield LexedToken(Token.TRPAREN, ")", line, column, linebuf)
        elif data[pointer] == '"':
            yield LexedToken(Token.TQUOTE, '"', line, column, linebuf)
        elif data[pointer] == '=' and data[pointer + 1] == '=':
            yield LexedToken(Token.TEQUALS, "==", line, column, linebuf)
            column += 1
            pointer += 1
        elif data[pointer] == '#' and was_newline:
            while data[pointer] != '\n':
                pointer += 1
            line += 1
            pointer += 1
            column = 0
            continue
        elif RE_LITERAL.match(data[pointer]):
            part = RE_TSTRING.match(data[pointer:])[0]
            if part[-1] == ':':
                part = part[:-1]
            yield LexedToken(Token.TSTRING, part, line, column, linebuf)
            column += len(part) - 1
            pointer += len(part) - 1
        elif data[pointer].isdigit():
            part = RE_TINTEGER.search(data[pointer:])[0]
            yield LexedToken(Token.TINTEGER, part, line, column, linebuf)
            column += len(part) - 1
            pointer += len(part) - 1
        elif data[pointer] == '=':
            yield LexedToken(Token.TSTRING, '=', line, column, linebuf)
        else:
            raise LexError("Parse error at {},{}: got '{}'".format(line, column, data[pointer]))
        was_newline = False
        pointer += 1
        column += 1


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='File to lex')
    args = parser.parse_args()
    with open(args.file) as handle:
        raw = handle.read()
    for token in lex_act(raw):
        print(token)
