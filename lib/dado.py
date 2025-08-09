# lib/dado.py
import random
from lucida_symbols import VarSymbol, BuiltInFunctionSymbol, ScopedSymbolTable, BuiltInTypeSymbol

# --- Lógica de Runtime ---
def lf_d6(args):
    return random.randint(1, 6)

def lf_rolar_entre(args):
    if len(args) != 2: raise TypeError("rolar_entre() espera 2 argumentos (min, max)")
    min_val, max_val = int(args[0]), int(args[1])
    return random.randint(min_val, max_val)

NATIVE_DADO_MODULE = {
    'd6': lf_d6,
    'rolar_entre': lf_rolar_entre,
}

# --- Descrição Semântica ---
def register_semantics():
    int_type = BuiltInTypeSymbol('int')
    module_scope = ScopedSymbolTable(scope_name='dado', scope_level=2)
    module_scope.define(BuiltInFunctionSymbol(name='d6', params=[], return_type=int_type))
    
    # --- A DEFINIÇÃO QUE PROVAVELMENTE FALTA ---
    module_scope.define(
        BuiltInFunctionSymbol(
            name='rolar_entre',
            params=[VarSymbol('min', int_type), VarSymbol('max', int_type)],
            return_type=int_type
        )
    )
    # -----------------------------------------
    
    return module_scope