from langchain_community.tools import WikipediaQueryRun, ArxivQueryRun, BraveSearch
from langchain_community.utilities import WikipediaAPIWrapper, ArxivAPIWrapper
from langchain_community.tools.reddit_search.tool import RedditSearchRun
from langchain_community.utilities.reddit_search import RedditSearchAPIWrapper
from langchain.tools import Tool
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# search = DuckDuckGoSearchRun()
# search_tool = Tool(
#     name="search",
#     func=search.run,
#     description="Search the web for information"
# )

search = BraveSearch()
search_tool = Tool(
    name="search",
    func=search.run,
    description="Search the web for information"
)

wik_api_wrapper = WikipediaAPIWrapper(top_k_results=5, doc_contents_char_max=10000)
wiki_tool = WikipediaQueryRun(api_wrapper=wik_api_wrapper)

arxiv_api_wrapper = ArxivAPIWrapper(top_k_results=10)
arxiv_tool = ArxivQueryRun(api_wrapper=arxiv_api_wrapper)

# ddg_api_wrapper = DuckDuckGoSearchAPIWrapper(max_results=10, safesearch='off')
# search_tool = DuckDuckGoSearchResults(api_wrapper=ddg_api_wrapper)

def write2file(data:str, filename:str="research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ftext = f"-- Research Output ---\nTimestamp:{timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(ftext)

    return f"Data successfully saved to {filename}"

save_tool = Tool(
    name="save_to_a_external_file",
    func=write2file,
    description="Saves structured research data to a text file"
)

reddit_wrapper = RedditSearchAPIWrapper()
reddit_tool = RedditSearchRun(api_wrapper=reddit_wrapper)
