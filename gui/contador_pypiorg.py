# gui_host.py (VERSÃO FINAL E CORRIGIDA)
import tkinter as tk
from tkinter import messagebox
import os
import sys

# Garante que os módulos da Lucida-Flow são encontrados
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from lucidaflow.lucida_lexer import Lexer
from lucidaflow.lucida_parser import Parser
from lucidaflow.lucida_analyzer import SemanticAnalyzer
from lucidaflow.lucida_interpreter import Interpreter, BuiltInFunction, Process, LfInstance
from lucidaflow.lucida_errors import LucidaError
from lucidaflow.lucida_ast import ProgramNode
from lucidaflow.lucida_symbols import TypeSymbol, VarSymbol, BuiltInFunctionSymbol, ModuleSymbol, ScopedSymbolTable

# --- O CORAÇÃO DA ARQUITETURA CORRIGIDA ---
# Estas instâncias agora são verdadeiramente globais e persistentes
ANALYZER = SemanticAnalyzer()
INTERPRETER = Interpreter()

class GuiManager:
    def __init__(self, root):
        self.root = root; self.widgets = {}
    def lf_criar_rotulo(self, args):
        id, texto = args[0], args[1]
        rotulo = tk.Label(self.root, text=texto, font=("Arial", 16))
        rotulo.pack(pady=10); self.widgets[id] = rotulo
    def lf_criar_botao(self, args):
        id, texto, nome_funcao_lf = args[0], args[1], args[2]
        botao = tk.Button(self.root, text=texto, command=lambda: run_lucida_function(nome_funcao_lf))
        botao.pack(pady=5); self.widgets[id] = botao
    def lf_alterar_texto(self, args):
        id_widget, novo_texto = args[0], args[1]
        if id_widget in self.widgets: self.widgets[id_widget].config(text=novo_texto)

def run_lucida_function(function_name):
    """Executa uma função específica USANDO O INTERPRETADOR JÁ EXISTENTE."""
    process_obj = INTERPRETER.global_scope.get(function_name)
    if process_obj and isinstance(process_obj, Process):
        try:
            INTERPRETER.call_process(process_obj, [])
        except LucidaError as e:
            messagebox.showerror("Erro de Runtime na Lucida-Flow", str(e))
        except Exception as e:
            messagebox.showerror("Erro Inesperado", str(e))

def setup_analyzer():
    """Configura o ANALYZER UMA VEZ."""
    ANALYZER.visit(ProgramNode([]))
    string_type = ANALYZER.current_scope.lookup('string'); null_type = ANALYZER.current_scope.lookup('null')
    gui_semantic_scope = ScopedSymbolTable('gui', 2)
    gui_semantic_scope.define(BuiltInFunctionSymbol('criar_rotulo', params=[VarSymbol('id', string_type), VarSymbol('texto', string_type)], return_type=null_type))
    gui_semantic_scope.define(BuiltInFunctionSymbol('criar_botao', params=[VarSymbol('id', string_type), VarSymbol('texto', string_type), VarSymbol('callback', string_type)], return_type=null_type))
    gui_semantic_scope.define(BuiltInFunctionSymbol('alterar_texto', params=[VarSymbol('id', string_type), VarSymbol('novo_texto', string_type)], return_type=null_type))
    ANALYZER.current_scope.define(ModuleSymbol('gui', symbol_table=gui_semantic_scope))

def main():
    root = tk.Tk()
    root.title("Minha App em Lucida-Flow")
    root.geometry("400x300")
    
    setup_analyzer()
    gui_manager = GuiManager(root)

    # Injeta as funções de runtime no Interpreter
    INTERPRETER.global_scope['gui'] = {
        "criar_rotulo": BuiltInFunction(name='criar_rotulo', python_callable=gui_manager.lf_criar_rotulo),
        "criar_botao": BuiltInFunction(name='criar_botao', python_callable=gui_manager.lf_criar_botao),
        "alterar_texto": BuiltInFunction(name='alterar_texto', python_callable=gui_manager.lf_alterar_texto)
    }

    try:
        with open("contador.lf", 'r', encoding='utf-8') as f: source_code = f.read()
        
        lexer = Lexer(source_code); parser = Parser(lexer); ast = parser.parse()
        
        # Analisa cada statement individualmente para preservar o escopo do analyzer
        for statement in ast.statements: ANALYZER.visit(statement)
        
        # Executa o script UMA VEZ com o nosso interpretador persistente
        INTERPRETER.visit(ast)
        
    except Exception as e:
        messagebox.showerror("Erro no Script Lucida-Flow", str(e))
        root.destroy(); return

    root.mainloop()

if __name__ == "__main__":
    main()
