# Arquivo: lucida_errors.py

class LucidaError(Exception):
    """Classe base para todos os erros da linguagem Lucida-Flow."""
    def __init__(self, message="", line=0, col=0):
        super().__init__(message)
        self.line = line
        self.col = col
        self.message = message

    def __str__(self):
        if self.line:
            return f"[Linha {self.line}:C{self.col}] {type(self).__name__}: {self.message}"
        return f"{type(self).__name__}: {self.message}"

class LucidaSemanticError(LucidaError):
    """Erro detectado durante a análise semântica."""
    pass

class LucidaRuntimeError(LucidaError):
    """Erro detectado durante a execução (interpretação)."""
    # Adicione 'error_type' ao construtor
    def __init__(self, message="", line=0, col=0, error_type="RuntimeException"):
        super().__init__(message, line, col)
        # O nome do tipo de erro para o 'catch' da linguagem Lucida
        self.error_type = error_type