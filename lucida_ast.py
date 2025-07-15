# Copie e cole TODO este conteúdo em seu arquivo lucida_ast.py

class ASTNode:
    """
    Nó base para todos os outros nós da AST.
    Agora, cada nó armazena sua localização (linha e coluna)
    a partir de um token de referência.
    """
    def __init__(self, token=None):
        self.token = token
        if token:
            self.line = token.line
            self.col = token.col
        else:
            self.line = 0
            self.col = 0

# --- Nós de Expressão (representam valores) ---

class SuperNode(ASTNode):
    """Representa a palavra-chave 'super'."""
    def __init__(self, token):
        super().__init__(token)
        self.token = token

    def __repr__(self):
        return f"SuperNode"

class NumberNode(ASTNode):
    def __init__(self, token):
        super().__init__(token)
        self.token = token
        self.value = token.value
    def __repr__(self):
        return f"NumberNode({self.value})"

class StringNode(ASTNode):
    def __init__(self, token):
        super().__init__(token)
        self.token = token
        self.value = token.value
    def __repr__(self):
        return f"StringNode({repr(self.value)})"

class BoolNode(ASTNode):
    def __init__(self, token):
        super().__init__(token)
        self.token = token
        self.value = True if token.value == 'true' else False
    def __repr__(self):
        return f"BoolNode({self.value})"

class NullNode(ASTNode):
    def __init__(self, token):
        super().__init__(token)
        self.token = token
        self.value = None
    def __repr__(self):
        return "NullNode"

class UnaryOpNode(ASTNode):
    def __init__(self, op_token, node):
        super().__init__(op_token)
        self.op_token = op_token
        self.node = node
    def __repr__(self):
        return f"UnaryOpNode(op={self.op_token.value}, expr={self.node})"

class BinOpNode(ASTNode):
    def __init__(self, left_node, op_token, right_node):
        super().__init__(op_token)
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node
    def __repr__(self):
        return f"BinOpNode({self.left_node}, {self.op_token.value}, {self.right_node})"

class TernaryOpNode(ASTNode):
    # ATUALIZADO para a nova sintaxe
    def __init__(self, condition_node, question_token, true_expr, false_expr):
        super().__init__(question_token) # A posição é a do '?'
        self.condition_node = condition_node
        self.true_expr = true_expr
        self.false_expr = false_expr
    def __repr__(self):
        return f"TernaryOpNode({self.condition_node} ? {self.true_expr} : {self.false_expr})"

class ListNode(ASTNode):
    # NOTA: O Parser precisa passar o token de abertura '['
    def __init__(self, start_token, element_nodes):
        super().__init__(start_token)
        self.element_nodes = element_nodes
    def __repr__(self):
        return f"ListNode(elements={self.element_nodes})"

class TupleNode(ASTNode):
    # NOTA: O Parser precisa passar o token de abertura '('
    def __init__(self, start_token, element_nodes):
        super().__init__(start_token)
        self.element_nodes = element_nodes
    def __repr__(self):
        return f"TupleNode(elements={self.element_nodes})"

class DictNode(ASTNode):
    # NOTA: O Parser precisa passar o token de abertura '{'
    def __init__(self, start_token, pairs):
        super().__init__(start_token)
        self.pairs = pairs
    def __repr__(self):
        return f"DictNode(pairs={self.pairs})"

class VarAccessNode(ASTNode):
    def __init__(self, token):
        super().__init__(token)
        self.token = token
        self.var_name = token.value
    def __repr__(self):
        return f"VarAccessNode(name='{self.var_name}')"

class IndexAccessNode(ASTNode):
    # O token de referência é o '[' que inicia o acesso
    def __init__(self, object_node, index_node, start_bracket_token):
        super().__init__(start_bracket_token)
        self.object_node = object_node
        self.index_node = index_node
    def __repr__(self):
        return f"IndexAccessNode(object={self.object_node}, index={self.index_node})"

class ProcessCallNode(ASTNode):
    # A posição da chamada é a do nome do processo/função
    def __init__(self, node_to_call, arg_nodes):
        super().__init__(node_to_call.token)
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes
    def __repr__(self):
        return f"ProcessCallNode(name='{self.node_to_call.var_name}', args={self.arg_nodes})"

class AttributeAccessNode(ASTNode):
    # A posição é a do atributo sendo acessado
    def __init__(self, object_node, attribute_token):
        super().__init__(attribute_token)
        self.object_node = object_node
        self.attribute_token = attribute_token
    def __repr__(self):
        return f"AttributeAccessNode(object={self.object_node}, attribute='{self.attribute_token.value}')"

class MethodCallNode(ASTNode):
    # A posição é a do nome do método
    def __init__(self, object_node, method_token, arg_nodes):
        super().__init__(method_token)
        self.object_node = object_node
        self.method_token = method_token
        self.arg_nodes = arg_nodes
    def __repr__(self):
        return f"MethodCallNode(object={self.object_node}, method='{self.method_token.value}', args={self.arg_nodes})"

class LambdaNode(ASTNode):
    # NOTA: O Parser precisa passar o token 'process'
    def __init__(self, process_token, params_node, body_node):
        super().__init__(process_token)
        self.params_node = params_node
        self.body_node = body_node
    def __repr__(self):
        return f"LambdaNode(params={self.params_node}, body={self.body_node})"

# --- Nós de Statement (representam ações ou estruturas) ---

class ProgramNode(ASTNode):
    def __init__(self, statements):
        super().__init__() # O programa como um todo não tem um token único
        self.statements = statements
    def __repr__(self):
        return f"ProgramNode({self.statements})"

