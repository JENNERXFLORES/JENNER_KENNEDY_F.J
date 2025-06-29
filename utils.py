import streamlit as st

# Tema 1: Profesional Azul Claro
def aplicar_css_estilo_clasico():
    st.markdown("""
    <style>
    body {
        background-color: #e6f0ff;
    }
    .stButton > button {
        background-color: #4a8cf7;
        color: white;
        border-radius: 10px;
        padding: 10px 24px;
        font-size: 1em;
    }
    .stTextInput > div > div > input {
        background-color: #ffffff;
        border: 2px solid #4a8cf7;
        border-radius: 8px;
        font-size: 1em;
    }
    h1, h2, h3 {
        color: #1a53ff;
    }
    .stSidebar {
        background-image: linear-gradient(#4a8cf7, #1a53ff);
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Tema 2: Universitario con Degradado y Sombra
def aplicar_css_estilo_universitario():
    st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #e0eafc, #cfdef3);
    }
    .stButton > button {
        background: linear-gradient(90deg, #1e3c72, #2a5298);
        color: white;
        border-radius: 12px;
        padding: 12px 20px;
        font-size: 1em;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.2);
    }
    .stTextInput > div > div > input {
        background-color: #f0f8ff;
        border: 1px solid #4682B4;
        border-radius: 10px;
        font-size: 1em;
        padding: 5px;
    }
    h1, h2, h3 {
        color: #0b3d91;
    }
    .stSidebar {
        background-image: linear-gradient(#1e3c72, #2a5298);
        color: white;
    }
    .stSidebar .css-ng1t4o {
        background: none;
    }
    </style>
    """, unsafe_allow_html=True)

# Tema 3: Moderno Adaptativo (oscuro/claro, responsivo)
def aplicar_css_moderno_adaptativo():
    st.markdown("""
    <style>
    :root {
        --main-blue: #2a68fd;
        --main-deep-blue: #0a1931;
        --main-light: #e9f1ff;
        --main-gray: #d8e3f0;
        --font-primary: #151a2b;
        --font-secondary: #f4f7fa;
        --button-hover: #11366b;
        --accent: #1ea896;
        --white: #fff;
        --border-radius: 13px;
    }
    @media (prefers-color-scheme: dark) {
        :root {
            --main-blue: #164690;
            --main-deep-blue: #11284a;
            --main-light: #1e2639;
            --main-gray: #22304c;
            --font-primary: #f3f5f8;
            --font-secondary: #232a40;
            --button-hover: #2176ff;
            --accent: #16e0bd;
            --white: #232a40;
        }
        body {
            background: linear-gradient(135deg, #1e2639, #11284a) !important;
            color: var(--font-primary) !important;
        }
        .stSidebar {
            background: linear-gradient(#1e2639, #11284a) !important;
        }
    }
    @media (prefers-color-scheme: light) {
        body {
            background: linear-gradient(135deg, #e9f1ff, #d8e3f0) !important;
            color: var(--font-primary) !important;
        }
        .stSidebar {
            background: linear-gradient(#e9f1ff, #cfd8e3) !important;
        }
    }
    @media (max-width: 650px) {
        html, body {
            font-size: 14px !important;
        }
        .stButton > button {
            padding: 10px 10px !important;
            font-size: 0.9em !important;
        }
        .stTextInput > div > div > input {
            font-size: 0.95em !important;
        }
    }
    .stButton > button {
        background: linear-gradient(90deg, var(--main-blue), var(--accent));
        color: var(--font-secondary);
        border-radius: var(--border-radius);
        border: none;
        padding: 13px 30px;
        font-size: 1.07em;
        font-weight: 600;
        box-shadow: 0px 2px 10px rgba(40,100,255,0.10);
        transition: 0.15s all;
    }
    .stButton > button:hover {
        background: var(--button-hover);
        color: var(--accent);
        box-shadow: 0px 5px 18px 2px rgba(34,52,95,0.12);
        transform: translateY(-2px) scale(1.03);
    }
    .stTextInput > div > div > input {
        background-color: var(--main-light) !important;
        border: 2px solid var(--main-blue);
        border-radius: var(--border-radius);
        font-size: 1.1em;
        padding: 9px;
        color: var(--font-primary) !important;
        transition: 0.12s border;
    }
    .stTextInput > div > div > input:focus {
        border: 2.5px solid var(--accent);
    }
    h1, h2, h3 {
        color: var(--main-blue);
        font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
        font-weight: 700;
    }
    @media (prefers-color-scheme: dark) {
        h1, h2, h3 { color: var(--accent); }
    }
    .stSidebar {
        border-radius: var(--border-radius) !important;
        box-shadow: 0px 1px 13px 0px rgba(34,52,95,0.05);
    }
    .stDataFrame, .stTable {
        background: var(--main-light) !important;
        border-radius: var(--border-radius);
    }
    </style>
    """, unsafe_allow_html=True)

# Fondo imagen login solo en main (personaliza ruta si es necesario)
def aplicar_css_fondo_login():
    st.markdown("""
    <style>
    .main > div:first-child {
        background: url('b361015d-7077-49e3-9bfa-be84756fc9c7.png') no-repeat center center fixed;
        background-size: cover;
        min-height: 100vh;
        transition: background 0.4s;
        position: relative;
    }
    .main > div:first-child::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(20, 24, 31, 0.45);
        z-index: 0;
    }
    @media (max-width: 650px) {
        .main > div:first-child {
            background: #161c23 !important;
        }
    }
    @media (prefers-color-scheme: dark) {
        .main, .main * {
            color: #f2f6fa !important;
        }
        .main > div:first-child::before {
            background: rgba(20,24,31,0.7);
        }
    }
    @media (prefers-color-scheme: light) {
        .main, .main * {
            color: #151a2b !important;
        }
        .main > div:first-child::before {
            background: rgba(255,255,255,0.4);
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Botones modernos para sidebar
def aplicar_css_botones_sidebar():
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] button {
        margin-bottom: 9px !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        background: linear-gradient(90deg,#1e3c72,#2a5298) !important;
        color: #fff !important;
        border: none !important;
        font-size: 1em !important;
        transition: 0.13s all !important;
        box-shadow: 0 2px 10px 0 rgba(34,52,95,0.07);
    }
    section[data-testid="stSidebar"] button:active,
    section[data-testid="stSidebar"] button[aria-pressed="true"] {
        background: linear-gradient(90deg,#38ef7d,#11998e) !important;
        color: #23263a !important;
        font-weight: 800 !important;
    }
    section[data-testid="stSidebar"] button:hover {
        background: linear-gradient(90deg,#21d4fd 0%,#b721ff 100%) !important;
        color: #23263a !important;
        transform: scale(1.03);
    }
    </style>
    """, unsafe_allow_html=True)
