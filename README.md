---
title: manjunath-career-conversation
app_file: main.py
sdk: gradio
sdk_version: 5.46.0
---

# Manjunath Career Conversation

This is an interactive AI-powered chatbot designed to answer questions about Manjunath Asundi's professional background, skills, and experience. The application leverages LLMs (OpenAI and Google Gemini) and Retrieval Augmented Generation (RAG) to provide detailed, context-aware responses based on Manjunath's resume, LinkedIn profile, and a curated summary.

🌐 **Try the AI Chatbot here:** [Manjunath Career Conversation on Hugging Face Spaces](https://huggingface.co/spaces/manju0707/manjunath-career-conversation)

## Features

- **Conversational AI**: Users can chat with an AI agent that represents Manjunath Asundi, asking about his career, skills, certifications, and more.
- **Multi-Model Support**: Integrates both OpenAI and Google Gemini models, with the ability to compare and evaluate responses.
- **Tool Use & Logging**: The AI can record user interest (email, name, notes) and log unknown questions for future improvement, using Pushover notifications.
- **Contextual Knowledge**: The agent is provided with Manjunath's resume, LinkedIn profile, and a summary, all loaded from local files.
- **Course & Certification Showcase**: Lists and provides links to Manjunath's professional certifications and completed courses.
- **Professional Links**: Shares links to GitHub, LinkedIn, personal website, and HackerRank profiles.

## How it Works

- The app loads Manjunath's professional data from PDF and text files in the `data/` directory.
- When a user interacts, the AI uses this context to answer questions as if it were Manjunath himself.
- If the AI cannot answer a question, it records the question for review.
- If a user expresses interest in connecting, the AI prompts for an email and records the details.


## Requirements

- Python 3.8+
- [Gradio](https://gradio.app/) >= 5.46.0
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [pypdf](https://pypi.org/project/pypdf/)
- [requests](https://pypi.org/project/requests/)

## Setup

1. **Clone the repository** and ensure the `data/` directory contains the required files.
2. **Install dependencies**:
   ```uv
   uv add -r requirements.txt
   ```
3. **Set up environment variables** in a `.env` file:
   ```
   OPENAI_API_KEY=your_openai_key
   GOOGLE_API_KEY=your_google_gemini_key
   PUSHOVER_TOKEN=your_pushover_token
   PUSHOVER_USER=your_pushover_user_key
   ```
4. **Run the app**:
   ```bash
   uv run main.py
   ```

## Usage

- Open the Gradio interface in your browser.
- Start a conversation to learn about Manjunath's experience, skills, and projects.
- Ask for certifications, resume details, or professional links.
- If you want to connect, provide your email when prompted.

## Notes

- The AI is instructed to always stay in character as Manjunath Asundi.
- All user interest and unknown questions are logged via Pushover for follow-up.
- The app demonstrates RAG and agentic AI concepts, as noted in `data/Personal-Notes`.

## Author

**Manjunath Asundi**  
- [GitHub](https://github.com/manju07)
- [LinkedIn](https://www.linkedin.com/in/manju07/)
- [Website](https://manju07.github.io/)
- [HackerRank](https://www.hackerrank.com/profile/manju07)

---
