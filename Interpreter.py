class Interpreter:
    def __init__(self):
        self.environment = {}

    def eval(self, node):
        if node[0] == 'action_definition':
            _, name, params, body = node
            self.environment[name] = ('action', params, body)
        elif node[0] == 'bucket_assignment':
            _, name, value = node
            self.environment[name] = self.eval(value)
        elif node[0] == 'if_statement':
            _, condition, then_body, else_body = node
            if self.eval(condition):
                for statement in then_body[1]:
                    self.eval(statement)
            elif else_body:
                for statement in else_body[1]:
                    self.eval(statement)
        elif node[0] == 'loop_statement':
            _, condition, body = node
            while self.eval(condition):
                for statement in body[1]:
                    self.eval(statement)
        elif node[0] == 'print_statement':
            expression = self.eval(node[1])
            print(expression)
        elif node[0] == 'statements':
            for statement in node[1]:
                self.eval(statement)
        elif node[0] == 'ID':
            if node[1] in self.environment:
                return self.environment[node[1]]
            else:
                raise RuntimeError(f"Undefined variable: {node[1]}")
        elif node[0] == 'NUMBER':
            return int(node[1])
        elif node[0] == 'STRING':
            return node[1].strip('"')
        elif node[0] == 'OP':
            left = self.eval(node[1])
            right = self.eval(node[2])
            op = node[1]
            if op == '+':
                return left + right
            elif op == '-':
                return left - right
            elif op == '*':
                return left * right
            elif op == '/':
                return left / right
        # Handle other cases (e.g., functions, arithmetic, etc.)
        else:
            raise RuntimeError(f"Unknown node type: {node[0]}")

# Running the Interpreter
interpreter = Interpreter()
parser = Parser(tokens)
ast = parser.parse()
interpreter.eval(ast)