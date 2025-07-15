T_INT, T_FLOAT, T_STRING, T_IDENTIFIER, T_KEYWORD = 'INT', 'FLOAT', 'STRING', 'IDENTIFIER', 'KEYWORD'
T_PLUS, T_MINUS, T_MUL, T_DIV, T_POW, T_MOD = 'PLUS', 'MINUS', 'MUL', 'DIV', 'POW', 'MOD'
T_ASSIGN, T_EQ, T_NE, T_LT, T_GT, T_LTE, T_GTE = 'ASSIGN', 'EQ', 'NE', 'LT', 'GT', 'LTE', 'GTE'
T_PLUS_ASSIGN, T_MINUS_ASSIGN, T_MUL_ASSIGN, T_DIV_ASSIGN, T_POW_ASSIGN, T_MOD_ASSIGN = 'PLUS_ASSIGN', 'MINUS_ASSIGN', 'MUL_ASSIGN', 'DIV_ASSIGN', 'POW_ASSIGN', 'MOD_ASSIGN'
T_LPAREN, T_RPAREN, T_LBRACE, T_RBRACE, T_LBRACKET, T_RBRACKET = 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET'
T_COMMA, T_COLON, T_ARROW, T_DOT, T_QUESTION, T_EOF = 'COMMA', 'COLON', 'ARROW', 'DOT', 'QUESTION', 'EOF'
T_AMPERSAND, T_PIPE, T_CARET, T_TILDE, T_LSHIFT, T_RSHIFT = 'AMPERSAND', 'PIPE', 'CARET', 'TILDE', 'LSHIFT', 'RSHIFT'
T_F_STRING = 'F_STRING'

