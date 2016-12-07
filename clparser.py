#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CAVEAT UTILITOR
#
# This file was automatically generated by Grako.
#
#    https://pypi.python.org/pypi/grako/
#
# Any changes you make to it will be overwritten the next time
# the file is generated.


from __future__ import print_function, division, absolute_import, unicode_literals

from grako.buffering import Buffer
from grako.parsing import graken, Parser
from grako.util import re, RE_FLAGS, generic_main  # noqa


__all__ = [
    'UnknownParser',
    'UnknownSemantics',
    'main'
]

KEYWORDS = set([])


class UnknownBuffer(Buffer):
    def __init__(
        self,
        text,
        whitespace=None,
        nameguard=None,
        comments_re=None,
        eol_comments_re=None,
        ignorecase=None,
        namechars='',
        **kwargs
    ):
        super(UnknownBuffer, self).__init__(
            text,
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            namechars=namechars,
            **kwargs
        )


class UnknownParser(Parser):
    def __init__(
        self,
        whitespace=None,
        nameguard=None,
        comments_re=None,
        eol_comments_re=None,
        ignorecase=None,
        left_recursion=False,
        parseinfo=True,
        keywords=None,
        namechars='',
        buffer_class=UnknownBuffer,
        **kwargs
    ):
        if keywords is None:
            keywords = KEYWORDS
        super(UnknownParser, self).__init__(
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            left_recursion=left_recursion,
            parseinfo=parseinfo,
            keywords=keywords,
            namechars=namechars,
            buffer_class=buffer_class,
            **kwargs
        )

    @graken()
    def _alpha_(self):
        self._pattern(r'[a-zA-Z]')

    @graken()
    def _alphanumeric_(self):
        self._pattern(r'[a-zA-Z0-9]')

    @graken()
    def _numeric_(self):
        self._pattern(r'[0-9]+')

    @graken()
    def _word_(self):
        self._pattern(r'[a-zA-z][a-zA-Z0-9]*')

    @graken()
    def _operator_(self):
        with self._choice():
            with self._option():
                self._token('+')
            with self._option():
                self._token('-')
            with self._option():
                self._token('*')
            with self._option():
                self._token('/')
            with self._option():
                self._token(':=')
            with self._option():
                self._token('==')
            with self._option():
                self._token('!=')
            with self._option():
                self._token('>=')
            with self._option():
                self._token('<=')
            with self._option():
                self._token('>')
            with self._option():
                self._token('<')
            self._error('expecting one of: != * + - / := < <= == > >=')

    @graken()
    def _ascii_(self):
        with self._optional():
            with self._choice():
                with self._option():
                    self._token('?')
                with self._option():
                    self._token('!')
                with self._option():
                    self._token('.')
                with self._option():
                    self._token("'")
                with self._option():
                    self._token(' ')
                with self._option():
                    self._token('\\n')
                with self._option():
                    self._token('$')
                self._error("expecting one of:   ! $ ' . ? \\n")

    @graken()
    def _W_(self):

        def block0():
            with self._choice():
                with self._option():
                    self._token('\t')
                with self._option():
                    self._token(' ')
                self._error('expecting one of: \t  ')
        self._closure(block0)

    @graken()
    def _NW_(self):

        def block0():
            with self._choice():
                with self._option():
                    self._token('\n')
                with self._option():
                    self._W_()
                self._error('expecting one of: \n')
        self._closure(block0)

    @graken()
    def _var_name_(self):
        self._word_()
        with self._optional():
            self._token('[')
            self._value_()
            self._token(']')

    @graken()
    def _literal_(self):
        with self._choice():
            with self._option():
                with self._group():
                    self._numeric_()
                    with self._optional():
                        self._token('.')
                        self._numeric_()
            with self._option():
                with self._group():
                    self._token('"')
                    self._alphanumeric_()
                    self._token('"')
            with self._option():
                self._token('True')
            with self._option():
                self._token('False')
            with self._option():
                self._token('[')
                self._W_()
                self._value_()

                def block0():
                    self._W_()
                    self._token(',')
                    self._W_()
                    self._value_()
                    self._W_()
                self._closure(block0)
                self._W_()
                self._token(']')
                self._W_()
            with self._option():
                self._token('"')
                self._ascii_()
                self._token('"')
            self._error('expecting one of: False True')

    @graken()
    def _type_keyword_(self):
        with self._choice():
            with self._option():
                self._token('int')
            with self._option():
                self._token('char')
            with self._option():
                self._token('bool')
            with self._option():
                self._token('float')
            self._error('expecting one of: bool char float int')

    @graken()
    def _type_declaration_(self):
        self._W_()
        self._type_keyword_()
        self._W_()
        self._var_name_()
        self._W_()
        with self._optional():
            self._token(':=')
            self._W_()
            self._value_()
        self._W_()
        self._token('\n')

    @graken()
    def _expression_(self):
        self._W_()
        self._token('(')
        self._W_()
        self._value_()
        self._W_()
        self._operator_()
        self._W_()
        self._value_()
        self._W_()
        self._token(')')
        self._W_()

    @graken()
    def _value_(self):
        with self._choice():
            with self._option():
                self._literal_()
            with self._option():
                self._expression_()
            with self._option():
                self._var_name_()
            self._error('no available options')

    @graken()
    def _assignment_(self):
        self._W_()
        self._var_name_()
        self._W_()
        self._token(':=')
        self._W_()
        with self._group():
            with self._choice():
                with self._option():
                    self._function_call_()
                with self._option():
                    self._value_()
                self._error('no available options')
        self._NW_()

    @graken()
    def _function_definition_(self):
        self._W_()
        self._token('def ')
        self._type_keyword_()
        self._W_()
        self._var_name_()
        self._W_()
        self._token('(')
        self._W_()
        with self._optional():
            self._type_keyword_()
            self._W_()
            self._var_name_()
            self._W_()

            def block0():
                self._token(',')
                self._W_()
                self._type_keyword_()
                self._W_()
                self._var_name_()
                self._W_()
            self._closure(block0)
        self._W_()
        self._token(')')
        self._W_()
        with self._optional():
            self._token('\n')
        self._block_()

    @graken()
    def _function_call_(self):
        self._W_()
        self._var_name_()
        self._W_()
        self._token('(')
        self._W_()
        with self._optional():
            self._value_()
            self._W_()

            def block0():
                self._W_()
                self._token(',')
                self._W_()
                self._value_()
            self._closure(block0)
        self._W_()
        self._token(')')
        self._NW_()

    @graken()
    def _condition_statement_(self):
        self._W_()
        self._token('if')
        self._W_()
        self._value_()
        self._NW_()
        self._block_()
        self._NW_()

    @graken()
    def _loop_statement_(self):
        self._W_()
        self._token('while')
        self._W_()
        self._value_()
        self._NW_()
        self._block_()
        self._NW_()

    @graken()
    def _control_statement_(self):
        with self._choice():
            with self._option():
                self._condition_statement_()
            with self._option():
                self._loop_statement_()
            self._error('no available options')

    @graken()
    def _block_(self):
        self._token('{')
        self._NW_()

        def block0():
            with self._choice():
                with self._option():
                    self._function_call_()
                with self._option():
                    self._type_declaration_()
                with self._option():
                    self._assignment_()
                with self._option():
                    self._control_statement_()
                with self._option():
                    self._function_definition_()
                self._error('no available options')
        self._closure(block0)
        self._NW_()
        self._token('}')
        self._NW_()

    @graken()
    def _program_(self):
        self._token('@@@')

        def block0():
            self._token('\n')
        self._closure(block0)

        def block1():
            with self._choice():
                with self._option():
                    self._function_definition_()
                with self._option():
                    self._type_declaration_()
                with self._option():
                    self._expression_()
                with self._option():
                    self._assignment_()
                with self._option():
                    self._function_call_()
                with self._option():
                    self._control_statement_()
                with self._option():
                    self._block_()
                self._error('no available options')
        self._closure(block1)

        def block3():
            self._token('\n')
        self._closure(block3)
        self._token('@@@')

    @graken()
    def _comment_(self):
        self._token('#')

        def block0():
            self._pattern(r'.')
        self._closure(block0)
        self._pattern(r'$')


