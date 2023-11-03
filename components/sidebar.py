

import streamlit as st
import requests
import json
import shared.constants as constants
from shared.utils import Utils

class Sidebar:
    def __init__(self):
        self.utils = Utils()

    def get_available_models(self):
        try:
            response = requests.get(constants.OPENROUTER_API_BASE + "/models")
            response.raise_for_status()
            models = json.loads(response.text)["data"]
            return [model["id"] for model in models]
        except requests.exceptions.RequestException as e:
            st.error(f"Error getting models from API: {e}")
            return []


    def handle_model_selection(self, available_models, selected_model, default_model):
        if selected_model and selected_model in available_models:
            selected_index = available_models.index(selected_model)
        else:
            selected_index = available_models.index(default_model)
        selected_model = st.selectbox(
            "Select a model", available_models, index=selected_index
        )
        return selected_model


    def exchange_code_for_api_key(self,code: str):
        print(f"Exchanging code for API key: {code}")
        try:
            response = requests.post(
                constants.OPENROUTER_API_BASE + "/auth/keys",
                json={"code": code},
            )
            response.raise_for_status()
            st.experimental_set_query_params()
            api_key = json.loads(response.text)["key"]
            st.session_state["api_key"] = api_key
            st.experimental_rerun()
        except requests.exceptions.RequestException as e:
            st.error(f"Error exchanging code for API key: {e}")

    def on_provider_change(self, provider):
        st.session_state["provider"] = provider

    
    def show_sidebar(self, default_model:str):
        with st.sidebar:
            st.title("Settings")
            provider = st.selectbox("Select Provider", ["OpenRouter", "LLMlite"])

            if provider == "OpenRouter":
                # OpenRouter-specific code goes here
                # ...
                continue_button = st.button("Connect OpenRouter")
                if continue_button:
                    self.exchange_code_for_api_key(self, st.session_state["code"])

            elif provider == "LLMlite":
                st.text("LLMlite settings go here")
                # Add any LLMlite-specific settings or authentication here

            
            
        return st.session_state.get("api_key", None), st.session_state.get("model", None), provider
