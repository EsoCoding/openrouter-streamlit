from streamlit.components.v1 import html
from urllib.parse import urlparse
from streamlit_javascript import st_javascript

class Utils:
    def __init__(self):
        pass


    def get_url(self):
        return st_javascript("await fetch('').then(r => window.parent.location.href)")


    def open_page(self, url):
        st_javascript(f"window.open('{url}', '_blank').focus()")

    def url_to_hostname(self, url):
        uri = urlparse(url)
        return f"{uri.scheme}://{uri.netloc}/"