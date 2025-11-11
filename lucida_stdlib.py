# Copie e cole TODO este conteúdo em seu arquivo lucida_stdlib.py

# --- Importações do Python ---
import math
import time
import os
import datetime

from lib.web import NATIVE_WEB_MODULE, register_semantics as register_web_semantics
from lib.json import NATIVE_JSON_MODULE, register_semantics as register_json_semantics
from lib.dado import NATIVE_DADO_MODULE, register_semantics as register_dado_semantics
from lib.math import NATIVE_MATH_MODULE, register_semantics as register_math_semantics
from lib.media import NATIVE_MEDIA_MODULE, register_semantics as register_media_semantics

# --- Importações dos Símbolos da Lucida-Flow ---
# (Necessário para a parte de descrição semântica)
from lucida_symbols import (
    VarSymbol, BuiltInFunctionSymbol, ScopedSymbolTable, BuiltInTypeSymbol,
    ListTypeSymbol, DictTypeSymbol, TupleTypeSymbol
)


# ==============================================================================
#  PARTE 1: IMPLEMENTAÇÃO EM TEMPO DE EXECUÇÃO (PARA O INTERPRETADOR)
# ==============================================================================

# --- Funções do Módulo 'math' ---
def lf_sqrt(args):
    if len(args) != 1:
        raise TypeError(f"sqrt() espera 1 argumento, mas recebeu {len(args)}")
    return math.sqrt(args[0])

def lf_sin(args):
    if len(args) != 1:
        raise TypeError(f"sin() espera 1 argumento, mas recebeu {len(args)}")
    return math.sin(args[0])

# --- Funções do Módulo 'time' ---
def lf_now(args):
    if len(args) != 0:
        raise TypeError(f"now() espera 0 argumentos, mas recebeu {len(args)}")
    return time.time()

# --- Funções do Módulo 'fs' ---
def lf_fs_write(args):
    if len(args) != 2:
        raise TypeError(f"write() espera 2 argumentos (caminho, conteudo), mas recebeu {len(args)}")
    filepath, content = str(args[0]), str(args[1])
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return None

def lf_fs_read(args):
    if len(args) != 1:
        raise TypeError(f"read() espera 1 argumento (caminho), mas recebeu {len(args)}")
    filepath = str(args[0])
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"O arquivo '{filepath}' não foi encontrado.")

def lf_fs_exists(args):
    if len(args) != 1:
        raise TypeError(f"exists() espera 1 argumento (caminho), mas recebeu {len(args)}")
    return os.path.exists(str(args[0]))

def lf_fs_delete(args):
    if len(args) != 1:
        raise TypeError(f"delete() espera 1 argumento (caminho), mas recebeu {len(args)}")
    try:
        os.remove(str(args[0]))
    except FileNotFoundError:
        pass
    return None

def lf_datetime_now(args):
    if len(args) != 0:
        raise TypeError(f"datetime.now() espera 0 argumentos, mas recebeu {len(args)}")
    return time.time() # Retorna o timestamp Unix atual

def lf_datetime_format(args):
    if len(args) != 2:
        raise TypeError(f"datetime.format() espera 2 argumentos (timestamp, formato), mas recebeu {len(args)}")
    timestamp, fmt_string = args[0], args[1]
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    return dt_object.strftime(fmt_string)

def lf_datetime_parse(args):
    if len(args) != 2:
        raise TypeError(f"datetime.parse() espera 2 argumentos (data_string, formato), mas recebeu {len(args)}")
    date_string, fmt_string = args[0], args[1]
    dt_object = datetime.datetime.strptime(date_string, fmt_string)
    return dt_object.timestamp()

# --- REGISTRO CENTRAL DE MÓDULOS NATIVOS (PARA O INTERPRETADOR) ---
NATIVE_MODULES = {
    "math": {
        "pi": math.pi,
        "sqrt": lf_sqrt,
        "sin": lf_sin,
    },
    "time": {
        "now": lf_now,
    },
    "fs": {
        "write": lf_fs_write,
        "read": lf_fs_read,
        "exists": lf_fs_exists,
        "delete": lf_fs_delete,
    },
    "datetime": {
        "now": lf_datetime_now,
        "format": lf_datetime_format,
        "parse": lf_datetime_parse,
    },
    "web": NATIVE_WEB_MODULE,
    "json": NATIVE_JSON_MODULE,
    "dado": NATIVE_DADO_MODULE,
    "math": NATIVE_MATH_MODULE,
    "media": NATIVE_MEDIA_MODULE,
}

# ==============================================================================
#  PARTE 2: DESCRIÇÃO SEMÂNTICA (PARA O ANALISADOR)
# ==============================================================================

# --- Tipos Comuns para Reutilização ---
string_type = BuiltInTypeSymbol('string')
float_type = BuiltInTypeSymbol('float')
bool_type = BuiltInTypeSymbol('bool')
int_type = BuiltInTypeSymbol('int')
null_type = BuiltInTypeSymbol('null')
any_type = BuiltInTypeSymbol('any')


