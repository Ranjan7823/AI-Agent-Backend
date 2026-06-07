
# # module1
# # Step1- Setup APIKeys for Groq and Travily 
# # SEtup LLM & Tools
# # Setup AI AGent with Search Tool nad functionality 

# # Step1- Setup APIKeys for Groq and Travily
# # API key

# import os;

# GROOQ_API_KEY = GROQ_API_KEY#os.environ.get("GROQ_API_KEY");
# TAVILY_API_KEY = TAVILY_API_KEY#os.environ.get("TAVILY_API_KEY");
# AGENTIC_OPENAI_KEY = AGENTIC_OPENAI_KEY#os.environ.get("AGENTIC_OPENAI_KEY");

# # Step2- Setup LLM & Tools

# from langchain_groq import ChatGroq
# from langchain_openai import ChatOpenAI
# from langchain_tavily import TavilySearch
# from langchain.agents import create_agent

# from langchain_core.messages.ai import AIMessage


# # Setup LLM OPEN AI
# openai_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.9, openai_api_key=AGENTIC_OPENAI_KEY)
# groq_llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.9, groq_api_key=GROOQ_API_KEY)

# #tools setup
# search_tool = TavilySearch(max_results=2, tavily_api_key=TAVILY_API_KEY)

# # Setup AI AGent with Search Tool functionality 


# from langchain.agents import create_agent
# system_prompt_modifier= "Act as AI chatbot assistant who is smart and friendly. You have access to a search tool that can be used to search the web for information. Use the search tool to find relevant information and answer the user's questions. Be concise and provide accurate information based on the search results."
# agent = create_agent(
#     model=groq_llm,
#     tools=[search_tool],
#     system_prompt=system_prompt_modifier
# )

# # response = agent.invoke(
# #     {
# #         "messages": [
# #             {
# #                 "role": "user",
# #                 "content": "tell me trends in crypto markets?"
# #             }
# #         ]
# #     }
# # )

# # print(response)

# question = "tell me trends in crypto markets?"
# state = {
#     "messages": [
#         ("user", question)
#     ]
# }
# response= agent.invoke(state)
# # response = agent.invoke(
# #     {
# #         "messages": [
# #             {
# #                 "role": "user",
# #                 "content": "tell me trends in crypto markets?"
# #             }
# #         ]
# #     }
# # )

# # messages = response.get("messages")
# # ai_message= [messages.content for msg in messages if isinstance(msg, AIMessage)]

# messages=response.get("messages")
# ai_messages=[message.content for message in messages if isinstance(message, AIMessage)]
# print(ai_messages[-1])

# #note - 
# # phase 2 - Setup Backend API with FastAPI and expose endpoint for the agent to interact with.
#   ## setup pyndantic models (schema validation) for request and response
#   ## setup AI Agent from  frontend interaction and connect with the agent created in module 
#   ## Run app & explore swager UI docs for testing the agent interaction with the API endpoint.

# #
# we will create a function and expose an API endpoint using FastAPI where we will send the user messages and system prompt from the frontend and get the response from the agent.
# we are going to modify the above code and create an API endpoint using FastAPI where we will send the user messages and system prompt from the frontend and get the response from the agent.


# module1
# Step1- Setup APIKeys for Groq and Travily 
# SEtup LLM & Tools
# Setup AI AGent with Search Tool nad functionality 

# Step1- Setup APIKeys for Groq and Travily
# API key

GROQ_API_KEY="key"
TAVILY_API_KEY="key"
AGENTIC_OPENAI_KEY="key"

import os;

GROOQ_API_KEY = GROQ_API_KEY#os.environ.get("GROQ_API_KEY");
TAVILY_API_KEY = TAVILY_API_KEY#os.environ.get("TAVILY_API_KEY");
AGENTIC_OPENAI_KEY = AGENTIC_OPENAI_KEY#os.environ.get("AGENTIC_OPENAI_KEY");

# Step2- Setup LLM & Tools

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain.agents import create_agent

from langchain_core.messages.ai import AIMessage


# Setup LLM OPEN AI
openai_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.9, openai_api_key=AGENTIC_OPENAI_KEY)
groq_llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.9, groq_api_key=GROOQ_API_KEY)

#tools setup
search_tool = TavilySearch(max_results=2, tavily_api_key=TAVILY_API_KEY)

# Setup AI AGent with Search Tool functionality 


from langchain.agents import create_agent

def get_response_from_ai_agent(llm_id, query,allow_search,system_prompt,provider):
    # if(provider=="groq"):
    #     llm= ChatGroq(model=llm_id)
    # elif(provider=="openai"):
    #     llm= ChatOpenAI(model=llm_id)    
    # tools = [search_tool] if allow_search else []

    # FIX 6: Explicitly pass your API keys inside this local logic block
    if provider == "groq":
        llm = ChatGroq(model=llm_id, groq_api_key=GROQ_API_KEY)
    elif provider == "openai":
        llm = ChatOpenAI(model=llm_id, openai_api_key=AGENTIC_OPENAI_KEY)    
    else:
        return "Error: Invalid Provider specified"
        
    tools = [search_tool] if allow_search else []
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt
    )
    state = {
        "messages": [
            ("user", query)
        ]
    }
    response= agent.invoke(state)
    messages=response.get("messages")
    ai_messages=[message.content for message in messages if isinstance(message, AIMessage)]
    print(ai_messages[-1])
    return ai_messages[-1]
