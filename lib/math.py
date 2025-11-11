# lib/math.py
from lucida_symbols import VarSymbol, BuiltInFunctionSymbol, ScopedSymbolTable, BuiltInTypeSymbol
import math

# --- PARTE 1: LÓGICA DE RUNTIME ---

def lf_soma(args):
    if len(args) != 2: raise TypeError("soma() espera 2 argumentos.")
    return float(args[0]) + float(args[1])

def lf_sub(args):
    if len(args) != 2: raise TypeError("sub() espera 2 argumentos.")
    return float(args[0]) - float(args[1])

def lf_mult(args):
    if len(args) != 2: raise TypeError("mult() espera 2 argumentos.")
    return float(args[0]) * float(args[1])

def lf_div(args):
    if len(args) != 2: raise TypeError("div() espera 2 argumentos.")
    if float(args[1]) == 0: raise ZeroDivisionError("Divisão por zero.")
    return float(args[0]) / float(args[1])

def lf_pot(args):
    if len(args) != 2: raise TypeError("pot() espera 2 argumentos.")
    return float(args[0]) ** float(args[1])


# O dicionário que o Interpreter irá usar
NATIVE_MATH_MODULE = {
    "soma": lf_soma,
    "sub": lf_sub,
    "mult": lf_mult,
    "div": lf_div,
    "pot": lf_pot,
    "pi": math.pi,
}

# --- PARTE 2: DESCRIÇÃO SEMÂNTICA ---

def register_semantics():
    float_type = BuiltInTypeSymbol('float')
    any_type = BuiltInTypeSymbol('any')
    
    module_scope = ScopedSymbolTable(scope_name='math', scope_level=2)
    
    module_scope.define(VarSymbol('pi', float_type))
    module_scope.define(BuiltInFunctionSymbol('soma', params=[VarSymbol('a', any_type), VarSymbol('b', any_type)], return_type=float_type))
    module_scope.define(BuiltInFunctionSymbol('sub', params=[VarSymbol('a', any_type), VarSymbol('b', any_type)], return_type=float_type))
    module_scope.define(BuiltInFunctionSymbol('mult', params=[VarSymbol('a', any_type), VarSymbol('b', any_type)], return_type=float_type))
    module_scope.define(BuiltInFunctionSymbol('div', params=[VarSymbol('a', any_type), VarSymbol('b', any_type)], return_type=float_type))
    module_scope.define(BuiltInFunctionSymbol('pot', params=[VarSymbol('a', any_type), VarSymbol('b', any_type)], return_type=float_type))
    
    return module_scope