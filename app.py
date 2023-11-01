import os
import streamlit as st
# this class starts AstroChatApp

def main():
    # make sure we are in the root directory
    # where chat.py is located and run it
    # using os.system
    os.chdir("..")
    os.system("streamlit run chat.py")

if __name__ == "__main__":
    # lets start the app using streamlit run app.py
    main()