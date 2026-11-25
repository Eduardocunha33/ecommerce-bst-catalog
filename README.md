# 🎮 E-commerce Gamer — Catálogo com Árvore Binária de Busca (BST)

Aplicação de e-commerce de eletrônicos e periféricos gamer desenvolvida em **Python** para a disciplina de **Estrutura de Dados**, demonstrando na prática o uso de uma **Árvore Binária de Busca (Binary Search Tree — BST)** para organização e filtragem otimizada de produtos por faixa de preço.

---

## ✨ Funcionalidades

* **Árvore Binária de Busca (BST) customizada (`tree.py`):**
  * Inserção automática ordenada por preço utilizando o método especial `__lt__` na classe `Product`.
  * **Busca otimizada por faixa de preço (`searchByPriceRange`):** poda galhos fora do intervalo mínimo/máximo e contabiliza em tempo real quantos nós foram visitados e quantos foram pulados em relação a uma busca linear.
  * Consulta rápida aos extremos do catálogo (`findMin` e `findMax`), contagem total de nós (`countNodes`) e listagem ordenada (`getAllInOrder`).
* **Catálogo com 42 produtos reais (`catalogData.py`):** consoles, monitores, headsets, controles, mouses e hardware inseridos em ordem balanceada para evitar a degeneração da árvore.
* **Interface Web Interativa (`app.py` com Streamlit):**
  * Tema gamer estilizado com efeitos de destaque/zoom ao passar o mouse e compatível com modo claro e escuro.
  * Barra lateral com filtro por faixa de preço, categoria, resumo da busca em tempo real e botão de limpar filtros.
  * Painel superior com métricas da árvore (total de itens, mais barato, mais caro e economia de nós visitados na BST).
  * **Carrinho flutuante interativo:** botão circular fixo com validação de estoque individual, limite máximo de 15 unidades, modal completo com miniaturas, ajuste de quantidade, remoção de itens, botão de pagamento demonstrativo e comportamento dinâmico ("fujão") enquanto estiver vazio.
* **Modo Terminal (`main.py`):** menu interativo em linha de comando para testes diretos da estrutura de dados.

---

## 📁 Estrutura do Projeto

```text
ecommerce-bst-catalog/
├── app.py              # Interface web interativa (Streamlit + CSS/JS)
├── main.py             # Interface em modo terminal (CLI)
├── tree.py             # Implementação da Árvore Binária de Busca (BinaryTree e Node)
├── product.py          # Modelo de dados do produto e ordenação por preço (__lt__)
├── catalogData.py      # Carga inicial dos 42 produtos balanceados na BST
├── images/             # Imagens locais dos produtos do catálogo
├── requirements.txt    # Dependências do projeto
└── README.md           # Documentação do repositório
```

---

## ⚡ Eficiência da BST na Busca por Preço

| Operação | Lista Comum (Busca Linear) | Árvore Binária de Busca (BST) |
| :--- | :--- | :--- |
| **Busca por faixa de preço** | Percorre todos os $n$ elementos — $O(n)$ | Ignora subárvores fora do intervalo — $O(\log n + k)$ |
| **Menor / Maior preço** | Percorre toda a lista — $O(n)$ | Desce apenas à esquerda ou direita — $O(\log n)$ |
| **Listagem ordenada** | Requer ordenação — $O(n \log n)$ | Percurso em-ordem (*in-order*) — $O(n)$ |

> **Observação:** Em `catalogData.py`, os produtos são inseridos a partir de um valor intermediário (evitando inserção estritamente crescente) para manter a árvore mais equilibrada e preservar o ganho de desempenho.

---

## 🚀 Como Executar Localmente

### Pré-requisitos
* Python 3.10 ou superior instalado.

### Passo a passo

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/SEU-USUARIO/ecommerce-bst-catalog.git](https://github.com/SEU-USUARIO/ecommerce-bst-catalog.git)
   cd ecommerce-bst-catalog
   ```

2. **Crie e ative o ambiente virtual:**
   * **Windows (PowerShell):**
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   * **Linux / macOS / WSL:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação web:**
   ```bash
   streamlit run app.py
   ```

*(Opcional) Para testar a versão em terminal:*
```bash
python main.py
```

---

## 🛠️ Tecnologias Utilizadas

* **Python 3**
* **Streamlit**
* **HTML / CSS / JavaScript** (estilização customizada e interatividade do carrinho)