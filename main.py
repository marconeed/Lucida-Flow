# main.py (Versão Final)

import sys
from lucida_lexer import Lexer
from lucida_parser import Parser
from lucida_analyzer import SemanticAnalyzer
from lucida_interpreter import Interpreter
from lucida_errors import LucidaError
from lucida_ast import ProgramNode # Import necessário para o "truque" do REPL
from lib.parser_patch import apply_patch
apply_patch()

# --- Função para executar um trecho de código ---
def run_code(source_code, analyzer, interpreter):
    """Função auxiliar que executa as 4 fases da linguagem."""
    # Fases 1 e 2: Lexer e Parser são sempre novos
    lexer = Lexer(source_code)
    parser = Parser(lexer)
    ast = parser.parse()

    # Fases 3 e 4: Analyzer e Interpreter são reutilizados para manter o estado
    analyzer.visit(ast)
    result = interpreter.visit(ast)
    return result

# --- Função para o modo REPL ---
def start_repl():
    print("Lucida-Flow REPL v1.0")
    print("Digite 'exit' ou 'sair' para terminar.")
    
    # Criamos as instâncias FORA do loop para manter o estado (variáveis, etc.)
    analyzer = SemanticAnalyzer()
    interpreter = Interpreter()

    # Truque para inicializar as tabelas de símbolos do analisador
    # antes de receber o primeiro input.
    analyzer.visit(ProgramNode([]))
    
    while True:
        try:
            # 1. READ (Ler)
            line = input("lf> ")
            if line.strip().lower() in ('exit', 'sair'):
                break
            
            if not line.strip():
                continue

            # 2. EVAL & PRINT (Avaliar e Imprimir)
            result = run_code(line, analyzer, interpreter)
            
            # Imprime o resultado da expressão, se houver um
            if result is not None:
                print(result)

        # Captura erros sem quebrar o REPL
        except LucidaError as e:
            print(e)
        except Exception as e:
            # Para erros inesperados do Python, mostra o traceback para nos ajudar
            import traceback
            print("--- ERRO DE SISTEMA NO REPL ---")
            traceback.print_exc()

# --- Função para executar um ficheiro ---
def run_file(filename):
    print(f"--- Lendo código do arquivo: {filename} ---")
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # Para execução de ficheiro, criamos instâncias novas a cada vez
        analyzer = SemanticAnalyzer()
        interpreter = Interpreter()
        run_code(source_code, analyzer, interpreter)

        print("\n--- Execução Concluída ---")

    except FileNotFoundError:
        print(f"\nERRO: O arquivo '{filename}' não foi encontrado.")
    except LucidaError as e:
        print(f"\n--- OCORREU UM ERRO NA LUCIDA-FLOW ---")
        print(e)
    except Exception as e:
        print(f"\n--- OCORREU UM ERRO INESPERADO NO SISTEMA ---")
        import traceback
        traceback.print_exc()


# --- Ponto de Entrada Principal ---
def main():
    # Se um nome de arquivo foi passado, executa o arquivo
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    # Se não, entra no modo REPL
    else:
        start_repl()

if __name__ == "__main__":
    main()
