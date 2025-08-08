# Copie e cole TODO este conteúdo em seu arquivo lucida_analyzer.py

from lucida_ast import *
from lucida_errors import LucidaSemanticError
from lucida_stdlib import NATIVE_MODULES_SEMANTICS
from lucida_symbols import (
    Symbol, VarSymbol, BuiltInTypeSymbol, BuiltInFunctionSymbol,
    ProcessSymbol, TypeSymbol, ModuleSymbol, ScopedSymbolTable,
    ListTypeSymbol, DictTypeSymbol, EnumSymbol, EnumMemberSymbol,
    FunctionTypeSymbol, TupleTypeSymbol # <--- ADICIONE AQUI
)
from lucida_lexer import (
    Lexer, T_PLUS, T_MINUS, T_MUL, T_DIV, T_POW, T_MOD, T_EQ, T_NE, T_LT,
    T_GT, T_LTE, T_GTE, T_AMPERSAND, T_PIPE, T_CARET, T_LSHIFT, T_RSHIFT,
    T_IDENTIFIER, Token  # <-- ADICIONE 'Token' AQUI
)
from lucida_parser import Parser
import importlib.util
import sys
from pathlib import Path

class NodeVisitor:
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'Nenhum método visit_{type(node).__name__} encontrado na classe {type(self).__name__}')

