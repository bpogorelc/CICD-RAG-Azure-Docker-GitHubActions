from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import os
from openai import OpenAI
from dotenv import load_dotenv
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

# Load .env file from the root directory (for local development)
load_dotenv('../.env')

app = FastAPI(title="Wine RAG API", description="Wine recommendation system using RAG")

# Request/Response models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# Initialize clients
def initialize_clients():
    try:
        # Get environment variables
        api_key = os.getenv("OPENAI_API_KEY")
        search_service = os.getenv("SEARCH_SERVICE_NAME", "https://demo-bogdan-search.search.windows.net")
        search_api_key = os.getenv("SEARCH_API_KEY")
        search_index = os.getenv("SEARCH_INDEX_NAME", "demo-index")
        
        if not all([api_key, search_api_key]):
            raise ValueError("Missing required environment variables")
        
        # Initialize OpenAI client (matching your notebook configuration)
        client = OpenAI(
            base_url="https://bogda-mflnsc12-eastus2.cognitiveservices.azure.com/openai/v1/",
            api_key=api_key
        )
        
        # Initialize Azure Search client
        search_client = SearchClient(
            endpoint=search_service,
            index_name=search_index,
            credential=AzureKeyCredential(search_api_key)
        )
        
        return client, search_client
    except Exception as e:
        print(f"Error initializing clients: {e}")
        raise

# Initialize clients at startup
try:
    openai_client, search_client = initialize_clients()
    print("✅ Clients initialized successfully!")
except Exception as e:
    print(f"❌ Failed to initialize clients: {e}")
    openai_client, search_client = None, None

def ai_RAG_chat(user_message: str):
    """RAG function matching your notebook's ai_RAG_chat_3 function"""
    if not openai_client or not search_client:
        raise HTTPException(status_code=500, detail="Clients not properly initialized")
    
    try:
        # Search Azure Search index (matching your notebook)
        search_results = search_client.search(
            search_text=user_message,
            top=20,
            select=["content"]  # Using only content field like ai_RAG_chat_3
        )
        top_results = list(search_results)
        
        # Simple context formation using top_results directly (like your notebook)
        context = str(top_results)
        
        # Chat completion (matching your notebook exactly)
        message_text = [
            {"role": "system", "content": "Assistant is a chatbot that helps you find the best wine for your taste."},
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": context}
        ]
        
        completion = openai_client.chat.completions.create(
            model="gpt-35-turbo-2",  # Your deployment name
            messages=message_text,
            temperature=0.7,
            max_tokens=4096,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )
        
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error in RAG chat: {e}")
        raise HTTPException(status_code=500, detail=f"RAG processing failed: {str(e)}")

# Routes
@app.get("/")
async def root():
    return {"message": "Wine RAG API is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "openai_client": "initialized" if openai_client else "failed",
        "search_client": "initialized" if search_client else "failed",
        "environment": {
            "OPENAI_API_KEY": "set" if os.getenv("OPENAI_API_KEY") else "missing",
            "SEARCH_SERVICE_NAME": os.getenv("SEARCH_SERVICE_NAME", "not set"),
            "SEARCH_API_KEY": "set" if os.getenv("SEARCH_API_KEY") else "missing",
            "SEARCH_INDEX_NAME": os.getenv("SEARCH_INDEX_NAME", "not set")
        }
    }

@app.post("/ask", response_model=ChatResponse)
async def ask_question(request: ChatRequest):
    try:
        response = ai_RAG_chat(request.message)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Alternative endpoint name"""
    return await ask_question(request)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)