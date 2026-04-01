# ⚡ AI Agent Chatbot

A tool-using AI agent built with Python, Flask, and the Anthropic Claude API. The agent can reason, decide when to use tools, and return answers — all in a clean web interface.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=flat&logo=flask&logoColor=white)
![Claude](https://img.shields.io/badge/Claude-Sonnet_4-7C6AF7?style=flat)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

---

## What it does

- Accepts natural language questions via a web chat UI
- Uses Claude to decide whether to call a tool or answer directly
- Currently supports two tools: **calculator** and **weather lookup**
- Shows tool calls transparently in the UI so you can follow the agent's reasoning

---

## Demo

> **User:** What's the weather in Tokyo and what is 500 / 4?
>
> **Agent (tool trace):**
> ```
> ▸ get_weather(city: "Tokyo")  →  🌧️ Tokyo: Rainy, 18°C
> ▸ calculator(expression: "500 / 4")  →  500 / 4 = 125.0
> ```
> **Agent:** It's rainy in Tokyo at 18°C right now. And 500 divided by 4 is 125.

---

## Project structure

```
ai-agent/
├── app.py              # Flask backend + agent loop
├── static/
│   └── index.html      # Chat UI (single-file, no build step)
├── requirements.txt
└── README.md
```

---

## Getting started

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/ai-agent.git
cd ai-agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your API key

Get your key from [console.anthropic.com](https://console.anthropic.com).

```bash
# Mac / Linux
export ANTHROPIC_API_KEY="sk-ant-..."

# Windows
set ANTHROPIC_API_KEY=sk-ant-...
```

### 4. Run the app

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## How the agent loop works

```
User message
    ↓
Claude thinks → needs a tool?
    ↓ yes                    ↓ no
Run the tool          Return final answer
    ↓
Send result back to Claude
    ↓
Claude thinks again → repeat until done
```

This loop is the core of any agentic AI system. The key insight: Claude tells *you* when it wants to call a tool — your code runs it and sends the result back.

---

## Adding your own tools

1. Define the tool schema in the `TOOLS` list in `app.py`:

```python
{
    "name": "my_tool",
    "description": "What this tool does.",
    "input_schema": {
        "type": "object",
        "properties": {
            "my_input": { "type": "string", "description": "..." }
        },
        "required": ["my_input"]
    }
}
```

2. Add the Python function:

```python
def my_tool(my_input):
    # do something
    return "result"
```

3. Register it in `run_tool()`:

```python
elif name == "my_tool":
    return my_tool(inputs["my_input"])
```

That's it — Claude will automatically start using it when relevant.

---

## Ideas for next tools

- `web_search` — search the web via [Tavily API](https://tavily.com)
- `read_file` — summarize uploaded documents
- `send_email` — send notifications via SendGrid
- `run_python` — execute code in a sandbox

---

## Requirements

```
anthropic>=0.25.0
flask>=2.3.0
```

---

## License

MIT — free to use, modify, and share.

---

## Author

Built by **Sudhir Rai** · [GitHub](https://github.com/sudhirrai15) · [LinkedIn](https://linkedin.com/in/raisudhir)

*First agentic AI project — feedback welcome!*
