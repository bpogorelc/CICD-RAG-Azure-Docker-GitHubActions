# CICD RAG Azure Docker GitHub Actions

A complete CI/CD pipeline for deploying a Wine Recommendation RAG (Retrieval Augmented Generation) application using Azure Container Apps, GitHub Actions, and Docker.

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GitHub Repo   │───▶│  GitHub Actions  │───▶│ Azure Container │
│                 │    │   CI/CD Pipeline │    │      Apps       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       ▼                       │
         │              ┌──────────────────┐             │
         │              │ GitHub Container │             │
         │              │    Registry      │             │
         │              │    (ghcr.io)     │             │
         │              └──────────────────┘             │
         │                                               │
         ▼                                               ▼
┌─────────────────┐                            ┌─────────────────┐
│  Wine RAG App   │                            │  Azure Cognitive│
│   FastAPI +     │◄───────────────────────────│     Search      │
│    OpenAI       │                            │                 │
└─────────────────┘                            └─────────────────┘
```

## 🚀 Features

- **🤖 RAG System**: Wine recommendation using Azure Cognitive Search + OpenAI GPT
- **🔄 CI/CD Pipeline**: Automated build and deployment with GitHub Actions
- **🐳 Containerized**: Docker-based deployment for consistency
- **☁️ Cloud Native**: Runs on Azure Container Apps with auto-scaling
- **📊 Wine Database**: 100K+ wine ratings and reviews
- **🔍 Intelligent Search**: Natural language queries for wine recommendations

## 🛠️ Tech Stack

| Component      | Technology                          |
| -------------- | ----------------------------------- |
| **Backend**    | FastAPI (Python)                    |
| **AI/ML**      | OpenAI GPT-3.5 Turbo                |
| **Search**     | Azure Cognitive Search              |
| **Database**   | Wine ratings CSV (100K+ records)    |
| **Container**  | Docker                              |
| **Registry**   | GitHub Container Registry (ghcr.io) |
| **Hosting**    | Azure Container Apps                |
| **CI/CD**      | GitHub Actions                      |
| **Monitoring** | Azure Application Insights          |

## 🏃‍♂️ Quick Start

### Prerequisites

- Azure subscription
- GitHub account
- Azure CLI installed
- Docker Desktop (for local development)

### 1. Clone the Repository

```bash
git clone https://github.com/bpogorelc/CICD-RAG-Azure-Docker-GitHubActions.git
cd CICD-RAG-Azure-Docker-GitHubActions
```

### 2. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_API_BASE=https://your-openai-endpoint.cognitiveservices.azure.com/
SEARCH_SERVICE_NAME=https://your-search-service.search.windows.net
SEARCH_API_KEY=your_search_api_key_here
SEARCH_INDEX_NAME=demo-index
```

### 3. Configure GitHub Secrets

Set up the following secrets in your GitHub repository:

```bash
gh secret set OPENAI_API_KEY --body "your_openai_api_key"
gh secret set SEARCH_SERVICE_API_KEY --body "your_search_api_key"
gh secret set AZURE_CREDENTIALS --body "$(cat azure_credentials.json)"
gh secret set PAT --body "your_github_personal_access_token"
```

### 4. Deploy to Azure

Trigger the deployment workflow:

```bash
gh workflow run "Trigger auto deployment for rg1 container app"
```

## 🧪 Testing the Deployed Application

### Web Interface

Visit your deployed app:

```
https://rg1.bravesand-0daa5720.eastus.azurecontainerapps.io
```

### API Testing

```python
import requests

# Test the health endpoint
health_response = requests.get("https://rg1.bravesand-0daa5720.eastus.azurecontainerapps.io/health")
print(health_response.json())

# Test wine recommendations
query = "What is the best Cabernet Sauvignon wine in Napa Valley above 94 points"
response = requests.post(
    "https://rg1.bravesand-0daa5720.eastus.azurecontainerapps.io/ask",
    json={"message": query}
)
print(response.json())
```

### Example Queries

- "What is the best Cabernet Sauvignon wine in Napa Valley above 94 points?"
- "Recommend a French Chardonnay under $50"
- "Show me highly rated Pinot Noir from Oregon"
- "What are the top-rated Italian wines?"

