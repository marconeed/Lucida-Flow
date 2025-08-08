# gui_host.py (VERSÃO FINAL E CORRIGIDA)
import tkinter as tk
from tkinter import messagebox
import os
import sys

# Garante que os módulos da Lucida-Flow são encontrados
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from lucida_lexer import Lexer
from lucida_parser import Parser
from lucida_analyzer import SemanticAnalyzer
from lucida_interpreter import Interpreter, BuiltInFunction, Process, LfInstance
from lucida_errors import LucidaError
from lucida_ast import ProgramNode
from lucida_symbols import TypeSymbol, VarSymbol, BuiltInFunctionSymbol, ModuleSymbol, ScopedSymbolTable
from lucida_stdlib import NATIVE_MODULES_SEMANTICS

# --- O CORAÇÃO DA ARQUITETURA CORRIGIDA ---
# Estas instâncias agora são verdadeiramente globais e persistentes
ANALYZER = SemanticAnalyzer()
INTERPRETER = Interpreter()

class GuiManager:
    def __init__(self, root):
        self.root = root
        self.widgets = {}
        self.checkbox_vars = {}
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
        if id_widget in self.widgets:
            # O método .config() do Tkinter é usado para alterar propriedades de widgets
            # CORREÇÃO: Garante que o novo texto seja uma string
            if not isinstance(novo_texto, str):
                raise TypeError("O novo texto deve ser uma string.")
        # CORREÇÃO: Garante que o Python interprete o '\n' como uma quebra de linha real
        texto_formatado = str(novo_texto).replace('\\n', '\n')
        self.widgets[id_widget].config(text=texto_formatado)
    def lf_agendar_atualizacao(self, args):
        """Agenda uma função Lucida-Flow para ser chamada após um certo tempo."""
        milissegundos, nome_funcao_lf = int(args[0]), str(args[1])
        # A função .after do Tkinter é a mágica aqui
        self.root.after(milissegundos, lambda: run_lucida_function(nome_funcao_lf))
    def lf_criar_caixa_texto(self, args):
        """Cria uma caixa de texto de múltiplas linhas."""
        id = args[0]
        # O widget Text do Tkinter é o que precisamos
        caixa_texto = tk.Text(self.root, font=("Arial", 12), height=10, width=40)
        caixa_texto.pack(pady=10, padx=10)
        self.widgets[id] = caixa_texto
    def lf_obter_texto_completo(self, args):
        """Retorna todo o conteúdo de uma caixa de texto."""
        id_widget = args[0]
        if id_widget in self.widgets and isinstance(self.widgets[id_widget], tk.Text):
            # O .get() para o widget Text precisa de um início ("1.0") e um fim ("end-1c")
            return self.widgets[id_widget].get("1.0", "end-1c")
        return ""
    def lf_definir_texto_completo(self, args):
        """Apaga o conteúdo atual e insere um novo texto numa caixa de texto."""
        id_widget, novo_texto = args[0], args[1]
        if id_widget in self.widgets and isinstance(self.widgets[id_widget], tk.Text):
            self.widgets[id_widget].delete("1.0", "end") # Apaga tudo
            self.widgets[id_widget].insert("1.0", novo_texto) # Insere o novo texto
    def lf_criar_entrada(self, args):
        """Cria uma caixa de entrada de texto."""
        id = args[0]
        entrada = tk.Entry(self.root, font=("Arial", 14), width=20)
        entrada.pack(pady=5)
        self.widgets[id] = entrada
    def lf_obter_texto(self, args):
        """Retorna o texto de um widget (como uma caixa de entrada)."""
        id_widget = args[0]
        if id_widget in self.widgets:
            # Para Entry widgets, usamos o método .get()
            if isinstance(self.widgets[id_widget], tk.Entry):
                return self.widgets[id_widget].get()
        return "" # Retorna uma string vazia se o widget não for encontrado

    def lf_criar_checkbox(self, args):
        """Cria uma caixa de seleção (checkbox)."""
        id, texto = args[0], args[1]
        var = tk.IntVar()
        checkbox = tk.Checkbutton(self.root, text=texto, variable=var, font=("Arial", 12))
        checkbox.pack(pady=2)
        self.widgets[id] = checkbox
        self.checkbox_vars[id] = var # Guarda a variável associada

    def lf_criar_slider(self, args):
        """Cria um slider horizontal."""
        id, de, para = args[0], int(args[1]), int(args[2])
        slider = tk.Scale(self.root, from_=de, to=para, orient="horizontal", length=200)
        slider.pack(pady=5)
        self.widgets[id] = slider

    def lf_obter_valor_checkbox(self, args):
        """Retorna 1 se o checkbox estiver marcado, 0 se não."""
        id_widget = args[0]
        if id_widget in self.checkbox_vars:
            return self.checkbox_vars[id_widget].get()
        return 0

    def lf_obter_valor_slider(self, args):
        """Retorna o valor atual de um slider."""
        id_widget = args[0]
        if id_widget in self.widgets and isinstance(self.widgets[id_widget], tk.Scale):
            return self.widgets[id_widget].get()
        return 0
    
    def lf_criar_rotulo_resultado(self, args):
        """Cria um rótulo de resultado grande e com fundo."""
        id, texto = args[0], args[1]
        rotulo = tk.Label(self.root, text=texto, font=("Arial", 16, "bold"), bg="lightgray", padx=10, pady=10)
        rotulo.pack(pady=10)
        self.widgets[id] = rotulo

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

    for name, scope in NATIVE_MODULES_SEMANTICS.items():
        ANALYZER.current_scope.define(ModuleSymbol(name, symbol_table=scope))

    string_type = ANALYZER.current_scope.lookup('string'); null_type = ANALYZER.current_scope.lookup('null')
    gui_semantic_scope = ScopedSymbolTable('gui', 2)
    gui_semantic_scope.define(BuiltInFunctionSymbol('criar_rotulo', params=[VarSymbol('id', string_type), VarSymbol('texto', string_type)], return_type=null_type))
    gui_semantic_scope.define(BuiltInFunctionSymbol('criar_botao', params=[VarSymbol('id', string_type), VarSymbol('texto', string_type), VarSymbol('callback', string_type)], return_type=null_type))
    gui_semantic_scope.define(BuiltInFunctionSymbol('alterar_texto', params=[VarSymbol('id', string_type), VarSymbol('novo_texto', string_type)], return_type=null_type))
    int_type = ANALYZER.current_scope.lookup('int') # Garanta que o int_type está definido
    gui_semantic_scope.define(
        BuiltInFunctionSymbol('agendar_atualizacao', params=[VarSymbol('ms', int_type), VarSymbol('callback', string_type)], return_type=null_type)
    )
    gui_semantic_scope.define(
        BuiltInFunctionSymbol('criar_caixa_texto', params=[VarSymbol('id', string_type)], return_type=null_type)
    )
    gui_semantic_scope.define(
        BuiltInFunctionSymbol('obter_texto_completo', params=[VarSymbol('id', string_type)], return_type=string_type)
    )
    gui_semantic_scope.define(
        BuiltInFunctionSymbol('definir_texto_completo', params=[VarSymbol('id', string_type), VarSymbol('novo_texto', string_type)], return_type=null_type)
    )
    gui_semantic_scope.define(
        BuiltInFunctionSymbol('criar_rotulo_resultado', params=[VarSymbol('id', string_type), VarSymbol('texto', string_type)], return_type=null_type)
    )
    gui_semantic_scope.define(BuiltInFunctionSymbol('obter_texto', params=[VarSymbol('id', string_type)], return_type=string_type))
    gui_semantic_scope.define(BuiltInFunctionSymbol('criar_entrada', params=[VarSymbol('id', string_type)], return_type=null_type))
    gui_semantic_scope.define(BuiltInFunctionSymbol('obter_valor_checkbox', params=[VarSymbol('id', string_type)], return_type=int_type))
    gui_semantic_scope.define(BuiltInFunctionSymbol('obter_valor_slider', params=[VarSymbol('id', string_type)], return_type=int_type))
    gui_semantic_scope.define(BuiltInFunctionSymbol('criar_checkbox', params=[VarSymbol('id', string_type), VarSymbol('texto', string_type)], return_type=null_type))
    gui_semantic_scope.define(BuiltInFunctionSymbol('criar_slider', params=[VarSymbol('id', string_type), VarSymbol('de', int_type), VarSymbol('para', int_type)], return_type=null_type))
    ANALYZER.current_scope.define(ModuleSymbol('gui', symbol_table=gui_semantic_scope))

