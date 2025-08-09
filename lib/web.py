# lib/web.py
import requests
from lucida_symbols import VarSymbol, BuiltInFunctionSymbol, ScopedSymbolTable, BuiltInTypeSymbol

# --- PARTE 1: Lógica de Runtime ---

def lf_web_get(args):
    if len(args) != 1:
        raise TypeError("A função get() espera 1 argumento (a URL)")
    url = str(args[0])
    try:
        response = requests.get(url)
        response.raise_for_status() # Lança um erro para status HTTP ruins (4xx ou 5xx)
        return response.text
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro de rede ao aceder a '{url}': {e}")

NATIVE_WEB_MODULE = {
    "get": lf_web_get,
}

# --- PARTE 2: Descrição Semântica ---

def register_semantics():
    string_type = BuiltInTypeSymbol('string')
    any_type = BuiltInTypeSymbol('any')
    
    module_scope = ScopedSymbolTable(scope_name='web', scope_level=2)
    module_scope.define(
        BuiltInFunctionSymbol(
            name='get',
            params=[VarSymbol('url', string_type)],
            return_type=string_type
        )
    )
    return module_scope