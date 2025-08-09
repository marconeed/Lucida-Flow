# lib/json.py
import json
from lucida_symbols import VarSymbol, BuiltInFunctionSymbol, ScopedSymbolTable, BuiltInTypeSymbol

# --- PARTE 1: Lógica de Runtime ---

def lf_json_parse(args):
    if len(args) != 1: raise TypeError("parse() espera 1 argumento (a string JSON)")
    try:
        return json.loads(args[0])
    except json.JSONDecodeError as e:
        raise ValueError(f"String JSON inválida: {e}")

def lf_json_stringify(args):
    obj_to_stringify = args[0]
    indent = int(args[1]) if len(args) > 1 else None
    return json.dumps(obj_to_stringify, indent=indent, ensure_ascii=False)

NATIVE_JSON_MODULE = {
    "parse": lf_json_parse,
    "stringify": lf_json_stringify,
}

# --- PARTE 2: Descrição Semântica ---

def register_semantics():
    string_type = BuiltInTypeSymbol('string')
    int_type = BuiltInTypeSymbol('int')
    any_type = BuiltInTypeSymbol('any')
    
    module_scope = ScopedSymbolTable(scope_name='json', scope_level=2)
    module_scope.define(
        BuiltInFunctionSymbol(
            name='parse', 
            params=[VarSymbol('json_string', string_type)], 
            return_type=any_type
        )
    )
    module_scope.define(
        BuiltInFunctionSymbol(
            name='stringify', 
            params=[VarSymbol('objeto', any_type), VarSymbol('indent', int_type, is_optional=True)],
            return_type=string_type
        )
    )
    return module_scope