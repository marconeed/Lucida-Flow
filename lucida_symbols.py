# lucida_symbols.py
class Symbol:
    def __init__(self, name, type=None):
        self.name = name
        self.type = type

    def __repr__(self):
        return f"<{self.name}>"

class VarSymbol(Symbol):
    # Garanta que o __init__ esteja exatamente assim
    def __init__(self, name, type, is_const=False, is_optional=False):
        super().__init__(name, type)
        self.is_const = is_const
        self.is_optional = is_optional

    def __repr__(self):
        type_str = self.type.name if self.type else 'any'
        return f"<VarSymbol(name='{self.name}', type='{type_str}')>"

class TypeSymbol(Symbol):
    def __init__(self, name, parent_type_symbol=None):
        super().__init__(name)
        self.parent_type_symbol = parent_type_symbol # <-- Para lembrar o pai
        self.fields = {}
        self.methods = {}

    def __repr__(self):
        parent_str = f" < {self.parent_type_symbol.name}" if self.parent_type_symbol else ""
        return f"<TypeSymbol(name='{self.name}{parent_str}')>"

    def lookup_member(self, name):
        """
        Procura por um membro (campo ou método) neste tipo
        ou em qualquer um dos seus tipos pais, recursivamente.
        """
        # 1. Procura nos membros deste próprio tipo
        symbol = self.fields.get(name) or self.methods.get(name)
        if symbol:
            return symbol

        # 2. Se não encontrou, e tem um pai, procura no pai
        if self.parent_type_symbol:
            return self.parent_type_symbol.lookup_member(name)

        # 3. Se não tem pai e não encontrou, o membro não existe
        return None

class BuiltInTypeSymbol(TypeSymbol):
    def __init__(self, name):
        # Agora chama o __init__ de TypeSymbol
        super().__init__(name)

    # Não precisa mais de __repr__, pois herdará um bom de TypeSymbol.

class BuiltInFunctionSymbol(Symbol):
    # A definição agora inclui 'return_type=None'
    def __init__(self, name, params=None, return_type=None):
        # Chama o __init__ da classe Symbol base, mas sem passar o tipo ainda
        super().__init__(name) 
        self.params = params if params is not None else []
        self.return_type = return_type
        
        # --- MUDANÇA PRINCIPAL ---
        # Cria um tipo função para si mesmo e o armazena no atributo .type
        # que herdamos da classe Symbol.
        param_types = [p.type for p in self.params]
        self.type = FunctionTypeSymbol(
            name=name,
            param_types=param_types,
            return_type=return_type
        )

class ProcessSymbol(Symbol):
    def __init__(self, name, params=None, return_type=None):
        super().__init__(name)
        self.params = params if params is not None else []
        self.return_type = return_type
        # A nova propriedade para saber a qual classe um método pertence
        self.defining_class_symbol = None # <--- ADICIONE ESTA LINHA

    def __repr__(self):
        return f"<ProcessSymbol(name='{self.name}', params={self.params})>"
        

class ModuleSymbol(Symbol):
    def __init__(self, name, symbol_table=None):
        super().__init__(name)
        self.symbol_table = symbol_table

class ScopedSymbolTable:
    def __init__(self, scope_name, scope_level, enclosing_scope=None):
        self._symbols = {}
        self.scope_name = scope_name
        self.scope_level = scope_level
        self.enclosing_scope = enclosing_scope
        if scope_level == 1:
            self.define(BuiltInTypeSymbol('int'))
            self.define(BuiltInTypeSymbol('float'))
            self.define(BuiltInTypeSymbol('string'))
            self.define(BuiltInTypeSymbol('bool'))
            self.define(BuiltInTypeSymbol('null'))

    def define(self, symbol):
        self._symbols[symbol.name] = symbol

    def lookup(self, name, current_scope_only=False):
        symbol = self._symbols.get(name)
        if symbol is not None:
            return symbol
        if current_scope_only:
            return None
        if self.enclosing_scope is not None:
            return self.enclosing_scope.lookup(name)
        return None

class ListTypeSymbol(TypeSymbol):
    """Representa o tipo de uma lista, por exemplo: 'list[int]'."""
    def __init__(self, element_type):
        # O nome é construído dinamicamente
        super().__init__(f'list[{element_type.name}]')
        self.element_type = element_type

    def __repr__(self):
        return f"<ListTypeSymbol(element_type='{self.element_type.name}')>"

class TupleTypeSymbol(TypeSymbol):
    """Representa o tipo de uma tupla, ex: 'tuple[int, string]'."""
    def __init__(self, element_types):
        # O nome é construído dinamicamente
        element_names = ", ".join([t.name for t in element_types])
        super().__init__(f'tuple[{element_names}]')
        self.element_types = element_types

    def __repr__(self):
        return f"<TupleTypeSymbol(element_types={[t.name for t in self.element_types]})>"

class DictTypeSymbol(TypeSymbol):
    """Representa o tipo de um dicionário, por exemplo: 'dict[string, float]'."""
    def __init__(self, key_type, value_type):
        super().__init__(f'dict[{key_type.name}, {value_type.name}]')
        self.key_type = key_type
        self.value_type = value_type

    def __repr__(self):
        return f"<DictTypeSymbol(key='{self.key_type.name}', value='{self.value_type.name}')>"

class EnumSymbol(TypeSymbol):
    """ Representa o tipo de um enum, ex: 'Status'. """
    def __init__(self, name):
        super().__init__(name)
        # Os membros serão armazenados aqui durante a análise
        self.members = {} 

    def __repr__(self):
        return f"<EnumSymbol(name='{self.name}')>"

class EnumMemberSymbol(Symbol):
    """ Representa um membro de um enum, ex: 'Status.CONECTADO'. """
    def __init__(self, name, enum_type):
        super().__init__(name, enum_type)
    
    def __repr__(self):
        return f"<EnumMemberSymbol(name='{self.name}', type='{self.type.name}')>"

class FunctionTypeSymbol(TypeSymbol):
    """ Representa o tipo de uma função ou processo. """
    def __init__(self, name, param_types, return_type):
        super().__init__(name)
        self.param_types = param_types
        self.return_type = return_type

    def __repr__(self):
        param_str = ", ".join([p.name for p in self.param_types])
        return_str = self.return_type.name if self.return_type else 'void'
        return f"<FunctionTypeSymbol(params=({param_str}) -> {return_str})>"
