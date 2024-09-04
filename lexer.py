import re

# Define token types and their regex patterns
TOKEN_SPECIFICATION = [
    ('NUMBER',   r'\d+(\.\d*)?'),   # Integer or decimal number
    ('ASSIGN',   r'='),             # Assignment operator
    ('END',      r';'),             # Statement terminator
    ('ID',       r'[A-Za-z]+'),     # Identifiers
    ('OP',       r'[+\-*/]'),       # Arithmetic operators
    ('NEWLINE',  r'\n'),            # Line endings
    ('SKIP',     r'[ \t]+'),        # Skip over spaces and tabs
    ('MISMATCH', r'.'),             # Any other character
]

# Build a regular expression for tokenizing
token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPECIFICATION)

def tokenize(code):
    for match in re.finditer(token_regex, code):
        kind = match.lastgroup
        value = match.group()
        if kind == 'NUMBER':
            value = float(value) if '.' in value else int(value)
        elif kind == 'ID':
            value = str(value)
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Unexpected character: {value}')
        yield kind, value