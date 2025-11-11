# lib/media.py
import pygame
from lucida_symbols import VarSymbol, BuiltInFunctionSymbol, ScopedSymbolTable, BuiltInTypeSymbol

# Inicializa o mixer do Pygame uma vez
pygame.mixer.init()

# --- Funções de Runtime ---
def lf_media_carregar(args):
    pygame.mixer.music.load(str(args[0]))
    return None

def lf_media_tocar(args):
    pygame.mixer.music.play()
    return None

def lf_media_pausar(args):
    pygame.mixer.music.pause()
    return None

def lf_media_continuar(args):
    pygame.mixer.music.unpause()
    return None

def lf_media_parar(args):
    pygame.mixer.music.stop()
    return None

def lf_media_definir_volume(args):
    # Volume é de 0.0 a 1.0
    volume = float(args[0])
    pygame.mixer.music.set_volume(volume)
    return None

def lf_media_esta_a_tocar(args):
    return pygame.mixer.music.get_busy()

NATIVE_MEDIA_MODULE = {
    "carregar": lf_media_carregar,
    "tocar": lf_media_tocar,
    "pausar": lf_media_pausar,
    "continuar": lf_media_continuar,
    "parar": lf_media_parar,
    "definir_volume": lf_media_definir_volume,
    "esta_a_tocar": lf_media_esta_a_tocar,
}

# --- Descrição Semântica ---
def register_semantics():
    string_type = BuiltInTypeSymbol('string'); float_type = BuiltInTypeSymbol('float')
    bool_type = BuiltInTypeSymbol('bool'); null_type = BuiltInTypeSymbol('null')
    
    scope = ScopedSymbolTable(scope_name='media', scope_level=2)
    scope.define(BuiltInFunctionSymbol('carregar', params=[VarSymbol('caminho', string_type)], return_type=null_type))
    scope.define(BuiltInFunctionSymbol('tocar', params=[], return_type=null_type))
    scope.define(BuiltInFunctionSymbol('pausar', params=[], return_type=null_type))
    scope.define(BuiltInFunctionSymbol('continuar', params=[], return_type=null_type))
    scope.define(BuiltInFunctionSymbol('parar', params=[], return_type=null_type))
    scope.define(BuiltInFunctionSymbol('definir_volume', params=[VarSymbol('volume', float_type)], return_type=null_type))
    scope.define(BuiltInFunctionSymbol('esta_a_tocar', params=[], return_type=bool_type))
    return scope