import openai
import solara as sl
from solara.alias import rv
from dataclasses import dataclass, asdict
from typing import List, Iterator

chatbox_css = """
.message {
    max-width: 450px;
    width: 100%;
}

.system-message, .system-message > * {
    background-color: #ffffff !important;
}

.user-message, .user-message > * {
    background-color: #f0f0f0 !important;
}

.assistant-message, .assistant-message > * {
    background-color: #9ab2e9 !important;
}

.avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  border: 2px solid transparent;
  overflow: hidden;
  display: flex;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
"""

@dataclass
class Message:
    role: str
    content: str

def get_chatgpt_response(messages: List[Message]) -> Iterator[Message]:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[asdict(m) for m in messages],
        temperature=0.1,
        stream=True
    )

    total = ""
    for chunk in response: 
        part = chunk['choices'][0]['delta'].get("content", "")
        total += part
        yield Message(role="assistant", content=total)
        
def ChatBox(message: Message) -> None:
    sl.Style(chatbox_css)
    align = "start" if message.role == "assistant" else "center" if message.role == "system" else "end"
    with sl.Column(align=align):
        with sl.Card(classes=["message", f"{message.role}-message"]):
            sl.Markdown(message.content)
        with sl.HBox(align_items="center"):
            sl.Image(f"{message.role}-logo.png", classes=["avatar"])
            sl.Text(message.role.capitalize())

@sl.component
def Chat() -> None:
    sl.Style("""
        .chat-input {
            max-width: 800px;
        })
    """)

    messages, set_messages = sl.use_state([
        Message(
            role="system",
            content="Assist the user with whatever they need.")
        ]
    )
    input, set_input = sl.use_state("")

    def ask_chatgpt():
        _messages = messages + [Message(role="user", content=input)]
        set_input("")
        set_messages(_messages)
        for new_message in get_chatgpt_response(_messages):
            set_messages(_messages + [new_message])

    with sl.VBox():
        for message in messages:
            ChatBox(message)
    
    with sl.Row(justify="center"):
        with sl.HBox(align_items="center", classes=["chat-input"]):
            rv.Textarea(v_model=input, on_v_model=set_input, solo=True, hide_details=True, outlined=True, rows=1, auto_grow=True)
            sl.IconButton("send", on_click=ask_chatgpt)