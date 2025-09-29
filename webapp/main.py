import os
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from openai import AzureOpenAI
from dotenv import load_dotenv

from azure.search.documents import SearchClient # replaces older AzureSearch()
from azure.core.credentials import AzureKeyCredential # for SearchClient

# Load .env file from the root directory
load_dotenv('../.env')  # Go up one level to the root

app = FastAPI()

# Check if required environment variables are set
required_vars = {
    'OPENAI_API_BASE': os.getenv('OPENAI_API_BASE'),
    'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
    'SEARCH_SERVICE_NAME': os.getenv('SEARCH_SERVICE_NAME'),
    'SEARCH_API_KEY': os.getenv('SEARCH_API_KEY'),
    'SEARCH_INDEX_NAME': os.getenv('SEARCH_INDEX_NAME')
}

print("Environment Variables Status:")
for var, value in required_vars.items():
    status = "✓ Set" if value else "✗ Missing"
    print(f"{var}: {status}")

# Only initialize clients if all required variables are set
if all(required_vars.values()):
    # Initialize Azure OpenAI client
    client = AzureOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        api_version=os.getenv("OPENAI_API_VERSION", "2023-07-01-preview"),
        azure_endpoint=os.getenv("OPENAI_API_BASE")
    )

    # Initialize Azure Search client  
    search_client = SearchClient(
        endpoint=os.getenv('SEARCH_SERVICE_NAME'),
        index_name=os.getenv('SEARCH_INDEX_NAME'),
        credential=AzureKeyCredential(os.getenv('SEARCH_API_KEY'))
    )

    print("\n✓ Clients initialized successfully!")
    print(f"Search endpoint: {os.getenv('SEARCH_SERVICE_NAME')}")
    print(f"Search index: {os.getenv('SEARCH_INDEX_NAME')}")
else:
    print("\nCannot initialize clients - missing required environment variables.")
    print("Please set the missing environment variables or create a .env file with:")
    print("OPENAI_API_BASE=your_azure_openai_endpoint")
    print("OPENAI_API_KEY=your_azure_openai_key") 
    print("SEARCH_SERVICE_NAME=your_search_service_endpoint")
    print("SEARCH_API_KEY=your_search_service_key")
    print("SEARCH_INDEX_NAME=your_search_index_name")


class Body(BaseModel):
    query: str


@app.get('/')
def root():
    return RedirectResponse(url='/docs', status_code=301)


@app.post('/ask')
def ask(body: Body):
    """
    Use the query parameter to interact with the Azure OpenAI Service
    using the Azure Cognitive Search API for Retrieval Augmented Generation.
    """
    search_result = search(body.query)
    chat_bot_response = assistant(body.query, search_result)
    return {'response': chat_bot_response}



def search(query):
    """
    Send the query to Azure Cognitive Search and return the top result
    """

    # Search using query syntax for filtering
    search_results = search_client.search(
        search_text=query,
        top=20,
        #select=["id", "name", "grape", "region", "variety", "rating", "notes", "content"]
        select=["content"] # using only content field to make it simpler and avoid token limit issues
    )
    top_results = list(search_results)

    ## Simple context formation using all top_results directly
    #context = str(top_results) # alternative 1
    #context = "\n".join([doc['content'] for doc in top_results]) # alternative 2

    # To use only one top result
    if top_results:
        context = top_results[0]['content']
    else:
        context = "No relevant documents found."
    print(context)
    return context


def assistant(query, context):

    from openai import OpenAI

    endpoint = "https://bogda-mflnsc12-eastus2.cognitiveservices.azure.com/openai/v1/"
    model_name = "gpt-35-turbo"
    deployment_name = "gpt-35-turbo-2"

    api_key = os.getenv("OPENAI_API_KEY")

    client = OpenAI(
        base_url=f"{endpoint}",
        api_key=api_key
    )

    messages=[
        # Set the system characteristics for this chat bot
        {"role": "system", "content": "Assistant is a chatbot that helps you find the best wine for your taste."},
        # Set the query so that the chatbot can respond to it
        {"role": "user", "content": query},
        # Add the context from the vector search results so that the chatbot can use
        # it as part of the response for an augmented context
        {"role": "assistant", "content": context}
    ]

    completion = client.chat.completions.create(
      model=deployment_name,
      messages=messages,
      temperature=0.7,
      max_tokens=4096,
      top_p=0.95,
      frequency_penalty=0,
      presence_penalty=0,
      stop=None
    )
    return completion.choices[0].message.content