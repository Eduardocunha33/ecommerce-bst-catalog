import os
import time
import streamlit as st
import streamlit.components.v1 as components
from tree import BinaryTree
from catalogData import loadCatalog

#Explicando: configura o titulo da aba do navegador e deixa a pagina no modo largo (wide)
st.set_page_config(page_title="E-commerce Gamer", layout="wide")

#Explicando: define o limite maximo de unidades permitidas no carrinho do cliente
maxCartItems = 15


def formatPrice(value):
    #Explicando: formata o valor no padrao brasileiro (ex: 7399.0 -> R$ 7.399,00)
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


#Explicando: injeta fonte gamer (Orbitron) e CSS completo (vitrine, sidebar e modal do carrinho) adaptado para tema claro e escuro
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;700;800&display=swap');

        /* --- BARRA LATERAL (FILTROS) --- */
        [data-testid="stSidebar"] {
            border-right: 1.5px solid rgba(168, 85, 247, 0.35) !important;
            background-image: linear-gradient(180deg, rgba(168, 85, 247, 0.06) 0%, rgba(16, 185, 129, 0.04) 100%) !important;
        }

        .sidebar-header {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 14px;
            border-radius: 14px;
            border: 1.5px solid rgba(168, 85, 247, 0.45);
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.12), rgba(168, 85, 247, 0.12));
            margin-bottom: 18px;
            transition: transform 0.24s ease, border-color 0.24s ease, box-shadow 0.24s ease;
        }

        .sidebar-header:hover {
            transform: translateY(-2px);
            border-color: #10b981;
            box-shadow: 0 6px 18px rgba(16, 185, 129, 0.18);
        }

        .sidebar-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 38px;
            height: 38px;
            border-radius: 10px;
            background: rgba(16, 185, 129, 0.16);
            border: 1.2px solid rgba(16, 185, 129, 0.55);
            color: #10b981;
            flex-shrink: 0;
            transition: transform 0.24s cubic-bezier(0.22, 1, 0.36, 1);
        }

        .sidebar-header:hover .sidebar-icon {
            transform: scale(1.14);
        }

        .sidebar-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 0.98rem;
            font-weight: 800;
            letter-spacing: 0.6px;
            background: linear-gradient(90deg, #10b981, #a855f7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            line-height: 1.2;
        }

        .sidebar-subtitle {
            font-size: 0.74rem;
            color: var(--text-color);
            opacity: 0.7;
            margin-top: 2px;
        }

        /* Explicando: estiliza os pinos e numeros do slider da barra lateral em verde neon */
        [data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] {
            background-color: #10b981 !important;
            border: 2px solid #ffffff !important;
            box-shadow: 0 0 10px rgba(16, 185, 129, 0.65) !important;
            transition: transform 0.2s ease !important;
        }

        [data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"]:hover {
            transform: scale(1.22) !important;
        }

        [data-testid="stSidebar"] [data-testid="stSliderThumbValue"] {
            color: #10b981 !important;
            font-weight: 700 !important;
        }

        /* Explicando: caixa do filtro de categoria com borda roxa e destaque verde no hover */
        [data-testid="stSidebar"] [data-baseweb="select"] > div {
            border-radius: 10px !important;
            border: 1.5px solid rgba(168, 85, 247, 0.45) !important;
            transition: border-color 0.22s ease, box-shadow 0.22s ease !important;
        }

        [data-testid="stSidebar"] [data-baseweb="select"] > div:hover {
            border-color: #10b981 !important;
            box-shadow: 0 0 12px rgba(16, 185, 129, 0.20) !important;
        }

        /* Card de resumo da busca na barra lateral */
        .sidebar-summary-card {
            margin-top: 14px;
            margin-bottom: 14px;
            padding: 14px 16px;
            border-radius: 14px;
            border: 1.5px solid rgba(16, 185, 129, 0.45);
            background: linear-gradient(155deg, rgba(16, 185, 129, 0.09), rgba(168, 85, 247, 0.07));
            transition: transform 0.24s ease, box-shadow 0.24s ease;
        }

        .sidebar-summary-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(16, 185, 129, 0.16);
        }

        .sidebar-summary-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 0.76rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: #10b981;
            margin-bottom: 10px;
        }

        .sidebar-stat-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.82rem;
            padding: 5px 0;
            border-bottom: 1px solid rgba(148, 163, 184, 0.18);
            color: var(--text-color);
        }

        .sidebar-stat-row:last-child {
            border-bottom: none;
            padding-bottom: 0;
        }

        .sidebar-stat-label {
            opacity: 0.72;
        }

        .sidebar-stat-val {
            font-weight: 700;
        }

        .sidebar-stat-green {
            color: #10b981;
            font-weight: 700;
        }

        .sidebar-stat-purple {
            color: #a855f7;
            font-weight: 700;
        }

        /* Botao de limpar filtros na barra lateral */
        .st-key-resetFiltersBtn button {
            border-radius: 10px !important;
            border: 1.5px solid rgba(168, 85, 247, 0.5) !important;
            background: linear-gradient(90deg, rgba(168, 85, 247, 0.14), rgba(16, 185, 129, 0.12)) !important;
            font-weight: 600 !important;
            transition: transform 0.22s ease, border-color 0.22s ease, box-shadow 0.22s ease !important;
        }

        .st-key-resetFiltersBtn button:hover:not(:disabled) {
            transform: scale(1.03) !important;
            border-color: #10b981 !important;
            box-shadow: 0 4px 14px rgba(16, 185, 129, 0.25) !important;
        }

        /* --- CABECALHO GAMER --- */
        .hero-header {
            display: flex;
            align-items: center;
            gap: 16px;
            margin-bottom: 4px;
        }

        .hero-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 54px;
            height: 54px;
            border-radius: 14px;
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.18), rgba(168, 85, 247, 0.18));
            border: 1.5px solid rgba(16, 185, 129, 0.6);
            box-shadow: 0 0 18px rgba(16, 185, 129, 0.25);
            color: #10b981;
            flex-shrink: 0;
            transition: transform 0.25s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.25s ease;
        }

        .hero-icon:hover {
            transform: scale(1.14);
            box-shadow: 0 0 26px rgba(16, 185, 129, 0.45);
        }

        .glow-title {
            font-family: 'Orbitron', sans-serif !important;
            font-size: clamp(1.7rem, 3vw, 2.55rem) !important;
            font-weight: 800 !important;
            letter-spacing: 1px;
            background: linear-gradient(90deg, #10b981 0%, #06b6d4 45%, #c026d3 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0 !important;
            line-height: 1.15 !important;
        }

        .sub-glow {
            color: var(--text-color);
            opacity: 0.72;
            font-size: 1.02rem;
            margin: 6px 0 22px 0;
        }

        /* --- CARDS DE METRICAS NEON (TOPO) --- */
        .metric-card {
            position: relative;
            min-height: 138px;
            padding: 18px 20px;
            border-radius: 16px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            backdrop-filter: blur(8px);
            transition: transform 0.26s cubic-bezier(0.22, 1, 0.36, 1),
                        box-shadow 0.26s ease,
                        border-color 0.26s ease;
        }

        .metric-green {
            border: 1.8px solid rgba(16, 185, 129, 0.65);
            background: linear-gradient(145deg, rgba(16, 185, 129, 0.10), rgba(16, 185, 129, 0.02));
            box-shadow: 0 4px 18px rgba(16, 185, 129, 0.14);
        }

        .metric-purple {
            border: 1.8px solid rgba(168, 85, 247, 0.65);
            background: linear-gradient(145deg, rgba(168, 85, 247, 0.11), rgba(192, 38, 211, 0.02));
            box-shadow: 0 4px 18px rgba(168, 85, 247, 0.16);
        }

        .metric-card:hover {
            transform: translateY(-5px) scale(1.025);
        }

        .metric-green:hover {
            border-color: #10b981;
            box-shadow: 0 10px 28px rgba(16, 185, 129, 0.28);
        }

        .metric-purple:hover {
            border-color: #c026d3;
            box-shadow: 0 10px 28px rgba(192, 38, 211, 0.28);
        }

        .metric-top {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 10px;
        }

        .metric-label {
            font-size: 0.84rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: var(--text-color);
            opacity: 0.72;
        }

        .metric-value {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.65rem;
            font-weight: 800;
            margin: 6px 0;
            color: var(--text-color);
            line-height: 1.2;
        }

        .metric-value-green {
            color: #10b981;
        }

        .metric-value-purple {
            color: #c026d3;
        }

        .metric-sub {
            font-size: 0.82rem;
            color: var(--text-color);
            opacity: 0.82;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .metric-pill {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 700;
            background: rgba(16, 185, 129, 0.20);
            color: #10b981;
            border: 1px solid rgba(16, 185, 129, 0.45);
        }

        .metric-icon {
            color: #10b981;
            opacity: 0.85;
            flex-shrink: 0;
            transition: transform 0.26s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.26s ease;
        }

        .metric-purple .metric-icon {
            color: #c026d3;
        }

        .metric-card:hover .metric-icon {
            transform: scale(1.18);
            opacity: 1;
        }

        /* --- BANNER CYBER DE BOAS-VINDAS --- */
        .welcome-banner {
            margin: 18px 0 8px 0;
            padding: 16px 22px;
            border-radius: 14px;
            border: 1.5px solid rgba(6, 182, 212, 0.45);
            border-left: 5px solid #10b981;
            background: linear-gradient(90deg, rgba(16, 185, 129, 0.10) 0%, rgba(6, 182, 212, 0.08) 55%, rgba(168, 85, 247, 0.10) 100%);
            box-shadow: 0 4px 16px rgba(6, 182, 212, 0.10);
            transition: transform 0.25s ease, box-shadow 0.25s ease;
        }

        .welcome-banner:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 22px rgba(16, 185, 129, 0.18);
        }

        .welcome-banner-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 0.95rem;
            font-weight: 700;
            color: #10b981;
            letter-spacing: 0.6px;
            margin-bottom: 4px;
        }

        .welcome-banner-text {
            font-size: 0.95rem;
            font-weight: 500;
            color: var(--text-color);
            opacity: 0.9;
        }

        /* --- CARDS DOS PRODUTOS --- */
        div[class*="st-key-productCard_"] {
            border: 1.6px solid rgba(168, 85, 247, 0.42) !important;
            border-radius: 16px !important;
            background: linear-gradient(155deg, rgba(168, 85, 247, 0.08) 0%, rgba(16, 185, 129, 0.04) 100%) !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12) !important;
            transition: transform 0.26s cubic-bezier(0.22, 1, 0.36, 1),
                        border-color 0.26s ease,
                        box-shadow 0.26s ease !important;
            margin-bottom: 14px !important;
        }

        div[class*="st-key-productCard_"]:hover {
            transform: translateY(-6px) scale(1.02) !important;
            border-color: #10b981 !important;
            box-shadow: 0 12px 28px rgba(16, 185, 129, 0.22), 0 0 16px rgba(168, 85, 247, 0.20) !important;
        }

        .prod-category {
            display: inline-block;
            font-size: 0.72rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #a855f7;
            margin-bottom: 4px;
        }

        .prod-name {
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--text-color);
            line-height: 1.25;
            min-height: 2.6em;
            margin-bottom: 6px;
        }

        .prod-spec-row {
            font-size: 0.82rem;
            color: var(--text-color);
            opacity: 0.85;
            margin-bottom: 10px;
        }

        .prod-spec-pill {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 6px;
            font-size: 0.78rem;
            font-weight: 600;
            background: rgba(148, 163, 184, 0.18);
            border: 1px solid rgba(148, 163, 184, 0.3);
            color: var(--text-color);
        }

        .prod-price {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.32rem;
            font-weight: 800;
            color: #10b981;
            margin: 6px 0 8px 0;
        }

        .prod-meta-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 6px;
            min-height: 26px;
            margin-bottom: 6px;
        }

        .prod-stock {
            font-size: 0.78rem;
            color: var(--text-color);
            opacity: 0.7;
        }

        .prod-cart-badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 999px;
            font-size: 0.74rem;
            font-weight: 700;
            background: rgba(16, 185, 129, 0.18);
            border: 1px solid rgba(16, 185, 129, 0.5);
            color: #10b981;
        }

        /* --- FOTOS DOS PRODUTOS COM ZOOM NO HOVER --- */
        /* Explicando: oculta o botao nativo de tela cheia das fotos para nao conflitar com o zoom do card */
     div[class*="st-key-productCard_"] [data-testid="stFullScreenFrame"] button,
     div[class*="st-key-productCard_"] [data-testid="stElementToolbar"],
     div[class*="st-key-cartItem_"] [data-testid="stFullScreenFrame"] button,
     div[class*="st-key-cartItem_"] [data-testid="stElementToolbar"] {
         display: none !important;
     }
        div[class*="st-key-productCard_"] [data-testid="stImage"] img {
            height: 138px !important;
            width: 100% !important;
            object-fit: contain !important;
            background-color: #ffffff !important;
            border-radius: 12px !important;
            padding: 8px !important;
            border: 1.5px solid rgba(168, 85, 247, 0.25) !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12) !important;
            transition: transform 0.28s cubic-bezier(0.22, 1, 0.36, 1),
                        border-color 0.28s ease,
                        box-shadow 0.28s ease !important;
        }

        div[class*="st-key-productCard_"]:hover [data-testid="stImage"] img {
            transform: scale(1.07) !important;
            border-color: #10b981 !important;
            box-shadow: 0 8px 20px rgba(16, 185, 129, 0.25) !important;
        }

        div[class*="st-key-productCard_"] [data-testid="stImage"] img:hover {
            transform: scale(1.11) !important;
        }

        .img-placeholder {
            height: 138px;
            width: 100%;
            border: 2px dashed rgba(168, 85, 247, 0.45);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            color: var(--text-color);
            opacity: 0.65;
            font-size: 13px;
            background-color: rgba(148, 163, 184, 0.08);
            transition: transform 0.28s ease, border-color 0.28s ease;
        }

        div[class*="st-key-productCard_"]:hover .img-placeholder {
            transform: scale(1.06);
            border-color: #10b981;
        }

        /* --- BOTOES DENTRO DOS CARDS --- */
        /* --- BOTOES DENTRO DOS CARDS --- */
     div[class*="st-key-add_"] button {
         border-radius: 10px !important;
         border: 1.5px solid rgba(168, 85, 247, 0.5) !important;
         background: linear-gradient(90deg, rgba(16, 185, 129, 0.12), rgba(168, 85, 247, 0.14)) !important;
         font-weight: 600 !important;
         transition: transform 0.22s cubic-bezier(0.22, 1, 0.36, 1),
                     border-color 0.22s ease,
                     box-shadow 0.22s ease,
                     background 0.22s ease !important;
     }

     div[class*="st-key-add_"] button:hover:not(:disabled) {
         transform: scale(1.03) !important;
         border-color: #10b981 !important;
         background: linear-gradient(90deg, rgba(16, 185, 129, 0.26), rgba(168, 85, 247, 0.24)) !important;
         box-shadow: 0 4px 14px rgba(16, 185, 129, 0.25) !important;
     }

        /* --- MODAL DO CARRINHO (ESTILO GAMER NEON) --- */
        div[role="dialog"] {
            border: 1.8px solid rgba(168, 85, 247, 0.60) !important;
            border-radius: 18px !important;
            box-shadow: 0 14px 44px rgba(16, 185, 129, 0.18), 0 0 32px rgba(168, 85, 247, 0.24) !important;
        }

        div[role="dialog"] header {
            border-bottom: 1px solid rgba(168, 85, 247, 0.28) !important;
        }

        .cart-modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }

        .cart-modal-label {
            font-size: 0.88rem;
            color: var(--text-color);
            opacity: 0.85;
        }

        .cart-modal-count {
            font-family: 'Orbitron', sans-serif;
            font-size: 0.85rem;
            font-weight: 700;
            color: #10b981;
            padding: 3px 10px;
            border-radius: 999px;
            background: rgba(16, 185, 129, 0.15);
            border: 1px solid rgba(16, 185, 129, 0.45);
        }

        /* Barra de capacidade neon do carrinho */
        .cart-progress-track {
            width: 100%;
            height: 10px;
            border-radius: 999px;
            background: rgba(148, 163, 184, 0.22);
            overflow: hidden;
            margin-bottom: 18px;
            border: 1px solid rgba(168, 85, 247, 0.28);
        }

        .cart-progress-fill {
            height: 100%;
            border-radius: 999px;
            background: linear-gradient(90deg, #10b981 0%, #06b6d4 55%, #a855f7 100%);
            box-shadow: 0 0 12px rgba(16, 185, 129, 0.55);
            transition: width 0.3s ease;
        }

        /* Cards de cada item dentro do modal do carrinho */
        div[class*="st-key-cartItem_"] {
            border: 1.4px solid rgba(168, 85, 247, 0.38) !important;
            border-radius: 14px !important;
            background: linear-gradient(135deg, rgba(168, 85, 247, 0.08), rgba(16, 185, 129, 0.04)) !important;
            transition: transform 0.22s ease, border-color 0.22s ease, box-shadow 0.22s ease !important;
            margin-bottom: 10px !important;
        }

        div[class*="st-key-cartItem_"]:hover {
            transform: translateY(-2px) !important;
            border-color: #10b981 !important;
            box-shadow: 0 6px 18px rgba(16, 185, 129, 0.16) !important;
        }

        /* Miniatura da foto dentro do carrinho */
        div[class*="st-key-cartItem_"] [data-testid="stImage"] img {
            height: 66px !important;
            width: 66px !important;
            object-fit: contain !important;
            background-color: #ffffff !important;
            border-radius: 10px !important;
            padding: 4px !important;
            border: 1.2px solid rgba(168, 85, 247, 0.35) !important;
            transition: transform 0.24s ease !important;
        }

        div[class*="st-key-cartItem_"]:hover [data-testid="stImage"] img {
            transform: scale(1.1) !important;
        }

        .cart-thumb-placeholder {
            height: 66px;
            width: 66px;
            border-radius: 10px;
            border: 1.5px dashed rgba(168, 85, 247, 0.45);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            background: rgba(148, 163, 184, 0.10);
        }

        .cart-item-title {
            font-size: 0.98rem;
            font-weight: 700;
            color: var(--text-color);
            margin-bottom: 4px;
        }

        .cart-item-meta {
            font-size: 0.80rem;
            color: var(--text-color);
            opacity: 0.78;
        }

        .cart-item-subtotal {
            font-family: 'Orbitron', sans-serif;
            color: #10b981;
            font-weight: 700;
            font-size: 0.86rem;
        }

        /* Botoes -, + e lixeira dentro do carrinho com zoom e destaque */
        div[class*="st-key-dec_"] button,
        div[class*="st-key-inc_"] button,
        div[class*="st-key-del_"] button {
            border-radius: 10px !important;
            border: 1.4px solid rgba(168, 85, 247, 0.45) !important;
            background: rgba(168, 85, 247, 0.08) !important;
            transition: transform 0.2s cubic-bezier(0.22, 1, 0.36, 1),
                        border-color 0.2s ease,
                        box-shadow 0.2s ease,
                        background 0.2s ease !important;
        }

        div[class*="st-key-dec_"] button:hover:not(:disabled) {
            transform: scale(1.12) !important;
            border-color: #a855f7 !important;
            box-shadow: 0 0 12px rgba(168, 85, 247, 0.35) !important;
        }

        div[class*="st-key-inc_"] button:hover:not(:disabled) {
            transform: scale(1.12) !important;
            border-color: #10b981 !important;
            background: rgba(16, 185, 129, 0.18) !important;
            box-shadow: 0 0 12px rgba(16, 185, 129, 0.38) !important;
        }

        div[class*="st-key-del_"] button:hover:not(:disabled) {
            transform: scale(1.12) !important;
            border-color: #ef4444 !important;
            background: rgba(239, 68, 68, 0.16) !important;
            box-shadow: 0 0 12px rgba(239, 68, 68, 0.35) !important;
        }

        /* Bloco do total no rodape do carrinho */
        .cart-total-box {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 14px 18px;
            margin: 14px 0 16px 0;
            border-radius: 14px;
            border: 1.5px solid rgba(16, 185, 129, 0.50);
            background: linear-gradient(90deg, rgba(16, 185, 129, 0.12), rgba(168, 85, 247, 0.10));
        }

        .cart-total-label {
            font-size: 0.92rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            color: var(--text-color);
            opacity: 0.85;
        }

        .cart-total-sub {
            font-size: 0.78rem;
            color: var(--text-color);
            opacity: 0.68;
        }

        .cart-total-value {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.45rem;
            font-weight: 800;
            color: #10b981;
        }

        /* Botao Esvaziar carrinho */
        .st-key-clearCartBtn button {
            border-radius: 12px !important;
            border: 1.5px solid rgba(148, 163, 184, 0.45) !important;
            background: rgba(148, 163, 184, 0.08) !important;
            font-weight: 600 !important;
            transition: transform 0.22s ease, border-color 0.22s ease, box-shadow 0.22s ease, background 0.22s ease !important;
        }

        .st-key-clearCartBtn button:hover {
            transform: scale(1.03) !important;
            border-color: #ef4444 !important;
            background: rgba(239, 68, 68, 0.14) !important;
            box-shadow: 0 4px 16px rgba(239, 68, 68, 0.22) !important;
        }

        /* Botao Prosseguir pagamento em degradê verde neon */
        .st-key-payCartBtn button {
            border-radius: 12px !important;
            border: 1.5px solid #34d399 !important;
            background: linear-gradient(90deg, #16a34a 0%, #10b981 55%, #06b6d4 100%) !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            box-shadow: 0 6px 20px rgba(16, 185, 129, 0.35) !important;
            transition: transform 0.22s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.22s ease !important;
        }

        .st-key-payCartBtn button:hover {
            transform: scale(1.03) !important;
            box-shadow: 0 8px 26px rgba(16, 185, 129, 0.55) !important;
            color: #ffffff !important;
        }

        /* --- BOTAO FLUTUANTE DO CARRINHO (CANTO INFERIOR DIREITO) --- */
        .st-key-floatingCartBtn {
            position: fixed !important;
            bottom: 28px !important;
            right: 28px !important;
            z-index: 9999 !important;
            width: 76px !important;
            height: 76px !important;
        }

        .st-key-floatingCartBtn button {
            width: 76px !important;
            height: 76px !important;
            border-radius: 50% !important;
            background: linear-gradient(135deg, #16a34a, #10b981) !important;
            color: #ffffff !important;
            border: 3px solid #86efac !important;
            box-shadow: 0 6px 22px rgba(16, 185, 129, 0.50) !important;
            padding: 0 !important;
            transition: transform 0.24s cubic-bezier(0.22, 1, 0.36, 1),
                        box-shadow 0.24s ease,
                        border-color 0.24s ease !important;
        }

        .st-key-floatingCartBtn button:hover {
            border-color: #ffffff !important;
            transform: scale(1.12) !important;
            box-shadow: 0 10px 30px rgba(16, 185, 129, 0.70) !important;
            color: #ffffff !important;
        }

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


# --- FUNCOES AUXILIARES DO CARRINHO E FILTROS ---
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


def resetFilters(minLim, maxLim):
    #Explicando: restaura a faixa de preco e a categoria para os valores iniciais
    st.session_state.priceRangeFilter = (minLim, maxLim)
    st.session_state.categoryFilter = "Todas"


#Explicando: @st.dialog cria uma janela flutuante (modal) por cima da loja para exibir e gerenciar o carrinho
@st.dialog("🛒 Seu Carrinho Gamer", width="large")
def showCartModal():
    cart = st.session_state.cart
    totalItems = getTotalCartItems()
    fillPercent = min((totalItems / maxCartItems) * 100, 100)

    #Explicando: barra de progresso customizada em degrade neon para indicar a lotacao do carrinho
    st.markdown(
        f"""
<div class="cart-modal-header">
  <span class="cart-modal-label">Capacidade do carrinho</span>
  <span class="cart-modal-count">{totalItems} / {maxCartItems} unidades</span>
</div>
<div class="cart-progress-track">
  <div class="cart-progress-fill" style="width: {fillPercent:.1f}%;"></div>
</div>
""",
        unsafe_allow_html=True
    )

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

        with st.container(border=True, key=f"cartItem_{productId}"):
            thumbCol, infoCol, minusCol, plusCol, removeCol = st.columns(
                [1.1, 4.4, 0.85, 0.85, 0.85],
                vertical_alignment="center"
            )

            with thumbCol:
                #Explicando: exibe a miniatura da foto do produto tambem dentro do carrinho
                imagePath = getattr(product, "image", "").strip()
                isWebUrl = imagePath.startswith("http://") or imagePath.startswith("https://")
                isLocalFile = imagePath != "" and os.path.exists(imagePath)

                if isWebUrl or isLocalFile:
                    st.image(imagePath, width=66)
                else:
                    st.markdown('<div class="cart-thumb-placeholder">🎮</div>', unsafe_allow_html=True)

            with infoCol:
                st.markdown(
                    f"""
<div class="cart-item-title">{product.name} <span class="prod-spec-pill">{product.specs}</span></div>
<div class="cart-item-meta">
  Qtd: <b>{quantity}</b> (máx: {product.stock}) &bull; Unit: {formatPrice(product.price)} &bull;
  Subtotal: <span class="cart-item-subtotal">{formatPrice(subtotal)}</span>
</div>
""",
                    unsafe_allow_html=True
                )

            with minusCol:
                if st.button("➖", key=f"dec_{productId}", help="Remover 1 unidade", use_container_width=True):
                    if quantity > 1:
                        cart[productId]["quantity"] -= 1
                    else:
                        del cart[productId]
                    #Explicando: so mantem a janela aberta se ainda sobrou algum produto no carrinho
                    st.session_state.reopenCart = getTotalCartItems() > 0
                    st.rerun()

            with plusCol:
                cannotAddMore = (quantity >= product.stock) or (totalItems >= maxCartItems)
                if st.button("➕", key=f"inc_{productId}", disabled=cannotAddMore, help="Adicionar 1 unidade", use_container_width=True):
                    cart[productId]["quantity"] += 1
                    st.session_state.reopenCart = True
                    st.rerun()

            with removeCol:
                if st.button("🗑️", key=f"del_{productId}", help="Remover produto do carrinho", use_container_width=True):
                    del cart[productId]
                    #Explicando: se removeu o ultimo item, fecha o modal e o botao volta a fugir
                    st.session_state.reopenCart = getTotalCartItems() > 0
                    st.rerun()

    #Explicando: caixa estilizada destacando o resumo de itens e o valor total da compra
    st.markdown(
        f"""
<div class="cart-total-box">
  <div>
    <div class="cart-total-label">Total no carrinho</div>
    <div class="cart-total-sub">{totalItems} {"unidade selecionada" if totalItems == 1 else "unidades selecionadas"}</div>
  </div>
  <div class="cart-total-value">{formatPrice(totalPrice)}</div>
</div>
""",
        unsafe_allow_html=True
    )

    if totalItems >= maxCartItems:
        st.warning(f"Você atingiu o limite máximo de {maxCartItems} unidades no carrinho.")

    #Explicando: coloca os botoes de acao lado a lado com estilos proprios (chaves clearCartBtn e payCartBtn)
    clearCol, payCol = st.columns(2)
    proceedPayment = False

    with clearCol:
        if st.button("🧹 Esvaziar carrinho", key="clearCartBtn", use_container_width=True):
            st.session_state.cart = {}
            st.session_state.reopenCart = False
            st.rerun()

    with payCol:
        proceedPayment = st.button("💳 Prosseguir pagamento", key="payCartBtn", use_container_width=True)

    if proceedPayment:
        st.info("💳 Ambiente demonstrativo: a etapa de pagamento não está ativa nesta versão.")


# --- CABECALHO DA PAGINA ---
st.markdown(
    """
<div class="hero-header">
  <div class="hero-icon" title="E-commerce Gamer ">
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="9" cy="21" r="1"></circle>
      <circle cx="20" cy="21" r="1"></circle>
      <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
    </svg>
  </div>
  <h1 class="glow-title">CATÁLOGO DE ELETRÔNICOS GAMER</h1>
</div>
<p class="sub-glow">Loja gamer</p>
""",
    unsafe_allow_html=True
)

# --- BARRA LATERAL (FILTROS ESTILIZADOS) ---
st.sidebar.markdown(
    """
<div class="sidebar-header">
  <div class="sidebar-icon">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
      <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon>
    </svg>
  </div>
  <div>
    <div class="sidebar-title">FILTROS</div>
    <div class="sidebar-subtitle">Busca rápida na BST</div>
  </div>
</div>
""",
    unsafe_allow_html=True
)

#Explicando: busca o maior preco atual na arvore para definir o limite maximo do slider
mostExpensiveInitial = catalog.findMax()
minLimit = 0.0
maxLimit = float(mostExpensiveInitial.price)

#Explicando: inicializa os filtros no session_state para permitir o botao de limpar filtros funcionar sem erro
if "priceRangeFilter" not in st.session_state:
    st.session_state.priceRangeFilter = (minLimit, maxLimit)
if "categoryFilter" not in st.session_state:
    st.session_state.categoryFilter = "Todas"

minPrice, maxPrice = st.sidebar.slider(
    "Faixa de preço (R$)",
    min_value=minLimit,
    max_value=maxLimit,
    step=1.0,
    key="priceRangeFilter"
)

#Explicando: pega todas as categorias existentes na arvore sem repeticao usando set() e ordena de A a Z
allProducts = catalog.getAllInOrder()
categories = sorted(set(item.category for item in allProducts))

selectedCategory = st.sidebar.selectbox(
    "Categoria",
    ["Todas"] + categories,
    key="categoryFilter"
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

#Explicando: exibe um resumo visual dos filtros ativos e da economia da arvore dentro da barra lateral
st.sidebar.markdown(
    f"""
<div class="sidebar-summary-card">
  <div class="sidebar-summary-title">Resumo da Busca</div>
  <div class="sidebar-stat-row">
    <span class="sidebar-stat-label">Mínimo</span>
    <span class="sidebar-stat-green">{formatPrice(minPrice)}</span>
  </div>
  <div class="sidebar-stat-row">
    <span class="sidebar-stat-label">Máximo</span>
    <span class="sidebar-stat-purple">{formatPrice(maxPrice)}</span>
  </div>
  <div class="sidebar-stat-row">
    <span class="sidebar-stat-label">Categoria</span>
    <span class="sidebar-stat-val">{selectedCategory}</span>
  </div>
  <div class="sidebar-stat-row">
    <span class="sidebar-stat-label">Encontrados</span>
    <span class="sidebar-stat-val">{len(displayProducts)} itens</span>
  </div>
  <div class="sidebar-stat-row">
    <span class="sidebar-stat-label">Galhos pulados</span>
    <span class="sidebar-stat-green">{savedPercent:.2f}%</span>
  </div>
</div>
""",
    unsafe_allow_html=True
)

#Explicando: so ativa o botao de limpar filtros se o usuario realmente alterou o preco ou a categoria
hasActiveFilter = (minPrice > minLimit) or (maxPrice < maxLimit) or (selectedCategory != "Todas")
st.sidebar.button(
    "🔄 Limpar filtros",
    key="resetFiltersBtn",
    disabled=not hasActiveFilter,
    use_container_width=True,
    on_click=resetFilters,
    args=(minLimit, maxLimit)
)

# --- PAINEL DE METRICAS NEON ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
<div class="metric-card metric-green">
  <div class="metric-top">
    <div>
      <div class="metric-label">Total na Árvore</div>
      <div class="metric-value">{totalNodes} itens</div>
    </div>
    <div class="metric-icon">
      <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
        <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
        <line x1="12" y1="22.08" x2="12" y2="12"></line>
      </svg>
    </div>
  </div>
  <div class="metric-sub">Catálogo organizado em BST</div>
</div>
""",
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
<div class="metric-card metric-green">
  <div class="metric-top">
    <div>
      <div class="metric-label">Mais Barato</div>
      <div class="metric-value metric-value-green">{formatPrice(cheapestProduct.price)}</div>
    </div>
    <div class="metric-icon">
      <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="23 18 13.5 8.5 8.5 13.5 1 6"></polyline>
        <polyline points="17 18 23 18 23 12"></polyline>
      </svg>
    </div>
  </div>
  <div class="metric-sub" title="{cheapestProduct.name}">↘ {cheapestProduct.name}</div>
</div>
""",
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
<div class="metric-card metric-purple">
  <div class="metric-top">
    <div>
      <div class="metric-label">Mais Caro</div>
      <div class="metric-value metric-value-purple">{formatPrice(mostExpensiveProduct.price)}</div>
    </div>
    <div class="metric-icon">
      <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline>
        <polyline points="17 6 23 6 23 12"></polyline>
      </svg>
    </div>
  </div>
  <div class="metric-sub" title="{mostExpensiveProduct.name}">↗ {mostExpensiveProduct.name}</div>
</div>
""",
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
<div class="metric-card metric-green">
  <div class="metric-top">
    <div>
      <div class="metric-label">Nós Visitados</div>
      <div class="metric-value">{visitedNodes} de {totalNodes}</div>
    </div>
    <div class="metric-icon">
      <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="5" r="2.2"></circle>
        <circle cx="6" cy="12" r="2.2"></circle>
        <circle cx="18" cy="12" r="2.2"></circle>
        <circle cx="3" cy="19" r="2"></circle>
        <circle cx="9" cy="19" r="2"></circle>
        <circle cx="15" cy="19" r="2"></circle>
        <circle cx="21" cy="19" r="2"></circle>
        <line x1="10.6" y1="6.7" x2="7.4" y2="10.3"></line>
        <line x1="13.4" y1="6.7" x2="16.6" y2="10.3"></line>
        <line x1="5" y1="14" x2="3.8" y2="17.2"></line>
        <line x1="7" y1="14" x2="8.2" y2="17.2"></line>
        <line x1="17" y1="14" x2="15.8" y2="17.2"></line>
        <line x1="19" y1="14" x2="20.2" y2="17.2"></line>
      </svg>
    </div>
  </div>
  <div><span class="metric-pill">↑ {savedPercent:.2f}% pulados</span></div>
</div>
""",
        unsafe_allow_html=True
    )

st.markdown(
    """
<div class="welcome-banner">
  <div class="welcome-banner-title">SEJA BEM-VINDO AO E-COMMERCE GAMES!</div>
  <div class="welcome-banner-text">Vamos dar o primeiro passo para aprimorar o seu setup gamer!</div>
</div>
""",
    unsafe_allow_html=True
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
            with st.container(border=True, key=f"productCard_{productId}"):
                infoCol, imgCol = st.columns([1.35, 1], vertical_alignment="center")

                cartBadgeHtml = (
                    f'<span class="prod-cart-badge">● No carrinho: {qtyInCart} un.</span>'
                    if qtyInCart > 0
                    else ""
                )

                with infoCol:
                    st.markdown(
                        f"""
<div class="prod-category">{product.category}</div>
<div class="prod-name">{product.name}</div>
<div class="prod-spec-row">Especificação: <span class="prod-spec-pill">{product.specs}</span></div>
<div class="prod-price">{formatPrice(product.price)}</div>
""",
                        unsafe_allow_html=True
                    )

                with imgCol:
                    imagePath = getattr(product, "image", "").strip()
                    isWebUrl = imagePath.startswith("http://") or imagePath.startswith("https://")
                    isLocalFile = imagePath != "" and os.path.exists(imagePath)

                    if isWebUrl or isLocalFile:
                        st.image(imagePath, use_container_width=True)
                    else:
                        st.markdown(
                            '<div class="img-placeholder">📷<br>Foto em breve</div>',
                            unsafe_allow_html=True
                        )

                st.markdown(
                    f"""
<div class="prod-meta-row">
  <span class="prod-stock">Estoque disponível: {remainingStock} un. (total: {product.stock})</span>
  {cartBadgeHtml}
</div>
""",
                    unsafe_allow_html=True
                )

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

components.html(runawayScript, height=0)