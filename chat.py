import openai
import streamlit as st
from streamlit_chat import message
import json
from shared import constants
from components.sidebar import Sidebar
from shared.utils import Utils
import llmlite

class AstroChatApp:
    def __init__(self):
        self.sidebar = Sidebar()
        self.utils = Utils()
        self.api_key, self.selected_model = self.sidebar.show_sidebar(constants.OPENROUTER_DEFAULT_CHAT_MODEL)
        self.setup_ui()

    def setup_ui(self):
        st.title("💬 Streamlit GPT")
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
        user_input = self.create_chat_form()
        self.display_messages()

        if user_input:
            self.handle_user_input(user_input)

    def create_chat_form(self):
        with st.form("chat_input", clear_on_submit=True):
            a, b = st.columns([4, 1])
            user_input = a.text_area(
                label="Your message:",
                placeholder="What would you like to say?",
                height=150,  # You can adjust the height as needed
            )
            b.form_submit_button("Send", use_container_width=True)
        return user_input
    
    def get_llmlite_prediction(self, user_input):
        # Use llmlite to get a prediction based on the user input
        result = llmlite.predict(user_input)
        return result

    def display_messages(self):
        for i, msg in enumerate(st.session_state.messages):
            message(msg["content"], is_user=msg["role"] == "user", key=i)

    def handle_user_input(self, user_input):
        st.session_state.messages.append({"role": "user", "content": user_input})
        message(user_input, is_user=True)

        if self.model_type == 'OpenRouter':
            if not self.api_key:
                st.info("Please click Connect OpenRouter to continue.")
            else:
                self.send_message_to_openai(user_input)
        elif self.model_type == 'llmlite':
            result = self.get_llmlite_prediction(user_input)
            st.session_state.messages.append({"role": "assistant", "content": result})
            message(result)

    def send_message_to_openai(self, user_input):
        openai.api_key = self.api_key
        openai.api_base = constants.OPENROUTER_API_BASE
        response = openai.ChatCompletion.create(
            model=self.selected_model,
            messages=st.session_state.messages,
            headers={"HTTP-Referer": constants.OPENROUTER_REFERRER},
        )
        self.handle_openai_response(response)

    def handle_openai_response(self, response):
        if isinstance(response, str):
            response = json.loads(response)
        msg = response["choices"][0]["message"]
        st.session_state.messages.append(msg)
        message(msg["content"])

if __name__ == '__main__':
    app = AstroChatApp()