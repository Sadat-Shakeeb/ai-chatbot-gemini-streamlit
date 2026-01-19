```markdown
# 🚀 Gemini AI Partner — Multimodal Chatbot

A fast, professional multimodal AI chatbot built with Streamlit and Google Gemini. The app supports real-time streaming text responses and image-based prompts so you can ask the model to describe, analyze, or debug images. It includes robust retry/backoff logic for improved stability when calling the Gemini API.

🔗 Live Demo: [ai-chatbot-gemini-app.streamlit.app](https://ai-chatbot-gemini-app.streamlit.app/)

---

## Key features

- Multimodal input: upload images (JPG, PNG, JPEG) and chat about their content
- Real-time streaming: token-by-token responses for a natural chat experience
- Multiple chat sessions: create, switch, and delete conversations with persisted history
- Reliability: exponential backoff & retry handling for API 503 / overloaded responses
- Performance: cached API client using Streamlit cache utilities for faster startup
- Simple, developer-friendly UI built with Streamlit

---

## Tech stack

- Language: Python (3.10+)
- AI Model: Google Gemini 2.5 Flash
- Framework: [Streamlit](https://streamlit.io/)
- Image handling: Pillow (PIL)
- SDK: `google-genai`

---

## Prerequisites

- Python 3.10 or higher
- A Google Gemini API key (available from AI Studio)
- Git (to clone repository)

---

## Quick start

1. Clone the repo
```bash
git clone https://github.com/Sadat-Shakeeb/ai-chatbot-gemini-streamlit.git
cd ai-chatbot-gemini-streamlit
```

2. Create and activate a virtual environment (recommended)
```bash
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows (cmd)
venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure your API key

Create a directory named `.streamlit` and add a `secrets.toml` file:

```toml
# .streamlit/secrets.toml
GOOGLE_API_KEY = "YOUR_ACTUAL_API_KEY_HERE"
```

(Alternatively, you may set the environment variable `GOOGLE_API_KEY` if you prefer not to use Streamlit secrets.)

5. Run the app
```bash
streamlit run app.py
```

The app will open in your browser. You can also use the Live Demo link above.

---

## Usage tips

- Upload an image and then ask the bot to describe or analyze it (e.g., "Describe this image", "What is wrong with this circuit?", "Explain the objects in the photo").
- Keep prompts clear and concise for best results.
- If you encounter API rate limits or 503 errors, the app will automatically retry with exponential backoff. If retries fail, check your API quota and key.

---

## Development & contribution

Contributions are welcome. Suggested workflow:

- Fork the repository
- Create a feature branch
- Open a pull request with a clear description of changes

Please include tests and keep changes small and focused.

---

## Troubleshooting

- "503 Server Overloaded": The app includes retry/backoff, but frequent 503s may indicate quota or regional throttling—check your Google Cloud / AI Studio usage.
- Authentication errors: Verify `GOOGLE_API_KEY` is correct and has required permissions.
- Missing dependencies: Re-run `pip install -r requirements.txt` inside the activated virtual environment.

---

## License

This project is open-source — feel free to fork and adapt for your own use.

---
- Create a short CONTRIBUTING.md template
- Add usage screenshots or GIFs for the UI
``` 
