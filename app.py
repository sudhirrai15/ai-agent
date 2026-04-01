from flask import Flask, request, jsonify, send_from_directory
import anthropic
import os

app = Flask(__name__, static_folder="static")
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

TOOLS = [
    {
        "name": "calculator",
        "description": "Performs basic math: add, subtract, multiply, divide.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "A math expression to evaluate, e.g. '12 * 4 + 7'"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "get_weather",
        "description": "Returns the current weather for a given city.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The name of the city, e.g. 'Paris'"
                }
            },
            "required": ["city"]
        }
    }
]

def calculator(expression):
    try:
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error: {e}"

def get_weather(city):
    fake_weather = {
        "paris":     {"temp": "14°C", "condition": "Cloudy", "icon": "☁️"},
        "new york":  {"temp": "22°C", "condition": "Sunny",  "icon": "☀️"},
        "tokyo":     {"temp": "18°C", "condition": "Rainy",  "icon": "🌧️"},
        "london":    {"temp": "11°C", "condition": "Overcast","icon": "🌥️"},
        "sydney":    {"temp": "25°C", "condition": "Sunny",  "icon": "☀️"},
        "dubai":     {"temp": "38°C", "condition": "Hot",    "icon": "🌞"},
    }
    data = fake_weather.get(city.lower())
    if data:
        return f"{data['icon']} {city.title()}: {data['condition']}, {data['temp']}"
    return f"No weather data found for '{city}'"

def run_tool(name, inputs):
    if name == "calculator":
        return calculator(inputs["expression"])
    elif name == "get_weather":
        return get_weather(inputs["city"])
    return f"Unknown tool: {name}"

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    messages = data.get("messages", [])

    tool_calls_log = []

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            tools=TOOLS,
            messages=messages
        )

        if response.stop_reason == "end_turn":
            text = ""
            for block in response.content:
                if hasattr(block, "text"):
                    text = block.text
            return jsonify({
                "reply": text,
                "tool_calls": tool_calls_log,
                "messages": messages + [{"role": "assistant", "content": response.content[0].text if hasattr(response.content[0], 'text') else str(response.content)}]
            })

        elif response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []

            for block in response.content:
                if block.type == "tool_use":
                    result = run_tool(block.name, block.input)
                    tool_calls_log.append({
                        "tool": block.name,
                        "input": block.input,
                        "result": result
                    })
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            messages.append({"role": "user", "content": tool_results})
        else:
            return jsonify({"reply": "Unexpected error.", "tool_calls": [], "messages": messages})

if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    app.run(debug=True, port=5000)
