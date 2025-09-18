from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests
from pypdf import PdfReader
import gradio as gr


load_dotenv(override=True)

def push(text):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        }
    )


def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}


def record_unknown_question(question):
    push(f"Recording {question}")
    return {"recorded": "ok"}


record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            },
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}


record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}


tools = [{"type": "function", "function": record_user_details_json},
         {"type": "function", "function": record_unknown_question_json}]


class Me:

    def __init__(self):
        self.openai = OpenAI()
        google_api_key = os.getenv('GOOGLE_API_KEY')
        self.gemini = OpenAI(api_key=google_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
        self.name = "Manjunath Asundi"

        reader = PdfReader("data/Profile.pdf")
        self.linkedin = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text

        reader = PdfReader("data/Manjunath_Asundi.pdf")
        self.resume = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.resume += text

        with open("data/summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()
        
        self.courses = [
            {
                "name": "Generative AI",
                "certificate": "https://www.udemy.com/certificate/UC-5b3312c7-f523-4511-bd71-3493a1c08d4f/"
            },
            {
                "name": "Advanced React",
                "certificate": "https://www.coursera.org/account/accomplishments/verify/OIDRUBBHNLGH"
            },
            {
                "name": "Exam Prep CKA: Certified Kubernetes Administrator",
                "certificate": "https://www.coursera.org/account/accomplishments/certificate/J282QAZ6CQ3F"
            },
            {
                "name": "BPMN Overview",
                "certificate": "https://verify.skilljar.com/c/hi9qm34coj63"
            },
            {
                "name": "Learning GraphQL",
                "certificate": "https://www.linkedin.com/learning/certificates/c628829b224a06f5a26c5b1e32e56ffd1d040262fdfaa0482295f9b7678a2dcb?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_certifications_details%3B1OKwzlAhTEmBNOqtLReMPw%3D%3D"
            },
            {
                "name": "Learning Kubernetes (2018)",
                "certificate": "https://www.linkedin.com/learning/certificates/d3ba3202025ec8b55f726953747905020e66e88d9eeb8df3f328c509af3824f0?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_certifications_details%3B1OKwzlAhTEmBNOqtLReMPw%3D%3D"
            },
            {
                "name": "JavaScript (Intermediate)",
                "certificate": "https://www.hackerrank.com/certificates/53a5b0a9f9be?utm_medium=email&utm_source=mail_template_1393&utm_campaign=hrc_skills_certificate"
            },
            {
                "name": "Learn Java Unit Testing with Junit & Mockito in 30 Steps",
                "certificate": "https://www.udemy.com/certificate/UC-b844646b-946c-412c-8856-b2c3498f42a1/"
            },
            {
                "name": "Java (Basic)",
                "certificate": "https://www.hackerrank.com/certificates/6600849c936d"
            },
            {
                "name": "JavaScript (Intermediate)",
                "certificate": "https://www.hackerrank.com/certificates/1444616f4785"
            },
            {
                "name": "Problem Solving (Advanced)",
                "certificate": "https://www.hackerrank.com/certificates/b81d11ec346d"
            },
            {
                "name": "Problem Solving (Basic)",
                "certificate": "https://www.hackerrank.com/certificates/db458d8c9338"
            },
            {
                "name": "React (Basic)",
                "certificate": "https://www.hackerrank.com/certificates/2001b5081bdb"
            },
            {
                "name": "SQL (Basic)",
                "certificate": "https://www.hackerrank.com/certificates/19ef91dbd737"
            },
            {
                "name": "SQL (Intermediate)",
                "certificate": "https://www.hackerrank.com/certificates/afd6f5e4359c"
            },
            {
                "name": "Master Microservices with Spring Boot and Spring Cloud",
                "certificate": "https://www.udemy.com/certificate/UC-6658e3f3-ac7c-4bd6-8a9b-6c4ebb47621f/"
            },
            {
                "name": "Jenkins, From Zero To Hero: Become a DevOps Jenkins Master",
                "certificate": "https://www.udemy.com/certificate/UC-437dfca9-c5bc-498a-8e96-1e567708d564/"
            }    
        ]

    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}", flush=True)
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append({"role": "tool", "content": json.dumps(result), "tool_call_id": tool_call.id})
        return results
    
    def system_prompt(self):
        system_prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s website, \
particularly questions related to {self.name}'s career, background, skills and experience. \
Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
You are given a summary of {self.name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "

        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n"
        system_prompt += f"\n\n## LinkedIn Profile:\n{self.linkedin}\n\n"
        system_prompt += f"\n\n## Resume:\n{self.resume}\n\n"
        system_prompt += f"\n\n## Courses:\n{self.courses}\n\n"
        system_prompt += f"\n\n## Github link:\nhttps://github.com/manju07\n\n"
        system_prompt += f"\n\n## LinkedIn link:\nhttps://www.linkedin.com/in/manju07/\n\n"
        system_prompt += f"\n\n## Website link:\nhttps://manju07.github.io/\n\n try to find the missing data from this website"
        system_prompt += f"\n\n## Hackerrank:https://www.hackerrank.com/profile/manju07\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt
    
    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        done = False
        while not done:
            # response = self.openai.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)
            response = self.gemini.chat.completions.create(
                model="gemini-2.0-flash",
                messages=messages,
                tools=tools
            )
            if response.choices[0].finish_reason == "tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True
        return response.choices[0].message.content


if __name__ == "__main__":
    me = Me()
    gr.ChatInterface(me.chat, type="messages").launch()