import streamlit as st
from streamlit.components.v1 import html

def render_my_component():
    # Este código cargará tu componente React desde el servidor local
    html(
        """
        <div id="root"></div>
        <script src="http://localhost:3000/main.js"></script>
        """,
        height=400,
    )

if __name__ == "__main__":
    render_my_component()
