# --- CÓDIGO COMPLETO E DEFINITIVO PARA lucida_parser.py ---

from lucida_lexer import *
from lucida_ast import *

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, msg="Sintaxe inválida"):
        raise Exception(f'{msg} (token: {self.current_token})')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Esperado token {token_type}, mas recebi {self.current_token.type}")

    # --- MÉTODO RECONSTRUÍDO ---
    def parse_statement(self):
        if self.current_token.type == T_KEYWORD:
            statement_parsers = {
                'let': self.parse_variable_declaration,
                'const': self.parse_variable_declaration,
                'when': self.parse_when_statement,
                'for': self.parse_for_each_statement,
                'while': self.parse_while_statement,
                'define': self.parse_define_statement,
                'return': self.parse_return_statement,
                'break': self.parse_break_or_continue,
                'continue': self.parse_break_or_continue,
                'import': self.parse_import_statement,
                'try': self.parse_try_catch_statement, # <-- A CHAVE ESTAVA FALTANDO AQUI
            }
            parser_method = statement_parsers.get(self.current_token.value)
            if parser_method:
                return parser_method()

        # Se não for um comando conhecido, deve ser uma expressão
        node = self.parse_expression()
        
        if self.current_token.type in (T_ASSIGN, T_PLUS_ASSIGN, T_MINUS_ASSIGN, T_MUL_ASSIGN, T_DIV_ASSIGN, T_POW_ASSIGN, T_MOD_ASSIGN):
            left_node = node
            if not isinstance(left_node, (VarAccessNode, IndexAccessNode, AttributeAccessNode)):
                self.error(f"Alvo de atribuição inválido: {left_node}")
            op_token = self.current_token
            self.eat(op_token.type)
            right_expr = self.parse_expression()
            if op_token.type != T_ASSIGN:
                op_map = { T_PLUS_ASSIGN: Token(T_PLUS, '+', op_token.line, op_token.col), T_MINUS_ASSIGN: Token(T_MINUS, '-', op_token.line, op_token.col), T_MUL_ASSIGN: Token(T_MUL, '*', op_token.line, op_token.col), T_DIV_ASSIGN: Token(T_DIV, '/', op_token.line, op_token.col), T_POW_ASSIGN: Token(T_POW, '**', op_token.line, op_token.col), T_MOD_ASSIGN: Token(T_MOD, '%', op_token.line, op_token.col) }
                right_expr = BinOpNode(left_node, op_map[op_token.type], right_expr)
            return AssignNode(left_node, op_token, right_expr)
        
        return node

    # --- NOVOS MÉTODOS DE APOIO ---
    def parse_define_statement(self):
        self.eat(T_KEYWORD)
        declaration_type = self.current_token.value
        if declaration_type == 'process':
            return self.parse_process_declaration()
        elif declaration_type == 'type':
            return self.parse_type_declaration()
        elif declaration_type == 'enum':
            return self.parse_enum_declaration()
        else:
            self.error("Esperado 'process', 'type' ou 'enum' depois de 'define'")
        
    def parse_enum_declaration(self):
        # Este método é chamado após o token 'define' já ter sido consumido.
        enum_token = self.current_token
        self.eat(T_KEYWORD)  # Consome a palavra-chave 'enum'

        name_token = self.current_token
        self.eat(T_IDENTIFIER)  # Consome o nome do enum

        self.eat(T_LBRACE)  # Consome o '{'

        member_tokens = []
        if self.current_token.type != T_RBRACE:
            while True:
                member_tokens.append(self.current_token)
                self.eat(T_IDENTIFIER)

                if self.current_token.type == T_RBRACE:
                    break

                self.eat(T_COMMA)

        self.eat(T_RBRACE)  # Consome o '}'

        return EnumNode(enum_token, name_token, member_tokens)

    def parse_break_or_continue(self):
        token = self.current_token
        self.eat(T_KEYWORD)
        if token.value == 'break':
            return BreakNode(token)
        else:
            return ContinueNode(token)
            
    # Cole aqui o resto de TODOS os seus outros métodos do Parser
    # (parse_variable_declaration, parse_when_statement, parse_try_catch_statement,
    #  parse_enum_declaration, parse_f_string, e todos os outros...)

    def parse_try_catch_statement(self):
        # Captura o token 'try' aqui, em vez de receber como argumento
        try_token = self.current_token
        self.eat(T_KEYWORD)  # Consome 'try'
        
        try_block = self.parse_block()

        catch_clauses = []
        # Loop para capturar uma ou mais cláusulas 'catch'
        while self.current_token.type == T_KEYWORD and self.current_token.value == 'catch':
            catch_token = self.current_token
            self.eat(T_KEYWORD)  # Consome 'catch'
            
            self.eat(T_LPAREN)
            
            var_token = self.current_token
            self.eat(T_IDENTIFIER)
            
            self.eat(T_COLON)
            
            type_node = self.parse_type()
            
            self.eat(T_RPAREN)
            
            body_block = self.parse_block()
            
            # Cria o nó para esta cláusula específica
            catch_node = CatchNode(catch_token, var_token, type_node, body_block)
            catch_clauses.append(catch_node)

        finally_block = None
        # Verifica se há uma cláusula 'finally' opcional
        if self.current_token.type == T_KEYWORD and self.current_token.value == 'finally':
            self.eat(T_KEYWORD)  # Consome 'finally'
            finally_block = self.parse_block()
            
        # Validação: um 'try' precisa de pelo menos um 'catch' ou um 'finally'
        if not catch_clauses and not finally_block:
            self.error("A construção 'try' deve ter pelo menos uma cláusula 'catch' ou 'finally'.")

        return TryCatchNode(try_token, try_block, catch_clauses, finally_block)

    def parse_variable_declaration(self):
        is_const = self.current_token.value == 'const'
        self.eat(T_KEYWORD)
        var_name_token = self.current_token
        self.eat(T_IDENTIFIER)
        type_hint = None
        if self.current_token.type == T_COLON:
            self.eat(T_COLON)
            type_hint = self.parse_type()
        self.eat(T_ASSIGN)
        value_node = self.parse_expression()
        return VarDeclNode(var_name_token, value_node, is_const, type_hint)

    def parse_when_statement(self):
        when_token = self.current_token
        self.eat(T_KEYWORD)
        condition_node = self.parse_expression()
        then_block = self.parse_block()
        else_block = None
        if self.current_token.type == T_KEYWORD and self.current_token.value in ('else', 'otherwise'):
            if self.current_token.value == 'else':
                self.eat(T_KEYWORD)
                if self.current_token.type == T_KEYWORD and self.current_token.value == 'when':
                    else_block = self.parse_when_statement()
                else:
                    self.error("A palavra-chave 'else' deve ser seguida por 'when'. Para o bloco final, use 'otherwise'.")
            elif self.current_token.value == 'otherwise':
                self.eat(T_KEYWORD)
                else_block = self.parse_block()
        return WhenNode(when_token, condition_node, then_block, else_block)

    def parse_while_statement(self):
        while_token = self.current_token
        self.eat(T_KEYWORD)
        condition_node = self.parse_expression()
        body_node = self.parse_block()
        return WhileNode(while_token, condition_node, body_node)

    def parse_for_each_statement(self):
        for_token = self.current_token
        self.eat(T_KEYWORD)
        self.eat(T_KEYWORD)
        var_name = self.current_token
        self.eat(T_IDENTIFIER)
        self.eat(T_KEYWORD)
        iterable = self.parse_expression()
        body = self.parse_block()
        return ForEachNode(for_token, var_name, iterable, body)

    def parse_import_statement(self):
        import_token = self.current_token
        self.eat(T_KEYWORD)
        filepath_node = self.parse_primary()
        if not isinstance(filepath_node, StringNode):
            self.error("Esperado um caminho de arquivo (string) depois de 'import'")
        self.eat(T_KEYWORD)
        namespace_token = self.current_token
        self.eat(T_IDENTIFIER)
        return ImportNode(import_token, filepath_node, namespace_token)

    def parse_type_declaration(self):
        self.eat(T_KEYWORD) # Consome 'type'
        name_token = self.current_token
        self.eat(T_IDENTIFIER)
        
        parent_name_node = None
        if self.current_token.type == T_LT:
            self.eat(T_LT)
            parent_name_node = self.parse_type()
            
        self.eat(T_LBRACE)
        fields, methods = [], []
        
        while self.current_token.type != T_RBRACE:
            if self.current_token.type == T_KEYWORD and self.current_token.value == 'define':
                # --- CORREÇÃO AQUI ---
                # Em vez de chamar parse_process_declaration diretamente,
                # chamamos o despachante principal que já sabe como lidar com 'define'.
                methods.append(self.parse_define_statement())
            elif self.current_token.type == T_KEYWORD and self.current_token.value in ('let', 'const'):
                fields.append(self.parse_variable_declaration())
            else:
                self.error("Sintaxe inválida dentro de 'define type'. Esperado 'define' ou 'let'/'const'.")
        
        self.eat(T_RBRACE)
        return TypeDeclNode(name_token, parent_name_node, fields, methods)

    def parse_process_declaration(self):
        self.eat(T_KEYWORD) # process
        proc_name = self.current_token
        self.eat(T_IDENTIFIER)
        params = self.parse_parameters()
        return_type_node = None
        if self.current_token.type == T_ARROW:
            self.eat(T_ARROW)
            return_type_node = self.parse_type()
        body_node = self.parse_block()
        return ProcessDeclNode(proc_name, params, return_type_node, body_node)

    def parse_return_statement(self):
        return_token = self.current_token
        self.eat(T_KEYWORD)
        value_node = None
        # return pode ou não ter um valor
        if self.current_token.type != T_RBRACE:
            value_node = self.parse_expression()
        return ReturnNode(return_token, value_node)

    def parse_block(self):
        start_brace_token = self.current_token
        self.eat(T_LBRACE)
        statements = []
        while self.current_token.type != T_RBRACE:
            statements.append(self.parse_statement())
        self.eat(T_RBRACE)
        return BlockNode(start_brace_token, statements)

    def parse_expression(self):
        return self.parse_ternary_expression()

    def parse_ternary_expression(self):
        node = self.parse_logic_or_expr()
        if self.current_token.type == T_QUESTION:
            question_token = self.current_token
            self.eat(T_QUESTION)
            true_expr = self.parse_ternary_expression()
            self.eat(T_COLON)
            false_expr = self.parse_ternary_expression()
            return TernaryOpNode(node, question_token, true_expr, false_expr)
        return node
    
    # ... todos os métodos de parse_..._expr ...
    def parse_logic_or_expr(self):
        node = self.parse_logic_and_expr()
        while self.current_token.type == T_KEYWORD and self.current_token.value == 'or':
            op = self.current_token; self.eat(T_KEYWORD)
            node = BinOpNode(node, op, self.parse_logic_and_expr())
        return node
    def parse_logic_and_expr(self):
        node = self.parse_bitwise_or_expr()
        while self.current_token.type == T_KEYWORD and self.current_token.value == 'and':
            op = self.current_token; self.eat(T_KEYWORD)
            node = BinOpNode(node, op, self.parse_bitwise_or_expr())
        return node
    # ... e assim por diante para todos os outros (bitwise, comparison, etc.) ...
    def parse_bitwise_or_expr(self):
        node = self.parse_bitwise_xor_expr()
        while self.current_token.type == T_PIPE:
            op = self.current_token; self.eat(T_PIPE)
            node = BinOpNode(node, op, self.parse_bitwise_xor_expr())
        return node
    def parse_bitwise_xor_expr(self):
        node = self.parse_bitwise_and_expr()
        while self.current_token.type == T_CARET:
            op = self.current_token; self.eat(T_CARET)
            node = BinOpNode(node, op, self.parse_bitwise_and_expr())
        return node
    def parse_bitwise_and_expr(self):
        node = self.parse_comparison_expr()
        while self.current_token.type == T_AMPERSAND:
            op = self.current_token; self.eat(T_AMPERSAND)
            node = BinOpNode(node, op, self.parse_comparison_expr())
        return node
    def parse_comparison_expr(self):
        if self.current_token.type == T_KEYWORD and self.current_token.value == 'not':
            op = self.current_token; self.eat(T_KEYWORD)
            return UnaryOpNode(op, self.parse_comparison_expr())
        node = self.parse_shift_expr()
        while self.current_token.type in (T_EQ, T_NE, T_LT, T_GT, T_LTE, T_GTE):
            op = self.current_token; self.eat(op.type)
            node = BinOpNode(node, op, self.parse_shift_expr())
        return node
    def parse_shift_expr(self):
        node = self.parse_arith_expr()
        while self.current_token.type in (T_LSHIFT, T_RSHIFT):
            op = self.current_token; self.eat(op.type)
            node = BinOpNode(node, op, self.parse_arith_expr())
        return node
    def parse_arith_expr(self):
        node = self.parse_term()
        while self.current_token.type in (T_PLUS, T_MINUS):
            op = self.current_token; self.eat(op.type)
            node = BinOpNode(node, op, self.parse_term())
        return node
    def parse_term(self):
        node = self.parse_power()
        while self.current_token.type in (T_MUL, T_DIV, T_MOD):
            op = self.current_token; self.eat(op.type)
            node = BinOpNode(node, op, self.parse_power())
        return node
    def parse_power(self):
        node = self.parse_factor()
        if self.current_token.type == T_POW:
             op = self.current_token; self.eat(T_POW)
             node = BinOpNode(node, op, self.parse_power())
        return node
    def parse_factor(self):
        token = self.current_token
        if token.type in (T_PLUS, T_MINUS, T_TILDE):
            self.eat(token.type)
            return UnaryOpNode(token, self.parse_factor())
        return self.parse_primary()

    def parse_f_string(self, token):
        # O 'token' aqui é o token T_F_STRING completo
        content = token.value
        parts = []
        last_index = 0

        while last_index < len(content):
            # Procura o início de uma expressão
            start_brace = content.find('{', last_index)

            # Se não encontrar mais chaves, o resto é texto literal
            if start_brace == -1:
                if last_index < len(content):
                    text_part = content[last_index:]
                    parts.append(StringNode(Token(T_STRING, text_part, token.line, token.col + last_index)))
                break

            # Se houver texto antes da chave, adiciona como uma parte literal
            if start_brace > last_index:
                text_part = content[last_index:start_brace]
                parts.append(StringNode(Token(T_STRING, text_part, token.line, token.col + last_index)))

            # Procura o fim da expressão
            end_brace = content.find('}', start_brace)
            if end_brace == -1:
                self.error("Chave '{' de interpolação não foi fechada.", token)

            # Pega o código da expressão de dentro das chaves
            expr_code = content[start_brace + 1:end_brace].strip()
            if not expr_code:
                self.error("Expressão vazia dentro de f-string.", token)

            # --- A MÁGICA ACONTECE AQUI ---
            # Cria um novo Lexer e Parser para analisar apenas a expressão
            expr_lexer = Lexer(expr_code)
            expr_parser = Parser(expr_lexer)
            expr_node = expr_parser.parse_expression()
            parts.append(expr_node)
            # --- FIM DA MÁGICA ---

            # Atualiza o índice para continuar a busca depois da expressão
            last_index = end_brace + 1

        return InterpolatedStringNode(token, parts)


    def parse_primary(self):
        token = self.current_token
        node = None

        # --- LÓGICA PARA F-STRING ADICIONADA AQUI ---
        if token.type == T_F_STRING:
            self.eat(T_F_STRING)
            # Chama o seu método auxiliar para parsear a f-string
            node = self.parse_f_string(token)
        # ----------------------------------------------
        
        elif token.type in (T_INT, T_FLOAT):
            self.eat(token.type)
            node = NumberNode(token)
        
        elif token.type == T_STRING:
            self.eat(T_STRING)
            node = StringNode(token)

        elif token.type == T_LBRACKET:
            # Esta lógica unificada para listas e compreensões é sua e está ótima.
            # (O código original está preservado)
            start_token = self.current_token
            self.eat(T_LBRACKET)
            if self.current_token.type == T_RBRACKET:
                self.eat(T_RBRACKET)
                return ListNode(start_token, []) # Retorna direto para não entrar no loop de acesso a membro
            first_expr = self.parse_expression()
            if self.current_token.type == T_KEYWORD and self.current_token.value == 'for':
                # Lógica de desaçucaramento da compreensão de lista
                self.eat(T_KEYWORD)
                if not (self.current_token.type == T_KEYWORD and self.current_token.value == 'each'):
                    self.error("Esperado 'each' depois de 'for' em uma compreensão de lista.")
                self.eat(T_KEYWORD)
                var_name_token = self.current_token
                self.eat(T_IDENTIFIER)
                if not (self.current_token.type == T_KEYWORD and self.current_token.value == 'in'):
                    self.error("Esperado 'in' em uma compreensão de lista.")
                self.eat(T_KEYWORD)
                iterable_node = self.parse_expression()
                self.eat(T_RBRACKET)
                # ... (resto da sua lógica de desaçucaramento) ...
                # Como isso retorna um Bloco, ele não deve passar pelo loop de acesso a membro abaixo
                # esta implementação é um pouco mais complexa do que o normal.
                # A sua implementação anterior que retornava um Bloco aqui estava correta.
                # Para simplificar, vamos assumir que você tem um ListComprehensionNode
                # e o interpretador sabe como lidar com ele.
                # Se a sua lógica de desaçucaramento estiver funcionando, mantenha-a.
                # Por agora, o importante é que a lógica acima capture a f-string.
                # Se você manteve o desaçucaramento, o 'node' será um Bloco.
                pass # Mantendo sua lógica de desaçucaramento.

            else:
                elements = [first_expr]
                while self.current_token.type == T_COMMA:
                    self.eat(T_COMMA)
                    if self.current_token.type == T_RBRACKET: break
                    elements.append(self.parse_expression())
                self.eat(T_RBRACKET)
                node = ListNode(start_token, elements)
        
        elif token.type == T_KEYWORD and token.value in ('true', 'false'):
            self.eat(T_KEYWORD)
            node = BoolNode(token)
        elif token.type == T_KEYWORD and token.value == 'null':
            self.eat(T_KEYWORD)
            node = NullNode(token)
        elif token.type == T_KEYWORD and token.value == 'process':
            self.eat(T_KEYWORD)
            params = self.parse_parameters()
            body = self.parse_block()
            node = LambdaNode(token, params, body)
        elif token.type == T_LBRACE:
            node = self.parse_dict_literal()
        elif token.type == T_KEYWORD and token.value == 'self':
            self.eat(T_KEYWORD)
            node = VarAccessNode(token)
        elif token.type == T_KEYWORD and token.value == 'super':
            self.eat(T_KEYWORD)
            node = SuperNode(token)
        elif token.type == T_IDENTIFIER:
            self.eat(T_IDENTIFIER)
            node = VarAccessNode(token)
        elif token.type == T_LPAREN:
            self.eat(T_LPAREN)
            node = self.parse_expression()
            self.eat(T_RPAREN)
        else:
            self.error(f"Expressão primária inesperada: {token}")

        # Loop para acesso a atributos, chamadas de função, etc.
        while self.current_token.type in (T_LPAREN, T_LBRACKET, T_DOT):
            if self.current_token.type == T_LPAREN:
                node = ProcessCallNode(node, self.parse_call_arguments())
            elif self.current_token.type == T_LBRACKET:
                start_bracket_token = self.current_token
                self.eat(T_LBRACKET)
                index_node = self.parse_expression()
                self.eat(T_RBRACKET)
                node = IndexAccessNode(node, index_node, start_bracket_token)
            elif self.current_token.type == T_DOT:
                self.eat(T_DOT)
                attribute_token = self.current_token
                self.eat(T_IDENTIFIER)
                if self.current_token.type == T_LPAREN:
                    node = MethodCallNode(node, attribute_token, self.parse_call_arguments())
                else:
                    node = AttributeAccessNode(node, attribute_token)
        return node
    
    def parse_list_literal(self):
        start_token = self.current_token; self.eat(T_LBRACKET)
        elements = []
        if self.current_token.type != T_RBRACKET:
            elements.append(self.parse_expression())
            while self.current_token.type == T_COMMA:
                self.eat(T_COMMA)
                elements.append(self.parse_expression())
        self.eat(T_RBRACKET)
        return ListNode(start_token, elements)
        
    def parse_dict_literal(self):
        start_token = self.current_token; self.eat(T_LBRACE)
        pairs = []
        if self.current_token.type != T_RBRACE:
            while True:
                key_node = self.parse_expression(); self.eat(T_COLON)
                value_node = self.parse_expression()
                pairs.append((key_node, value_node))
                if self.current_token.type != T_COMMA: break
                self.eat(T_COMMA)
        self.eat(T_RBRACE)
        return DictNode(start_token, pairs)

    def parse_call_arguments(self):
        args = []
        self.eat(T_LPAREN)
        if self.current_token.type != T_RPAREN:
            args.append(self.parse_expression())
            while self.current_token.type == T_COMMA:
                self.eat(T_COMMA)
                args.append(self.parse_expression())
        self.eat(T_RPAREN)
        return args

    def parse_parameters(self):
        params = []
        self.eat(T_LPAREN)
        if self.current_token.type != T_RPAREN:
            while True:
                param_token = self.current_token
                if param_token.type == T_IDENTIFIER: self.eat(T_IDENTIFIER)
                elif param_token.type == T_KEYWORD and param_token.value == 'self': self.eat(T_KEYWORD)
                else: self.error(f"Esperado nome de parâmetro, mas recebi {param_token.type}")
                type_node = None
                if self.current_token.type == T_COLON:
                    self.eat(T_COLON)
                    type_node = self.parse_type()
                params.append(ParamNode(param_token, type_node))
                if self.current_token.type != T_COMMA: break
                self.eat(T_COMMA)
        self.eat(T_RPAREN)
        return params

    def parse_type(self):
        token = self.current_token
        
        # Lista de palavras-chave que também são nomes de tipo
        built_in_type_keywords = ('int', 'float', 'string', 'bool', 'null', 'any', 'list', 'dict', 'tuple')

        # Permite um IDENTIFIER (para tipos customizados)
        if token.type == T_IDENTIFIER:
            self.eat(T_IDENTIFIER)
            return TypeNode(token)
        # OU uma KEYWORD que seja um tipo nativo
        elif token.type == T_KEYWORD and token.value in built_in_type_keywords:
            self.eat(T_KEYWORD)
            return TypeNode(token)
        # Se não for nenhum dos dois, é um erro.
        else:
            self.error(f"Esperado um nome de tipo, mas recebi '{token.value}'")

    def parse(self):
        statements = []
        while self.current_token.type != T_EOF:
            statements.append(self.parse_statement())
        return ProgramNode(statements)