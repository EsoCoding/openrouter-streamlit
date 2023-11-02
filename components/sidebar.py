
import streamlit as st
import requests
import json
import shared.constants as constants
import shared.utils


class Sidebar:
    def __init__(self):
        self.utils = shared.utils.Utils()

    @staticmethod
    def get_available_models():
        try:
            response = requests.get(constants.OPENROUTER_API_BASE + "/models")
            response.raise_for_status()
            models = json.loads(response.text)["data"]
            return [model["id"] for model in models]
        except requests.exceptions.RequestException as e:
            st.error(f"Error getting models from API: {e}")
            return []

    @staticmethod
    def handle_model_selection(available_models, selected_model, default_model):
        if selected_model and selected_model in available_models:
            selected_index = available_models.index(selected_model)
        else:
            selected_index = available_models.index(default_model)
        selected_model = st.selectbox(
            "Select a model", available_models, index=selected_index
        )
        return selected_model

    @staticmethod
    def exchange_code_for_api_key(code: str):
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

    def show_sidebar(self, default_model: str):
        with st.sidebar:
            params = st.experimental_get_query_params()
            code = params.get("code", [""])[0]
            if code:
                self.exchange_code_for_api_key(code)
            api_key = st.session_state.get("api_key")
            selected_model = params.get("model", [None])[0] or st.session_state.get(
                "model", None
            )
            url = self.utils.url_to_hostname(self.utils.get_url())
            if not api_key:
                st.button(
                    "Connect OpenRouter",
                    on_click=self.utils.open_page,
                    args=(f"{constants.OPENROUTER_BASE}/auth?callback_url={url}",),
                )
            available_models = Sidebar.get_available_models()
            selected_model = Sidebar.handle_model_selection(
                available_models, selected_model, default_model
            )
            st.session_state["model"] = selected_model
            st.experimental_set_query_params(model=selected_model)

            if api_key:
                st.text("Connected to OpenRouter")
                if st.button("Log out"):
                    del st.session_state["api_key"]
                    st.experimental_rerun()

            st.markdown(
                "[View the source code](https://github.com/alexanderatallah/openrouter-streamlit)"
            )

        return api_key, selected_model