## 📁 Project Structure

```
CICD-RAG-Azure-Docker-GitHubActions/
├── .github/workflows/
│   └── main.yml                     # CI/CD pipeline
├── webapp/
│   ├── main.py                      # FastAPI application
│   ├── test_deployed_RAG_app.ipynb  # Testing notebook
│   └── requirements.txt             # Python dependencies
├── examples/
│   └── 1-setup-application/
│       └── acs.ipynb               # RAG development notebook
├── Dockerfile                      # Container configuration
├── wine-ratings.csv               # Wine dataset (100K+ records)
├── .env.example                   # Environment variables template
└── README.md                      # This file
```

## 🔧 API Endpoints

| Method | Endpoint  | Description                          |
| ------ | --------- | ------------------------------------ |
| `GET`  | `/`       | Root endpoint - API status           |
| `GET`  | `/health` | Health check with client status      |
| `POST` | `/ask`    | Main RAG endpoint for wine questions |
| `POST` | `/chat`   | Alternative chat endpoint            |

### Request Format

```json
{
  "message": "What is the best Cabernet Sauvignon wine in Napa Valley above 94 points?"
}
```

### Response Format

```json
{
  "response": "Based on our wine database, here are the top Cabernet Sauvignon recommendations from Napa Valley with ratings above 94 points..."
}
```

## 🔄 CI/CD Pipeline

The GitHub Actions workflow automatically:

1. **Builds** Docker image from source code
2. **Pushes** image to GitHub Container Registry
3. **Deploys** to Azure Container Apps
4. **Configures** environment variables
5. **Updates** container resources (2 CPU, 4GB RAM)

### Trigger Deployment

```bash
# Manual trigger
gh workflow run "Trigger auto deployment for rg1 container app"

# Monitor deployment
gh run watch
```

## 🏗️ Local Development

### Run Locally with Docker

```bash
# Build the image
docker build -t wine-rag-app .

# Run the container
docker run -p 8000:8000 --env-file .env wine-rag-app
```

### Run with Python

```bash
# Install dependencies
pip install -r webapp/requirements.txt

# Run the FastAPI server
cd webapp
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 📊 Dataset

The application uses a comprehensive wine dataset with:

- **100,000+** wine reviews and ratings
- **Regions**: Worldwide wine regions
- **Varieties**: 100+ grape varieties
- **Ratings**: Professional wine scores
- **Tasting Notes**: Detailed flavor profiles

## 🔍 RAG Implementation

The RAG system combines:

1. **Retrieval**: Azure Cognitive Search finds relevant wines
2. **Augmentation**: Context is formatted for the AI model
3. **Generation**: OpenAI GPT generates personalized recommendations

### Search Process

```python
# Search wine database
search_results = search_client.search(
    search_text=user_query,
    top=20,
    select=["content"]
)

# Generate AI response
completion = openai_client.chat.completions.create(
    model="gpt-35-turbo-2",
    messages=[
        {"role": "system", "content": "Assistant helps find the best wine for your taste."},
        {"role": "user", "content": user_query},
        {"role": "assistant", "content": search_context}
    ]
)
```

## 🚨 Troubleshooting

### Common Issues

1. **500 Internal Server Error**

   - Check environment variables are set correctly
   - Verify Azure services are accessible

2. **Authentication Errors**

   - Ensure API keys are valid and not expired
   - Check Azure service permissions

3. **No Search Results**
   - Verify Azure Cognitive Search index exists
   - Check wine data was uploaded correctly

### Debug Commands

```bash
# Check container logs
az containerapp logs show --name rg1 --resource-group rg1 --follow

# Test health endpoint
curl https://rg1.bravesand-0daa5720.eastus.azurecontainerapps.io/health

# Check workflow status
gh run list --workflow="main.yml"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT models
- Azure Cognitive Services team
- Wine rating data providers
- FastAPI and Docker communities

## 📧 Contact

**Bogdan Pogorelc** - [GitHub](https://github.com/bpogorelc)

Project Link: [https://github.com/bpogorelc/CICD-RAG-Azure-Docker-GitHubActions](https://github.com/bpogorelc/CICD-RAG-Azure-Docker-GitHubActions)

---

\*\*🍷 Cheers to intelligent wine
