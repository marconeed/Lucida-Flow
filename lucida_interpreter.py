# Copie e cole TODO este conteúdo em seu arquivo do Interpretador

import numpy as np
from lucida_ast import *
from lucida_lexer import *
from lucida_symbols import *
from lucida_parser import Parser
from lucida_errors import LucidaRuntimeError
from lucida_stdlib import NATIVE_MODULES
from lucida_stdlib import NATIVE_MODULES_SEMANTICS
import importlib.util # Para carregar código Python dinamicamente
import sys # Para ajustar o caminho de busca
from pathlib import Path # Para manipular caminhos de arquivo
from lucida_stdlib import NATIVE_TYPE_METHODS
# Removido o import do SemanticAnalyzer, pois não é usado aqui
# from lucida_analyzer import SemanticAnalyzer

class LfEnum:
    """Representa o tipo de um enum em tempo de execução. Ex: 'Status'"""
    def __init__(self, name):
        self.name = name
        self.members = {}

    def __repr__(self):
        return f"<Enum type {self.name}>"

class LfEnumMember:
    """Representa um membro específico de um enum. Ex: 'Status.CONECTADO'"""
    def __init__(self, enum_type, name):
        self.enum_type = enum_type
        self.name = name

    def __repr__(self):
        return f"{self.enum_type.name}.{self.name}"

# --- Classes de Suporte para o Runtime ---
class BuiltInFunction:
    # ATUALIZADO: agora guarda a função Python real
    def __init__(self, name, python_callable=None):
        self.name = name
        self.python_callable = python_callable

    def __repr__(self):
        return f"<BuiltInFunction name='{self.name}'>"

class ActivationRecord:
    def __init__(self, name, nesting_level, enclosing_scope=None):
        self.name = name
        self.nesting_level = nesting_level
        self.members = {}
        self.enclosing_scope = enclosing_scope

    def __setitem__(self, key, value):
        self.members[key] = value

    def __getitem__(self, key):
        return self.members.get(key)

    def get(self, key):
        val = self.members.get(key)
        if val is not None:
            return val
        if self.enclosing_scope is not None:
            return self.enclosing_scope.get(key)
        return None

    def __repr__(self):
        return f"<ActivationRecord(name='{self.name}')>"
    
    def find_scope(self, key):
        """Procura recursivamente o escopo que contém a variável 'key'."""
        # Se a chave existe nos membros deste escopo, encontramos.
        if key in self.members:
            return self
        
        # Se não, e se houver um escopo pai, pede para ele procurar.
        if self.enclosing_scope is not None:
            return self.enclosing_scope.find_scope(key)
            
        # Se chegamos ao topo sem encontrar, ela não existe.
        return None

class CallStack:
    def __init__(self):
        self._records = []

    def push(self, record):
        self._records.append(record)

    def pop(self):
        return self._records.pop()

    def peek(self):
        return self._records[-1]

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value
class BreakException(Exception): pass
class ContinueException(Exception): pass

class Process:
    def __init__(self, name, params_node, body_node, defining_scope):
        self.name, self.params_node, self.body_node, self.defining_scope = name, params_node, body_node, defining_scope
    def __repr__(self): return f"<Process name='{self.name}'>"

class LfInstance:
    def __init__(self, type_symbol):
        self.type_symbol = type_symbol
        self.fields = {}
    def __repr__(self):
        return f"<instância de {self.type_symbol.name} com campos {self.fields}>"

class BoundMethod:
    # ATUALIZADO para guardar a classe onde o método foi definido
    def __init__(self, instance, process, bound_class_symbol):
        self.instance = instance
        self.process = process
        self.bound_class_symbol = bound_class_symbol # <-- NOVO

    def __repr__(self):
        return f"<Método vinculado {self.process.name} da classe {self.bound_class_symbol.name}>"

class SuperProxy:
    """Um objeto temporário que representa 'super' durante a execução."""
    def __init__(self, instance, bound_class_symbol):
        self.instance = instance # A instância original (self)
        self.bound_class_symbol = bound_class_symbol # A classe onde o 'super' foi chamado

    def __repr__(self):
        return f"<SuperProxy para a classe {self.bound_class_symbol.name}>"