def main():
    root = tk.Tk()
    root.title("Minha App em Lucida-Flow")
    root.geometry("400x300")
    
    setup_analyzer()
    gui_manager = GuiManager(root)

    # Injeta as funções de runtime no Interpreter
    INTERPRETER.global_scope['gui'] = {
        "criar_entrada": BuiltInFunction(name='criar_entrada', python_callable=gui_manager.lf_criar_entrada),
        "criar_rotulo": BuiltInFunction(name='criar_rotulo', python_callable=gui_manager.lf_criar_rotulo),
        "criar_botao": BuiltInFunction(name='criar_botao', python_callable=gui_manager.lf_criar_botao),
        "alterar_texto": BuiltInFunction(name='alterar_texto', python_callable=gui_manager.lf_alterar_texto),
        "agendar_atualizacao": BuiltInFunction(name='agendar_atualizacao', python_callable=gui_manager.lf_agendar_atualizacao),
        "criar_caixa_texto": BuiltInFunction(name='criar_caixa_texto', python_callable=gui_manager.lf_criar_caixa_texto),
        "obter_texto_completo": BuiltInFunction(name='obter_texto_completo', python_callable=gui_manager.lf_obter_texto_completo),
        "definir_texto_completo": BuiltInFunction(name='definir_texto_completo', python_callable=gui_manager.lf_definir_texto_completo),
        "obter_texto": BuiltInFunction(name='obter_texto', python_callable=gui_manager.lf_obter_texto),
        "criar_checkbox": BuiltInFunction(name='criar_checkbox', python_callable=gui_manager.lf_criar_checkbox),
        "criar_slider": BuiltInFunction(name='criar_slider', python_callable=gui_manager.lf_criar_slider),
        "obter_valor_checkbox": BuiltInFunction(name='obter_valor_checkbox', python_callable=gui_manager.lf_obter_valor_checkbox),
        "obter_valor_slider": BuiltInFunction(name='obter_valor_slider', python_callable=gui_manager.lf_obter_valor_slider),
        "criar_rotulo_resultado": BuiltInFunction(name='criar_rotulo_resultado', python_callable=gui_manager.lf_criar_rotulo_resultado)
    }

    try:
        with open("gerador_senha.lf", 'r', encoding='utf-8') as f: source_code = f.read()
        
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