from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor

from tools import search_tool, wiki_tool, arxiv_tool, save_tool, reddit_tool


load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]


llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro")
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help generate a research paper.
            answer the user query and use necessary tools.
            Try to give a complete and informative answer.
            Wrap the output in this format and provide no other text\n{format_instructions}.
            Also save results to a text file.
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [search_tool, wiki_tool, arxiv_tool, save_tool]
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools = tools
)

def ask_agent(query):

    agent_executer = AgentExecutor(agent=agent, tools=tools, verbose=True)
    raw_response = agent_executer.invoke({"query":query})

    # response = llm.invoke("What is meant by vibe coding?")
    response = parser.parse(raw_response.get("output"))

    return response.dict()

