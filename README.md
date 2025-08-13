[Volume 1: O Manual de Referência](https://www.amazon.com.br/dp/B0FJ1HYJN8)

[Volume 2: Construindo Aplicações Gráficas](https://www.amazon.com.br/dp/B0FLJ8PNYJ)

[Lucida-Flow Support - Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=SoteroApps.lucidaflow-support)

[Lucida-Flow - pypi org](https://pypi.org/project/lucidaflow)

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

______________________________________________________________________________________________

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

______________________________________________________________________________________________

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

_______________________________________________________________________________________________________________________________________________________________________________________________________________________

## Ativar o REPL (em qualquer pasta do computador):

transformar a sua linguagem numa ferramenta de linha de comando profissional

```python -m lucidaflow.cli```

_______________________________________________________________________________________________________________________________________________________________________________________________________________________

# Fluindo com Código: O Guia Definitivo da Linguagem Lucida-Flow
Subtítulo: Da Automação de Scripts à Criação de Sistemas Extensíveis

Introdução

Bem-vindo ao universo da Lucida-Flow! Se você já se perguntou como as linguagens de programação são criadas, ou se simplesmente procura uma ferramenta de script moderna e flexível para os seus projetos, você está no lugar certo. Este livro é o seu guia completo para dominar a Lucida-Flow, desde os seus conceitos mais básicos até as suas funcionalidades mais poderosas.

O que é a Lucida-Flow?

A Lucida-Flow é uma linguagem de programação de script, de alto nível, moderna e extensível. Ela foi projetada com dois objetivos principais em mente: simplicidade e poder. A sua sintaxe é limpa e intuitiva, inspirada no melhor de linguagens como Python e JavaScript, o que a torna fácil de aprender e agradável de escrever.

Ao mesmo tempo, ela possui recursos avançados como um sistema de tipos gradual, orientação a objetos completa com herança, e uma arquitetura de plugins dinâmica que serve como uma ponte para o vasto e poderoso ecossistema de bibliotecas Python.

A Filosofia por Trás do Flow

Acreditamos que uma linguagem de script não precisa de ser complicada para ser poderosa. A Lucida-Flow foi criada para ser a ferramenta perfeita para "colar" sistemas, automatizar tarefas do dia-a-dia, prototipar ideias rapidamente e servir como um cérebro lógico para aplicações maiores e mais complexas.

Este guia foi escrito para:

Desenvolvedores e Hobbyistas: Que procuram uma nova linguagem de script para os seus projetos pessoais e ferramentas.

Estudantes de Ciência da Computação: Que querem ver, na prática, como os conceitos de compiladores, interpretadores e design de linguagens se materializam num projeto real.

Futuros Arquitetos de Software: Que desejam entender como criar sistemas extensíveis e linguagens de domínio específico (DSLs).

Estrutura da Documentação

O livro está dividido em quatro partes, projetadas para levá-lo numa jornada de aprendizado contínuo:

Parte I: Cobre os fundamentos essenciais da linguagem.

Parte II: Mergulha na estruturação da lógica com funções e coleções.

Parte III: Explora os tópicos avançados como Orientação a Objetos e o sistema de módulos.

Parte I: Os Fundamentos

Capítulo 1: Primeiros Passos - O Seu "Olá, Mundo!"

Bem-vindo ao ponto de partida prático! Neste capítulo, vamos garantir que o seu ambiente está configurado e que você consegue executar o seu primeiro programa em Lucida-Flow.

1.1. O Que Você Precisa

Antes de mais nada, garanta que você tem o Python 3.x instalado no seu sistema. A Lucida-Flow é implementada em Python, então o seu interpretador é necessário para executar nossos scripts.

1.2. Obtendo o Código

A Lucida-Flow é um projeto de código aberto. Para começar, clone o repositório oficial a partir do GitHub para a sua máquina local:

Bash

```
git clone https://github.com/marconeed/Lucida-Flow
cd Lucida-Flow
```

1.3. A Anatomia de um Script Lucida-Flow

Todos os arquivos de código da Lucida-Flow usam a extensão .lf. São simples arquivos de texto que você pode criar e editar em qualquer editor de código, como o VS Code.

1.4. Escrevendo o Primeiro Script: ola.lf

Vamos criar o nosso "Olá, Mundo!". Crie um novo arquivo chamado ola.lf e escreva a seguinte linha dentro dele:

Snippet de código

```print("Olá, Mundo da Lucida-Flow!")```

A função print() é uma função nativa da linguagem usada para exibir texto no console.

1.5. Executando o Script

Para executar o seu script, navegue até a pasta do projeto no seu terminal e use o interpretador Python para rodar o main.py, passando o nome do seu script como argumento:

Bash

```python main.py ola.lf```

Se tudo correu bem, você deverá ver a seguinte saída:

```
--- Lendo código do arquivo: ola.lf ---
... (mensagens do sistema) ...
Olá, Mundo da Lucida-Flow!
...
--- Execução Concluída ---
```

Parabéns, você é oficialmente um programador Lucida-Flow!

1.6. Modo Interativo: O REPL

Para experimentação rápida, você pode usar o REPL (Read-Eval-Print Loop). Basta executar o main.py sem nenhum argumento:

Bash

```python main.py```

Isso iniciará um prompt interativo (lf> ), onde você pode digitar comandos um por um. Para sair, digite exit ou sair.

Capítulo 2: A Memória da Linguagem - Variáveis, Constantes e Tipos

Todo programa, do mais simples ao mais complexo, precisa de uma forma de guardar e manipular informações. Na Lucida-Flow, fazemos isso através de variáveis e constantes. Neste capítulo, vamos explorar as ferramentas fundamentais para lidar com dados.

2.1. Guardando Informação: let e const

A Lucida-Flow oferece duas maneiras de declarar um "contentor" para um valor, cada uma com um propósito diferente.

let - Variáveis Mutáveis

Use a palavra-chave let para declarar uma variável cujo valor pode mudar ao longo do tempo. Esta é a forma mais comum de armazenar dados que serão processados ou atualizados.

Snippet de código

```
// Declara a variável 'pontuacao' e inicializa com 100
let pontuacao = 100
print("Pontuação inicial:", pontuacao) // Saída: 100
// O valor de 'pontuacao' pode ser modificado depois
pontuacao = 150
print("Pontuação final:", pontuacao) // Saída: 150
```

const - Constantes Imutáveis

Use a palavra-chave const para declarar uma constante. Uma vez que um valor é atribuído a uma constante, ele não pode ser alterado. Isso é útil para valores que devem permanecer fixos durante toda a execução do programa, como configurações ou valores matemáticos.

Snippet de código

```
const PI = 3.14159
print("O valor de PI é:", PI)
```

```
// A linha abaixo causaria um erro, pois não se pode reatribuir uma constante.
// O Analisador Semântico da Lucida-Flow protege você contra isso!
// PI = 3.14 // ERRO!
```

2.2. Os Blocos de Construção: Tipos Primitivos

Todo valor na Lucida-Flow tem um tipo, que define que tipo de dado ele é e o que se pode fazer com ele. A linguagem suporta os seguintes tipos primitivos:

int e float: Para representar números. int para inteiros (ex: 10, 42) e float para números com casas decimais (ex: 9.8, 3.14).

Snippet de código

```
let idade = 42
let preco = 19.99
```

string: Para representar texto. As strings podem ser criadas com aspas duplas (") ou simples (') e suportam caracteres de escape, como \n para uma nova linha.

Snippet de código

```
let saudacao = "Olá, Mundo!"
let aviso = 'Cuidado:\nUse a barra invertida para escapar.'
```

A Lucida-Flow também suporta F-Strings para facilitar a formatação de texto:

Snippet de código

```
let versao = 1.0
let msg = f"Bem-vindo à Lucida-Flow v{versao}!"
print(msg) // Saída: Bem-vindo à Lucida-Flow v1.0!
```

bool: Representa valores lógicos, que só podem ser true (verdadeiro) ou false (falso). São a base de todas as decisões em programação.

Snippet de código

```
let motor_ligado = true
let porta_aberta = false
```

null: Este tipo especial representa a ausência intencional de um valor. É o "vazio".

Snippet de código

```let proximo_chefe = null // Ainda não há um próximo chefe no jogo```

2.3. Tipagem Gradual: Segurança e Flexibilidade

A Lucida-Flow usa um sistema de tipagem gradual, oferecendo o melhor de dois mundos: a segurança da tipagem estática e a flexibilidade da tipagem dinâmica.

Anotações de Tipo (O Lado Seguro)

Você pode (e deve, para código mais robusto) declarar explicitamente o tipo de uma variável usando dois-pontos (:). Isso permite que o Analisador Semântico da Lucida-Flow verifique seu código e encontre erros de tipo antes mesmo de o programa rodar.

Snippet de código

```
let nome: string = "Marco"
let idade: int = 35
```

```
// O Analisador Semântico lançaria um erro aqui, pois 123 não é uma string.
// let nome_errado: string = 123 // ERRO SEMÂNTICO!
```

O Tipo any (O Lado Flexível)

Se você não especificar um tipo, a Lucida-Flow assume que a variável é do tipo any. Uma variável any pode guardar qualquer tipo de valor, e seu tipo pode mudar durante a execução. Isso é útil para prototipagem rápida ou quando a flexibilidade é mais importante.

Snippet de código

```
let item_magico = "Poção de Cura" // O tipo de item_magico é inferido como 'string'
print(item_magico)
```

```
// Em outro ponto do programa, o item pode mudar
// Se item_magico fosse declarado como 'let item_magico: string', a linha abaixo daria erro.
// Mas como o tipo foi inferido, a linguagem permite a flexibilidade.
// Para forçar a flexibilidade, você pode declarar: let item_magico: any = "Poção"
```

```
item_magico = 500 // Agora item_magico guarda um 'int'
print(item_magico)
```

Capítulo 3: Dando Vida aos Dados - Operadores e Expressões

Variáveis e constantes são úteis para armazenar dados, mas o verdadeiro poder da programação vem da capacidade de operar sobre esses dados. Uma expressão é qualquer pedaço de código que resulta em um valor. A expressão mais simples é um literal (como 10 ou "olá"), mas as mais interessantes são criadas combinando valores com operadores.

3.1. Operadores Aritméticos

A Lucida-Flow suporta todas as operações aritméticas padrão para trabalhar com os tipos int e float.

+ (Adição)

- (Subtração)

* (Multiplicação)

/ (Divisão) - Nota: A divisão sempre resulta em um float.

% (Módulo) - Retorna o resto de uma divisão.

** (Potência) - Eleva um número a uma potência.

Precedência de Operadores: A Lucida-Flow respeita a ordem matemática padrão das operações. Multiplicação e divisão são executadas antes de adição e subtração. Você pode usar parênteses () para forçar uma ordem de execução específica.

Snippet de código

```
let soma = 10 + 5          // 15
let produto = 10 * 5         // 50
let resto = 10 % 3           // 1
let potencia = 2 ** 3          // 8
// Precedência em ação
let resultado1 = 10 + 5 * 2  // 10 + 10 = 20
let resultado2 = (10 + 5) * 2  // 15 * 2 = 30
```

3.2. Operadores de Comparação

Operadores de comparação avaliam a relação entre dois valores e sempre resultam em um valor bool (true ou false). Eles são a base para a tomada de decisões.

== (Igual a)

!= (Diferente de)

> (Maior que)

< (Menor que)

>= (Maior ou igual a)

<= (Menor ou igual a)

Snippet de código

```
let idade = 25
print(idade == 25)  // Saída: true
print(idade > 30)   // Saída: false
print("lucida" != "flow") // Saída: true
```

3.3. Operadores Lógicos

Operadores lógicos são usados para combinar múltiplas expressões booleanas.

and: Retorna true somente se ambos os lados forem verdadeiros.

or: Retorna true se pelo menos um dos lados for verdadeiro.

not: Inverte um valor booleano (not true se torna false).

Snippet de código

```
let tem_chave = true
let porta_aberta = false
let pode_entrar = tem_chave and not porta_aberta
print("Pode entrar?", pode_entrar) // Saída: true
```

3.4. Operadores Bitwise (Avançado)

Para manipulação de baixo nível em números inteiros (int), a Lucida-Flow oferece operadores bitwise.

& (AND bit a bit)

| (OR bit a bit)

^ (XOR bit a bit)

~ (NOT bit a bit)

<< (Shift para a esquerda)

>> (Shift para a direita)

Snippet de código

```
let a = 10  // Binário: ...1010
let b = 12  // Binário: ...1100
// 1010 AND 1100 = 1000 (que é 8)
print("10 & 12 =", a & b) // Saída: 8
```

3.5. Expressões Convenientes (Açúcar Sintático)

A Lucida-Flow oferece atalhos para tornar o código mais limpo.

Atribuições Compostas: Um atalho para modificar uma variável com base no seu próprio valor.

```
x += 1 é o mesmo que x = x + 1.
y *= 2 é o mesmo que y = y * 2.
(Funciona para +, -, *, /, **, %)
```

Operador Ternário: Um if/else em uma única linha para expressões.

condicao ? valor_se_true : valor_se_false

Snippet de código

```
let temperatura = 28
let status_ar = temperatura > 25 ? "Ligado" : "Desligado"
print("Status do Ar Condicionado:", status_ar) // Saída: Ligado
```

Parte II: Estruturando a Lógica

Capítulo 4: Controlando o Fluxo do Programa

Até agora, nossos scripts foram executados de forma linear, uma linha após a outra. No entanto, para criar programas úteis, precisamos de controlar quais linhas são executadas e quantas vezes. A Lucida-Flow oferece estruturas de controle poderosas e legíveis para gerir este fluxo.

4.1. Tomando Decisões com when

A estrutura when é a principal ferramenta da Lucida-Flow para tomar decisões. Ela avalia uma condição e, se for true, executa um bloco de código.

A sua sintaxe é projetada para ser clara e expressiva, especialmente para múltiplas condições.

when simples:

Snippet de código

```
let idade = 20
when idade >= 18 {
print("É maior de idade.")
}
```

when com otherwise (senão):

O bloco otherwise é executado se a condição do when for false.

Snippet de código

```
let temperatura = 15
when temperatura > 25 {
print("Ligar o ar condicionado.")
} otherwise {
print("Manter o ar condicionado desligado.")
}
```

Múltiplas Condições com else when:

Para verificar várias condições em sequência, use else when. Isso torna o código muito mais limpo do que aninhar múltiplos whens.```

Snippet de código

```
let nota = 85
when nota >= 90 {
print("Nota: A")
} else when nota >= 80 {
print("Nota: B") // Este bloco será executado
} else when nota >= 70 {
print("Nota: C")
} otherwise {
print("Nota: D")
}
```

4.2. Repetindo Tarefas com while

O loop while (enquanto) executa um bloco de código repetidamente, enquanto uma condição permanecer true. É ideal para situações em que você não sabe de antemão quantas vezes o loop precisa de ser executado.

Snippet de código

```
let contador = 1
while contador <= 5 {
print("Contagem:", contador)
contador += 1
}
#Saída:
#Contagem: 1
#Contagem: 2
#Contagem: 3
#Contagem: 4
#Contagem: 5
```

Cuidado: Certifique-se de que a condição do while eventualmente se torne false, caso contrário, você criará um loop infinito!

4.3. Iterando sobre Coleções com for each

Esta é a forma mais comum e segura de percorrer os elementos de uma coleção (como uma lista ou dicionário). Para cada elemento na coleção, o for each executa um bloco de código.

Snippet de código

```
let nomes = ["Ana", "Bruno", "Carlos"]
for each nome in nomes {
print(f"Olá, {nome}!")
}
#Saída:
#Olá, Ana!
#Olá, Bruno!
#Olá, Carlos!
```

4.4. Controle Fino de Loops: break e continue

Às vezes, você precisa de mais controle sobre o comportamento de um loop while ou for each.

break: Interrompe e sai do loop imediatamente, independentemente da condição do loop.

continue: Pula a iteração atual e avança para a próxima.

Snippet de código

```
#Exemplo combinando os dois
let numeros = [1, 2, -1, 4, 5, 99, 7]
for each n in numeros {
when n < 0 {
        print("Número negativo encontrado, pulando com 'continue'...")
         continue
    }
    when n > 50 {
      print("Número muito grande encontrado, parando com 'break'...")
       break
   }
   print("Processando número:", n)
}
#Saída:
#Processando número: 1
#Processando número: 2
#Número negativo encontrado, pulando com 'continue'...
#Processando número: 4
#Processando número: 5
#Número muito grande encontrado, parando com 'break'...
```

Capítulo 5: Organizando Dados em Massa - Coleções

Raramente trabalhamos com dados isolados. Na maioria das vezes, precisamos de agrupar informações: uma lista de utilizadores, um conjunto de configurações, as coordenadas de um ponto. A Lucida-Flow oferece estruturas de dados poderosas, chamadas de coleções, para lidar com esses cenários.

5.1. Listas: Coleções Ordenadas e Mutáveis

A lista é a coleção mais fundamental. É uma sequência ordenada de itens, e você pode adicionar, remover e modificar seus elementos a qualquer momento.

Criação: As listas são criadas com colchetes [], e seus elementos são separados por vírgulas. Uma lista pode conter diferentes tipos de dados.

Snippet de código

```
let lista_vazia = []
let numeros = [1, 2, 3, 5, 8]
let itens_misturados = ["Maçã", 3, true]
```

Acesso e Modificação: Os elementos são acessados pela sua posição (índice), começando em zero.

Snippet de código

```
let frutas = ["Maçã", "Banana", "Laranja"]
print(frutas[0]) // Saída: Maçã
// Modificando um item
frutas[1] = "Morango"
print(frutas) // Saída: ["Maçã", "Morango", "Laranja"]
```

Métodos Nativos ("Superpoderes"):

.append(item): Adiciona um item ao final da lista.

Snippet de código

```numeros.append(13) // numeros agora é [1, 2, 3, 5, 8, 13]```

.pop(): Remove e retorna o último item da lista.

Snippet de código

```let ultimo_numero = numeros.pop() // ultimo_numero é 13```

.length(): Retorna a quantidade de itens na lista.

Snippet de código

```print(numeros.length()) // Saída: 5```

5.2. Dicionários: Coleções Chave-Valor

Um dicionário é uma coleção não ordenada que armazena pares de chave: valor. É extremamente eficiente para procurar um valor quando você conhece a sua chave.

Criação: Dicionários são criados com chaves {}.

Snippet de código

```
let carro = {
    "marca": "Lucida Motors",
    "ano": 2025,
   "eletrico": true
}
```

Acesso e Modificação: O acesso e a modificação são feitos através da chave.

Snippet de código

```
print(carro["marca"]) // Saída: Lucida Motors
// Modificando um valor existente
carro["ano"] = 2026
// Adicionando um novo par chave-valor
carro["cor"] = "azul"
```

Métodos Nativos:

.keys(): Retorna uma lista com todas as chaves do dicionário.

.values(): Retorna uma lista com todos os valores.

.get(chave, [valor_padrão]): Acessa uma chave de forma segura. Se a chave não existir, retorna null ou o valor padrão que você fornecer.

Snippet de código

```
let modelo = carro.get("modelo") // Retorna null, pois a chave não existe
let motor = carro.get("motor", "elétrico") // Retorna "elétrico"
```

5.3. Tuplas: Coleções Ordenadas e Imutáveis

Uma tupla é como uma lista, mas com uma grande diferença: ela é imutável. Uma vez criada, você não pode alterar, adicionar ou remover seus elementos. São úteis para dados que devem permanecer constantes, como coordenadas RGB ou registros de banco de dados.

Criação: Tuplas são criadas com parênteses ().

Snippet de código

```
let rgb = (255, 100, 50)
let registro = ("Marcos", 35, "Portugal")
print(rgb[0]) // Saída: 255
```

```
// A linha abaixo causaria um erro de runtime, pois tuplas são imutáveis
// rgb[0] = 200 // ERRO!
```

5.4. Bônus: Compreensão de Lista

A Lucida-Flow suporta uma sintaxe de "açúcar sintático" muito poderosa para criar novas listas a partir de outras existentes.

Snippet de código

```
let numeros = [1, 2, 3, 4, 5]
// Cria uma nova lista com o quadrado de cada número
let quadrados = [n * n for each n in numeros]
print(quadrados) // Saída: [1, 4, 9, 16, 25]
```

Parte III: Tópicos Avançados

Capítulo 6: O Poder dos Processos - Funções, Escopo e Closures

Já vimos como declarar e chamar processos (o nome para funções na Lucida-Flow), mas para realmente dominar a linguagem, precisamos de entender como eles funcionam "por baixo dos panos". Os conceitos de escopo e closures são o que dão às funções da Lucida-Flow a sua incrível flexibilidade e poder.

6.1. Revisão: A Anatomia de um Processo

Como vimos, um processo é um bloco de código reutilizável. A sua forma mais completa inclui um nome, uma lista de parâmetros com tipos, um tipo de retorno e um corpo.

Snippet de código

```
define process calcular_imposto(valor: float) -> float {
    const TAXA = 0.2
    return valor * TAXA
    }
```

Até aqui, tudo simples. Mas a verdadeira magia acontece quando um processo é definido dentro de outro.

6.2. O Conceito Mais Importante: Escopo Léxico

O escopo de uma variável define onde ela pode ser acessada. A Lucida-Flow usa um escopo léxico (também chamado de escopo estático). Isso significa uma coisa muito importante:

Uma função "lembra" do escopo em que foi criada, não do escopo em que é chamada.

Vamos ver um exemplo poderoso que ilustra isso, uma "fábrica de funções":

Snippet de código

```
define process criar_multiplicador(multiplicador: int) -> any {
   // Este processo interno "captura" a variável 'multiplicador' do seu escopo pai.
  define process funcao_interna(numero: int) -> int {
        return numero * multiplicador
   }
   // O processo 'criar_multiplicador' retorna a função interna.
   return funcao_interna
}
```

```
// Criamos duas funções diferentes usando a nossa "fábrica"
let dobrar = criar_multiplicador(2)
let triplicar = criar_multiplicador(3)
// Agora usamos as funções que foram criadas
print("Dobrar 10:", dobrar(10))     // Saída: 20
print("Triplicar 10:", triplicar(10))   // Saída: 30
```

6.3. Closures na Prática

O que aconteceu no exemplo acima? A função funcao_interna formou uma closure.

Uma closure é a combinação de uma função com o seu ambiente léxico – as variáveis que existiam no escopo onde a função foi criada. A função "carrega uma mochila" com essas variáveis e pode acessá-las a qualquer momento, mesmo que o escopo original (a função criar_multiplicador) já tenha terminado a sua execução.

É por isso que a variável dobrar lembra que seu multiplicador é 2, e a variável triplicar lembra que o seu é 3.

6.4. Funções de Primeira Classe

Na Lucida-Flow, funções são "cidadãs de primeira classe". Isso significa que elas são tratadas como qualquer outro valor (como um número ou uma string). Você pode:

Atribuir uma função a uma variável: let minha_func = criar_multiplicador(5)

Passar uma função como argumento para outra função.

Retornar uma função de outra função (como fizemos no exemplo criar_multiplicador).

O exemplo clássico é uma função mapa, que aplica uma função a cada item de uma lista:

Snippet de código

```
define process mapa(lista, funcao) -> list {
let nova_lista = []
   for each item in lista {
        nova_lista.append(funcao(item))
   }
   return nova_lista
}
let numeros = [1, 2, 3]
let dobrados = mapa(numeros, dobrar) // Passando a função 'dobrar' como argumento!
print(dobrados) // Saída: [2, 4, 6]
```

6.5. Funções Anônimas (Lambdas)

Às vezes, você precisa de uma função simples apenas para passá-la como argumento, e não quer se preocupar em lhe dar um nome. Para isso, você pode criar uma função anônima, ou lambda. A sintaxe é a mesma, mas sem o nome após define process.

Snippet de código

```
let numeros = [1, 2, 3]
// Em vez de definir 'cubo' separadamente, a criamos diretamente na chamada
let cubos = mapa(numeros, process(n) { return n ** 3 })
print(cubos) // Saída: [1, 8, 27]
```

Capítulo 7: Construindo com Blocos - A Orientação a Objetos

A Orientação a Objetos (ou POO) é uma forma de pensar em programação onde agrupamos dados (campos) e as funções que operam nesses dados (métodos) em uma única entidade chamada objeto. Um objeto é uma "instância" de um "molde" chamado tipo (ou classe). A Lucida-Flow possui um sistema de POO completo e poderoso.

7.1. Definindo Tipos com define type

A palavra-chave define type é o ponto de partida para criar um novo "molde" para os seus objetos.

Snippet de código

```
define type Jogador {
// Membros (campos e métodos) vêm aqui.
    }
```

7.2. Campos, Métodos e o self

Campos: Variáveis que pertencem a cada instância, guardando o seu estado.

Métodos: Funções que definem o comportamento do objeto.

Dentro de um método, a palavra-chave self é uma referência à instância específica do objeto que está a ser usada.

Snippet de código

```
define type Jogador {
let nome = "Anônimo"
    let vida = 100
    define process apresentar(self) {
       print(f"Olá, meu nome é {self.nome} e tenho {self.vida} de vida.")
   }
   }
```

7.3. O Construtor: __init__

Para inicializar cada objeto com valores únicos, usamos o método especial __init__. Ele é executado automaticamente sempre que um novo objeto é criado.

Snippet de código

```
define type Jogador {
define process __init__(self, nome_inicial: string) {
        self.nome = nome_inicial
        self.vida = 100
    }
     //...
   }
let heroi = Jogador("Gandalf") // Passa "Gandalf" para o parâmetro nome_inicial
```

7.4. Herança com < e super

A herança permite que um tipo (filho) herde todos os campos e métodos de outro tipo (pai), permitindo a reutilização de código. Uma classe filha pode fornecer a sua própria implementação de um método (sobreposição) e ainda chamar a versão do pai usando super.

Snippet de código

```
define type Inimigo {
define process __init__(self, nome: string) {
       self.nome = nome
        }
    define process atacar(self) {
        print(f"{self.nome} ataca!")
        }
   }// Goblin herda de Inimigo
define type Goblin < Inimigo {
    // O construtor do Goblin também chama o construtor do pai
    define process __init__(self, nome: string) {
      super.__init__(nome) // Inicializa a parte 'Inimigo' do Goblin
       }
    // Sobrepõe o método 'atacar'
    define process atacar(self) {
        print("O Goblin ataca com uma adaga enferrujada!")
        super.atacar() // Opcionalmente, chama a lógica do pai
    }
}
let goblin_soldado = Goblin("Snaga")`
goblin_soldado.atacar()
```

```
Saída:
O Goblin ataca com uma adaga enferrujada!
Snaga ataca!
```

Capítulo 8: Escrevendo Código à Prova de Falhas - Tratamento de Erros

Programas robustos não quebram ao encontrar situações inesperadas. Eles as tratam. A Lucida-Flow oferece um sistema completo de tratamento de exceções com try, catch e finally.

8.1. O Bloco try...catch

Colocamos o código que pode falhar dentro de um bloco try. Se um erro (uma exceção) ocorrer, a execução do try para e o controlo passa para o bloco catch correspondente.

Snippet de código

```
try {
print("Tentando dividir por zero...")
   let resultado = 10 / 0
   } catch (erro: Exception) {
print("Um erro genérico foi capturado:", erro)
   }
```

8.2. Capturando Erros Específicos

É uma boa prática capturar os tipos de erro mais específicos possíveis. Isso permite dar um tratamento diferente para cada falha.

Snippet de código

```
import "fs" as fs
try {
let conteudo = fs.read("arquivo_inexistente.txt")
} catch (e: FileNotFoundError) {
 print("ERRO DE FICHEIRO: Verifique o caminho e o nome do ficheiro.")
  } catch (e: Exception) {
print("ERRO GENÉRICO: Ocorreu um problema inesperado:", e)
  }
```

A Lucida-Flow conhece os seguintes tipos de erro: Exception, ArithmeticError, FileNotFoundError, TypeError, ValueError, IndexError.

8.3. A Garantia do finally

O bloco finally contém código de "limpeza" que é sempre executado, não importa se o bloco try teve sucesso ou se um erro foi capturado.

Snippet de código

```
print("Abrindo um recurso...")
try {
// ... código que pode dar erro ...
    } catch (e: Exception) {
    print("Tratando o erro...")
    } finally {
   print("Fechando o recurso. Isto sempre executa!")
}
```

Capítulo 9: O Ecossistema - Expandindo a Lucida-Flow com Módulos

O verdadeiro poder da Lucida-Flow vem da sua capacidade de ser estendida. O comando import é a sua porta de entrada para um universo de funcionalidades.

9.1. Sintaxe do import

import "nome_do_modulo" as alias

O alias é um "apelido" que você usará para aceder às funcionalidades do módulo, evitando conflitos de nomes.

9.2. Biblioteca Padrão

A Lucida-Flow vem com módulos nativos para tarefas comuns:

math: Funções e constantes matemáticas (m.pi, m.sqrt(...)).

fs: Manipulação do sistema de ficheiros (fs.read(...), fs.write(...)).

time e datetime: Funções para lidar com tempo e datas.

json: Para analisar (parse) e criar (stringify) strings no formato JSON.

9.3. Tutorial: Criando Seu Próprio Módulo com Python

Qualquer script Python pode se tornar um módulo para a Lucida-Flow.

Crie o Ficheiro: Na pasta lib/ do seu projeto, crie um arquivo, por exemplo, meu_plugin.py.

Escreva a Lógica em Python: Crie funções que recebem uma lista de argumentos.

Python

```
 lib/meu_plugin.py
 #--- Lógica de Runtime ---
def lf_saudacao_especial(args):
nome = args[0] if args else "estranho"
   return f"Olá do meu plugin, {nome}!!! ✨"
   NATIVE_PLUGIN_MODULE = { "saudacao": lf_saudacao_especial }
   #--- Descrição Semântica ---
   from lucida_symbols import *`
    def register_semantics():
    string_type = BuiltInTypeSymbol('string')
    module_scope = ScopedSymbolTable(scope_name='meu_plugin', scope_level=2)
    module_scope.define(
        BuiltInFunctionSymbol(
            name='saudacao',
            params=[VarSymbol('nome', string_type)],
            return_type=string_type
        )
    )
     return module_scope
```
    
Registre o Plugin em lucida_stdlib.py: Adicione o seu novo módulo aos dicionários NATIVE_MODULES e NATIVE_MODULES_SEMANTICS.

Use na Lucida-Flow:

Snippet de código

```
import "meu_plugin" as plugin
print(plugin.saudacao("Marco")
```


## Apoie o Projeto

A Lucida-Flow é um projeto independente e de código aberto. Se você gosta da linguagem e quer ver o seu desenvolvimento continuar, considere [tornar-se um patrocinador no GitHub Sponsors](https://github.com/sponsors/marconeed)! O seu apoio é fundamental para a manutenção e evolução do projeto.



# Construindo Aplicações Gráficas com Lucida-Flow
Subtítulo: Do Terminal à Janela: Criando GUIs com Lucida-Flow

Introdução: Do Terminal à Janela

Bem-vindo ao segundo volume da Biblioteca Lucida-Flow! Se você já dominou os fundamentos da linguagem com o nosso "Manual de Referência", está agora no lugar certo para dar o próximo e mais excitante passo: dar vida às suas ideias com interfaces gráficas interativas.

Para que serve este livro? Este livro é puramente prático. É o seu guia "mãos na massa" para usar a Lucida-Flow para o que ela faz de melhor: atuar como o cérebro lógico por trás de aplicações complexas. Ao longo dos próximos capítulos, vamos deixar o terminal para trás e começar a construir programas com janelas, botões, caixas de texto, telas de desenho e muito mais.

A Filosofia: Aprender Fazendo Acreditamos que a melhor forma de aprender a programar aplicações é construindo-as. Em vez de longas explicações teóricas, cada capítulo deste livro é focado num projeto prático e completo. Começaremos com uma aplicação simples e, a cada capítulo, introduziremos um novo conceito, um novo widget e um novo desafio, terminando com aplicações que interagem com o sistema de ficheiros, com a internet e com os seus próprios movimentos do rato.

O que você vai construir:

•	Um contador de cliques interativo.

•	Um relógio digital que se atualiza em tempo real.

•	Um gerador de palavras-passe seguras com opções customizáveis.

•	Um bloco de notas funcional para ler e salvar ficheiros de texto.

•	E muito mais!

Para seguir este livro, você já deve estar confortável com a sintaxe básica da Lucida-Flow, como a declaração de variáveis, loops e funções. Se precisar de rever estes conceitos, o "Livro 1: O Manual de Referência" é o seu companheiro ideal.

Prepare-se para transformar o seu código em experiências visuais e interativas. Vamos começar a construir.

Estrutura do Livro

Este livro foi projetado para ser uma jornada prática e incremental. Em vez de focarmos na teoria, vamos mergulhar diretamente na construção de aplicações reais, onde cada capítulo introduz um novo desafio e um novo conjunto de ferramentas.

A nossa abordagem é "aprender fazendo". Cada projeto é autocontido, mas os conceitos aprendidos em um serão a base para o próximo.

Capítulo 1: O Contador de Cliques

Começamos com o "Olá, Mundo!" das aplicações gráficas. Este projeto simples ensina os conceitos mais fundamentais: como gerir o estado de uma aplicação (uma variável que guarda o número) e como fazer a interface reagir a eventos do utilizador (cliques nos botões).

Capítulo 2: O Relógio Digital

Neste capítulo, damos vida à nossa aplicação. Aprenderemos a criar interfaces que se atualizam sozinhas em intervalos de tempo, um conceito essencial para qualquer programa dinâmico, desde jogos a dashboards.

Capítulo 3: O Gerador de Palavras-passe

Vamos além dos botões e rótulos básicos. Este projeto introduz novos widgets de interface, como Checkboxes e Sliders, permitindo que o utilizador personalize a sua experiência e dando-nos mais ferramentas para criar UIs complexas.

Capítulo 4: O Bloco de Notas Simples

Aqui, unimos a nossa interface gráfica ao sistema de ficheiros. Você aprenderá a usar widgets de texto de múltiplas linhas e a implementar a lógica para abrir e salvar o trabalho do utilizador em ficheiros de texto.
Capítulo 5: A Aplicação de Meteorologia

Este é o nosso primeiro projeto conectado à internet. Aprenderemos a usar os módulos web e json da Lucida-Flow para comunicar com uma API externa, obter dados em tempo real e exibi-los na nossa aplicação.

Capítulo 6: O Cronómetro

Aprofundamos a nossa gestão de estado. Este projeto ensina a lidar com uma lógica mais complexa (estados como "a correr", "parado", "resetado") para criar uma ferramenta de produtividade funcional.

Capítulo 7: A Aplicação de Desenho "Paint"

No nosso projeto final, libertamo-nos dos widgets tradicionais. Aprenderemos a usar uma "tela" (Canvas) e a reagir diretamente aos movimentos e cliques do rato para criar uma aplicação de desenho livre, a base para projetos mais criativos e jogos.

Capítulo 1: O Contador de Cliques (Foco em Estado e Eventos)

Introdução Este é o "Olá, Mundo!" das aplicações gráficas. Construiremos uma janela com um número (começando em zero) e dois botões: "+" e "-". Clicar nos botões irá incrementar ou decrementar o número. Este projeto ensina o conceito mais importante de uma GUI: a relação entre estado (uma variável que guarda o valor) e eventos (o clique do utilizador).

Conceitos a Aprender

•	Manter o "estado" da aplicação numa variável.

•	Ter múltiplos botões a chamar diferentes funções.

•	Atualizar um widget (o rótulo do número) em resposta a um evento.

O Código (contador.lf)

```
#contador.lf
print("A construir a aplicação de contador...")
#--- 1. Estado da Aplicação ---
#A variável que guarda o número atual.
let valor_contador = 0
#--- 2. Funções de Callback (O que os botões fazem) ---
#Esta função é chamada pelo botão '+'
define process incrementar() {
    valor_contador += 1
    # Atualiza o texto do rótulo com o novo valor
    gui.alterar_texto("rotulo_contador", f"Valor: {valor_contador}")
}
#Esta função é chamada pelo botão '-'
define process decrementar() {
    valor_contador -= 1
    gui.alterar_texto("rotulo_contador", f"Valor: {valor_contador}")
}
#--- 3. Construção da Interface Gráfica ---
gui.criar_rotulo("rotulo_contador", f"Valor: {valor_contador}")
gui.criar_botao("botao_mais", "+", "incrementar")
gui.criar_botao("botao_menos", "-", "decrementar")
```

Executando o Projeto Para executar este projeto, o anfitrião gui_host.py deve estar configurado para carregar o ficheiro contador.lf. Ao ser executado, uma janela simples aparecerá, e os botões irão atualizar o valor do contador em tempo real, demonstrando a interação entre a lógica Lucida-Flow e a interface gráfica.

Capítulo 2: O Relógio Digital (Foco em Atualizações Automáticas)

Introdução

No nosso primeiro projeto, a interface só era atualizada quando o utilizador clicava num botão. Mas e se quisermos que uma aplicação se atualize sozinha? Neste capítulo, construiremos um relógio digital que mostra a hora atual e se atualiza a cada segundo, sem qualquer intervenção do utilizador.

Este projeto é a introdução perfeita à programação orientada a eventos baseados no tempo, uma técnica essencial para criar animações, jogos e qualquer aplicação que precise de "viver" e mudar com o tempo.

Conceitos a Aprender

•	Eventos Agendados: O conceito de agendar uma função para ser executada no futuro.

•	Loops Recursivos de Atualização: A técnica de uma função se agendar a si mesma repetidamente para criar um ciclo de atualização contínuo.

•	Módulos Nativos: Usar o módulo datetime para obter e formatar a hora atual.

•	Gestão de Estado: Manter o "motor" do relógio a funcionar através de uma variável de estado.

O Código (relogio.lf)

A beleza deste projeto está na sua simplicidade. A lógica principal é uma única função que faz três coisas: obtém a hora, atualiza a interface e agenda a sua próxima execução.
Ação: Crie um ficheiro chamado relogio.lf e cole o seguinte código.

```
#relogio.lf
import "datetime" as dt
print("A construir a aplicação de relógio digital...")
#--- Função de Lógica Principal ---
define process atualizar_relogio() {
    # 1. Obtém o timestamp atual do sistema
    let agora = dt.now()
    # 2. Formata o timestamp para o formato de Hora:Minuto:Segundo
    let hora_formatada = dt.format(agora, "%H:%M:%S")
    # 3. Atualiza o texto do rótulo na interface gráfica
    gui.alterar_texto("visor_relogio", hora_formatada)
    # 4. A MÁGICA: Agenda esta mesma função para ser chamada novamente
    #    daqui a 1 segundo (1000 milissegundos).
    gui.agendar_atualizacao(1000, "atualizar_relogio")
}
#--- Construção da Interface Gráfica ---
#Usamos o nosso rótulo especial de resultado para dar um estilo de relógio digital
gui.criar_rotulo_resultado("visor_relogio", "A carregar...")
#Inicia o ciclo de atualização pela primeira vez, que depois continuará para sempre
atualizar_relogio()
```

Executando o Projeto

1.	No seu anfitrião gui_host.py, altere a linha de carregamento para with open("relogio.lf", 'r', encoding='utf-8') as f:.
2.	Execute o anfitrião no seu terminal: python gui_host.py.

Uma janela irá aparecer, mostrando a hora atual a mudar a cada segundo. Você acabou de criar uma aplicação dinâmica!

Desafios para Expansão

•	Modifique o dt.format() para incluir também a data (%d/%m/%Y).

•	Adicione um botão "Parar/Continuar" que controle uma variável booleana (como esta_pausado) para parar e retomar as atualizações.

Capítulo 3: O Bloco de Notas Simples (Foco em Texto Multilinha e Interação com Ficheiros)

Introdução

Aplicações de texto são a base de muita da nossa interação com computadores. Neste capítulo, vamos construir um editor de texto minimalista, o nosso próprio "Bloco de Notas". A nossa aplicação terá uma área de texto principal onde o utilizador pode escrever livremente, e dois botões essenciais: "Abrir" para carregar um ficheiro de texto, e "Salvar" para guardar o trabalho.

Este projeto é um exemplo perfeito de como a Lucida-Flow pode orquestrar a interação entre a interface gráfica do utilizador e o sistema de ficheiros do computador.

Conceitos a Aprender

•	Widget de Texto Multilinha: Como criar uma área de texto grande para edição.

•	Interação com Módulos Nativos: Usar o módulo fs (fs.read e fs.write) para carregar e salvar o conteúdo da área de texto.

•	Diálogos do Sistema: Usar o gui para abrir as janelas nativas de "Abrir Ficheiro" e "Salvar Ficheiro".

•	Combinação de Lógica: Juntar a lógica da UI com a lógica de manipulação de ficheiros num único programa.

O Código (bloco_de_notas.lf)

Este script define a interface e as funções que os botões irão chamar.

Ação: Crie um ficheiro chamado bloco_de_notas.lf e cole o seguinte código.

```
#bloco_de_notas.lf
import "fs" as fs
print("A construir a aplicação de Bloco de Notas...")
#--- Funções de Lógica ---
define process salvar_ficheiro() {
    # 1. Abre o diálogo "Salvar Como..." do sistema
    let caminho_ficheiro = gui.salvar_dialogo_ficheiro()
        # 2. Se o utilizador não cancelou...
    when caminho_ficheiro != "" {
        print(f"A salvar o ficheiro em: {caminho_ficheiro}")
        # 3. Obtém todo o texto da caixa de texto
        let conteudo = gui.obter_texto_completo("caixa_principal")
        # 4. Escreve o conteúdo no ficheiro escolhido
        fs.write(caminho_ficheiro, conteudo)
        # 5. Atualiza a barra de status
        gui.alterar_texto("rotulo_status", f"Ficheiro salvo com sucesso!")
    }
}
define process abrir_ficheiro() {
    # 1. Abre o diálogo "Abrir Ficheiro..." do sistema
    let caminho_ficheiro = gui.abrir_dialogo_ficheiro()
    # 2. Se o utilizador escolheu um ficheiro...
    when caminho_ficheiro != "" {
        print(f"A abrir o ficheiro: {caminho_ficheiro}")
        try {
            # 3. Lê o conteúdo do ficheiro
            let conteudo = fs.read(caminho_ficheiro)
            # 4. Coloca o conteúdo na caixa de texto
            gui.definir_texto_completo("caixa_principal", conteudo)
            gui.alterar_texto("rotulo_status", f"Ficheiro '{caminho_ficheiro}' carregado.")
        } catch (e: Exception) {
            gui.alterar_texto("rotulo_status", f"Erro ao ler o ficheiro: {e}")
        }
    }
}
#--- Construção da Interface Gráfica ---
gui.criar_botao("botao_abrir", "Abrir", "abrir_ficheiro")
gui.criar_botao("botao_salvar", "Salvar", "salvar_ficheiro")
gui.criar_caixa_texto("caixa_principal")
gui.criar_rotulo("rotulo_status", "Bem-vindo ao Bloco de Notas Lucida-Flow!")
```


Executando o Projeto

1.	No seu anfitrião gui_host.py, altere a linha de carregamento para with open("bloco_de_notas.lf", 'r', encoding='utf-8') as f:.

2.	Execute o anfitrião no seu terminal: python gui_host.py.

Uma janela com uma área de texto e os botões "Abrir" e "Salvar" irá aparecer. Teste o ciclo completo: escreva algo, clique em "Salvar" e guarde o seu ficheiro. Depois, apague o texto, clique em "Abrir" e carregue o ficheiro que acabou de salvar. O seu texto deverá reaparecer!

Desafios para Expansão

•	Adicione um menu "Ficheiro" com as opções "Abrir" e "Salvar" em vez de usar botões.

•	Mostre o nome do ficheiro que está a ser editado no título da janela.

•	Implemente uma verificação de "ficheiro modificado" para perguntar ao utilizador se ele quer salvar as alterações antes de fechar a aplicação.

Capítulo 4: Previsão do Tempo (Foco em APIs e Módulos web e json)

Introdução

Neste capítulo, vamos construir uma aplicação gráfica que vai além do nosso computador. Criaremos uma ferramenta de "Previsão do Tempo" que consulta um serviço online (uma API) para obter e exibir a temperatura e a condição do tempo atuais para qualquer cidade do mundo que o utilizador digitar.

Este projeto é um exemplo fantástico de como a Lucida-Flow pode ser usada como uma "linguagem de cola" para orquestrar diferentes tecnologias: a interface gráfica, a comunicação com a internet e a análise de dados.
Conceitos a Aprender

•	Consumo de APIs: O conceito fundamental de como um programa pode "conversar" com um serviço na internet para pedir informações.

•	Módulos web e json: Usaremos o nosso plugin web para fazer o pedido à API e o json para analisar a resposta.

•	UI Dinâmica: Atualizar múltiplos rótulos na interface com os dados recebidos da API.

Passo 1: A Ferramenta Essencial - Uma API Key Gratuita

Para obter dados de meteorologia, precisamos de nos registar num serviço que os forneça. Usaremos o OpenWeatherMap, que é muito popular e oferece um plano gratuito excelente.

1.	Vá ao site OpenWeatherMap.

2.	Crie uma conta gratuita.

3.	Depois de fazer login, navegue até à secção "API keys" do seu perfil.

4.	Copie a sua "API key" padrão. É uma longa sequência de letras e números. Guarde-a, pois vamos precisar dela no nosso script.

O Código (previsao_tempo.lf)

Este script define a interface e a lógica para chamar a API.

Ação: Crie um ficheiro chamado previsao_tempo.lf.

```
#previsao_tempo.lf
import "web" as web
import "json" as json
print("A construir a aplicação de Meteorologia...")
#--- Configuração ---
#IMPORTANTE: Cole a sua API Key do OpenWeatherMap aqui
const API_KEY = "SUA_API_KEY_AQUI"
#--- Funções de Lógica ---
define process obter_previsao() {
    let cidade = gui.obter_texto("entrada_cidade")
    when cidade == "" {
        gui.alterar_texto("rotulo_resultado", "Por favor, insira o nome de uma cidade.")
        return
    }
    gui.alterar_texto("rotulo_resultado", f"A procurar o tempo para {cidade}...")
    # Monta a URL da API, pedindo unidades métricas e a resposta em português
    let url = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&units=metric&lang=pt"
    try {
        # 1. Faz o pedido à internet
        let resposta_json = web.get(url)
        # 2. Analisa a resposta JSON
        let dados = json.parse(resposta_json)
        # 3. Extrai as informações de que precisamos
        # A resposta vem num dicionário aninhado, que acedemos com []
        let descricao = dados["weather"][0]["description"]
        let temperatura = dados["main"]["temp"]
        # 4. Atualiza a interface
        let resultado_final = f"Tempo: {descricao}\nTemperatura: {temperatura}°C"
        gui.alterar_texto("rotulo_resultado", resultado_final)
    } catch (e: Exception) {
        gui.alterar_texto("rotulo_resultado", "Erro: Cidade não encontrada ou problema de rede.")
    }
}
#--- Construção da Interface Gráfica ---
gui.criar_rotulo("rotulo_instrucao", "Digite o nome de uma cidade:")
gui.criar_entrada("entrada_cidade")
gui.criar_botao("botao_pesquisar", "Ver Previsão do Tempo", "obter_previsao")
#Usamos o nosso rótulo de resultado especial para dar mais destaque
gui.criar_rotulo_resultado("rotulo_resultado", "")
```

Executando o Projeto

1.	No seu ficheiro previsao_tempo.lf, não se esqueça de substituir "SUA_API_KEY_AQUI" pela sua chave real do OpenWeatherMap.

2.	Altere o seu gui_host.py para carregar o previsao_tempo.lf.

3.	Execute o anfitrião: python gui_host.py.

Uma janela irá aparecer. Digite o nome de uma cidade (ex: "Porto", "São Paulo", "Nova Iorque"), clique no botão e, após um momento, a temperatura e a condição do tempo atuais deverão aparecer!
Desafios para Expansão

•	Adicione mais informações à interface, como a humidade (humidity) ou a velocidade do vento (wind.speed), que também vêm na resposta da API.

•	Mude o ícone da aplicação com base no tempo (ex: um sol para "céu limpo", uma nuvem para "nublado").

•	Guarde a última cidade pesquisada num ficheiro para que a aplicação se lembre da sua preferência.

Capítulo 5: O Gerador de Palavras-passe (Foco em Novos Widgets: Checkbox e Slider)

Introdução

Neste capítulo, vamos construir uma ferramenta de segurança muito útil: um Gerador de Palavras-passe. Esta aplicação permitirá ao utilizador definir critérios para a sua palavra-passe, como o comprimento e os tipos de caracteres a incluir (maiúsculas, números, símbolos).

Este projeto é excelente para aprendermos a usar componentes de UI mais avançados, como caixas de seleção (checkboxes) para opções de "ligado/desligado" e um controlo deslizante (slider) para selecionar um valor num intervalo.

Conceitos a Aprender

•	Novos Widgets: Checkbox para opções e Slider para valores numéricos.

•	Lógica Condicional na UI: Construir uma string de caracteres permitidos com base nas opções que o utilizador selecionou.

•	Geração Aleatória: Usar o nosso módulo dado para escolher caracteres aleatórios e construir a palavra-passe final.

O Código (gerador_senha.lf)

Este script define a interface e a lógica principal da aplicação.

Ação: Crie um ficheiro chamado gerador_senha.lf e cole o seguinte código.

```
#gerador_senha.lf
import "dado" as d
print("A construir a aplicação Gerador de Senhas...")
#--- Função de Lógica ---
define process gerar_senha() {
    let caracteres_base = "abcdefghijklmnopqrstuvwxyz"
    let numeros = "0123456789"
    let simbolos = "!@#$%&*()_+"
    let caracteres_permitidos = caracteres_base
    # Verifica os checkboxes e adiciona os conjuntos de caracteres
    when gui.obter_valor_checkbox("check_maiusculas") == 1 {
        caracteres_permitidos = caracteres_permitidos + caracteres_base.to_upper()
    }
    when gui.obter_valor_checkbox("check_numeros") == 1 {
        caracteres_permitidos = caracteres_permitidos + numeros
    }
    when gui.obter_valor_checkbox("check_simbolos") == 1 {
        caracteres_permitidos = caracteres_permitidos + simbolos
    }
    let comprimento = gui.obter_valor_slider("slider_comprimento")
    let senha_final = ""
    when comprimento > 0 {
        let i = 0
        while i < comprimento {
            let indice_aleatorio = d.rolar_entre(0, caracteres_permitidos.length() - 1)
            let caractere_aleatorio = caracteres_permitidos[indice_aleatorio]
            senha_final = senha_final + caractere_aleatorio
            i += 1
        }
    }
    gui.alterar_texto("rotulo_senha", senha_final)
}
#--- Construção da Interface Gráfica ---
gui.criar_rotulo("titulo", "Gerador de Palavras-passe")
gui.criar_checkbox("check_maiusculas", "Incluir Letras Maiúsculas")
gui.criar_checkbox("check_numeros", "Incluir Números")
gui.criar_checkbox("check_simbolos", "Incluir Símbolos")
gui.criar_rotulo("label_comprimento", "\nComprimento da Senha:")
gui.criar_slider("slider_comprimento", 8, 32)
gui.criar_botao("botao_gerar", "Gerar Senha", "gerar_senha")
#Usa o nosso rótulo especial de resultado
gui.criar_rotulo_resultado("rotulo_senha", "[Sua senha aparecerá aqui]")
```

Executando o Projeto

1.	Certifique-se de que o seu anfitrião gui_host.py está atualizado com as funções para criar os novos widgets (Checkbox e Slider).

2.	Altere a linha de carregamento no seu gui_host.py para with open("gerador_senha.lf", 'r', encoding='utf-8') as f:.

3.	Execute o anfitrião no seu terminal: python gui_host.py.

Uma janela irá aparecer com todas as opções. Marque as caixas que desejar, ajuste o comprimento no slider e clique em "Gerar Senha". Uma nova palavra-passe segura será criada e exibida no rótulo de resultado!
Desafios para Expansão

•	Adicione um botão "Copiar" que copie a senha gerada para a área de transferência.

•	Mostre uma indicação da "força" da palavra-passe (fraca, média, forte) com base nas opções selecionadas e no comprimento.

•	Garanta que a palavra-passe gerada contém pelo menos um caractere de cada tipo selecionado.

Capítulo 6: Cronómetro (Foco em Gestão de Estado Complexa)

Introdução

Neste capítulo, vamos construir uma aplicação que a maioria de nós já usou: um cronómetro. A nossa versão terá um visor para o tempo decorrido e dois botões: um para "Iniciar/Parar" e outro para "Resetar".

Este projeto é um excelente exercício para aprofundar a nossa compreensão sobre a gestão de estado numa aplicação. A lógica precisará de saber a todo o momento se o cronómetro está a correr, parado ou se foi reiniciado, e reagir de acordo com as ações do utilizador.

Conceitos a Aprender

•	Gestão de Estado com Variáveis: Usar uma variável booleana (esta_a_correr) para controlar o fluxo principal da aplicação.

•	Eventos Agendados: Reforçar o uso de gui.agendar_atualizacao para criar o "motor" do tempo que atualiza a interface.

•	Lógica Condicional: Usar when para alterar o comportamento da aplicação com base no seu estado atual.

•	Formatação de Tempo: Converter um número de segundos (float) num formato de tempo legível (MM:SS.d).

O Código (cronometro.lf)

Toda a lógica viverá no nosso ficheiro Lucida-Flow. Usaremos variáveis para controlar o estado e a função de agendamento para criar o "motor" do tempo.

Ação: Crie um ficheiro chamado cronometro.lf.

```
#cronometro.lf
print("A construir a aplicação de Cronómetro...")
#--- 1. Variáveis de Estado da Aplicação ---
let tempo_decorrido = 0.0  # Em segundos
let esta_a_correr = false
#--- 2. Funções de Lógica e Callbacks ---
#A função principal que corre a cada 100ms
define process atualizar_cronometro() {
    # Só faz alguma coisa se o cronómetro estiver ligado
    when esta_a_correr == true {
        tempo_decorrido += 0.1
        # Formata o tempo para MM:SS.d
        let minutos = to_int(tempo_decorrido / 60)
        let segundos = to_int(tempo_decorrido % 60)
        let decimos = to_int((tempo_decorrido * 10) % 10)
        # Garante que os números têm sempre 2 dígitos (ex: 01, 02...)
        let min_str = f"0{minutos}"
        when minutos > 9 { min_str = f"{minutos}" }
        let seg_str = f"0{segundos}"
        when segundos > 9 { seg_str = f"{segundos}" }
        let tempo_formatado = f"{min_str}:{seg_str}.{decimos}"
        gui.alterar_texto("visor", tempo_formatado)
        # Agenda a si própria para ser chamada novamente
        gui.agendar_atualizacao(100, "atualizar_cronometro")
    }
}
#Chamada pelo botão "Iniciar/Parar"
define process iniciar_parar() {
    esta_a_correr = not esta_a_correr
    # Se acabámos de o ligar, temos de iniciar o ciclo de atualização
    when esta_a_correr == true {
        atualizar_cronometro()
    }
}
#Chamada pelo botão "Resetar"
define process resetar() {
    esta_a_correr = false
    tempo_decorrido = 0.0
    gui.alterar_texto("visor", "00:00.0")
}
#--- 3. Construção da Interface Gráfica ---
gui.criar_rotulo_resultado("visor", "00:00.0")
gui.criar_botao("botao_iniciar", "Iniciar/Parar", "iniciar_parar")
gui.criar_botao("botao_resetar", "Resetar", "resetar")
```

Executando o Projeto

1.	No seu anfitrião gui_host.py, altere a linha de carregamento para with open("cronometro.lf", 'r', encoding='utf-8') as f:.
2.	Execute o anfitrião no seu terminal: python gui_host.py.

Uma janela com um cronómetro irá aparecer. O botão "Iniciar/Parar" irá alternar entre correr e pausar o tempo, e o botão "Resetar" irá zerar o contador.

Desafios para Expansão

•	Adicione um botão "Volta" (Lap) que grave o tempo atual numa lista e o exiba numa caixa de texto.

•	Mude o texto do botão "Iniciar/Parar" para "Pausar" quando o cronómetro estiver a correr.

•	Converta o cronómetro num temporizador regressivo (countdown timer).

Capítulo 7: Paint (Foco em Canvas e Eventos do Rato)

Introdução

Neste capítulo final, vamos construir a nossa própria aplicação de desenho, um "Paint" super básico. Em vez de widgets pré-definidos como botões e rótulos, criaremos uma "tela" em branco onde o utilizador poderá desenhar livremente usando o rato.

Este projeto introduz o conceito de programação orientada a eventos com o rato, abrindo as portas para criar jogos e aplicações muito mais interativas e dinâmicas.

Conceitos a Aprender

•	Widget de Tela (Canvas): Como criar uma área de desenho livre.

•	Eventos do Rato: Como fazer a nossa linguagem reagir a eventos como "o botão do rato foi pressionado", "o rato moveu-se" e "o botão do rato foi solto".

•	Lógica de Desenho: Usar as coordenadas do rato para desenhar linhas e criar traços contínuos.

•	Gestão de Estado: Guardar a última posição do rato para saber de onde a onde desenhar.

O Código (paint.lf)

Este script cria a interface e define as funções que irão "ouvir" os eventos do rato para desenhar na tela.

Ação: Crie um ficheiro chamado paint.lf e cole o seguinte código.

```
#paint.lf
print("A construir a aplicação de Paint...")
#--- Variáveis de Estado ---
#Guardam a última posição do rato para sabermos de onde a onde desenhar a linha.
let ultimo_x = 0
let ultimo_y = 0
#--- Funções de Callback (Eventos do Rato) ---
#Esta função é chamada quando o botão esquerdo do rato é pressionado na tela.
define process ao_pressionar_botao(x: int, y: int) {
    # Define o ponto de partida do nosso traço.
    ultimo_x = x
    ultimo_y = y
}
#Esta função é chamada quando o rato se move COM o botão pressionado.
define process ao_mover_rato(x: int, y: int) {
    # Desenha uma pequena linha da última posição até à posição atual.
    gui.desenhar_linha("tela_desenho", ultimo_x, ultimo_y, x, y, "black")
    # Atualiza a "última posição" para a posição atual, para que a próxima linha
    # comece a partir daqui.
    ultimo_x = x
    ultimo_y = y
}
#--- Construção da Interface Gráfica ---
gui.criar_rotulo("titulo", "Aplicação de Desenho Lucida-Flow")
gui.criar_tela("tela_desenho", 500, 400, "white") # Uma tela branca de 500x400 pixels
#Vincula as nossas funções aos eventos do rato que acontecem no widget "tela_desenho".
gui.vincular_evento_rato("tela_desenho", "botao_pressionado", "ao_pressionar_botao")
gui.vincular_evento_rato("tela_desenho", "movimento", "ao_mover_rato")
```

Executando o Projeto

1.	Garanta que o seu anfitrião gui_host.py está atualizado com as funções para criar_tela, vincular_evento_rato e desenhar_linha.
2.	Altere a linha de carregamento no seu gui_host.py para with open("paint.lf", 'r', encoding='utf-8') as f:.
3.	Execute o anfitrião no seu terminal: python gui_host.py.

Uma janela com uma tela branca irá aparecer. Clique com o botão esquerdo do rato e arraste-o sobre a tela para desenhar!

Desafios para Expansão

•	Adicione botões para permitir que o utilizador mude a cor do pincel (ex: "Preto", "Vermelho", "Azul").

•	Adicione um slider para controlar a espessura do pincel.

•	Crie um botão "Limpar" que apague todo o conteúdo da tela.


## Apoie o Projeto

A Lucida-Flow é um projeto independente e de código aberto. Se você gosta da linguagem e quer ver o seu desenvolvimento continuar, considere [tornar-se um patrocinador no GitHub Sponsors](https://github.com/sponsors/marconeed)! O seu apoio é fundamental para a manutenção e evolução do projeto.
