import os

import gradio as gr

from career_bot.agent import CareerAgent
from career_bot.config import LINKS, NAME

SUGGESTIONS = [
    "What are you building at Intuit?",
    "Tell me about Columbus at Walmart.",
    "Which AI projects should I see?",
    "How do I reach you?",
]

CSS = """
.gradio-container {
  background: #0c0f14 !important;
  max-width: 760px !important;
  margin: 0 auto !important;
  padding-top: 28px !important;
}
.top {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 16px;
  margin: 0 0 18px;
}
.top h1 {
  margin: 0;
  font-size: 22px;
  font-weight: 600;
  color: #f4f4f5;
  letter-spacing: -0.02em;
}
.top p { margin: 4px 0 0; color: #a1a1aa; font-size: 14px; }
.top nav { display: flex; gap: 14px; }
.top a { color: #d4d4d8; font-size: 14px; text-decoration: none; }
.top a:hover { color: #fff; }
footer { display: none !important; }
"""

THEME = gr.themes.Base(
    primary_hue=gr.themes.colors.zinc,
    neutral_hue=gr.themes.colors.zinc,
    font=gr.themes.GoogleFont("Inter"),
).set(
    body_background_fill="#0c0f14",
    body_text_color="#f4f4f5",
    background_fill_primary="#0c0f14",
    background_fill_secondary="#18181b",
    border_color_primary="#27272a",
    block_background_fill="#0c0f14",
    block_border_width="0px",
    input_background_fill="#18181b",
    input_border_color="#3f3f46",
    button_primary_background_fill="#f4f4f5",
    button_primary_text_color="#18181b",
    button_secondary_background_fill="#18181b",
    button_secondary_text_color="#e4e4e7",
    button_secondary_border_color="#3f3f46",
)


def launch():
    agent = CareerAgent()

    def respond(message, history):
        text = (message or "").strip()
        prior = [turn for turn in (history or []) if turn.get("role") != "system"]
        if not text:
            yield "", prior
            return
        shown = prior + [
            {"role": "user", "content": text},
            {"role": "assistant", "content": "…"},
        ]
        yield "", shown
        answer = agent.chat(text, prior)
        shown[-1] = {"role": "assistant", "content": answer}
        yield "", shown

    def ask(prompt):
        def _ask(history):
            for _, updated in respond(prompt, history):
                yield updated
        return _ask

    with gr.Blocks(title=NAME, theme=THEME, css=CSS) as demo:
        gr.HTML(
            f"""
            <div class="top">
              <div>
                <h1>{NAME}</h1>
                <p>Senior software engineer, Intuit</p>
              </div>
              <nav>
                <a href="{LINKS["website"]}" target="_blank">Portfolio</a>
                <a href="{LINKS["linkedin"]}" target="_blank">LinkedIn</a>
                <a href="{LINKS["github"]}" target="_blank">GitHub</a>
              </nav>
            </div>
            """
        )
        chatbot = gr.Chatbot(
            type="messages",
            height=420,
            show_label=False,
            show_copy_button=True,
            placeholder="Ask about a system, a role, or how to work together.",
        )
        with gr.Row():
            for prompt in SUGGESTIONS:
                gr.Button(prompt, size="sm", variant="secondary").click(
                    ask(prompt), chatbot, chatbot
                )
        message = gr.Textbox(
            placeholder="Ask a question",
            show_label=False,
            lines=1,
            autofocus=True,
            container=False,
        )
        with gr.Row():
            send = gr.Button("Send", variant="primary", scale=0)
            clear = gr.Button("Clear", variant="secondary", scale=0)

        send.click(respond, [message, chatbot], [message, chatbot])
        message.submit(respond, [message, chatbot], [message, chatbot])
        clear.click(lambda: [], outputs=chatbot)

    port = os.getenv("GRADIO_SERVER_PORT")
    demo.launch(server_port=int(port) if port else None)


if __name__ == "__main__":
    launch()
