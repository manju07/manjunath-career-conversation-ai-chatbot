import os

from openai import OpenAI

from career_bot.config import GEMINI_BASE_URL, GEMINI_MODEL
from career_bot.knowledge import load_profile
from career_bot.prompt import build_system_prompt
from career_bot.tools import TOOLS, handle_tool_calls


class CareerAgent:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url=GEMINI_BASE_URL,
        )
        self.system_prompt = build_system_prompt(load_profile())

    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt}] + history + [
            {"role": "user", "content": message}
        ]
        while True:
            response = self.client.chat.completions.create(
                model=GEMINI_MODEL,
                messages=messages,
                tools=TOOLS,
            )
            choice = response.choices[0]
            if choice.finish_reason == "tool_calls":
                assistant_message = choice.message
                messages.append(assistant_message)
                messages.extend(handle_tool_calls(assistant_message.tool_calls))
                continue
            return choice.message.content or ""
