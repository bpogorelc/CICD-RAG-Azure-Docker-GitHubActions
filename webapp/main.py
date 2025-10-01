from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
# Remove this line - causing redirect loop with Azure Container Apps
# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from openai import OpenAI
from dotenv import load_dotenv
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

# Load .env file from the root directory (for local development)
load_dotenv('../.env')

app = FastAPI(
    title="Wine RAG API", 
    description="Secure Wine recommendation system using RAG with SSL/HTTPS",
    docs_url="/docs" if os.getenv("ENVIRONMENT") != "production" else None,
    redoc_url="/redoc" if os.getenv("ENVIRONMENT") != "production" else None
)

# 🔒 SECURITY MIDDLEWARE IMPLEMENTATION
# Remove HTTPSRedirectMiddleware - Azure Container Apps handles HTTPS redirect
# app.add_middleware(HTTPSRedirectMiddleware)  # COMMENTED OUT

# Trusted host validation
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=[
        "rg1.bravesand-0daa5720.eastus.azurecontainerapps.io", 
        "localhost", 
        "127.0.0.1",
        "*.azurecontainerapps.io"  # Allow Azure Container Apps domains
    ]
)

# CORS with secure configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://rg1.bravesand-0daa5720.eastus.azurecontainerapps.io",
        "https://localhost:8000" if os.getenv("ENVIRONMENT") != "production" else ""
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization", "X-API-Key"],
)

# 🛡️ SECURITY HEADERS MIDDLEWARE
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add comprehensive security headers for HTTPS/SSL security"""
    response = await call_next(request)
    
    # SSL/HTTPS Security Headers
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    
    # Custom security info header
    response.headers["X-Security-Features"] = "HTTPS-Enforced-By-Azure,HSTS-Enabled,SSL-Termination"
    
    return response

# 🔐 API KEY AUTHENTICATION
async def verify_api_key(x_api_key: Optional[str] = Header(None, alias="X-API-Key")):
    """Verify API key for secure access to protected endpoints"""
    expected_api_key = os.getenv("API_KEY")
    
    # Skip API key check if not configured (for development)
    if not expected_api_key:
        return True
    
    if not x_api_key or x_api_key != expected_api_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key. Include X-API-Key header.",
            headers={"WWW-Authenticate": "ApiKey"}
        )
    return True

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

# 🌐 PUBLIC ROUTES (No authentication required)
@app.get("/")
async def root():
    return {
        "message": "🔒 Secure Wine RAG API is running with HTTPS/SSL!", 
        "status": "healthy",
        "security": {
            "https_enforced": "Azure Container Apps handles HTTPS redirect",
            "ssl_termination": "Azure Container Apps",
            "security_headers": "enabled",
            "api_authentication": "enabled" if os.getenv("API_KEY") else "disabled"
        }
    }

@app.get("/health")
async def health_check():
    """Public health check endpoint"""
    return {
        "status": "healthy",
        "security_status": "🔒 HTTPS/SSL Enabled by Azure Container Apps",
        "ssl_info": {
            "https_enforced": "Azure Container Apps handles HTTPS redirect automatically",
            "hsts_enabled": True,
            "ssl_termination": "Azure Container Apps manages SSL certificates",
            "security_headers": "Custom security headers implemented"
        },
        "openai_client": "initialized" if openai_client else "failed",
        "search_client": "initialized" if search_client else "failed",
        "environment": {
            "OPENAI_API_KEY": "set" if os.getenv("OPENAI_API_KEY") else "missing",
            "SEARCH_SERVICE_NAME": os.getenv("SEARCH_SERVICE_NAME", "not set"),
            "SEARCH_API_KEY": "set" if os.getenv("SEARCH_API_KEY") else "missing",
            "SEARCH_INDEX_NAME": os.getenv("SEARCH_INDEX_NAME", "not set"),
            "API_KEY_CONFIGURED": "yes" if os.getenv("API_KEY") else "no"
        }
    }

# 🔐 PROTECTED ROUTES (Require API key authentication)
@app.post("/ask", response_model=ChatResponse, dependencies=[Depends(verify_api_key)])
async def ask_question(request: ChatRequest):
    """Secure endpoint requiring API key authentication"""
    try:
        response = ai_RAG_chat(request.message)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse, dependencies=[Depends(verify_api_key)])
async def chat(request: ChatRequest):
    """Alternative secure chat endpoint"""
    return await ask_question(request)

# 🔧 DEVELOPMENT/TESTING ROUTE (Public for easy testing)
@app.post("/ask-public", response_model=ChatResponse)
async def ask_question_public(request: ChatRequest):
    """Public endpoint for testing (no API key required)"""
    try:
        response = ai_RAG_chat(request.message)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # For local development
    uvicorn.run(app, host="0.0.0.0", port=8000)