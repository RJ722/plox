import lox
from lox.scanner import Scanner
from lox.tokentype import TokenType
from lox.token import Token

from . import l

def get_tokens(code, l):
    return Scanner(code, l).scan_tokens()

def check_tokens(result, expected):
    ''' result: [Token*]
        expected: [TokenType*]
    '''
    assert len(result) == len(expected)
    for i in range(len(result)):
        assert result[i].tokentype == expected[i]

def _check(tfn, l):
    code, expected = tfn(l)
    expected.append(TokenType.EOF)
    tokens = get_tokens(code, l)
    check_tokens(tokens, expected)

def raises_no_error(tfn):
    def inner(l):
        _check(tfn, l)
        assert l.had_error == False
    return inner

def raises_error(tfn):
    def inner(l):
        _check(tfn, l)
        assert l.had_error == True
    return inner

@raises_no_error
def test_empty(l):
    code = ''
    expected = []
    return code, expected

@raises_no_error
def test_print(l):
    code = 'print 1 + 2;'
    expected = [
        TokenType.PRINT, TokenType.NUMBER, TokenType.PLUS, TokenType.NUMBER,
        TokenType.SEMICOLON]
    return code, expected

@raises_no_error
def test_print_print(l):
    code = 'print "print a + b";'
    expected = [TokenType.PRINT, TokenType.STRING, TokenType.SEMICOLON]
    return code, expected

@raises_error
def test_underscore(l):
    code = '_'
    expected = []
    return code, expected

@raises_error
def test_single_quotes(l):
    code = "''"
    expected = []
    return code, expected

@raises_error
def test_unexpected_in_middle(l):
    code = """\
class
fun
@
{}
()
"""
    expected = [
        TokenType.CLASS, TokenType.FUN, TokenType.LEFT_BRACE,
        TokenType.RIGHT_BRACE, TokenType.LEFT_PAREN, TokenType.RIGHT_PAREN
    ]
    return code, expected

@raises_no_error
def test_keywords(l):
    code = """\
and
class
else
false
fun
for
if
nil
or
print
return
super
this
true
var
while
"""
    expected = [
        TokenType.AND, TokenType.CLASS, TokenType.ELSE, TokenType.FALSE,
        TokenType.FUN, TokenType.FOR, TokenType.IF, TokenType.NIL, TokenType.OR,
        TokenType.PRINT, TokenType.RETURN, TokenType.SUPER, TokenType.THIS,
        TokenType.TRUE, TokenType.VAR, TokenType.WHILE]
    return code, expected

@raises_no_error
def test_symbols(l):
    code = """\
()
{}
,.
-+
;
/*
!
!=
==
=
>
>=
<
<=
"""
    expected = [
        TokenType.LEFT_PAREN, TokenType.RIGHT_PAREN, TokenType.LEFT_BRACE,
        TokenType.RIGHT_BRACE, TokenType.COMMA, TokenType.DOT, TokenType.MINUS,
        TokenType.PLUS, TokenType.SEMICOLON, TokenType.SLASH, TokenType.STAR,
        TokenType.BANG, TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL,
        TokenType.EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL,
        TokenType.LESS, TokenType.LESS_EQUAL]
    return code, expected

@raises_no_error
def test_tricky_double_symbols(l):
    code = """\
!!!=
== ====
===
<<=
<>=
<=>
"""
    expected = [
        TokenType.BANG, TokenType.BANG, TokenType.BANG_EQUAL,
        TokenType.EQUAL_EQUAL, TokenType.EQUAL_EQUAL, TokenType.EQUAL_EQUAL,
        TokenType.EQUAL_EQUAL, TokenType.EQUAL, TokenType.LESS,
        TokenType.LESS_EQUAL, TokenType.LESS, TokenType.GREATER_EQUAL,
        TokenType.LESS_EQUAL, TokenType.GREATER]
    return code, expected

@raises_no_error
def test_multiline_strings(l):
    code = """\
"This is a
multi line
string"

"Lox allows
multi-line strings
because they are cool.



"
"""
    expected = [TokenType.STRING, TokenType.STRING]
    return code, expected

@raises_no_error
def test_ignore_comments(l):
    code = "// This is a comment"
    expected = []
    return code, expected

@raises_no_error
def test_ignore_inline_comments(l):
    code = "var a = 1; // Ignore me!"
    expected = [TokenType.VAR, TokenType.IDENTIFIER, TokenType.EQUAL,
    TokenType.NUMBER, TokenType.SEMICOLON]
    return code, expected
