import re

# Define the token specifications for "Black"
TOKEN_SPECIFICATION = [
    ('NUMBER',   r'\d+(\.\d*)?'),        # Integer or decimal number
    ('STRING',   r'"[^"]*"'),            # String literal
    ('ASSIGN',   r'='),                  # Assignment operator
    ('ID',       r'[A-Za-z_][A-Za-z0-9_]*'),  # Identifiers (names of actions, buckets)
    ('OP',       r'[+\-*/]'),            # Arithmetic operators
    ('LPAREN',   r'\('),                 # Left parenthesis
    ('RPAREN',   r'\)'),                 # Right parenthesis
    ('LBRACE',   r'\{'),                 # Left brace
    ('RBRACE',   r'\}'),                 # Right brace
    ('KEYWORD',  r'\b(action|bucket|if|then|ifnot|loop|print)\b'), # Keywords specific to Black
    ('WHITESPACE', r'[ \t]+'),           # Spaces and tabs
    ('NEWLINE',  r'\n'),                 # Line endings
    ('SKIP',     r'[ \t]+'),             # Skip over spaces and tabs
    ('MISMATCH', r'.'),                  # Any other character
]

# Build the regex pattern from token specifications
token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPECIFICATION)

def tokenize(code):
    tokens = []
    for match in re.finditer(token_regex, code):
        kind = match.lastgroup
        value = match.group()
        if kind == 'WHITESPACE' or kind == 'NEWLINE':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Unexpected character: {value}')
        else:
            tokens.append((kind, value))
    return tokens

# Example usage with the new syntax
code = """
action greet(name) {
    print("Hello, " + name)
}

bucket x = 10
if (x > 5) then {
    greet("World")
} ifnot {
    print("x is too small")
}

bucket Kevin = 0

loop if bucket Kevin < 5 {
    print("Kevin is " + Kevin)
    break
}

"""

tokens = tokenize(code)
print(tokens)  # Output: A list of tokens representing the source code for "Black"