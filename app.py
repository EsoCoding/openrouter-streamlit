import os
import AstroChat 

# launches main app
def main():
    AstroChat.start()

# stream lit app
if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.system("streamlit run app.py")