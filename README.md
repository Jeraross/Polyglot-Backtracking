# Polyglot-Backtracking

Bem-vindo a este "laboratório" de código dedicado à exploração e análise de algoritmos de **backtracking** implementados em múltiplas linguagens de programação.

Este projeto foi desenvolvido como requisito para a disciplina de **Teoria da Computação**. Nosso principal objetivo é analisar e comparar as implementações em três eixos principais:

1.  **Performance:** Tempo de execução e uso de memória em diferentes tamanhos de entrada.
2.  **Expressividade:** Legibilidade, quantidade de linhas e clareza do código.
3.  **Paradigma:** A "forma idiomática" de resolver o problema em cada linguagem (ex: imperativo vs. funcional vs. baixo nível).

---

## O que você encontrará aqui?

Este repositório está organizado por problemas. Para cada problema, você encontrará uma ou mais implementações em cada uma das linguagens de estudo.

### Problemas Clássicos

* **`n-queens/`**: O problema clássico de posicionar N rainhas em um tabuleiro NxN sem que ataquem umas às outras.
* **`sudoku-solver/`**: Um solucionador de Sudoku que preenche grades vazias usando a lógica de backtracking.

### Estudo de Caso Especial: A Analogia de Metroid

A seção `/metroid` é um caso especial. Ela não resolve um problema combinatório, mas sim **implementa a analogia** que usamos para entender o backtracking. Veja a seção dedicada abaixo.

---

## As Linguagens (Os "Poliglotas")

A escolha das linguagens foi feita para maximizar as diferenças de paradigma e performance:

* **Python (Alto Nível):** Focado na clareza, legibilidade e velocidade de *implementação*.
* **C++ (Compilada):** Focado no desempenho bruto, controle manual de memória e otimizações de baixo nível.
* **Haskell (Funcional Pura):** Focado em uma abordagem declarativa, imutável e na elegância matemática da solução.
* **Assembly (Nível de Máquina):** Usado como a *baseline* definitiva para performance, demonstrando o custo real das abstrações das outras linguagens.

---

## Estudo de Caso: A Analogia de Metroid

**Por que Metroid está em um repositório de backtracking?**

Usamos o gênero *Metroidvania* como a principal analogia para explicar o backtracking: um algoritmo de "tentativa e erro" inteligente.

* **O Jogo:** Samus (o algoritmo) explora um mapa (o espaço de busca).
* **A Tentativa:** Ela escolhe um caminho (uma "escolha" recursiva).
* **O Beco Sem Saída:** Ela encontra uma porta vermelha sem mísseis (uma "constraint" ou regra violada).
* **O "Backtrack":** Ela **volta atrás** (desfaz a escolha/retorna da recursão) até o último ponto de decisão e tenta o *outro* caminho.
* **A Solução Parcial:** Ela encontra um *power-up* (ex: Morph Ball), que muda seu estado e permite que caminhos anteriormente inválidos agora sejam explorados.

Os códigos nesta pasta (`/metroid`) **simulam esse processo de exploração de mapa**, servindo como uma ferramenta de estudo visual e prática da lógica fundamental do backtracking.

---

## Como Usar

Cada pasta de problema (ex: `n-queens/`) contém seu próprio `README.md` com instruções de compilação e execução para cada linguagem.

Geralmente, você precisará de:
* Um compilador C++ (g++, clang)
* Um interpretador Python 3
* O compilador GHC (para Haskell)
* Um montador (ex: NASM) e linker (ld) para Assembly.

Scripts de benchmark e os resultados da análise de performance podem ser encontrados na pasta `/analysis`.