class SemanticAnalyzer(NodeVisitor):
    def __init__(self):
        self.current_scope = None
        self.loop_level = 0
        self.current_process_symbol = None
        self.current_class_symbol = None
        # Adicione este dicionário para guardar os "modelos" de métodos
        self._native_type_method_templates = {}

    def _initialize_native_type_methods(self):
        # Este método cria os "templates" de métodos para cada tipo nativo.
        
        # Primeiro, pegamos referências aos tipos básicos que usaremos nas assinaturas
        string_type = self.current_scope.lookup('string')
        int_type = self.current_scope.lookup('int')
        bool_type = self.current_scope.lookup('bool')
        any_type = self.current_scope.lookup('any')
        null_type = self.current_scope.lookup('null')

        # Template de métodos para STRING
        string_methods = {
            'to_upper': BuiltInFunctionSymbol(name='to_upper', return_type=string_type),
            'to_lower': BuiltInFunctionSymbol(name='to_lower', return_type=string_type),
            'trim': BuiltInFunctionSymbol(name='trim', return_type=string_type),
            'split': BuiltInFunctionSymbol(name='split', params=[VarSymbol('sep', string_type)], return_type=ListTypeSymbol(string_type)),
            'replace': BuiltInFunctionSymbol(name='replace', params=[VarSymbol('old', string_type), VarSymbol('new', string_type)], return_type=string_type),
            'contains': BuiltInFunctionSymbol(name='contains', params=[VarSymbol('substring', string_type)], return_type=bool_type),
            'starts_with': BuiltInFunctionSymbol(name='starts_with', params=[VarSymbol('prefix', string_type)], return_type=bool_type),
            'ends_with': BuiltInFunctionSymbol(name='ends_with', params=[VarSymbol('suffix', string_type)], return_type=bool_type),
            'slice': BuiltInFunctionSymbol(name='slice', params=[VarSymbol('start', int_type), VarSymbol('end', int_type)], return_type=string_type),
            'length': BuiltInFunctionSymbol(name='length', params=[], return_type=int_type),
        }
        self._native_type_method_templates['string'] = string_methods
        
        # Template de métodos para LISTA
        list_methods = {
            'append': BuiltInFunctionSymbol(name='append', params=[VarSymbol('item', any_type)], return_type=null_type),
            'pop': BuiltInFunctionSymbol(name='pop', params=[], return_type=any_type),
            'length': BuiltInFunctionSymbol(name='length', params=[], return_type=int_type),
        }
        self._native_type_method_templates['list'] = list_methods
        
        # Template de métodos para DICIONÁRIO
        dict_methods = {
            'keys': BuiltInFunctionSymbol(name='keys', params=[], return_type=ListTypeSymbol(any_type)),
            'values': BuiltInFunctionSymbol(name='values', params=[], return_type=ListTypeSymbol(any_type)),
            # Esta é a definição semântica correta que o analisador usará
            'get': BuiltInFunctionSymbol(
                name='get', 
                params=[
                    VarSymbol('key', any_type), 
                    VarSymbol('default', any_type, is_optional=True)
                ], 
                return_type=any_type
            ),
        }
        self._native_type_method_templates['dict'] = dict_methods

    def check_type_compatibility(self, type1, type2, error_message, node):
        # type1 é o tipo esperado (ex: 'list')
        # type2 é o tipo real que foi passado (ex: 'list[int]')

        if not type1 or not type2 or type1.name == 'any' or type2.name == 'any':
            return True

        if type1.name == type2.name:
            return True

        # --- LÓGICA DE SUBTIPO ADICIONADA AQUI ---
        # Regra: Qualquer 'list[T]' é compatível com o tipo base 'list'.
        if isinstance(type2, ListTypeSymbol) and type1.name == 'list':
            return True
        # Regra: Qualquer 'dict[K, V]' é compatível com o tipo base 'dict'.
        if isinstance(type2, DictTypeSymbol) and type1.name == 'dict':
            return True
        # Regra: Qualquer 'tuple[...]' é compatível com o tipo base 'tuple'.
        if isinstance(type2, TupleTypeSymbol) and type1.name == 'tuple':
            return True
        # --- FIM DA LÓGICA DE SUBTIPO ---

        # Regra especial para números
        if type1.name == 'float' and type2.name == 'int':
            return True

        # Se nenhuma regra de compatibilidade for atendida, lança o erro.
        self.error(error_message, node)
    def error(self, message, node):
        # Esta definição aceita o 'node' e o usa para criar o erro com linha e coluna.
        raise LucidaSemanticError(message, node.line, node.col)

    def visit_EnumNode(self, node):
        enum_name = node.name_token.value
        if self.current_scope.lookup(enum_name, current_scope_only=True):
            self.error(f"Símbolo '{enum_name}' já declarado neste escopo.", node.name_token)

        enum_symbol = EnumSymbol(enum_name)
        self.current_scope.define(enum_symbol)

        for member_token in node.member_tokens:
            member_name = member_token.value
            if member_name in enum_symbol.members:
                self.error(f"Membro de enum duplicado: '{member_name}'", member_token)
            
            # O tipo do membro é o próprio enum
            member_symbol = EnumMemberSymbol(name=member_name, enum_type=enum_symbol)
            enum_symbol.members[member_name] = member_symbol

    def visit_TryCatchNode(self, node):
        # 1. Visita o bloco 'try' normalmente
        self.visit(node.try_block)
        
        # 2. Visita cada uma das cláusulas 'catch'
        for catch_clause in node.catch_clauses:
            self.visit(catch_clause)
            
        # 3. Se houver um bloco 'finally', visita-o
        if node.finally_block:
            self.visit(node.finally_block)

    def visit_CatchNode(self, node):
        # Entra em um novo escopo para o bloco catch
        catch_scope = ScopedSymbolTable(
            'catch', 
            self.current_scope.scope_level + 1, 
            self.current_scope
        )
        self.current_scope = catch_scope
        
        # Pega o nome do tipo do erro (ex: 'FileNotFoundError')
        error_type_name = node.type_node.name
        # Procura por este tipo no escopo
        error_type_symbol = self.current_scope.lookup(error_type_name)
        
        # Validação: O tipo de erro existe e é um tipo?
        if not error_type_symbol or not isinstance(error_type_symbol, TypeSymbol):
            self.error(f"O tipo de exceção '{error_type_name}' não foi definido.", node.type_node)
            
        # Pega o nome da variável (ex: 'e')
        var_name = node.var_token.value
        # Cria o símbolo da variável com o tipo de erro correto
        var_symbol = VarSymbol(var_name, type=error_type_symbol)
        
        # Define a variável de erro no escopo do catch
        self.current_scope.define(var_symbol)
        
        # Agora, analisa o corpo do bloco 'catch' dentro deste novo escopo
        self.visit(node.body_block)
        
        # Sai do escopo do catch, restaurando o escopo anterior
        self.current_scope = self.current_scope.enclosing_scope

    def visit_ProgramNode(self, node):
        print("--- Análise Semântica Iniciada ---")
        global_scope = ScopedSymbolTable('global', 1)
        self.current_scope = global_scope

        # =================================================================
        # PASSO 1: Definir todos os tipos nativos que a linguagem conhece.
        # =================================================================
        
        # A ScopedSymbolTable já define: int, float, string, bool, null.
        # Nós adicionamos o que falta:
        global_scope.define(BuiltInTypeSymbol('any'))
        
        # Para anotações de tipo, pegamos referências a estes símbolos.
        any_type = global_scope.lookup('any')
        string_type = global_scope.lookup('string')
        int_type = global_scope.lookup('int')
        float_type = global_scope.lookup('float')
        bool_type = global_scope.lookup('bool')
        null_type = global_scope.lookup('null')

        # Define os tipos de coleção base para serem usados em anotações como '-> list'
        list_type = ListTypeSymbol(any_type)
        list_type.name = 'list' # Força o nome para ser simples e encontrável
        global_scope.define(list_type)

        dict_type = DictTypeSymbol(any_type, any_type)
        dict_type.name = 'dict'
        global_scope.define(dict_type)

        tuple_type = TupleTypeSymbol([any_type]) # Exemplo, pode ser melhorado
        tuple_type.name = 'tuple'
        global_scope.define(tuple_type)
        
        # Define os tipos de erro para as cláusulas 'catch'
        global_scope.define(TypeSymbol('Exception'))
        global_scope.define(TypeSymbol('FileNotFoundError'))
        global_scope.define(TypeSymbol('ValueError'))
        global_scope.define(TypeSymbol('TypeError'))
        global_scope.define(TypeSymbol('ArithmeticError'))
        global_scope.define(TypeSymbol('IndexError'))

        # =================================================================
        # PASSO 2: Anexar métodos aos tipos nativos
        # =================================================================
        
        self._initialize_native_type_methods()
        
        global_scope.lookup('string').methods = self._native_type_method_templates.get('string', {})
        global_scope.lookup('list').methods = self._native_type_method_templates.get('list', {})
        global_scope.lookup('dict').methods = self._native_type_method_templates.get('dict', {})

        # =================================================================
        # PASSO 3: Definir todas as funções globais nativas com suas assinaturas
        # =================================================================

        global_scope.define(BuiltInFunctionSymbol(name='print', params=[], return_type=null_type))
        global_scope.define(BuiltInFunctionSymbol(name='read', params=[VarSymbol('prompt', string_type)], return_type=string_type))
        global_scope.define(BuiltInFunctionSymbol(name='to_int', params=[VarSymbol('value', any_type)], return_type=int_type))
        global_scope.define(BuiltInFunctionSymbol(name='to_float', params=[VarSymbol('value', any_type)], return_type=float_type))
        global_scope.define(BuiltInFunctionSymbol(name='typeof', params=[VarSymbol('value', any_type)], return_type=string_type))
        global_scope.define(BuiltInFunctionSymbol(name='len', params=[VarSymbol('value', any_type)], return_type=int_type))
        global_scope.define(BuiltInFunctionSymbol(name='abs', params=[VarSymbol('number', any_type)], return_type=any_type))
        global_scope.define(BuiltInFunctionSymbol(name='round', params=[VarSymbol('number', float_type)], return_type=int_type))
        global_scope.define(BuiltInFunctionSymbol(name='sum', params=[VarSymbol('list', list_type)], return_type=any_type))
        global_scope.define(BuiltInFunctionSymbol(name='max', params=[VarSymbol('list', list_type)], return_type=any_type))
        global_scope.define(BuiltInFunctionSymbol(name='min', params=[VarSymbol('list', list_type)], return_type=any_type))

        # =================================================================
        # PASSO 4: Iniciar a análise do programa do usuário
        # =================================================================
        
        for child in node.statements:
            self.visit(child)
        
        print("--- Análise Semântica Concluída com Sucesso ---")

    def visit_BlockNode(self, node):
        # 1. Cria um novo escopo aninhado ao escopo atual
        block_scope = ScopedSymbolTable(
            scope_name='block',
            scope_level=self.current_scope.scope_level + 1,
            enclosing_scope=self.current_scope
        )
        # 2. Entra no novo escopo
        self.current_scope = block_scope

        # Visita todas as declarações dentro do novo escopo
        for statement in node.statements:
            self.visit(statement)

        # 3. Sai do escopo do bloco, restaurando o escopo anterior
        self.current_scope = self.current_scope.enclosing_scope

    def visit_VarDeclNode(self, node):
        var_name = node.var_name_token.value
        if self.current_scope.lookup(var_name, current_scope_only=True):
            self.error(f"Variável '{var_name}' já declarada neste escopo.", node.var_name_token)  # Corrigido aqui também para ser mais preciso

        right_type = self.visit(node.value_node)

        final_type = right_type
        if node.type_hint_node:
            hint_type_name = node.type_hint_node.name
            hint_type_symbol = self.current_scope.lookup(hint_type_name)
            if not hint_type_symbol:
                self.error(f"Tipo '{hint_type_name}' desconhecido.", node.type_hint_node)

            error_msg = f"Não se pode atribuir o tipo '{right_type.name if right_type else 'desconhecido'}' a uma variável do tipo '{hint_type_symbol.name}'."

            # --- A CORREÇÃO ESTÁ AQUI ---
            # Adicione 'node.value_node' como o último argumento
            self.check_type_compatibility(hint_type_symbol, right_type, error_msg, node.value_node)
            # --- FIM DA CORREÇÃO ---

            final_type = hint_type_symbol

        var_symbol = VarSymbol(var_name, type=final_type, is_const=node.is_const)
        self.current_scope.define(var_symbol)

    def visit_AssignNode(self, node):
        right_type = self.visit(node.value_node)

        # --- LÓGICA ATUALIZADA PARA CRIAR CAMPOS DINAMICAMENTE ---
        if isinstance(node.left_node, AttributeAccessNode):
            # O lado esquerdo é algo como 'self.x'
            attr_access_node = node.left_node
            object_type = self.visit(attr_access_node.object_node)

            if not isinstance(object_type, TypeSymbol):
                self.error("Acesso a atributo só é permitido em instâncias de tipos.", attr_access_node)

            attr_name = attr_access_node.attribute_token.value
            member_symbol = object_type.lookup_member(attr_name)

            # Se o membro (campo) não existe, nós o criamos!
            if not member_symbol:
                new_field = VarSymbol(attr_name, type=right_type)
                object_type.fields[attr_name] = new_field
                return  # A atribuição é válida, pois está criando o campo.
            # Se o membro já existe, continuamos com a checagem de tipo normal...
        # --- FIM DA LÓGICA ATUALIZADA ---

        # Lógica antiga para variáveis normais e campos existentes
        left_type = self.visit(node.left_node)

        if isinstance(node.left_node, VarAccessNode):
            var_symbol = self.current_scope.lookup(node.left_node.var_name)
            if var_symbol and var_symbol.is_const:
                self.error(f"Não é possível atribuir a uma constante '{var_symbol.name}'.", node)

        error_msg = f"Não se pode atribuir o tipo '{right_type.name}' a uma variável do tipo '{left_type.name}'."
        self.check_type_compatibility(left_type, right_type, error_msg, node.value_node)

    def visit_NumberNode(self, node):
        return self.current_scope.lookup('int' if node.token.type == 'INT' else 'float')

    def visit_StringNode(self, node):
        return self.current_scope.lookup('string')

    def visit_BoolNode(self, node):
        return self.current_scope.lookup('bool')

    def visit_NullNode(self, node):
        return self.current_scope.lookup('null')

    def visit_VarAccessNode(self, node):
        var_name = node.var_name
        var_symbol = self.current_scope.lookup(var_name)
        if not var_symbol:
            self.error(f"Variável '{var_name}' não foi declarada.", node)
        
        # --- LÓGICA CORRIGIDA ---
        # Se o símbolo é um tipo, módulo ou enum, ele é o próprio "tipo".
        if isinstance(var_symbol, (TypeSymbol, ModuleSymbol, EnumSymbol)):
            return var_symbol
        
        # Se for uma variável comum, retornamos o tipo da variável.
        return var_symbol.type

    # --- FUNÇÃO CORRIGIDA ---
    def visit_BinOpNode(self, node):
        left_type = self.visit(node.left_node)
        right_type = self.visit(node.right_node)
        op = node.op_token

        if op.type == 'PLUS' and (left_type.name == 'string' or right_type.name == 'string'):
            return self.current_scope.lookup('string')
        
        if not left_type or not right_type:
            # Se um dos lados não tem tipo, o resultado é desconhecido
            return self.current_scope.lookup('any')

        # --- LÓGICA REFINADA PARA O TIPO 'any' ---
        if left_type.name == 'any' or right_type.name == 'any':
            # Operações de comparação e lógicas sempre resultam em 'bool'
            if op.type in (T_EQ, T_NE, T_LT, T_GT, T_LTE, T_GTE) or op.value in ('and', 'or'):
                return self.current_scope.lookup('bool')
            
            # Concatenação de string com '+' resulta em string
            if op.type == T_PLUS and (left_type.name == 'string' or right_type.name == 'string'):
                return self.current_scope.lookup('string')
            
            # Para todas as outras operações com 'any' (ex: any + int, any * any),
            # não podemos saber o resultado estaticamente, então ele é 'any'.
            return self.current_scope.lookup('any')
        
        # --- O resto da lógica para tipos estritos continua igual ---
        if op.type in (T_PLUS, T_MINUS, T_MUL, T_DIV, T_POW, T_MOD):
            if not (left_type.name in ('int', 'float') and right_type.name in ('int', 'float')):
                self.error(f"Operador '{op.value}' inválido para os tipos '{left_type.name}' e '{right_type.name}'.", node)
            if left_type.name == 'float' or right_type.name == 'float':
                return self.current_scope.lookup('float')
            return self.current_scope.lookup('int')

        if op.type in (T_EQ, T_NE, T_LT, T_GT, T_LTE, T_GTE) or op.value in ('and', 'or'):
            return self.current_scope.lookup('bool')

        if op.type in (T_AMPERSAND, T_PIPE, T_CARET, T_LSHIFT, T_RSHIFT):
            if not (left_type.name == 'int' and right_type.name == 'int'):
                self.error(f"Operadores bitwise só podem ser usados com o tipo 'int'.", node)
            return self.current_scope.lookup('int')
            
        self.error(f"Operador binário '{op.value}' não suportado para os tipos '{left_type.name}' e '{right_type.name}'.", node)

    def visit_UnaryOpNode(self, node):
        return self.visit(node.node)

    def visit_ProcessDeclNode(self, node):
        proc_name = node.name
        if self.current_scope.lookup(proc_name, current_scope_only=True):
            self.error(f"Símbolo '{proc_name}' já declarado neste escopo.", node)

        # Lógica para tipo de retorno (a mesma de antes)
        return_type_symbol = None
        if node.return_type_node:
            return_type_name = node.return_type_node.name
            return_type_symbol = self.current_scope.lookup(return_type_name)
            if not return_type_symbol:
                self.error(f"Tipo de retorno '{return_type_name}' não definido.", node.return_type_node)

        # Cria o símbolo do processo e o define no escopo ATUAL
        proc_symbol = ProcessSymbol(proc_name, return_type=return_type_symbol)
        self.current_scope.define(proc_symbol)

        # Guarda o estado atual do analisador
        previous_process = self.current_process_symbol
        self.current_process_symbol = proc_symbol

        # Cria o ESCOPO INTERNO da função
        proc_scope = ScopedSymbolTable(proc_name, self.current_scope.scope_level + 1, self.current_scope)
        self.current_scope = proc_scope

        # --- LÓGICA SIMPLIFICADA (UMA PASSAGEM) ---
        param_types = []
        for param_node in node.params:
            # 1. Analisa o nó do parâmetro (isso o define no proc_scope)
            self.visit(param_node)
            # 2. Pega o símbolo que acabou de ser definido
            param_symbol = self.current_scope.lookup(param_node.var_name_token.value)
            # 3. Adiciona o símbolo à lista de parâmetros do ProcessSymbol
            proc_symbol.params.append(param_symbol)
            # 4. Adiciona o TIPO do símbolo à lista de tipos para o FunctionTypeSymbol
            param_types.append(param_symbol.type)
        # --- FIM DA LÓGICA SIMPLIFICADA ---

        # Agora, com a lista de tipos pronta, cria o TIPO FUNÇÃO e anexa ao símbolo
        proc_symbol.type = FunctionTypeSymbol(
            name=proc_name,
            param_types=param_types,
            return_type=return_type_symbol
        )

        # Analisa o corpo da função
        self.visit(node.body_node)

        # Restaura o escopo e o estado do analisador
        self.current_scope = self.current_scope.enclosing_scope
        self.current_process_symbol = previous_process

    def visit_ProcessCallNode(self, node):
        callable_symbol = self.visit(node.node_to_call)
        
        if callable_symbol is None:
            self.error("Tentativa de chamar um valor nulo ou 'void'.", node)

        # --- LÓGICA DE INSTANCIAÇÃO CORRIGIDA ---
        if isinstance(callable_symbol, TypeSymbol):
            # É uma instanciação, como Carro(...)
            init_method = callable_symbol.lookup_member('__init__')
            
            if init_method:
                 # Nós visitamos a chamada ao construtor para VALIDAR os argumentos,
                 # mas ignoramos o seu valor de retorno (que é 'null').
                 self.visit(MethodCallNode(
                     node.node_to_call, 
                     Token(T_IDENTIFIER, '__init__'), # Token de mentira para o nome do método
                     node.arg_nodes
                 ))
            
            # O tipo da expressão de instanciação é SEMPRE o próprio tipo da classe.
            return callable_symbol
        # --- FIM DA CORREÇÃO ---

        # Validação para funções normais (continua igual)
        if not isinstance(callable_symbol, (ProcessSymbol, BuiltInFunctionSymbol)):
             self.error(f"O símbolo '{callable_symbol.name}' não é chamável.", node)

        params = callable_symbol.params
        arg_types = [self.visit(arg) for arg in node.arg_nodes]
        
        min_args = sum(1 for p in params if not p.is_optional)
        max_args = len(params)
        num_provided_args = len(arg_types)

        if not (min_args <= num_provided_args <= max_args):
            expected_str = f"{min_args}" if min_args == max_args else f"de {min_args} a {max_args}"
            self.error(f"Função '{callable_symbol.name}' espera {expected_str} argumentos, mas recebeu {num_provided_args}.", node)

        for i, param_symbol in enumerate(params[:num_provided_args]):
            arg_type = arg_types[i]
            error_msg = f"Argumento {i+1}: tipo '{arg_type.name}' incompatível com o parâmetro tipo '{param_symbol.type.name}'."
            self.check_type_compatibility(param_symbol.type, arg_type, error_msg, node.arg_nodes[i])
        
        return callable_symbol.type.return_type

    def visit_WhenNode(self, node):
        condition_type = self.visit(node.condition_node)
        if condition_type and condition_type.name != 'bool':
            # A CORREÇÃO É ADICIONAR ', node' AQUI
            self.error("Condição de 'when' deve ser um booleano.", node)
            
        self.visit(node.then_block)
        if node.else_block:
            self.visit(node.else_block)

    def visit_WhileNode(self, node):
        self.loop_level += 1
        condition_type = self.visit(node.condition_node)
        if condition_type and condition_type.name != 'bool':
            self.error("Condição de 'while' deve ser um booleano.")
        self.visit(node.body_node)
        self.loop_level -= 1

    def visit_BreakNode(self, node):
        if self.loop_level == 0:
            self.error("'break' só pode ser usado dentro de um loop.")

    def visit_ContinueNode(self, node):
        # A regra para 'continue' é a mesma que para 'break':
        # só pode ser usado dentro de um loop.
        if self.loop_level == 0:
            self.error("'continue' só pode ser usado dentro de um loop.", node)

    def visit_ReturnNode(self, node):
        if self.current_process_symbol is None:
            self.error("'return' só pode ser usado dentro de um processo.", node)

        expected_type = self.current_process_symbol.return_type

        # Se o processo não deveria retornar nada (void)
        if expected_type is None:
            if node.node_to_return:  # Se 'return' tem um valor
                self.error(f"O processo '{self.current_process_symbol.name}' não deveria retornar um valor.", node)
            return  # OK, return vazio

        # Se o processo deveria retornar um valor
        if not node.node_to_return:  # Se 'return' está vazio
            self.error(f"O processo '{self.current_process_symbol.name}' deve retornar um valor do tipo '{expected_type.name}'.", node)

        actual_type = self.visit(node.node_to_return)

        # Usamos nossa função de checagem de compatibilidade
        error_msg = (
            f"Tipo de retorno incompatível. O processo '{self.current_process_symbol.name}' "
            f"espera '{expected_type.name}', mas recebeu '{actual_type.name}'."
        )
        self.check_type_compatibility(expected_type, actual_type, error_msg, node.node_to_return)

    def visit_ForEachNode(self, node):
        self.loop_level += 1
        iterable_type = self.visit(node.iterable_node)

        # --- LÓGICA CORRIGIDA ---
        # Permite tipos de coleção conhecidos OU o tipo 'any'.
        # Só lança um erro se for um tipo que DEFINITIVAMENTE não é iterável (ex: int, bool).
        if (
            not isinstance(iterable_type, (ListTypeSymbol, TupleTypeSymbol, DictTypeSymbol)) 
            and iterable_type.name != 'any'
        ):
            self.error(f"O tipo '{iterable_type.name}' não é iterável e não pode ser usado em um loop 'for each'.", node.iterable_node)
        # --- FIM DA CORREÇÃO ---

        # Cria um novo escopo para o loop
        loop_scope = ScopedSymbolTable(
            'foreach_loop', 
            self.current_scope.scope_level + 1,
            self.current_scope
        )
        self.current_scope = loop_scope

        # Define a variável do loop com o tipo correto
        element_type = self.current_scope.lookup('any') # Padrão para o caso de a coleção ser 'any'
        if isinstance(iterable_type, (ListTypeSymbol, TupleTypeSymbol)):
            element_type = iterable_type.element_type
        elif isinstance(iterable_type, DictTypeSymbol):
            # Em um 'for each' em um dicionário, tradicionalmente iteramos sobre as chaves.
            element_type = iterable_type.key_type

        var_name = node.var_name_token.value
        var_symbol = VarSymbol(var_name, type=element_type)
        self.current_scope.define(var_symbol)

        # Analisa o corpo do loop
        self.visit(node.body_node)

        self.current_scope = self.current_scope.enclosing_scope
        self.loop_level -= 1

    def visit_TernaryOpNode(self, node):
        self.visit(node.true_expr)
        self.visit(node.condition_node)
        self.visit(node.false_expr)

    def visit_ListNode(self, node):
        if not node.element_nodes:
            element_type = self.current_scope.lookup('any')
        else:
            element_types = [self.visit(e) for e in node.element_nodes]
            element_type = element_types[0]

        # 1. Cria o tipo específico da lista, ex: 'list[int]'
        list_type = ListTypeSymbol(element_type)

        # 2. Copia os métodos do nosso "modelo" de lista para este novo tipo
        if 'list' in self._native_type_method_templates:
            list_type.methods = self._native_type_method_templates['list']

        return list_type

    def visit_TupleNode(self, node):
        # Visita cada elemento para obter seus tipos
        element_types = [self.visit(e) for e in node.element_nodes]
        
        # Cria e retorna o tipo da tupla
        tuple_type = TupleTypeSymbol(element_types)
        
        # Futuramente, você pode adicionar métodos nativos para tuplas aqui
        # if 'tuple' in self._native_type_method_templates:
        #     tuple_type.methods = self._native_type_method_templates['tuple']

        return tuple_type

    def visit_DictNode(self, node):
        any_type = self.current_scope.lookup('any')
        
        # Se o dicionário estiver vazio, o tipo é dict[any, any]
        if not node.pairs:
            dict_type = DictTypeSymbol(any_type, any_type)
        else:
            # Visita todas as chaves e valores primeiro
            key_types = [self.visit(k) for k, v in node.pairs]
            value_types = [self.visit(v) for k, v in node.pairs]

            # --- LÓGICA DE INFERÊNCIA APRIMORADA ---
            # Verifica se todos os tipos de chave são iguais
            final_key_type = key_types[0]
            for kt in key_types[1:]:
                if kt.name != final_key_type.name:
                    final_key_type = any_type # Se misturados, o tipo da chave vira 'any'
                    break
            
            # Verifica se todos os tipos de valor são iguais
            final_value_type = value_types[0]
            for vt in value_types[1:]:
                if vt.name != final_value_type.name:
                    final_value_type = any_type # Se misturados, o tipo do valor vira 'any'
                    break
            # --- FIM DA LÓGICA APRIMORADA ---

            dict_type = DictTypeSymbol(final_key_type, final_value_type)
        
        # Anexa os métodos nativos de dicionário (ex: .keys())
        if 'dict' in self._native_type_method_templates:
            dict_type.methods = self._native_type_method_templates['dict']
            
        return dict_type

    def visit_AttributeAccessNode(self, node):
        attr_name = node.attribute_token.value
        
        # --- Lógica para obter o símbolo à esquerda do '.' ---
        left_symbol = None
        if isinstance(node.object_node, VarAccessNode):
            var_name = node.object_node.var_name
            left_symbol = self.current_scope.lookup(var_name)
            if not left_symbol:
                self.error(f"O símbolo '{var_name}' não foi declarado.", node.object_node)
        elif isinstance(node.object_node, SuperNode):
             # O caso 'super' retorna o símbolo do membro diretamente, o que está correto
            parent_type = self.visit(node.object_node)
            member_symbol = parent_type.lookup_member(attr_name)
            if not member_symbol:
                self.error(f"O membro '{attr_name}' não foi encontrado na cadeia de herança de '{parent_type.name}'.", node.attribute_token)
            return member_symbol
        else:
            left_symbol = self.visit(node.object_node)

        # --- Lógica para encontrar o membro e retornar a coisa certa (TIPO ou SÍMBOLO) ---
        member_symbol = None
        
        if isinstance(left_symbol, ModuleSymbol):
            member_symbol = left_symbol.symbol_table.lookup(attr_name)
            if not member_symbol:
                self.error(f"O módulo '{left_symbol.name}' não possui um membro chamado '{attr_name}'.", node.attribute_token)

        elif isinstance(left_symbol, EnumSymbol):
            member_symbol = left_symbol.members.get(attr_name)
            if not member_symbol:
                self.error(f"O enum '{left_symbol.name}' não possui um membro chamado '{attr_name}'.", node.attribute_token)
        
        elif isinstance(left_symbol, TypeSymbol):
            member_symbol = left_symbol.lookup_member(attr_name)
            if not member_symbol:
                 self.error(f"O tipo '{left_symbol.name}' não possui um atributo ou método chamado '{attr_name}'.", node.attribute_token)
        
        else:
            type_name = left_symbol.type.name if hasattr(left_symbol, 'type') and left_symbol.type else 'desconhecido'
            self.error(f"Não é possível acessar o atributo '{attr_name}' em um valor do tipo '{type_name}'.", node.object_node)

        # --- REGRA FINAL: O que retornar? ---
        # Se o membro é um valor (variável, constante, membro de enum), retorne seu TIPO.
        if isinstance(member_symbol, (VarSymbol, EnumMemberSymbol)):
            return member_symbol.type
        
        # Se o membro é algo chamável (função, método), retorne o SÍMBOLO em si.
        elif isinstance(member_symbol, (ProcessSymbol, BuiltInFunctionSymbol)):
            return member_symbol
        
        # Fallback para outros tipos de símbolo que possam existir
        return member_symbol

    def visit_MethodCallNode(self, node):
        object_or_module = self.visit(node.object_node)
        method_name = node.method_token.value

        # --- LÓGICA DE DESPACHO APRIMORADA ---

        # Caso 1: A chamada é em um Módulo (ex: math.sqrt())
        if isinstance(object_or_module, ModuleSymbol):
            # Procura a função dentro da tabela de símbolos do módulo
            func_symbol = object_or_module.symbol_table.lookup(method_name)
            if not func_symbol or not isinstance(func_symbol, BuiltInFunctionSymbol):
                self.error(f"O módulo '{object_or_module.name}' não possui a função '{method_name}'.", node.method_token)
            
            # Reutiliza a lógica de validação de chamada de função que já temos
            # (Esta parte é idêntica à de visit_ProcessCallNode)
            params = func_symbol.params
            arg_types = [self.visit(arg) for arg in node.arg_nodes]
            min_args = sum(1 for p in params if not p.is_optional)
            max_args = len(params)
            if not (min_args <= len(arg_types) <= max_args):
                expected_str = f"{min_args}" if min_args == max_args else f"de {min_args} a {max_args}"
                self.error(f"Função '{func_symbol.name}' espera {expected_str} argumentos, mas recebeu {len(arg_types)}.", node)
            for i, param_symbol in enumerate(params[:len(arg_types)]):
                self.check_type_compatibility(param_symbol.type, arg_types[i], f"Argumento {i+1} da função '{func_symbol.name}': tipo '{arg_types[i].name}' incompatível com o tipo esperado '{param_symbol.type.name}'.", node.arg_nodes[i])
            return func_symbol.type.return_type

        # Caso 2: A chamada é em um Tipo de Classe (continua como antes)
        elif isinstance(object_or_module, TypeSymbol):
            method_symbol = object_or_module.lookup_member(method_name)
            if not method_symbol or not isinstance(method_symbol, (ProcessSymbol, BuiltInFunctionSymbol)):
                self.error(f"O tipo '{object_or_module.name}' não possui um método chamado '{method_name}'.", node.method_token)
            
            callable_type = method_symbol.type
            arg_types = [self.visit(arg_node) for arg_node in node.arg_nodes]
            
            params_to_check = method_symbol.params[1:] if isinstance(method_symbol, ProcessSymbol) else method_symbol.params
            min_args = sum(1 for p in params_to_check if not p.is_optional)
            max_args = len(params_to_check)

            if not (min_args <= len(arg_types) <= max_args):
                expected_str = f"{min_args}" if min_args == max_args else f"de {min_args} a {max_args}"
                self.error(f"Método '{method_name}' espera {expected_str} argumentos, mas recebeu {len(arg_types)}.", node)
            
            for i, param_symbol in enumerate(params_to_check[:len(arg_types)]):
                self.check_type_compatibility(param_symbol.type, arg_types[i], f"Argumento {i+1} do método '{method_name}': tipo '{arg_types[i].name}' incompatível com tipo '{param_symbol.type.name}'.", node.arg_nodes[i])
            
            return callable_type.return_type
        
        else:
            self.error(f"Não é possível chamar métodos em um valor do tipo '{object_or_module.name if object_or_module else 'desconhecido'}'.", node.object_node)

    def visit_IndexAccessNode(self, node):
        collection_type = self.visit(node.object_node)
        index_type = self.visit(node.index_node)

        if collection_type.name == 'any':
            return self.current_scope.lookup('any')

        elif isinstance(collection_type, self.current_scope.lookup('string').__class__):
             if index_type.name != 'int':
                self.error("O índice de uma string deve ser um inteiro.", node.index_node)
             # O resultado de aceder a um caractere de uma string é outra string
             return self.current_scope.lookup('string')

        if isinstance(collection_type, ListTypeSymbol):
            if index_type.name != 'int':
                self.error("Índice de lista deve ser um inteiro.", node.index_node)
            return collection_type.element_type

        elif isinstance(collection_type, DictTypeSymbol):
            error_msg = f"Tipo de chave incompatível para o dicionário. Esperado '{collection_type.key_type.name}', mas recebeu '{index_type.name}'."
            # --- CORREÇÃO AQUI: Adiciona 'node.index_node' como último argumento ---
            self.check_type_compatibility(
                collection_type.key_type, 
                index_type,
                error_msg,
                node.index_node
            )
            return collection_type.value_type
        
        else:
            self.error(f"O tipo '{collection_type.name}' não suporta acesso por índice '[]'.", node.object_node)

    def visit_TypeDeclNode(self, node):
        type_name = node.name_token.value
        parent_symbol = None

        if node.parent_name_node:
            parent_name = node.parent_name_node.name
            parent_symbol = self.current_scope.lookup(parent_name)
            if not parent_symbol or not isinstance(parent_symbol, TypeSymbol):
                self.error(f"O tipo pai '{parent_name}' é inválido.", node.parent_name_node)
            if parent_symbol.name == type_name:
                self.error("Um tipo não pode herdar de si mesmo.", node.name_token)
        
        # Cria o símbolo do tipo, passando o pai
        type_symbol = TypeSymbol(type_name, parent_type_symbol=parent_symbol)
        self.current_scope.define(type_symbol)

        # Define o estado da classe atual para que os métodos saibam a quem pertencem
        previous_class_symbol = self.current_class_symbol
        self.current_class_symbol = type_symbol

        # Entra em um novo escopo para os membros da classe
        type_scope = ScopedSymbolTable(type_name, self.current_scope.scope_level + 1, self.current_scope)
        self.current_scope = type_scope
        
        # --- LÓGICA DE REGISTRO ADICIONADA AQUI ---
        # Visita e REGISTRA todos os campos e métodos no TypeSymbol
        for field_node in node.fields:
            self.visit(field_node)
            # Pega o símbolo que foi definido no escopo e o adiciona ao dicionário do tipo
            field_symbol = self.current_scope.lookup(field_node.var_name_token.value)
            type_symbol.fields[field_symbol.name] = field_symbol

        for method_node in node.methods:
            self.visit(method_node)
            # Pega o símbolo do método e o adiciona ao dicionário do tipo
            method_symbol = self.current_scope.lookup(method_node.name)
            type_symbol.methods[method_symbol.name] = method_symbol
        # --- FIM DA LÓGICA DE REGISTRO ---

        # Sai do escopo da classe
        self.current_scope = self.current_scope.enclosing_scope
        
        # Restaura o estado de classe anterior
        self.current_class_symbol = previous_class_symbol

    def visit_LambdaNode(self, node):
        # Guarda o processo anterior
        previous_process = self.current_process_symbol
        
        # --- A CORREÇÃO PRINCIPAL ESTÁ AQUI ---
        # Primeiro, pegamos o tipo 'any' para usar como retorno padrão
        any_type = self.current_scope.lookup('any')
        # Agora, criamos o símbolo do processo JÁ COM o tipo de retorno
        lambda_symbol = ProcessSymbol('<lambda>', return_type=any_type)
        self.current_process_symbol = lambda_symbol
        # --- FIM DA CORREÇÃO ---

        # Cria o escopo da lambda
        lambda_scope = ScopedSymbolTable(
            'lambda',
            self.current_scope.scope_level + 1,
            self.current_scope
        )
        self.current_scope = lambda_scope
        
        # Analisa os parâmetros e coleta seus tipos
        param_types = []
        for param_node in node.params_node:
            self.visit(param_node)
            param_symbol = self.current_scope.lookup(param_node.var_name_token.value)
            param_types.append(param_symbol.type)

        # Analisa o corpo da lambda
        self.visit(node.body_node)
        
        # Restaura o escopo e o processo anterior
        self.current_scope = self.current_scope.enclosing_scope
        self.current_process_symbol = previous_process
        
        # Retorna um tipo função que descreve a lambda
        func_type_name = f"lambda_({','.join([t.name for t in param_types])})"
        return FunctionTypeSymbol(func_type_name, param_types, any_type)

    def visit_TypeNode(self, node):
        pass

    def visit_ParamNode(self, node):
        param_name = node.var_name_token.value
        type_symbol = None
        
        # --- LÓGICA ADICIONADA PARA TRATAR 'self' ---
        # Se o parâmetro é 'self' E estamos dentro da análise de uma classe...
        if param_name == 'self' and self.current_class_symbol:
            # O tipo de 'self' é a própria classe!
            type_symbol = self.current_class_symbol
            # Um erro comum é anotar o tipo de self, o que é redundante.
            if node.type_node:
                self.error("O parâmetro 'self' não pode ter uma anotação de tipo.", node.type_node)
        # --- FIM DA LÓGICA 'self' ---
        
        # Se não for 'self', a lógica continua como antes
        elif node.type_node:
            type_name = node.type_node.name
            type_symbol = self.current_scope.lookup(type_name)
            if not type_symbol:
                self.error(f"O tipo '{type_name}' do parâmetro '{param_name}' não foi definido.", node.type_node)
        else:
            type_symbol = self.current_scope.lookup('any')

        if self.current_scope.lookup(param_name, current_scope_only=True):
            self.error(f"Parâmetro '{param_name}' já foi definido.", node)

        param_symbol = VarSymbol(param_name, type=type_symbol)
        self.current_scope.define(param_symbol)

    def visit_FieldDeclNode(self, node):
        pass
    
    def visit_SuperNode(self, node):
        # Regra 1: 'super' deve estar dentro de um método.
        if not self.current_process_symbol:
            self.error("'super' só pode ser usado dentro de um método.", node)

        # Regra 2: O método deve pertencer a uma classe.
        if not self.current_class_symbol:
            self.error("'super' só pode ser usado dentro de um método de uma classe.", node)

        # Regra 3: A classe deve ter uma classe pai.
        if not self.current_class_symbol.parent_type_symbol:
            self.error(f"'super' usado na classe base '{self.current_class_symbol.name}', que não tem pai.", node)

        # Se todas as regras passaram, o 'valor' de 'super' é o tipo da classe pai.
        return self.current_class_symbol.parent_type_symbol

    # Em lucida_analyzer.py, na classe SemanticAnalyzer

    def visit_ImportNode(self, node):
        module_name = node.filepath_node.value
        namespace = node.namespace_token.value

        if self.current_scope.lookup(namespace, current_scope_only=True):
            self.error(f"O nome '{namespace}' já está em uso neste escopo.", node.namespace_token)

        semantic_scope = None

        # 1. Procura primeiro nos módulos nativos INTERNOS
        if module_name in NATIVE_MODULES_SEMANTICS:
            semantic_scope = NATIVE_MODULES_SEMANTICS[module_name]
        else:
            # 2. Se não achar, procura por um arquivo .py na pasta 'lib'
            try:
                plugin_path = Path('lib') / f'{module_name}.py'
                if not plugin_path.exists():
                    self.error(f"Módulo '{module_name}' não encontrado.", node)

                spec = importlib.util.spec_from_file_location(module_name, plugin_path)
                python_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(python_module)

                # 3. Chama a função 'register_semantics' para pegar a descrição
                if hasattr(python_module, 'register_semantics'):
                    semantic_scope = python_module.register_semantics()
                else:
                    self.error(f"O módulo externo '{module_name}' não possui a função 'register_semantics()'.", node)
            except Exception as e:
                self.error(f"Falha ao carregar a semântica do módulo externo '{module_name}': {e}", node)

        # O resto do processo é o mesmo
        if semantic_scope:
            module_symbol = ModuleSymbol(namespace, symbol_table=semantic_scope)
            self.current_scope.define(module_symbol)
    
    def visit_InterpolatedStringNode(self, node):
        # Percorre todas as partes da string interpolada
        for part in node.parts:
            # Visita cada parte. Se for um StringNode, não faz nada.
            # Se for um nó de expressão, ele será validado.
            self.visit(part)
        
        # O tipo de uma f-string é sempre 'string'
        return self.current_scope.lookup('string')

    def visit_ListComprehensionNode(self, node):
        # Esta função transforma a AST de [expr for each var in iterable]
        # na AST para o seguinte código Lucida:
        #
        # {
        #     let __comp_list = [];
        #     for each var in iterable {
        #         __comp_list.append(expr);
        #     }
        #     __comp_list;
        # }
        
        # 1. Cria um nome único para a lista temporária
        temp_list_name = f"__comp_list_{node.line}_{node.col}"
        temp_list_token = Token(T_IDENTIFIER, temp_list_name, node.line, node.col)
        
        # 2. Cria o nó para a declaração da lista: let __comp_list = []
        list_decl_node = VarDeclNode(
            var_name_token=temp_list_token,
            value_node=ListNode(node.token, []),
            is_const=False,
            type_hint_node=None
        )

        # 3. Cria o nó para o corpo do loop: __comp_list.append(expr)
        append_call = MethodCallNode(
            object_node=VarAccessNode(temp_list_token),
            method_token=Token(T_IDENTIFIER, 'append', node.expression_node.line, node.expression_node.col),
            arg_nodes=[node.expression_node]
        )
        loop_body = BlockNode(node.token, [append_call])
        
        # 4. Cria o nó do loop 'for each'
        for_each_node = ForEachNode(
            for_token=node.token,
            var_name_token=node.var_name_token,
            iterable_node=node.iterable_node,
            body_node=loop_body
        )

        # 5. Cria o nó de acesso final à lista, que será o valor de retorno do bloco
        final_access_node = VarAccessNode(temp_list_token)

        # 6. Junta tudo em um único Bloco de código
        comprehension_block = BlockNode(
            node.token,
            [list_decl_node, for_each_node, final_access_node]
        )
        
        # --- A CORREÇÃO MÁGICA ---
        # Em vez de retornar um tipo, nós efetivamente substituímos este nó
        # pelo bloco que acabamos de criar, visitando-o imediatamente.
        # O analisador continuará a partir daqui como se o programador
        # tivesse escrito o 'for' loop manualmente.
        return self.visit(comprehension_block)
