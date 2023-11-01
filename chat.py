import os
import openai
import streamlit as st
from streamlit_chat import message
from components.Sidebar import sidebar
import json
from shared import constants

class AstroChatApp:
    def __init__(self, **kwargs):
        self.api_key, self.selected_model = sidebar(constants.OPENROUTER_DEFAULT_CHAT_MODEL)
        self.setup_chat_display()

    def setup_chat_display(self):
        st.title("💬 Streamlit GPT")
        messages = st.session_state.get("messages", [{"role": "assistant", "content": "How can I help you?"}])
        user_input = self.create_chat_form()
        self.display_messages(messages)

        if user_input:
            self.handle_user_input(user_input, messages)

    def create_chat_form(self):
        with st.form("chat_input", clear_on_submit=True):
            a, b = st.columns([4, 1])
            user_input = a.text_input(
                label="Your message:",
                placeholder="What would you like to say?",
                label_visibility="collapsed",
            )
            b.form_submit_button("Send", use_container_width=True)
        return user_input

    @staticmethod
    def display_messages(messages):
        for i, msg in enumerate(messages):
            message(msg["content"], is_user=msg["role"] == "user", key=i)

    def handle_user_input(self, user_input, messages):
        if not self.api_key:
            st.info("Please click Connect OpenRouter to continue.")
            return

        messages.append({"role": "user", "content": user_input})
        message(user_input, is_user=True)
        self.send_message_to_openai(messages)

    def send_message_to_openai(self, messages):
        openai.api_key = self.api_key
        openai.api_base = constants.OPENROUTER_API_BASE
        response = openai.ChatCompletion.create(
            model=self.selected_model,
            messages=messages,
            headers={"HTTP-Referer": constants.OPENROUTER_REFERRER},
        )
        self.handle_openai_response(response, messages)

    def handle_openai_response(self, response, messages):
        if isinstance(response, str):
            response = json.loads(response)

        msg = response["choices"][0]["message"]
        messages.append(msg)
        message(msg["content"])