class Token:
    """Um Token agora carrega seu tipo, valor e sua localização no código-fonte."""
    def __init__(self, type, value=None, line=0, col=0):
        self.type = type
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        # A nova representação ajuda muito no debugging!
        return f'Token({self.type}, {repr(self.value)}, L{self.line}:C{self.col})'

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
        # Adicionamos os contadores de linha e coluna
        self.line = 1
        self.col = 1
        self.KEYWORDS = {
            'let': Token(T_KEYWORD, 'let'),
            'const': Token(T_KEYWORD, 'const'),
            'when': Token(T_KEYWORD, 'when'),
            'else': Token(T_KEYWORD, 'else'),
            'otherwise': Token(T_KEYWORD, 'otherwise'),
            'for': Token(T_KEYWORD, 'for'),
            'each': Token(T_KEYWORD, 'each'),
            'in': Token(T_KEYWORD, 'in'),
            'while': Token(T_KEYWORD, 'while'),
            'define': Token(T_KEYWORD, 'define'),
            'process': Token(T_KEYWORD, 'process'),
            'type': Token(T_KEYWORD, 'type'),
            'return': Token(T_KEYWORD, 'return'),
            'true': Token(T_KEYWORD, 'true'),
            'false': Token(T_KEYWORD, 'false'),
            'and': Token(T_KEYWORD, 'and'),
            'or': Token(T_KEYWORD, 'or'),
            'not': Token(T_KEYWORD, 'not'),
            'null': Token(T_KEYWORD, 'null'),
            'break': Token(T_KEYWORD, 'break'),
            'continue': Token(T_KEYWORD, 'continue'),
            'import': Token(T_KEYWORD, 'import'),
            'as': Token(T_KEYWORD, 'as'),
            'self': Token(T_KEYWORD, 'self'),
            'super': Token(T_KEYWORD, 'super'),
            'enum': Token(T_KEYWORD, 'enum'),
            'try': Token(T_KEYWORD, 'try'),         # <--- ADICIONE
            'catch': Token(T_KEYWORD, 'catch'),     # <--- ADICIONE
            'finally': Token(T_KEYWORD, 'finally')  # <--- ADICIONE
        }

    def error(self, msg='Caractere inválido'):
        raise Exception(f'{msg}: {self.current_char}')

    def advance(self):
        """Avança o ponteiro e atualiza os contadores de linha/coluna."""
        if self.current_char is not None:
            if self.current_char == '\n':
                self.line += 1
                self.col = 0 # A coluna é resetada após a quebra de linha

            self.pos += 1
            self.col += 1 # A coluna sempre avança com o caractere

        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def peek(self):
        peek_pos = self.pos + 1
        return self.text[peek_pos] if peek_pos < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char is not None and self.current_char != '\n':
            self.advance()

    def _number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        if self.current_char == '.':
            result += '.'
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
        if '.' in result:
            return Token(T_FLOAT, float(result))
        else:
            return Token(T_INT, int(result))

    def _string(self):
        result = ''
        self.advance()  # Pula o " inicial
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        self.advance()  # Pula o " final
        return Token(T_STRING, result)

    def _identifier(self):
        start_line, start_col = self.line, self.col # Guarda a posição inicial
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        # Pega o token do keyword ou cria um novo IDENTIFIER, passando a posição
        token = self.KEYWORDS.get(result, Token(T_IDENTIFIER, result, start_line, start_col))
        
        # Se o token veio do dicionário, ele não tem posição, então atualizamos
        token.line = start_line
        token.col = start_col
        
        return token

    def peek_token(self):
        saved_pos = self.pos
        saved_char = self.current_char
        token = self.get_next_token()
        self.pos = saved_pos
        self.current_char = saved_char
        return token

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if (self.current_char == '/' and self.peek() == '/') or self.current_char == '#':
                self.skip_comment()
                continue
            if self.current_char == 'f' and self.peek() == '"':
                return self._f_string()
            if self.current_char.isdigit():
                return self._number()
            if self.current_char in ('"', "'"):
                return self._string()
            if self.current_char.isalnum() or self.current_char == '_':
                return self._identifier()

            # Operadores de múltiplos caracteres
            if self.current_char == '=' and self.peek() == '=':
                self.advance(); self.advance(); return Token(T_EQ, '==')
            if self.current_char == '!' and self.peek() == '=':
                self.advance(); self.advance(); return Token(T_NE, '!=')
            if self.current_char == '<' and self.peek() == '=':
                self.advance(); self.advance(); return Token(T_LTE, '<=')
            if self.current_char == '>' and self.peek() == '=':
                self.advance(); self.advance(); return Token(T_GTE, '>=')
            if self.current_char == '-' and self.peek() == '>':
                self.advance(); self.advance(); return Token(T_ARROW, '->')
            if self.current_char == '+' and self.peek() == '=':
                self.advance(); self.advance(); return Token(T_PLUS_ASSIGN, '+=')
            if self.current_char == '-' and self.peek() == '=':
                self.advance(); self.advance(); return Token(T_MINUS_ASSIGN, '-=')
            if self.current_char == '*' and self.peek() == '=':
                self.advance(); self.advance(); return Token(T_MUL_ASSIGN, '*=')
            if self.current_char == '/' and self.peek() == '=':
                self.advance(); self.advance(); return Token(T_DIV_ASSIGN, '/=')
            if self.current_char == '*' and self.peek() == '*':
                self.advance()
                if self.peek() == '=':
                    self.advance(); self.advance(); return Token(T_POW_ASSIGN, '**=')
                self.advance(); return Token(T_POW, '**')
            if self.current_char == '%' and self.peek() == '=':
                self.advance(); self.advance(); return Token(T_MOD_ASSIGN, '%=')
            if self.current_char == '<' and self.peek() == '<':
                self.advance(); self.advance(); return Token(T_LSHIFT, '<<')
            if self.current_char == '>' and self.peek() == '>':
                self.advance(); self.advance(); return Token(T_RSHIFT, '>>')

            start_line, start_col = self.line, self.col
            if self.current_char == '=' and self.peek() == '=': self.advance(); self.advance(); return Token(T_EQ, '==', start_line, start_col)

            # Operadores de um caractere
            token_map = {'+':T_PLUS,'-':T_MINUS,'*':T_MUL,'/':T_DIV,'%':T_MOD,'(':T_LPAREN,')':T_RPAREN,'{':T_LBRACE,'}':T_RBRACE,'[':T_LBRACKET,']':T_RBRACKET,',':T_COMMA,':':T_COLON,'.':T_DOT,'=':T_ASSIGN,'<':T_LT,'>':T_GT, '&':T_AMPERSAND, '|':T_PIPE, '^':T_CARET, '~':T_TILDE, '?':T_QUESTION}
            if self.current_char in token_map:
                char = self.current_char
                start_line, start_col = self.line, self.col # Guarda a posição
                self.advance()
                return Token(token_map[char], char, start_line, start_col)

            self.error()
        return Token(T_EOF)

    def _string(self):
        start_line, start_col = self.line, self.col
        result = ''
        quote_char = self.current_char # Salva o caractere de aspas (' ou ")
        self.advance()  # Pula a aspa inicial
        
        while self.current_char is not None and self.current_char != quote_char:
            # --- LÓGICA DE ESCAPE ---
            if self.current_char == '\\':
                self.advance() # Pula a barra
                if self.current_char == 'n':
                    result += '\n'
                elif self.current_char == 't':
                    result += '\t'
                elif self.current_char == quote_char: # Escapando a própria aspa
                    result += quote_char
                elif self.current_char == '\\':
                    result += '\\'
                else:
                    # Se for uma sequência desconhecida, apenas adiciona o caractere literal
                    result += self.current_char
            else:
                result += self.current_char
            # --- FIM DA LÓGICA DE ESCAPE ---
            self.advance()
            
        if self.current_char is None:
            self.error(f"String iniciada com {quote_char} não foi fechada.")

        self.advance()  # Pula a aspa final
        return Token(T_STRING, result, start_line, start_col)
        
    def _f_string(self):
        start_line, start_col = self.line, self.col
        self.advance() # Consome o 'f'
        self.advance() # Consome o '"' inicial
        
        result = ''
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
            
        if self.current_char is None:
            self.error("F-string não foi fechada.")

        self.advance() # Consome o '"' final
        
        # O token T_F_STRING foi definido em um passo anterior
        return Token(T_F_STRING, result, start_line, start_col)