class NodeVisitor:
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'; visitor = getattr(self, method_name, self.generic_visit); return visitor(node)
    def generic_visit(self, node): raise Exception(f'Nenhum método visit_{type(node).__name__} encontrado na classe {type(self).__name__}')

class BoundNativeMethod:
    """Representa um método nativo vinculado a uma instância, como 'minha_lista.append'."""
    def __init__(self, instance, python_callable):
        self.instance = instance  # O valor em si (ex: a lista [1,2] ou a string "olá")
        self.python_callable = python_callable # A função Python que faz o trabalho

    def __repr__(self):
        return f"<BoundNativeMethod for {type(self.instance).__name__}>"

class Interpreter(NodeVisitor):
    def __init__(self):
        self.call_stack = CallStack()
        global_scope = ActivationRecord('global', 1)
        self.call_stack.push(global_scope)
        # Centralizamos o registro de todas as funções e tipos nativos
        self._register_global_builtins(global_scope)

    def _register_global_builtins(self, scope):
        # Tipos
        scope['int'] = TypeSymbol('int')
        scope['float'] = TypeSymbol('float')
        scope['string'] = TypeSymbol('string')
        scope['bool'] = TypeSymbol('bool')
        scope['null'] = TypeSymbol('null')
        scope['any'] = TypeSymbol('any')
        
        # Funções
        scope['print'] = BuiltInFunction('print', lambda args: print(*args))
        scope['read'] = BuiltInFunction('read', lambda args: input(args[0] if args else ""))
        scope['len'] = BuiltInFunction('len', lambda args: len(args[0]))
        scope['typeof'] = BuiltInFunction('typeof', lambda args: self._lf_typeof(args[0]))
        
        # Funções de conversão
        scope['to_int'] = BuiltInFunction('to_int', lambda args: int(args[0]))
        scope['to_float'] = BuiltInFunction('to_float', lambda args: float(args[0]))

        # Funções matemáticas
        scope['abs'] = BuiltInFunction('abs', lambda args: abs(args[0]))
        scope['round'] = BuiltInFunction('round', lambda args: round(*args))
        scope['sum'] = BuiltInFunction('sum', lambda args: sum(args[0]))
        scope['max'] = BuiltInFunction('max', lambda args: max(args[0]))
        scope['min'] = BuiltInFunction('min', lambda args: min(args[0]))

    def _lf_typeof(self, value):
        # Função auxiliar para typeof, para manter a lógica limpa
        if isinstance(value, bool): return "bool"
        if isinstance(value, int): return "int"
        if isinstance(value, float): return "float"
        if isinstance(value, str): return "string"
        if isinstance(value, list): return "list"
        if isinstance(value, tuple): return "tuple"
        if isinstance(value, dict): return "dict"
        if isinstance(value, LfEnumMember): return value.enum_type.name # ex: 'Status'
        if isinstance(value, LfEnum): return 'enum_type' # O tipo de um tipo enum é 'enum_type'
        if isinstance(value, LfInstance): return value.type_symbol.name
        if value is None: return "null"
        return "unknown"

    def visit_ImportNode(self, node):
        module_name = node.filepath_node.value
        namespace = node.namespace_token.value
        
        # 1. Procura primeiro nos módulos nativos INTERNOS
        if module_name in NATIVE_MODULES:
            module_data = NATIVE_MODULES[module_name]
        else:
            # 2. Se não achar, procura por um arquivo .py em uma pasta 'lib'
            try:
                # Constrói o caminho para o arquivo do plugin
                plugin_path = Path('lib') / f'{module_name}.py'

                if not plugin_path.exists():
                    self.error(f"Módulo '{module_name}' não encontrado.", node)

                # Carrega o arquivo .py dinamicamente
                spec = importlib.util.spec_from_file_location(module_name, plugin_path)
                python_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(python_module)

                # 3. Chama a função 'register_module' para pegar as definições
                if hasattr(python_module, 'register_module'):
                    module_data = python_module.register_module()
                else:
                    self.error(f"O módulo externo '{module_name}' não possui a função 'register_module()'.", node)
            except Exception as e:
                self.error(f"Falha ao carregar o módulo externo '{module_name}': {e}", node)
        
        # O resto do processo é o mesmo para ambos os tipos de módulo
        module_scope = ActivationRecord(name=namespace, nesting_level=self.call_stack.peek().nesting_level)
        for name, value in module_data.items():
            if callable(value):
                module_scope[name] = BuiltInFunction(name, python_callable=value)
            else:
                module_scope[name] = value
        
        self.call_stack.peek()[namespace] = module_scope

    @property
    def global_scope(self):
        return self.call_stack._records[0]

    def error(self, message, node, error_type="RuntimeException"):
        raise LucidaRuntimeError(message, node.line, node.col, error_type)

    def visit_EnumNode(self, node):
        enum_name = node.name_token.value
        enum_type_obj = LfEnum(enum_name)
        
        for member_token in node.member_tokens:
            member_name = member_token.value
            member_obj = LfEnumMember(enum_type_obj, member_name)
            enum_type_obj.members[member_name] = member_obj
            
        self.call_stack.peek()[enum_name] = enum_type_obj

    def visit_ProgramNode(self, node):
        for statement in node.statements:
            self.visit(statement)

    def visit_BlockNode(self, node):
        # 1. Cria um novo escopo (registro de ativação) aninhado ao atual
        block_scope = ActivationRecord(
            name='block',
            nesting_level=self.call_stack.peek().nesting_level + 1,
            enclosing_scope=self.call_stack.peek()
        )
        # 2. Empilha o novo escopo, tornando-o o escopo ativo
        self.call_stack.push(block_scope)

        result = None
        # Itera sobre todas as declarações, exceto a última
        for statement in node.statements[:-1]:
            try:
                self.visit(statement)
            except (BreakException, ContinueException) as e:
                # Se um break/continue acontecer, sai do escopo e propaga a exceção
                self.call_stack.pop()
                raise e
        
        # Visita e guarda o valor da última declaração no bloco
        if node.statements:
            result = self.visit(node.statements[-1])
        
        # 3. Desempilha o escopo, destruindo todas as suas variáveis
        self.call_stack.pop()
        
        # Retorna o resultado da última expressão do bloco
        return result

    def visit_VarDeclNode(self, node):
        var_name = node.var_name_token.value
        value = self.visit(node.value_node)
        self.call_stack.peek()[var_name] = value

    def visit_AssignNode(self, node):
        # Avalia o valor da direita primeiro
        value_to_assign = self.visit(node.value_node)
        left_node = node.left_node

        # Caso 1: Atribuição a uma variável (ex: x = 10)
        if isinstance(left_node, VarAccessNode):
            var_name = left_node.var_name
            
            # Procura o escopo onde a variável foi originalmente declarada
            target_scope = self.call_stack.peek().find_scope(var_name)
            
            if target_scope is None:
                self.error(f"Variável '{var_name}' não foi declarada.", node.left_node)
            else:
                # Atualiza a variável no escopo ONDE ELA FOI ENCONTRADA
                target_scope[var_name] = value_to_assign
                
        # Caso 2: Atribuição a um índice (ex: d["chave"] = 123)
        elif isinstance(left_node, IndexAccessNode):
            container = self.visit(left_node.object_node)
            key = self.visit(left_node.index_node)
            if not isinstance(container, (list, dict)):
                self.error("Atribuição por índice só é permitida em listas ou dicionários.", left_node.object_node)
            container[key] = value_to_assign

        # Caso 3: Atribuição a um atributo (ex: self.x = 10)
        elif isinstance(left_node, AttributeAccessNode):
            instance = self.visit(left_node.object_node)
            if not isinstance(instance, LfInstance):
                 self.error("Atribuição de atributo só é permitida em instâncias.", left_node)
            attr_name = left_node.attribute_token.value
            instance.fields[attr_name] = value_to_assign
            
        else:
            self.error("Alvo de atribuição inválido.", node)

    def visit_VarAccessNode(self, node):
        var_name = node.var_name
        current_scope = self.call_stack.peek()
        
        # Loop que sobe na hierarquia dos escopos para encontrar a variável
        temp_scope = current_scope
        while temp_scope is not None:
            if var_name in temp_scope.members:
                # Se existe, retorna seu valor, mesmo que seja 'None' (null)
                return temp_scope.members[var_name]
            
            # Se não encontrou, passa para o escopo pai
            temp_scope = temp_scope.enclosing_scope
            
        # Se o loop terminar, a variável realmente não existe em nenhum escopo.
        self.error(f"Variável '{var_name}' não definida.", node)

    def visit_NumberNode(self, node): return node.value
    def visit_StringNode(self, node): return node.value
    def visit_BoolNode(self, node): return node.value
    def visit_NullNode(self, node): return None
    def visit_ListNode(self, node):
        return [self.visit(e) for e in node.element_nodes]

    def visit_TupleNode(self, node):
        return tuple(self.visit(e) for e in node.element_nodes)

    def visit_DictNode(self, node):
        py_dict = {}
        for key_node, value_node in node.pairs:
            py_dict[self.visit(key_node)] = self.visit(value_node)
        return py_dict

    def visit_UnaryOpNode(self, node):
        op = node.op_token.type
        op_val = node.op_token.value
        value = self.visit(node.node)
        if op == T_MINUS:
            return -value
        if op == T_PLUS:
            return +value
        if op == T_TILDE:
            return ~value
        if op == T_KEYWORD and op_val == 'not':
            return not bool(value)
        raise Exception(f"Operador unário desconhecido: {op_val}")

    def visit_BinOpNode(self, node):
        left = self.visit(node.left_node)
        op_token = node.op_token
        right = self.visit(node.right_node)

        try:
            if op_token.type == T_PLUS:
                return left + right
            if op_token.type == T_MINUS:
                return left - right
            if op_token.type == T_MUL:
                return left * right
            if op_token.type == T_DIV:
                if right in (0, 0.0):
                    self.error("Divisão por zero.", node, error_type='ArithmeticError')
                return left / right
            if op_token.type == T_POW:
                return left ** right
            if op_token.type == T_MOD:
                return left % right
            if op_token.type == T_EQ:
                return left == right
            if op_token.type == T_NE:
                return left != right
            if op_token.type == T_LT:
                return left < right
            if op_token.type == T_GT:
                return left > right
            if op_token.type == T_LTE:
                return left <= right
            if op_token.type == T_GTE:
                return left >= right
            if op_token.type == T_AMPERSAND:
                return left & right
            if op_token.type == T_PIPE:
                return left | right
            if op_token.type == T_CARET:
                return left ^ right
            if op_token.type == T_LSHIFT:
                return left << right
            if op_token.type == T_RSHIFT:
                return left >> right
            if op_token.value == 'and':
                return bool(left) and bool(right)
            if op_token.value == 'or':
                return bool(left) or bool(right)
        except TypeError:
            tipo_esq = type(left).__name__
            tipo_dir = type(right).__name__
            self.error(f"Não é possível aplicar o operador '{op_token.value}' aos tipos '{tipo_esq}' e '{tipo_dir}'.", node)

    def visit_WhenNode(self, node):
        if bool(self.visit(node.condition_node)):
            self.visit(node.then_block)
        elif node.else_block is not None:
            self.visit(node.else_block)
    def visit_WhileNode(self, node):
        while bool(self.visit(node.condition_node)):
            try:
                self.visit(node.body_node)
            except ContinueException:
                continue
            except BreakException:
                break

    def visit_ForEachNode(self, node):
        iterable = self.visit(node.iterable_node)
        if not isinstance(iterable, (list, tuple, str, dict)):
            self.error("O objeto em um loop 'for each' deve ser uma coleção (lista, tupla, string ou dicionário).", node.iterable_node)
        
        var_name = node.var_name_token.value
        
        # Loop sobre a coleção
        for item in iterable:
            # --- LÓGICA DE ESCOPO CORRIGIDA ---
            # 1. Cria um novo escopo para CADA iteração do loop.
            loop_body_scope = ActivationRecord(
                'foreach_body',
                self.call_stack.peek().nesting_level + 1,
                self.call_stack.peek()
            )
            
            # 2. Define a variável do loop (ex: 'item') DENTRO deste novo escopo.
            loop_body_scope[var_name] = item
            
            # 3. Empilha o escopo, tornando-o ativo para a execução do corpo.
            self.call_stack.push(loop_body_scope)
            
            try:
                # 4. Executa o corpo do loop.
                self.visit(node.body_node)
            except ContinueException:
                # Se 'continue' for chamado, o escopo atual é removido e o loop continua.
                self.call_stack.pop()
                continue
            except BreakException:
                # Se 'break' for chamado, o escopo atual é removido e o loop para.
                self.call_stack.pop()
                break
            
            # 5. Remove o escopo do corpo do loop no final da iteração.
            self.call_stack.pop()
            # --- FIM DA LÓGICA CORRIGIDA ---

    def visit_TypeDeclNode(self, node):
        type_name = node.name_token.value
        parent_type_symbol = None

        if node.parent_name_node:
            parent_name = node.parent_name_node.name
            parent_type_symbol = self.call_stack.peek().get(parent_name)

        type_symbol = TypeSymbol(type_name, parent_type_symbol=parent_type_symbol)

        # ADICIONADO: Guarde os nós dos campos para usar no construtor
        type_symbol.field_nodes = node.fields

        self.call_stack.peek()[type_name] = type_symbol

        defining_scope = self.call_stack.peek()
        for method_node in node.methods:
            proc_name = method_node.name
            method_proc = Process(proc_name, method_node.params, method_node.body_node, defining_scope)
            type_symbol.methods[proc_name] = method_proc

    def visit_ProcessDeclNode(self, node):
        proc_name = node.name
        defining_scope = self.call_stack.peek()
        process = Process(proc_name, node.params, node.body_node, defining_scope)
        defining_scope[proc_name] = process
        
    def visit_ProcessCallNode(self, node):
        callable_obj = self.visit(node.node_to_call)
        evaluated_args = [self.visit(arg) for arg in node.arg_nodes]

        if isinstance(callable_obj, Process):
            return self.call_process(callable_obj, evaluated_args)
        elif isinstance(callable_obj, BoundMethod):
            return self.call_bound_method(callable_obj, evaluated_args)
        elif isinstance(callable_obj, BuiltInFunction):
            # A correção é adicionar ', node' ao final desta chamada.
            return self.call_builtin(callable_obj, evaluated_args, node)
        elif isinstance(callable_obj, BoundNativeMethod):
            # Chama a função python associada, passando a instância e os argumentos
            return callable_obj.python_callable(callable_obj.instance, evaluated_args)
        elif isinstance(callable_obj, TypeSymbol):
            return self.instantiate_type(callable_obj, evaluated_args, node) # Passe o 'node'

        self.error(f"Objeto do tipo '{type(callable_obj).__name__}' não é chamável.", node)

    def visit_LambdaNode(self, node):
        defining_scope = self.call_stack.peek()
        return Process(name='<lambda>', params_node=node.params_node, body_node=node.body_node, defining_scope=defining_scope)

    def instantiate_type(self, type_symbol, evaluated_args, node):
        # 1. Cria a instância "vazia"
        instance = LfInstance(type_symbol)

        # 2. Inicializa os campos com valores padrão da hierarquia
        types_in_chain = []
        curr_type = type_symbol
        while curr_type:
            types_in_chain.insert(0, curr_type)
            curr_type = curr_type.parent_type_symbol

        for t in types_in_chain:
            if hasattr(t, 'field_nodes'):
                for field_decl_node in t.field_nodes:
                    field_name = field_decl_node.var_name_token.value
                    if field_name not in instance.fields:
                        instance.fields[field_name] = self.visit(field_decl_node.value_node)

        # 3. Procura e chama o construtor __init__
        init_method = type_symbol.lookup_member('__init__')

        if init_method:
            bound_init = BoundMethod(instance, init_method, type_symbol)
            # A chamada aqui agora passa o 'node' adiante, como esperado
            self.call_bound_method(bound_init, evaluated_args, node)

        # 4. Retorna a instância completamente inicializada
        return instance

    def call_builtin(self, func, evaluated_args, node):
        if not func.python_callable:
            self.error(f"A função nativa '{func.name}' não foi implementada.", node)
        
        try:
            # Chama a função Python real (ex: lf_fs_read)
            return func.python_callable(evaluated_args)
        # Transforma erros do Python em nossos LucidaRuntimeError com a etiqueta correta
        except FileNotFoundError as e:
            self.error(str(e), node, error_type='FileNotFoundError')
        except ValueError as e:
            self.error(str(e), node, error_type='ValueError')
        except TypeError as e:
            self.error(str(e), node, error_type='TypeError')
        except Exception as e:
            # Captura genérica para outros erros inesperados
            self.error(f"Erro interno na função nativa '{func.name}': {e}", node, error_type='Exception')
            
    def call_process(self, process, evaluated_args):
        expected_params = len(process.params_node)
        if expected_params != len(evaluated_args):
            raise TypeError(f"Processo '{process.name}' espera {expected_params} argumentos, mas recebeu {len(evaluated_args)}.")
        
        enclosing_scope = process.defining_scope
        new_scope = ActivationRecord(process.name, enclosing_scope.nesting_level + 1, enclosing_scope)
        
        for param_node, arg_value in zip(process.params_node, evaluated_args):
            new_scope[param_node.var_name_token.value] = arg_value
            
        self.call_stack.push(new_scope)
        return_value = None
        try: self.visit(process.body_node)
        except ReturnException as e: return_value = e.value
        self.call_stack.pop(); return return_value
        
    def call_bound_method(self, bound_method, evaluated_args, node):
        process = bound_method.process
        instance = bound_method.instance # Este é o 'self' implícito

        # A lista de parâmetros que o método DECLARA (ex: [self, x, y])
        expected_params_list = process.params_node
        
        # A lista de argumentos que o método REALMENTE recebe
        # (o 'self' implícito + os argumentos que o usuário passou)
        full_args_list = [instance] + evaluated_args
        
        # 1. Verifica se o número total de parâmetros bate com o número total de argumentos
        if len(expected_params_list) != len(full_args_list):
            num_expected_user_args = len(expected_params_list) - 1 if len(expected_params_list) > 0 else 0
            num_provided_user_args = len(evaluated_args)
            self.error(
                f"Método '{process.name}' espera {num_expected_user_args} argumentos, mas recebeu {num_provided_user_args}.",
                node
            )

        # 2. Configura o novo escopo para a chamada
        enclosing_scope = process.defining_scope
        new_scope = ActivationRecord(process.name, enclosing_scope.nesting_level + 1, enclosing_scope)
        
        # 3. Mapeia cada NOME de parâmetro para cada VALOR de argumento
        for param_node, arg_value in zip(expected_params_list, full_args_list):
            new_scope[param_node.var_name_token.value] = arg_value
        
        # 4. CRÍTICO: Salva a classe do método na memória da chamada para que 'super' funcione!
        new_scope['_bound_class'] = bound_method.bound_class_symbol
            
        # 5. Executa o corpo do método
        self.call_stack.push(new_scope)
        return_value = None
        try:
            self.visit(process.body_node)
        except ReturnException as e:
            return_value = e.value
        self.call_stack.pop()
        return return_value

    def visit_ReturnNode(self, node): raise ReturnException(self.visit(node.node_to_return))
    def visit_BreakNode(self, node): raise BreakException()
    def visit_ContinueNode(self, node): raise ContinueException()
    
    # --- FUNÇÃO CORRIGIDA ---
    def visit_AttributeAccessNode(self, node):
        obj = self.visit(node.object_node)
        attr_name = node.attribute_token.value

        # Caso 1: Acesso em 'super' (ex: super.iniciar)
        if isinstance(obj, SuperProxy):
            start_type = obj.bound_class_symbol.parent_type_symbol
            current_type = start_type
            while current_type:
                if attr_name in current_type.methods:
                    method_process = current_type.methods[attr_name]
                    return BoundMethod(
                        instance=obj.instance,
                        process=method_process,
                        bound_class_symbol=current_type
                    )
                current_type = current_type.parent_type_symbol
            self.error(f"O membro '{attr_name}' não foi encontrado na cadeia 'super'.", node.attribute_token)

        # Caso 2: Acesso em um módulo (ex: m.sqrt)
        elif isinstance(obj, ActivationRecord):
            member = obj.get(attr_name)
            if member is None:
                self.error(f"O módulo '{obj.name}' não possui um membro chamado '{attr_name}'.", node.attribute_token)
            return member

        # Caso 3: Acesso em um Enum (ex: Status.ATIVO)
        elif isinstance(obj, LfEnum):
            member = obj.members.get(attr_name)
            if member is None:
                self.error(f"O enum '{obj.name}' não possui um membro chamado '{attr_name}'.", node.attribute_token)
            return member

        # Caso 4: Acesso em uma instância de um tipo Lucida (ex: meu_carro.marca)
        elif isinstance(obj, LfInstance):
            if attr_name in obj.fields:
                return obj.fields[attr_name]
            current_type = obj.type_symbol
            while current_type:
                if attr_name in current_type.methods:
                    method_process = current_type.methods[attr_name]
                    return BoundMethod(
                        instance=obj,
                        process=method_process,
                        bound_class_symbol=current_type
                    )
                current_type = current_type.parent_type_symbol
            self.error(f"O atributo ou método '{attr_name}' não foi encontrado no tipo '{obj.type_symbol.name}'.", node.attribute_token)

        # --- INÍCIO DA CORREÇÃO ---
        # Caso 5: Acesso em um dicionário Python (usado pelo nosso módulo 'gui')
        elif isinstance(obj, dict):
            if attr_name in obj:
                return obj[attr_name]
            # Se a chave não existe, procuramos nos métodos nativos de dicionário
            if 'dict' in NATIVE_TYPE_METHODS and attr_name in NATIVE_TYPE_METHODS['dict']:
                python_callable = NATIVE_TYPE_METHODS['dict'][attr_name]
                return BoundNativeMethod(instance=obj, python_callable=python_callable)
            
            self.error(f"A chave '{attr_name}' não foi encontrada no dicionário.", node.attribute_token)
        # --- FIM DA CORREÇÃO ---

        # Caso 6: Acesso em um tipo nativo (string, lista, etc.)
        else:
            py_type_name = type(obj).__name__
            lf_type_name = {'str': 'string', 'list': 'list', 'tuple': 'tuple'}.get(py_type_name)

            if lf_type_name and lf_type_name in NATIVE_TYPE_METHODS:
                methods_for_type = NATIVE_TYPE_METHODS[lf_type_name]
                if attr_name in methods_for_type:
                    python_callable = methods_for_type[attr_name]
                    return BoundNativeMethod(instance=obj, python_callable=python_callable)

            # Se não encontrou um método válido, lança o erro
            tipo_obj = self._lf_typeof(obj)
            self.error(f"Acesso a atributo '.' não é suportado para o tipo '{tipo_obj}'.", node.object_node)

    def visit_SuperNode(self, node):
        # Procura na memória da chamada atual pela classe do método em execução
        bound_class = self.call_stack.peek().get('_bound_class')
        # E também pela instância 'self'
        instance = self.call_stack.peek().get('self')
        
        # Cria nosso objeto proxy com o contexto necessário
        return SuperProxy(instance, bound_class)
    
    def visit_MethodCallNode(self, node):
        # Passo 1: Descobrir o que é o 'método'.
        # Fingimos um acesso a atributo para obter o objeto chamável.
        attr_access_node = AttributeAccessNode(node.object_node, node.method_token)
        callable_obj = self.visit(attr_access_node)

        # Passo 2: Avaliar os argumentos da chamada
        evaluated_args = [self.visit(arg) for arg in node.arg_nodes]

        # Caso 1: É um método de uma classe definida pelo usuário (ex: meu_carro.ligar())
        if isinstance(callable_obj, BoundMethod):
            return self.call_bound_method(callable_obj, evaluated_args, node)

        # Caso 2: É uma função global (embora seja raro chamar via '.')
        if isinstance(callable_obj, BuiltInFunction):
            return self.call_builtin(callable_obj, evaluated_args, node)

        # --- A CORREÇÃO PRINCIPAL ESTÁ AQUI ---
        # Caso 3: É um método nativo de um tipo como string ou lista
        if isinstance(callable_obj, BoundNativeMethod):
            try:
                # Chama a função Python associada, passando a instância e os argumentos
                return callable_obj.python_callable(callable_obj.instance, evaluated_args)
            except Exception as e:
                # Captura erros da execução do método nativo (ex: split com argumento errado)
                self.error(f"Erro ao executar o método nativo '{node.method_token.value}': {e}", node)
        # --- FIM DA CORREÇÃO ---

        # Se não for nenhum dos tipos chamáveis que conhecemos, é um erro.
        self.error(f"'{node.method_token.value}' não é um método ou função chamável.", node)

    def visit_IndexAccessNode(self, node):
        container = self.visit(node.object_node)
        index = self.visit(node.index_node)
        try:
            return container[index]
        except TypeError:
            self.error(f"O tipo '{type(container).__name__}' não suporta acesso por índice '[]'.", node.object_node)
        except IndexError:
            self.error("Índice fora dos limites da lista.", node.index_node)
        except KeyError:
            self.error(f"A chave {repr(index)} não foi encontrada no dicionário.", node.index_node)
    
    def visit_TernaryOpNode(self, node):
        if bool(self.visit(node.condition_node)):
            return self.visit(node.true_expr)
        else:
            return self.visit(node.false_expr)

    def visit_TryCatchNode(self, node):
        # A cláusula 'finally' em Python garante a execução do nosso 'finally'
        try:
            # Dentro do try principal, temos outro para o 'catch'
            try:
                # 1. Executa o bloco 'try' da Lucida-Flow
                self.visit(node.try_block)

            except LucidaRuntimeError as error_obj:
                # 2. Se um erro de runtime da Lucida ocorrer...
                error_caught = False
                for catch_clause in node.catch_clauses:
                    expected_error_type = catch_clause.type_node.name
                    actual_error_type = error_obj.error_type

                    # Captura se os tipos forem idênticos OU se o catch for para o genérico 'Exception'
                    if expected_error_type == actual_error_type or expected_error_type == 'Exception':
                        catch_scope = ActivationRecord('catch', self.call_stack.peek().nesting_level + 1, self.call_stack.peek())
                        error_var_name = catch_clause.var_token.value
                        catch_scope[error_var_name] = error_obj.message
                        
                        self.call_stack.push(catch_scope)
                        self.visit(catch_clause.body_block)
                        self.call_stack.pop()
                        
                        error_caught = True
                        break 
                
                if not error_caught:
                    raise error_obj
                    
        finally:
            # 3. Executa o bloco 'finally' da Lucida-Flow no final de tudo
            if node.finally_block:
                self.visit(node.finally_block)

    def visit_InterpolatedStringNode(self, node):
        final_string = ""
        for part in node.parts:
            # Avalia a parte. Se for um StringNode, o resultado é o próprio texto.
            # Se for um nó de expressão, o resultado será o valor da expressão.
            value = self.visit(part)
            
            # Converte o valor para string e o adiciona ao resultado final
            final_string += str(value)
            
        return final_string
