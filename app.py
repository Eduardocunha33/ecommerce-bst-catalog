import streamlit as st
from tree import BinaryTree
from product import Product
from catalogData import loadCatalog

# configura o titulo da aba do navegador e deixa a pagina no modo largo (wide)
st.set_page_config(page_title="E-commerce BST", layout="wide")

# o Streamlit roda o arquivo inteiro de cima a baixo a cada clique ou movimento do slider.
#O st.session_state funciona como uma memoria da pagina para a arvore nao ser apagada e recriada toda hora.
if "catalog" not in st.session_state:
    # cria a BST e carrega os 42 produtos apenas na primeira vez que a pagina abre
    catalogTree = BinaryTree()
    loadCatalog(catalogTree)
    st.session_state.catalog = catalogTree

# cria um apelido curto para facilitar o uso da arvore guardada na memoria
catalog = st.session_state.catalog

# --- CABECALHO DA PAGINA ---
st.title("🛒 Catálogo de Eletrônicos com Árvore Binária")
st.caption("Busca otimizada por faixa de preço pulando galhos fora do intervalo.")

# --- BARRA LATERAL (FILTROS E CADASTRO) ---
st.sidebar.header("Filtros do Catálogo")

# busca o maior preco atual na arvore para definir o limite maximo do slider
mostExpensiveInitial = catalog.findMax()
minLimit = 0.0
maxLimit = float(mostExpensiveInitial.price)

# cria o controle deslizante com dois pontos (preco minimo e preco maximo)
minPrice, maxPrice = st.sidebar.slider(
    "Faixa de preço (R$)",
    min_value=minLimit,
    max_value=maxLimit,
    value=(minLimit, maxLimit),
    step=1.0
)

# pega todas as categorias existentes na arvore sem repeticao usando set() e ordena de A a Z
allProducts = catalog.getAllInOrder()
categories = sorted(set(item.category for item in allProducts))

# menu suspenso para filtrar opcionalmente por categoria (alem do preco)
selectedCategory = st.sidebar.selectbox(
    "Categoria",
    ["Todas"] + categories
)

st.sidebar.divider()

# cria uma caixinha recolhivel na barra lateral para cadastrar novos produtos ao vivo
with st.sidebar.expander("➕ Cadastrar novo produto"):
    # st.form agrupa os campos para a pagina so atualizar quando clicar no botao de envio
    with st.form("addProductForm", clear_on_submit=True):
        newName = st.text_input("Nome do produto")
        newCategory = st.selectbox("Categoria", categories)
        newSpecs = st.text_input("Especificação (ex: 1 TB, Sem fio)")
        newPrice = st.number_input("Preço (R$)", min_value=1.0, value=100.0, step=10.0)
        newStock = st.number_input("Estoque", min_value=1, value=10, step=1)
        submitted = st.form_submit_button("Inserir na árvore")

        if submitted:
            # strip() remove espacos extras nas pontas para evitar cadastrar nome em branco
            if newName.strip() == "":
                st.error("Informe o nome do produto.")
            else:
                newProduct = Product(
                    newName.strip(),
                    newCategory,
                    newSpecs.strip(),
                    float(newPrice),
                    int(newStock)
                )
                # insere o produto novo na BST usando o mesmo metodo insert() da aula
                catalog.insert(newProduct)
                st.success(f"'{newProduct.name}' inserido na árvore!")

# --- BUSCA NA BST E CALCULO DE EFICIENCIA ---
# chama o metodo da sua BinaryTree, recebendo a lista filtrada e o numero de nos visitados
filteredProducts, visitedNodes = catalog.searchByPriceRange(minPrice, maxPrice)

# se o usuario escolheu uma categoria especifica, filtra a lista que ja veio pronta da BST
if selectedCategory != "Todas":
    displayProducts = [item for item in filteredProducts if item.category == selectedCategory]
else:
    displayProducts = filteredProducts

# atualiza os extremos e calcula a economia da BST em relacao a uma lista comum
cheapestProduct = catalog.findMin()
mostExpensiveProduct = catalog.findMax()
totalNodes = catalog.countNodes()
skippedNodes = totalNodes - visitedNodes
savedPercent = (skippedNodes / totalNodes) * 100 if totalNodes > 0 else 0

# --- PAINEL DE METRICAS ---
# divide a largura da tela em 4 colunas lado a lado para exibir os indicadores
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total na Árvore", f"{totalNodes} itens")
col2.metric("Mais Barato (findMin)", f"R$ {cheapestProduct.price:.2f}", cheapestProduct.name, delta_color="off")
col3.metric("Mais Caro (findMax)", f"R$ {mostExpensiveProduct.price:.2f}", mostExpensiveProduct.name, delta_color="off")
col4.metric("Nós Visitados (BST)", f"{visitedNodes} de {totalNodes}", f"{savedPercent:.2f}% pulados")

# caixa de destaque mostrando ao vivo o ganho da arvore na faixa selecionada
st.info(
    f"**Eficiência da busca por preço:** uma lista comum precisaria verificar todos os **{totalNodes}** produtos. "
    f"Sua BST analisou apenas **{visitedNodes}** nós e ignorou **{skippedNodes}** galhos (**{savedPercent:.2f}% de economia**)."
)

st.divider()

# --- VITRINE DE PRODUTOS ---
st.subheader(f"Produtos encontrados: {len(displayProducts)}")

if not displayProducts:
    st.warning("Nenhum produto encontrado com os filtros selecionados.")
else:
    # cria 3 colunas para montar a grade de cards da loja
    cardsPerRow = 3
    columns = st.columns(cardsPerRow)

    # o operador % (resto da divisao) distribui os cards em ciclo nas colunas 0, 1 e 2
    for index, product in enumerate(displayProducts):
        currentCol = columns[index % cardsPerRow]
        with currentCol:
            # container com borda cria o visual de card para cada produto
            with st.container(border=True):
                st.caption(product.category)
                st.markdown(f"**{product.name}**")
                st.write(f"Especificação: {product.specs}")
                st.markdown(f"### R$ {product.price:.2f}")
                st.caption(f"Estoque disponível: {product.stock} un.")