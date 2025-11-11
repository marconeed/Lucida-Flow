[Volume 1: O Manual de Referência](https://www.amazon.com.br/dp/B0FJ1HYJN8)

[Volume 2: Construindo Aplicações Gráficas](https://www.amazon.com.br/dp/B0FLJ8PNYJ)

[Lucida-Flow Support - Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=SoteroApps.lucidaflow-support)

[Lucida-Flow - pypi org](https://pypi.org/project/lucidaflow)

[Sponsor](https://github.com/sponsors/marconeed)

______________________________________________________________________________________________

## Usando o Terminal:

OBS:

Faça download do repositorio Lucida-Flow em uma pasta usando o terminal Windows ou o terminal do VScode:

```
git clone https://github.com/marconeed/Lucida-Flow
cd Lucida-Flow
```

OBS:

Baixe as dependencias usando o terminal Windows ou o terminal do VScode:

```pip install requests```   

OBS:

Para criar programas com interface grafica precisamos criar 2 arquivos o:

O arquivo .py contendo os codigos para desenhar a interface grafica

O arquivo .lf contendo os codigos da logica  do programa

Os 2 arquivos precisam estar na raiz da linguagem de programação, onde fica todo o codigo da linguagem, ou você pode colocar em outros locais, mais tera que referenciar nos 2 arquivos as pastas onde estão as importações de que os 2 arquivos precisam para funcionar

a linguagem contem codigos das guis usadas no livro, estão na raiz do projeto em uma pasta chamada gui, basta colocar as que for usar na raiz junto ao arquivo .lf. Se quiser deixar onde esta precisa mudar o caminho das importações dos 2 arquivos.

OBS:

Para executar basta colocar esse comando usando o terminal Windows ou o terminal do VScode na pasta onde esta os arquivos e lembrar de refenciar o arquivo .lf na nome-do-arquivo-gui_host.py:

```python main.py nome_arquivo.lf```

```python nome-do-arquivo-gui_host.py```


## Usando o VS code:

OBS:

Faça download da estensão da linguagem para VS code

```https://marketplace.visualstudio.com/items?itemName=SoteroApps.lucidaflow-support```

OBS:

Baixe as dependencias usando o terminal Windows ou o terminal do VScode:

```pip install requests```   

OBS:

A extensão funciona para auxiliar na contrução do codigo com sugestões e constução da sytanxe sublinhando as palavras, fica melhor programar no VS code

O VS code suporta executar o codigo direto nele nome_arquivo.lf, mais para porgramas de interface grafica tera que usar o terminal do VS code para dar o comando para executar. o comando é o mesmo ```python nome-do-arquivo-gui_host.py```


## Usando o pypi org:

OBS:

Faça download da linguagem na pypi org

```https://pypi.org/project/lucidaflow```

```pip install lucidaflow```

OBS:

Usando a linguagem dessa forma você elimina a necessidade dos arquivos da linguagem estar na mesma pasta para funcionar, basta cria uma pasta vazia com o .lf e executar, ou nome-do-arquivo-gui_host.py + .lf e executar se for com interface grafica. Para executar o comando é ```python -m lucidaflow nome_arquivo.lf``` ou ```python nome-do-arquivo-gui_host.py```

Usar dessa forma combinado com o VS code e a extensão funciona para auxiliar na contrução do codigo com sugestões e constução da sytanxe sublinhando as palavras, fica melhor programar no VS code

Para executar no terminal Windows basta abrir o terminal windows na pasta onde esta o .lf e digitar ```python -m lucidaflow nome-do-arquivo.lf```, ou abrir o terminal windows na pasta onde esta o gui.py e digitar ```python nome-do-arquivo-gui_host.py`` se for com interface grafica

Para executar no VS code basta apertar play para arquivos .lf. Para arquivo .lf e gui.py precisa ser usado o terminal do VS code ```python nome-do-arquivo-gui_host.py```


## Ativar o REPL (em qualquer pasta do computador):

transformar a sua linguagem numa ferramenta de linha de comando profissional

```python -m lucidaflow.cli```

_____________________________________________________________________________________________________________________________________________________________________________

## Apoie o Projeto

A Lucida-Flow é um projeto independente e de código aberto. Se você gosta da linguagem e quer ver o seu desenvolvimento continuar, considere [tornar-se um patrocinador no GitHub Sponsors](https://github.com/sponsors/marconeed)! O seu apoio é fundamental para a manutenção e evolução do projeto.