class UnknownSemantics(object):
    def alpha(self, ast):
        return ast

    def alphanumeric(self, ast):
        return ast

    def numeric(self, ast):
        return ast

    def word(self, ast):
        return ast

    def operator(self, ast):
        return ast

    def ascii(self, ast):
        return ast

    def W(self, ast):
        return ast

    def NW(self, ast):
        return ast

    def var_name(self, ast):
        return ast

    def literal(self, ast):
        return ast

    def type_keyword(self, ast):
        return ast

    def type_declaration(self, ast):
        return ast

    def expression(self, ast):
        return ast

    def value(self, ast):
        return ast

    def assignment(self, ast):
        return ast

    def function_definition(self, ast):
        return ast

    def function_call(self, ast):
        return ast

    def condition_statement(self, ast):
        return ast

    def loop_statement(self, ast):
        return ast

    def control_statement(self, ast):
        return ast

    def block(self, ast):
        return ast

    def program(self, ast):
        return ast

    def comment(self, ast):
        return ast


def main(filename, startrule, **kwargs):
    with open(filename) as f:
        text = f.read()
    parser = UnknownParser(parseinfo=False)
    return parser.parse(text, startrule, filename=filename, **kwargs)

if __name__ == '__main__':
    import json
    ast = generic_main(main, UnknownParser, name='Unknown')
    print('AST:')
    print(ast)
    print()
    print('JSON:')
    print(json.dumps(ast, indent=2))
    print()
