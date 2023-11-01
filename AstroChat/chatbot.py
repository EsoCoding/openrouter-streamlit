import streamlit as st

class OpenRouterStreamChat:
    def __init__(self) -> None:
        pass

    # start streamlit chat
    def start():        
        x = st.slider('Select a value')
        st.write(x, 'squared is', x * x)