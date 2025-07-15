# from agno.agent import Agent
# from agno.models.google import Gemini
# from agno.models.openai import OpenAIChat
# from agno.tools.reasoning import ReasoningTools
# from agno.tools.yfinance import YFinanceTools

# from dotenv import load_dotenv

# load_dotenv()

# agent = Agent(
#     model=Gemini(id="gemini-2.0-flash"),
#     tools=[
#         ReasoningTools(add_instructions=True),
#         YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True)
#     ],
#     instructions=[
#         "Use tables to display data",
#         "Only output the report, no other text"
#     ],
#     markdown=True
# )

# agent.print_response("Write a report on Microsoft", stream=True, show_all_reasoning=True, stream_intermediate_steps=True)


from flask import Flask, request, jsonify
from flask_cors import CORS
from agent import ask_agent

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

@app.route('/api/v1/ask', methods=['POST'])
def ask():
    data = request.get_json()
    query = data.get('query') if data else None
    if not query:
        return jsonify({'error': 'Missing query parameter'}), 400

    answer = ask_agent(query)  # your agent handling logic
    return jsonify(answer)

if __name__ == '__main__':
    app.run(debug=True)