# --- Definição Semântica para Métodos de Dicionário ---
dict_semantic_scope = ScopedSymbolTable('dict', scope_level=2)

# Definição para .get() (já está correta)
dict_semantic_scope.define(
    BuiltInFunctionSymbol(
        name='get',
        params=[
            VarSymbol('key', any_type), 
            VarSymbol('default', any_type, is_optional=True)
        ],
        return_type=any_type
    )
)


# --- Definição Semântica do Módulo 'math' ---
math_semantic_scope = ScopedSymbolTable('math', scope_level=2)
math_semantic_scope.define(
    VarSymbol('pi', float_type)
)
math_semantic_scope.define(
    BuiltInFunctionSymbol(name='sqrt', params=[VarSymbol('x', float_type)], return_type=float_type)
)
math_semantic_scope.define(
    BuiltInFunctionSymbol(name='sin', params=[VarSymbol('x', float_type)], return_type=float_type)
)


# --- Definição Semântica do Módulo 'time' ---
time_semantic_scope = ScopedSymbolTable('time', scope_level=2)
time_semantic_scope.define(
    BuiltInFunctionSymbol(name='now', params=[], return_type=float_type)
)

# --- Definição Semântica do Módulo 'fs' ---
fs_semantic_scope = ScopedSymbolTable('fs', scope_level=2)
fs_semantic_scope.define(
    BuiltInFunctionSymbol(name='write', params=[VarSymbol('caminho', string_type), VarSymbol('conteudo', string_type)], return_type=null_type)
)
fs_semantic_scope.define(
    BuiltInFunctionSymbol(name='read', params=[VarSymbol('caminho', string_type)], return_type=string_type)
)
fs_semantic_scope.define(
    BuiltInFunctionSymbol(name='exists', params=[VarSymbol('caminho', string_type)], return_type=bool_type)
)
fs_semantic_scope.define(
    BuiltInFunctionSymbol(name='delete', params=[VarSymbol('caminho', string_type)], return_type=null_type)
)
# --- Definição Semântica do Módulo 'datetime' ---
datetime_semantic_scope = ScopedSymbolTable('datetime', scope_level=2)
datetime_semantic_scope.define(
    BuiltInFunctionSymbol(name='now', params=[], return_type=float_type)
)
datetime_semantic_scope.define(
    BuiltInFunctionSymbol(
        name='format', 
        params=[VarSymbol('timestamp', float_type), VarSymbol('formato', string_type)],
        return_type=string_type
    )
)
datetime_semantic_scope.define(
    BuiltInFunctionSymbol(
        name='parse', 
        params=[VarSymbol('data_string', string_type), VarSymbol('formato', string_type)],
        return_type=float_type
    )
)


# --- REGISTRO CENTRAL DA SEMÂNTICA (PARA O ANALISADOR) ---
NATIVE_MODULES_SEMANTICS = {
    "math": math_semantic_scope,
    "time": time_semantic_scope,
    "fs": fs_semantic_scope,
    "datetime": datetime_semantic_scope,
    "web": register_web_semantics(),
    "json": register_json_semantics(),
    "dado": register_dado_semantics(),
    "math": register_math_semantics(),
    "media": register_media_semantics(),
}

# ==============================================================================
#  PARTE 3: MÉTODOS DE TIPOS NATIVOS (PARA O INTERPRETADOR)
# ==============================================================================

NATIVE_TYPE_METHODS = {
    'string': {
        # O primeiro argumento 'instance' é a própria string.
        # 'args' são os argumentos passados na chamada do método em Lucida.
        'to_upper': lambda instance, args: instance.upper(),
        'to_lower': lambda instance, args: instance.lower(),
        'trim': lambda instance, args: instance.strip(),
        'split': lambda instance, args: instance.split(args[0] if args else None),
        # --- ADIÇÕES AQUI ---
        'replace': lambda instance, args: instance.replace(args[0], args[1]),
        'contains': lambda instance, args: args[0] in instance,
        'starts_with': lambda instance, args: instance.startswith(args[0]),
        'ends_with': lambda instance, args: instance.endswith(args[0]),
        # O slice do Python pode receber até 3 args (start, stop, step),
        # aqui vamos simplificar para start e stop.
        'slice': lambda instance, args: instance[args[0]:args[1]],
        'length': lambda instance, args: len(instance),
    },
    'list': {
        # 'pop', 'sort', etc. podem ser adicionados aqui no futuro.
        # instance é a própria lista, args[0] é o primeiro argumento passado
        'append': lambda instance, args: instance.append(args[0]),
        'pop': lambda instance, args: instance.pop(),
        'length': lambda instance, args: len(instance),
    },
    # --- ADIÇÕES PARA DICIONÁRIO AQUI ---
    'dict': {
        'keys': lambda instance, args: list(instance.keys()),
        'values': lambda instance, args: list(instance.values()),
        'get': lambda instance, args: instance.get(args[0], args[1] if len(args) > 1 else None),
    },
}
