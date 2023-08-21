import solara as sl
from chat import Chat

css = """
    .main {
        width: 100%;
        height: 100%;
        max-width: 1200px;
        margin: auto;
        padding: 1em;
    }
"""

@sl.component
def Page() -> None:
    sl.Style(css)
    with sl.VBox(classes=["main"]):
        sl.HTML(tag="h1", style="margin: auto;", unsafe_innerHTML="ChatGPT in Solara")

        Chat()

Page()