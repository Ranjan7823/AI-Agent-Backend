# phase 2 - Setup Backend API with FastAPI and expose endpoint for the agent to interact with.
# setup pydantic models (schema validation) for request and response
# setup AI Agent from frontend interaction and connect with the agent created in module
# Run app & explore swagger UI docs for testing the agent interaction with the API endpoint.

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from ai_agent import get_response_from_ai_agent

from fastapi.middleware.cors import CORSMiddleware

#  Define the app ONCE
app = FastAPI(title="Langgraph AI Agent")

# Add CORS middleware to the SAME app instance
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5175", "http://127.0.0.1:5175"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# FIX 1: Expanded the list to accept actual model IDs, including the one you are testing
ALLOWED_MODELS = ["openai/gpt-oss-120b", "gpt-4o-mini"]
class RequestState(BaseModel):
    model_name: str
    model_provider: str
    system_prompt: str
    messages: List[str]
    allow_search: bool = False



@app.post("/chat")
def chat_endpoint(request: RequestState):
    """Endpoint to handle chat interactions with the AI agent."""
    # ✅ Validate model name
    if request.model_name not in ALLOWED_MODELS:
        return {"error": f"Invalid model name. Supported models are {ALLOWED_MODELS}"}

    llm_id = request.model_name
    # ✅ Extract last message safely
    query = request.messages[-1] if request.messages else "Hello"
    allow_search = request.allow_search
    system_prompt = request.system_prompt
    provider = request.model_provider.lower()

    # ✅ Call your agent once
    response = get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider)
    return {"response": response}

      #commneted - 7-6-2026 working fine  with API Tetsing 
    # # """Endpoint to handle chat interactions with the AI agent."""
    # # # FIX 2: Check against the actual model list instead of just provider names
    # # if request.model_name not in ALLOWED_MODELS:
    # #     return {"error": f"Invalid model name. Supported models are {ALLOWED_MODELS}"}

    # # llm_id = request.model_name
    
    # # # FIX 3: request.messages is a list of strings. Extract the last string message as the query.
    # # query = request.messages[-1] if request.messages else "Hello"
    
    # # allow_search = request.allow_search
    # # system_prompt = request.system_prompt
    
    # # # FIX 4: Convert provider to lowercase ("Groq" -> "groq") to prevent string comparison failures
    # # provider = request.model_provider.lower()

    # # # Create AI Agent and get response from the agent
    # # response = get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider)
    # # return {"response": response}

# #     llm_id = request.model_name
# #     query = request.messages
# #     allow_search = request.allow_search
# #     system_prompt = request.system_prompt
# #     provider = request.model_provider

# # # Create AI Agent and get response from the agent
# #     response = get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider)
# #     return {"response": response}

# step 3 - Run the FastAPI app and test the endpoint using Swagger UI or any API testing tool like Postman. You can send a POST request to the /chat endpoint with the required parameters and see the response from the AI agent


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1"  , port=8000);