class BlockNode(ASTNode):
    # NOTA: O Parser precisa passar o token de abertura '{'
    def __init__(self, start_brace_token, statements):
        super().__init__(start_brace_token)
        self.statements = statements
    def __repr__(self):
        return f"BlockNode({self.statements})"

class VarDeclNode(ASTNode):
    def __init__(self, var_name_token, value_node, is_const, type_hint_node=None):
        super().__init__(var_name_token)
        self.var_name_token = var_name_token
        self.value_node = value_node
        self.is_const = is_const
        self.type_hint_node = type_hint_node

class AssignNode(ASTNode):
    # NOTA: O Parser precisa passar o token de atribuição (ex: '=')
    def __init__(self, left_node, op_token, value_node):
        super().__init__(op_token)
        self.left_node = left_node
        self.value_node = value_node
    def __repr__(self):
        return f"AssignNode({self.left_node} = {self.value_node})"

class WhenNode(ASTNode):
    # NOTA: O Parser precisa passar o token 'when'
    def __init__(self, when_token, condition_node, then_block, else_block):
        super().__init__(when_token)
        self.condition_node = condition_node
        self.then_block = then_block
        self.else_block = else_block

class WhileNode(ASTNode):
    # NOTA: O Parser precisa passar o token 'while'
    def __init__(self, while_token, condition_node, body_node):
        super().__init__(while_token)
        self.condition_node = condition_node
        self.body_node = body_node

class ForEachNode(ASTNode):
    # NOTA: O Parser precisa passar o token 'for'
    def __init__(self, for_token, var_name_token, iterable_node, body_node):
        super().__init__(for_token)
        self.var_name_token = var_name_token
        self.iterable_node = iterable_node
        self.body_node = body_node

class BreakNode(ASTNode):
    def __init__(self, token):
        super().__init__(token)
        self.token = token

class ContinueNode(ASTNode):
    def __init__(self, token):
        super().__init__(token)
        self.token = token

class ReturnNode(ASTNode):
    # NOTA: O Parser precisa passar o token 'return'
    def __init__(self, return_token, node_to_return):
        super().__init__(return_token)
        self.node_to_return = node_to_return

class ProcessDeclNode(ASTNode):
    def __init__(self, proc_name_token, params, return_type_node, body_node):
        super().__init__(proc_name_token)
        self.proc_name_token = proc_name_token
        self.name = proc_name_token.value
        self.params = params
        self.return_type_node = return_type_node
        self.body_node = body_node

class ParamNode(ASTNode):
    def __init__(self, var_name_token, type_node):
        super().__init__(var_name_token)
        self.var_name_token = var_name_token
        self.type_node = type_node

class TypeNode(ASTNode):
    def __init__(self, token):
        super().__init__(token)
        self.token = token
        self.name = token.value

class TypeDeclNode(ASTNode):
    # Modificamos o __init__ para aceitar um 'parent_name_node'
    def __init__(self, name_token, parent_name_node, fields, methods):
        super().__init__(name_token)
        self.name_token = name_token
        self.parent_name_node = parent_name_node # <--- A NOVA LINHA
        self.fields = fields
        self.methods = methods

class ImportNode(ASTNode):
    # NOTA: O Parser precisa passar o token 'import'
    def __init__(self, import_token, filepath_node, namespace_token):
        super().__init__(import_token)
        self.filepath_node = filepath_node
        self.namespace_token = namespace_token

class EnumNode(ASTNode):
    """
    Representa uma declaração de enum completa. Ex: 'define enum Status { ... }'
    """
    def __init__(self, enum_token, name_token, member_tokens):
        super().__init__(enum_token)
        self.name_token = name_token      # O token com o nome do enum
        self.member_tokens = member_tokens # Uma lista de tokens com os nomes dos membros

    def __repr__(self):
        member_names = [t.value for t in self.member_tokens]
        return f"EnumNode(name='{self.name_token.value}', members={member_names})"

class TryCatchNode(ASTNode):
    """Representa a estrutura completa 'try-catch-finally'."""
    def __init__(self, try_token, try_block, catch_clauses, finally_block):
        super().__init__(try_token)
        self.try_block = try_block
        self.catch_clauses = catch_clauses  # Uma lista de CatchNode
        self.finally_block = finally_block  # Pode ser None

class CatchNode(ASTNode):
    """Representa uma única cláusula 'catch (e: TipoErro) { ... }'."""
    def __init__(self, catch_token, var_token, type_node, body_block):
        super().__init__(catch_token)
        self.var_token = var_token          # O token da variável (ex: 'e')
        self.type_node = type_node          # O nó do tipo do erro (ex: 'FileNotFoundError')
        self.body_block = body_block        # O bloco de código a ser executado

class InterpolatedStringNode(ASTNode):
    """Representa uma f-string, contendo uma lista de partes."""
    def __init__(self, start_token, parts):
        super().__init__(start_token)
        # 'parts' é uma lista de nós, que podem ser StringNode ou qualquer outro nó de expressão.
        self.parts = parts

    def __repr__(self):
        return f"InterpolatedStringNode(parts={self.parts})"

class ListComprehensionNode(ASTNode):
    """Representa uma compreensão de lista: [expr for each var in iterable]"""
    def __init__(self, start_token, expression_node, var_name_token, iterable_node):
        super().__init__(start_token)
        self.expression_node = expression_node # A expressão a ser avaliada (ex: n * n)
        self.var_name_token = var_name_token   # A variável do loop (ex: n)
        self.iterable_node = iterable_node     # A lista a ser percorrida (ex: numeros)