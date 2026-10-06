import gradio as gr

from career_bot.agent import CareerAgent
from career_bot.config import LINKS, NAME

EXAMPLES = [
    "What are you working on at Intuit?",
    "Walk me through your Walmart Labs work.",
    "Which AI and agent projects have you built?",
    "What is your tech stack?",
    "How can I get in touch?",
]


def launch():
    agent = CareerAgent()
    gr.ChatInterface(
        agent.chat,
        type="messages",
        title=f"{NAME}",
        description=(
            "Ask about experience, projects, skills, and writing. "
            f"Portfolio: {LINKS['website']}"
        ),
        examples=EXAMPLES,
    ).launch()


if __name__ == "__main__":
    launch()
