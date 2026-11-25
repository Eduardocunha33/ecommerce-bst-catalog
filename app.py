import time
import streamlit as st
import streamlit.components.v1 as components
from tree import BinaryTree
from catalogData import loadCatalog

#Explicando: configura o titulo da aba do navegador e deixa a pagina no modo largo (wide)
st.set_page_config(page_title="E-commerce Gamer", layout="wide")

#Explicando: define o limite maximo de unidades permitidas no carrinho do cliente
maxCartItems = 15

#Explicando: injeta CSS para transformar o botao do carrinho em um circulo verde fixo no canto inferior direito
st.markdown(
    """
    <style>
        /* Explicando: fixa o container do botao no canto inferior direito acima do resto da pagina */
        .st-key-floatingCartBtn {
            position: fixed !important;
            bottom: 28px !important;
            right: 28px !important;
            z-index: 9999 !important;
            width: 76px !important;
            height: 76px !important;
        }

        /* Explicando: estiliza o botao em formato redondo, cor verde vibrante e sombra destacada */
        .st-key-floatingCartBtn button {
            width: 76px !important;
            height: 76px !important;
            border-radius: 50% !important;
            background-color: #16a34a !important;
            color: #ffffff !important;
            border: 3px solid #86efac !important;
            box-shadow: 0 6px 20px rgba(22, 163, 74, 0.55) !important;
            padding: 0 !important;
            transition: transform 0.2s ease, background-color 0.2s ease !important;
        }

        /* Explicando: efeito visual ao passar o mouse por cima do botao do carrinho */
        .st-key-floatingCartBtn button:hover {
            background-color: #15803d !important;
            border-color: #ffffff !important;
            transform: scale(1.08) !important;
            color: #ffffff !important;
        }

        /* Explicando: ajusta o tamanho e o alinhamento do icone + contador dentro do circulo */
        .st-key-floatingCartBtn button p {
            font-size: 18px !important;
            font-weight: 700 !important;
            margin: 0 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

#Explicando: o Streamlit roda o arquivo inteiro a cada clique. O session_state guarda a arvore na memoria.
if "catalog" not in st.session_state:
    catalogTree = BinaryTree()
    loadCatalog(catalogTree)
    st.session_state.catalog = catalogTree

#Explicando: cria o carrinho na memoria da sessao (dicionario guardando cada produto e sua quantidade)
if "cart" not in st.session_state:
    st.session_state.cart = {}

#Explicando: controla se a janela do carrinho precisa continuar aberta apos editar itens la dentro
if "reopenCart" not in st.session_state:
    st.session_state.reopenCart = False

#Explicando: apelido curto para facilitar o uso da arvore guardada na memoria
catalog = st.session_state.catalog


# --- FUNCOES AUXILIARES DO CARRINHO ---
def getTotalCartItems():
    #Explicando: soma a quantidade de todos os produtos que estao dentro do carrinho
    return sum(item["quantity"] for item in st.session_state.cart.values())


def addToCart(product):
    #Explicando: id(product) gera um numero unico para cada objeto na memoria
    productId = id(product)
    currentTotal = getTotalCartItems()
    currentQty = st.session_state.cart[productId]["quantity"] if productId in st.session_state.cart else 0

    #Explicando: trava de seguranca - impede passar de 15 itens no carrinho ou ultrapassar o estoque do produto
    if currentTotal >= maxCartItems:
        return
    if currentQty >= product.stock:
        return

    #Explicando: se o produto ja existe no carrinho soma +1, senao cria uma nova entrada com quantidade 1
    if productId in st.session_state.cart:
        st.session_state.cart[productId]["quantity"] += 1
    else:
        st.session_state.cart[productId] = {"product": product, "quantity": 1}


#Explicando: @st.dialog cria uma janela flutuante (modal) por cima da loja para exibir e gerenciar o carrinho
@st.dialog("🛒 Seu Carrinho", width="large")
def showCartModal():
    cart = st.session_state.cart
    totalItems = getTotalCartItems()

    #Explicando: barra de progresso visual mostrando quantas das 15 unidades permitidas ja foram usadas
    st.caption(f"Capacidade do carrinho: **{totalItems} / {maxCartItems}** unidades")
    st.progress(min(totalItems / maxCartItems, 1.0))

    if not cart:
        st.info("Seu carrinho está vazio. Adicione produtos pelo catálogo!")
        return

    totalPrice = 0.0

    #Explicando: list(cart.items()) cria uma copia segura para permitir remover itens durante o loop sem erro
    for productId, itemData in list(cart.items()):
        product = itemData["product"]
        quantity = itemData["quantity"]
        subtotal = product.price * quantity
        totalPrice += subtotal

        with st.container(border=True):
            infoCol, minusCol, plusCol, removeCol = st.columns([5, 1, 1, 1])

            with infoCol:
                st.markdown(f"**{product.name}** ({product.specs})")
                st.caption(
                    f"Qtd: **{quantity}** (estoque máx: {product.stock}) • "
                    f"Unit: R$ {product.price:.2f} • Subtotal: **R$ {subtotal:.2f}**"
                )

            with minusCol:
                if st.button("➖", key=f"dec_{productId}", help="Remover 1 unidade"):
                    if quantity > 1:
                        cart[productId]["quantity"] -= 1
                    else:
                        del cart[productId]
                    #Explicando: so mantem a janela aberta se ainda sobrou algum produto no carrinho
                    st.session_state.reopenCart = getTotalCartItems() > 0
                    st.rerun()

            with plusCol:
                cannotAddMore = (quantity >= product.stock) or (totalItems >= maxCartItems)
                if st.button("➕", key=f"inc_{productId}", disabled=cannotAddMore, help="Adicionar 1 unidade"):
                    cart[productId]["quantity"] += 1
                    st.session_state.reopenCart = True
                    st.rerun()

            with removeCol:
                if st.button("🗑️", key=f"del_{productId}", help="Remover produto do carrinho"):
                    del cart[productId]
                    #Explicando: se removeu o ultimo item, fecha o modal e o botao volta a fugir
                    st.session_state.reopenCart = getTotalCartItems() > 0
                    st.rerun()

    st.divider()
    st.markdown(f"### Total no carrinho: R$ {totalPrice:.2f}")

    if totalItems >= maxCartItems:
        st.warning(f"Você atingiu o limite máximo de {maxCartItems} unidades no carrinho.")

    if st.button("🧹 Esvaziar carrinho", use_container_width=True):
        st.session_state.cart = {}
        st.session_state.reopenCart = False
        st.rerun()


# --- CABECALHO DA PAGINA ---
st.title("🛒 Catálogo de Eletrônicos Gamer")
st.caption("Busca otimizada por faixa de preço.")

# --- BARRA LATERAL (FILTROS) ---
st.sidebar.header("Filtros do Catálogo")

#Explicando: busca o maior preco atual na arvore para definir o limite maximo do slider
mostExpensiveInitial = catalog.findMax()
minLimit = 0.0
maxLimit = float(mostExpensiveInitial.price)

#Explicando: cria o controle deslizante com dois pontos (preco minimo e preco maximo)
minPrice, maxPrice = st.sidebar.slider(
    "Faixa de preço (R$)",
    min_value=minLimit,
    max_value=maxLimit,
    value=(minLimit, maxLimit),
    step=1.0
)

#Explicando: pega todas as categorias existentes na arvore sem repeticao usando set() e ordena de A a Z
allProducts = catalog.getAllInOrder()
categories = sorted(set(item.category for item in allProducts))

#Explicando: menu suspenso para filtrar opcionalmente por categoria (alem do preco)
selectedCategory = st.sidebar.selectbox(
    "Categoria",
    ["Todas"] + categories
)

# --- BUSCA NA BST E CALCULO DE EFICIENCIA ---
filteredProducts, visitedNodes = catalog.searchByPriceRange(minPrice, maxPrice)

if selectedCategory != "Todas":
    displayProducts = [item for item in filteredProducts if item.category == selectedCategory]
else:
    displayProducts = filteredProducts

cheapestProduct = catalog.findMin()
mostExpensiveProduct = catalog.findMax()
totalNodes = catalog.countNodes()
skippedNodes = totalNodes - visitedNodes
savedPercent = (skippedNodes / totalNodes) * 100 if totalNodes > 0 else 0

# --- PAINEL DE METRICAS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total na Árvore", f"{totalNodes} itens")
col2.metric("Mais Barato", f"R$ {cheapestProduct.price:.2f}", cheapestProduct.name, delta_color="off")
col3.metric("Mais Caro", f"R$ {mostExpensiveProduct.price:.2f}", mostExpensiveProduct.name, delta_color="off")
col4.metric("Nós Visitados", f"{visitedNodes} de {totalNodes}", f"{savedPercent:.2f}% pulados")

st.info(
    "**SEJA BEM-VINDO AO E-COMMERCE GAMES!**\n\n"
    "**Vamos dar o primeiro passo para aprimorar o seu setup gamer!**"
)

st.divider()

# --- VITRINE DE PRODUTOS ---
st.subheader(f"Produtos encontrados: {len(displayProducts)}")

totalCartItems = getTotalCartItems()

if not displayProducts:
    st.warning("Nenhum produto encontrado com os filtros selecionados.")
else:
    cardsPerRow = 3
    columns = st.columns(cardsPerRow)

    for index, product in enumerate(displayProducts):
        currentCol = columns[index % cardsPerRow]
        productId = id(product)
        qtyInCart = st.session_state.cart[productId]["quantity"] if productId in st.session_state.cart else 0
        remainingStock = product.stock - qtyInCart

        with currentCol:
            with st.container(border=True):
                st.caption(product.category)
                st.markdown(f"**{product.name}**")
                st.write(f"Especificação: {product.specs}")
                st.markdown(f"### R$ {product.price:.2f}")
                st.caption(f"Estoque disponível: {remainingStock} un. (total: {product.stock})")

                if qtyInCart > 0:
                    st.caption(f"🟢 No carrinho: {qtyInCart} un.")

                if remainingStock <= 0:
                    buttonLabel = "Limite de estoque atingido"
                    isDisabled = True
                elif totalCartItems >= maxCartItems:
                    buttonLabel = f"Carrinho cheio ({maxCartItems}/{maxCartItems})"
                    isDisabled = True
                else:
                    buttonLabel = "➕ Adicionar ao carrinho"
                    isDisabled = False

                st.button(
                    buttonLabel,
                    key=f"add_{productId}",
                    disabled=isDisabled,
                    use_container_width=True,
                    on_click=addToCart,
                    args=(product,)
                )

# --- BOTAO FLUTUANTE DO CARRINHO (CANTO INFERIOR DIREITO) ---
cartHelpText = "Adicione um produto primeiro!" if totalCartItems == 0 else "Abrir carrinho de compras"

if st.button(f"🛒 {totalCartItems}", key="floatingCartBtn", help=cartHelpText):
    if totalCartItems > 0:
        showCartModal()
elif st.session_state.reopenCart:
    st.session_state.reopenCart = False
    if totalCartItems > 0:
        showCartModal()

# --- SCRIPT DO BOTAO FUJAO (QUANDO CARRINHO VAZIO) ---
#Explicando: gera um codigo unico a cada atualizacao para o navegador sempre executar o script atualizado
scriptNonce = str(time.time_ns())

runawayScript = r"""
<!-- nonce: __NONCE__ | cartCount: __CART_COUNT__ -->
<script>
(function() {
    const parentWin = window.parent;
    const parentDoc = parentWin.document;

    function findCartBox() {
        const byKey = parentDoc.querySelector('.st-key-floatingCartBtn');
        if (byKey) return byKey;

        const buttons = parentDoc.querySelectorAll('button');
        for (const btn of buttons) {
            if (btn.textContent && btn.textContent.includes('🛒')) {
                return btn.closest('[data-testid="stElementContainer"]') || btn.parentElement;
            }
        }
        return null;
    }

    // Explicando: le o numero direto do botao na tela (ex: "🛒 0" -> 0) para nunca perder a sincronia
    function getCartCount(cartBox) {
        if (!cartBox) return -1;
        const btn = cartBox.querySelector('button') || cartBox;
        const match = (btn.textContent || "").match(/(\d+)/);
        return match ? parseInt(match[1], 10) : -1;
    }

    function moveCartAway(mouseX, mouseY) {
        const cartBox = findCartBox();
        if (!cartBox) return;

        if (parentWin.__cartReturnTimer) {
            clearTimeout(parentWin.__cartReturnTimer);
            parentWin.__cartReturnTimer = null;
        }

        // Explicando: pausa curta de 180ms para o botao deslizar suave sem tremer no lugar
        const now = Date.now();
        if (parentWin.__lastCartDodge && (now - parentWin.__lastCartDodge) < 180) {
            return;
        }
        parentWin.__lastCartDodge = now;

        const rect = cartBox.getBoundingClientRect();
        const btnW = rect.width || 76;
        const btnH = rect.height || 76;
        const winW = parentWin.innerWidth;
        const winH = parentWin.innerHeight;

        if (!cartBox.style.left || cartBox.style.left === 'auto') {
            cartBox.style.setProperty('position', 'fixed', 'important');
            cartBox.style.setProperty('left', Math.round(rect.left) + 'px', 'important');
            cartBox.style.setProperty('top', Math.round(rect.top) + 'px', 'important');
            cartBox.style.setProperty('right', 'auto', 'important');
            cartBox.style.setProperty('bottom', 'auto', 'important');
            void cartBox.offsetWidth;
        }

        const sidebar = parentDoc.querySelector('[data-testid="stSidebar"]');
        let minX = 24;
        if (sidebar) {
            const sbRect = sidebar.getBoundingClientRect();
            if (sbRect.right > 0 && sbRect.right < winW - 200) {
                minX = Math.round(sbRect.right) + 24;
            }
        }
        const maxX = Math.max(minX + 60, winW - btnW - 28);
        const minY = 80;
        const maxY = Math.max(minY + 60, winH - btnH - 28);

        let targetX = minX;
        let targetY = minY;
        let bestDist = -1;

        for (let i = 0; i < 20; i++) {
            const randX = minX + Math.random() * (maxX - minX);
            const randY = minY + Math.random() * (maxY - minY);
            const dist = Math.hypot((randX + btnW / 2) - mouseX, (randY + btnH / 2) - mouseY);
            if (dist > bestDist) {
                bestDist = dist;
                targetX = randX;
                targetY = randY;
            }
            if (dist > 240) break;
        }

        cartBox.style.setProperty('transition', 'left 0.22s ease-out, top 0.22s ease-out', 'important');
        cartBox.style.setProperty('left', Math.round(targetX) + 'px', 'important');
        cartBox.style.setProperty('top', Math.round(targetY) + 'px', 'important');
    }

    function returnCartHome() {
        const cartBox = findCartBox();
        if (!cartBox) return;

        if (cartBox.style.left && cartBox.style.left !== 'auto') {
            const winW = parentWin.innerWidth;
            const winH = parentWin.innerHeight;
            const rect = cartBox.getBoundingClientRect();
            const homeX = Math.round(winW - (rect.width || 76) - 28);
            const homeY = Math.round(winH - (rect.height || 76) - 28);

            cartBox.style.setProperty('transition', 'left 0.3s ease-out, top 0.3s ease-out', 'important');
            cartBox.style.setProperty('left', homeX + 'px', 'important');
            cartBox.style.setProperty('top', homeY + 'px', 'important');

            parentWin.__cartReturnTimer = setTimeout(() => {
                const box = findCartBox();
                if (box && getCartCount(box) > 0) {
                    box.style.removeProperty('left');
                    box.style.removeProperty('top');
                    box.style.removeProperty('right');
                    box.style.removeProperty('bottom');
                    box.style.removeProperty('transition');
                }
            }, 320);
        }
    }

    if (__CART_COUNT__ > 0) {
        returnCartHome();
        setTimeout(returnCartHome, 120);
    }

    const onMouseMove = function(e) {
        // Explicando: so pausa se o modal do carrinho estiver realmente visivel na tela
        const dialog = parentDoc.querySelector('[data-testid="stDialog"]');
        if (dialog && dialog.offsetParent !== null) return;

        const cartBox = findCartBox();
        if (!cartBox || getCartCount(cartBox) !== 0) return;

        const rect = cartBox.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        const distance = Math.hypot(e.clientX - centerX, e.clientY - centerY);

        if (distance < 85) {
            moveCartAway(e.clientX, e.clientY);
        }
    };

    const onMouseDown = function(e) {
        const cartBox = findCartBox();
        if (!cartBox || getCartCount(cartBox) !== 0) return;

        if (cartBox.contains(e.target)) {
            e.preventDefault();
            e.stopPropagation();
            moveCartAway(e.clientX, e.clientY);
        }
    };

    // Explicando: remove os sensores do iframe antigo (que foi destruido pelo Streamlit) e cadastra os novos
    parentWin.__cartRunawayHandlers = null;
    try {
        if (parentWin.__cartMouseMoveFn) {
            parentDoc.removeEventListener('mousemove', parentWin.__cartMouseMoveFn, true);
        }
        if (parentWin.__cartMouseDownFn) {
            parentDoc.removeEventListener('mousedown', parentWin.__cartMouseDownFn, true);
        }
    } catch (err) {}

    parentWin.__cartMouseMoveFn = onMouseMove;
    parentWin.__cartMouseDownFn = onMouseDown;
    parentDoc.addEventListener('mousemove', onMouseMove, true);
    parentDoc.addEventListener('mousedown', onMouseDown, true);
})();
</script>
""".replace("__NONCE__", scriptNonce).replace("__CART_COUNT__", str(totalCartItems))

#Explicando: renderiza o script sem ocupar espaco visivel na tela
components.html(runawayScript, height=0)