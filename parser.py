class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.pos = -1
        self.next_token()
    
    def next_token(self):
        self.pos += 1
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def parse(self):
        return self.parse_statements()

    def parse_statements(self):
        statements = []
        while self.current_token and self.current_token[0] != 'RBRACE':
            statements.append(self.parse_statement())
        return ('statements', statements)

    def parse_statement(self):
        if self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'action':
            return self.parse_action_definition()
        elif self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'bucket':
            return self.parse_bucket_assignment()
        elif self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'if':
            return self.parse_if_statement()
        elif self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'loop':
            return self.parse_loop_statement()
        elif self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'print':
            return self.parse_print_statement()
        else:
            raise RuntimeError(f"Unknown statement: {self.current_token}")

    def parse_action_definition(self):
        self.next_token()  # Consume 'action'
        name = self.current_token[1]
        self.next_token()  # Consume action name
        self.next_token()  # Consume '('
        parameters = self.parse_parameters()
        self.next_token()  # Consume ')'
        self.next_token()  # Consume '{'
        body = self.parse_statements()
        self.next_token()  # Consume '}'
        return ('action_definition', name, parameters, body)

    def parse_bucket_assignment(self):
        self.next_token()  # Consume 'bucket'
        name = self.current_token[1]
        self.next_token()  # Consume bucket name
        self.next_token()  # Consume '='
        value = self.parse_expression()
        return ('bucket_assignment', name, value)

    def parse_if_statement(self):
        self.next_token()  # Consume 'if'
        condition = self.parse_expression()
        self.next_token()  # Consume 'then'
        self.next_token()  # Consume '{'
        then_body = self.parse_statements()
        self.next_token()  # Consume '}'
        
        if self.current_token and self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'ifnot':
            self.next_token()  # Consume 'ifnot'
            self.next_token()  # Consume '{'
            else_body = self.parse_statements()
            self.next_token()  # Consume '}'
            return ('if_statement', condition, then_body, else_body)
        
        return ('if_statement', condition, then_body, None)

    def parse_loop_statement(self):
        self.next_token()  # Consume 'loop'
        self.next_token()  # Consume 'if'
        condition = self.parse_expression()
        self.next_token()  # Consume '{'
        body = self.parse_statements()
        self.next_token()  # Consume '}'
        return ('loop_statement', condition, body)

    def parse_print_statement(self):
        self.next_token()  # Consume 'print'
        expression = self.parse_expression()
        return ('print_statement', expression)

    def parse_parameters(self):
        params = []
        while self.current_token and self.current_token[0] != 'RPAREN':
            if self.current_token[0] == 'ID':
                params.append(self.current_token[1])
            self.next_token()
        return params

    def parse_expression(self):
        # For simplicity, assume expressions are single tokens (e.g., literals or variables)
        token = self.current_token
        self.next_token()
        return token