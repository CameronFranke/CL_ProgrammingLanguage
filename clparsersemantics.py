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
        d = {'type': "operator", 'value': ast}
        return d

    def var_name(self, ast):
        return {'type': "var_name", 'value': ast}

    def literal(self, ast):
        return {"type": "literal", "value": ast}

    def type_keyword(self, ast):
        return {"type": "type_keyword", "value": ast}

    def type_declaration(self, ast):
	while [] in ast:
	    ast.remove([])
        return {"type": "type_declaration", "value": ast}

    def expression(self, ast):
        return {"type": "expression", "value": ast}

    def value(self, ast):
        return {"type": "value", "value": ast}

    def assignment(self, ast):
	while [] in ast:
            ast.remove([])
	while [" "] in ast:
	    ast.remove([" "])
        return {"type": "assignment", "value": ast}

    def function_definition(self, ast):
        return {"type": "function_definition", "value": ast}

    def function_call(self, ast):
	while [] in ast:
		ast.remove([])
        return {"type": "function_call", "value": ast}

    def condition_statement(self, ast):
        return {"type": "condition_statement", "value": ast}

    def loop_statement(self, ast):
        return {"type": "loop_statement", "value": ast}

    def control_statement(self, ast):
        return ast

    def block(self, ast):
        return {'type': "block", 'value': ast}

    def program(self, ast):
        return {"type": "program", "value": ast}

    def comment(self, ast):
        return ast

    def W(self, ast):
	return
