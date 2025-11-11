# lib/parser_patch.py
from lucida_parser import Parser

def apply_patch():
    """
    Esta função aplica um "remendo" em tempo de execução na classe Parser
    para corrigir a assinatura do método de erro.
    """
    print("-> Aplicando patch no Parser...")

    # 1. Guardamos a função de erro original
    original_error_method = Parser.error

    # 2. Definimos uma nova função de erro que aceita o argumento 'token'
    def novo_metodo_de_erro(self, msg="Sintaxe inválida", token=None):
        # Esta nova função simplesmente chama a original da forma que ela espera
        token_to_report = token if token else self.current_token
        detailed_msg = f'{msg} (token: {token_to_report})'
        # A chamada à função original precisa de ser feita com o 'self' correto
        original_error_method(self, detailed_msg)

    # 3. Substituímos a função de erro antiga da classe Parser pela nossa nova versão
    Parser.error = novo_metodo_de_erro
    print("-> Patch do Parser aplicado com sucesso!")