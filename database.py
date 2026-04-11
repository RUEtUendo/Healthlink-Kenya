import streamlit as st
import streamlit.components.v1 as components

# Make the page wide to fit your new dashboard
st.set_page_config(page_title="HealthLink Kenya", layout="wide", initial_sidebar_state="collapsed")

# Read the HTML file you uploaded
with open("index.html", "r", encoding="utf-8") as f:
    html_code = f.read()

# Embed the HTML directly into the Streamlit app
components.html(html_code, height=900, scrolling=True)
