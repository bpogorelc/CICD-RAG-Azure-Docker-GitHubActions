# CICD RAG Azure Docker GitHub Actions

A complete CI/CD pipeline for deploying a **Secure Wine Recommendation RAG** (Retrieval Augmented Generation) application using Azure Container Apps, GitHub Actions, and Docker with comprehensive SSL/HTTPS security.

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
│  🔒 SSL/HTTPS   │                            │                 │
└─────────────────┘                            └─────────────────┘
```

## 🚀 Features

- **🤖 RAG System**: Wine recommendation using Azure Cognitive Search + OpenAI GPT
- **🔒 SSL/HTTPS Security**: Comprehensive web security with managed SSL certificates
- **🔐 API Authentication**: Secure endpoints with API key authentication
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
| **Security**   | SSL/TLS, HSTS, CSP, API Key Auth    |
| **Monitoring** | Azure Application Insights          |

## 🔒 Security Features

### **SSL/HTTPS Implementation**

- **Managed SSL Certificates**: Azure Container Apps automatically provisions and renews SSL certificates
- **HTTPS Enforcement**: All HTTP traffic automatically redirected to HTTPS
- **SSL Termination**: Handled at the Azure platform level for optimal performance

### **Security Headers**

- **HSTS**: HTTP Strict Transport Security prevents protocol downgrade attacks
- **CSP**: Content Security Policy blocks XSS and code injection
- **X-Frame-Options**: Prevents clickjacking attacks
- **X-Content-Type-Options**: MIME sniffing protection

### **API Security**

- **API Key Authentication**: Secure endpoints require `X-API-Key` header
- **CORS Policies**: Controlled cross-origin access
- **Environment-based Configuration**: Production vs development security settings

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
SEARCH_SERVICE_NAME=https://your-search-service.search.windows.net
SEARCH_API_KEY=your_search_api_key_here
SEARCH_INDEX_NAME=demo-index
API_KEY=your_secure_api_key_here
ENVIRONMENT=production
```

### 3. Configure GitHub Secrets

Set up the following secrets in your GitHub repository:

```bash
gh secret set OPENAI_API_KEY --body "your_openai_api_key"
gh secret set SEARCH_SERVICE_API_KEY --body "your_search_api_key"
gh secret set API_KEY --body "your_secure_api_key"
gh secret set ENVIRONMENT --body "production"
gh secret set AZURE_CREDENTIALS --body "$(cat azure_credentials.json)"
gh secret set PAT --body "your_github_personal_access_token"
```

### 4. Deploy to Azure

Trigger the deployment workflow:

```bash
gh workflow run "Trigger auto deployment for rg1 container app"
```

## 🧪 Testing the Deployed Application

### **Live Demo Commands**

```bash
# Test health endpoint with security status
curl https://rg1.bravesand-0daa5720.eastus.azurecontainerapps.io/health

# Test security configuration
curl https://rg1.bravesand-0daa5720.eastus.azurecontainerapps.io/security-test

# Public wine recommendation (no API key required)
curl -X POST "https://rg1.bravesand-0daa5720.eastus.azurecontainerapps.io/ask-public" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the best Cabernet Sauvignon wine in Napa Valley?"}'

# Secure wine recommendation (API key required)
curl -X POST "https://rg1.bravesand-0daa5720.eastus.azurecontainerapps.io/ask" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: wine-rag-secure-api-key-2024" \
  -d '{"message": "Recommend a wine for dinner with steak"}'

# Test authentication (should return 401)
curl -X POST "https://rg1.bravesand-0daa5720.eastus.azurecontainerapps.io/ask" \
  -H "Content-Type: application/json" \
  -d '{"message": "Test without API key"}'
```

### **Python API Testing**

```python
import requests

url = "https://rg1.bravesand-0daa5720.eastus.azurecontainerapps.io"
headers = {"X-API-Key": "wine-rag-secure-api-key-2024"}

# Test health and security
health = requests.get(f"{url}/health")
security = requests.get(f"{url}/security-test")
print(f"Health: {health.status_code} | Security: {security.json()['security_status']}")

# Test public endpoint
public_response = requests.post(
    f"{url}/ask-public",
    json={"message": "What is the best Cabernet Sauvignon?"}
)
print(f"Public API: {public_response.status_code}")

# Test secure endpoint
secure_response = requests.post(
    f"{url}/ask",
    json={"message": "What is the best Cabernet Sauvignon?"},
    headers=headers
)
print(f"Secure API: {secure_response.status_code}")
print(f"Response: {secure_response.json()['response'][:100]}...")
```

### **Web Interface**

Visit your deployed app:

```
https://rg1.bravesand-0daa5720.eastus.azurecontainerapps.io
```

**Note**: API documentation (Swagger/OpenAPI) is disabled in production for security. For development access, set `ENVIRONMENT=development` in your environment variables.

### **Example Queries**

- "What is the best Cabernet Sauvignon wine in Napa Valley above 94 points?"
- "Recommend a French Chardonnay under $50"
- "Show me highly rated Pinot Noir from Oregon"
- "What are the top-rated Italian wines?"
- "Wine pairing for grilled salmon"

## 📁 Project Structure

```
CICD-RAG-Azure-Docker-GitHubActions/
├── .github/workflows/
│   └── main.yml                     # CI/CD pipeline with security configs
├── webapp/
│   ├── main.py                      # Secure FastAPI application
│   ├── test_deployed_RAG_app.ipynb  # Testing notebook
│   └── requirements.txt             # Python dependencies
├── examples/
│   └── 1-setup-application/
│       └── acs.ipynb               # RAG development notebook
├── test_secure_webapp_complete.py  # Security testing script
├── Dockerfile                      # Container configuration
├── wine-ratings.csv               # Wine dataset (100K+ records)
├── .env.example                   # Environment variables template
└── README.md                      # This file
```

## 🔧 API Endpoints

| Method | Endpoint         | Authentication       | Description                                   |
| ------ | ---------------- | -------------------- | --------------------------------------------- |
| `GET`  | `/`              | None                 | Root endpoint - API status with security info |
| `GET`  | `/health`        | None                 | Health check with security status             |
| `GET`  | `/security-test` | None                 | Security configuration details                |
| `POST` | `/ask`           | **API Key Required** | Secure RAG endpoint for wine questions        |
| `POST` | `/chat`          | **API Key Required** | Alternative secure chat endpoint              |
| `POST` | `/ask-public`    | None                 | Public RAG endpoint for demos                 |

### **Request Format**

```json
{
  "message": "What is the best Cabernet Sauvignon wine in Napa Valley above 94 points?"
}
```

### **Response Format**

```json
{
  "response": "Based on our wine database, here are the top Cabernet Sauvignon recommendations from Napa Valley with ratings above 94 points..."
}
```

### **Authentication**

For secure endpoints, include the API key in headers:

```bash
X-API-Key: your-api-key-here
```

## 🔄 CI/CD Pipeline

The GitHub Actions workflow automatically:

1. **Builds** Docker image from source code
2. **Pushes** image to GitHub Container Registry
3. **Deploys** to Azure Container Apps
4. **Configures** environment variables and security settings
5. **Updates** container resources (2 CPU, 4GB RAM)

### **Trigger Deployment**

```bash
# Manual trigger
gh workflow run "Trigger auto deployment for rg1 container app"

# Monitor deployment
gh run watch

# Check deployment status
gh run list --workflow="main.yml"
```

## 🏗️ Local Development

### **Run Locally with Docker**

```bash
# Build the image
docker build -t wine-rag-app .

# Run the container with environment file
docker run -p 8000:8000 --env-file .env wine-rag-app
```

### **Run with Python**

```bash
# Install dependencies
pip install -r webapp/requirements.txt

# Run the FastAPI server
cd webapp
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Local access**: http://localhost:8000 (API docs available in development mode)

## 📊 Dataset

The application uses a comprehensive wine dataset with:

- **100,000+** wine reviews and ratings
- **Regions**: Worldwide wine regions
- **Varieties**: 100+ grape varieties
- **Ratings**: Professional wine scores
- **Tasting Notes**: Detailed flavor profiles

## 🔍 RAG Implementation

The RAG system combines:

1. **Retrieval**: Azure Cognitive Search finds relevant wines using hybrid search
2. **Augmentation**: Context is formatted for the AI model
3. **Generation**: OpenAI GPT generates personalized recommendations

### **Search Process**

```python
# Search wine database
search_results = search_client.search(
    search_text=user_query,
    top=20,
    select=["content"]
)

# Generate AI response with context
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

### **Common Issues**

1. **500 Internal Server Error**

   - Check environment variables are set correctly in Azure Container Apps
   - Verify Azure services (OpenAI, Cognitive Search) are accessible
   - Check container logs for client initialization errors

2. **401 Unauthorized**

   - Ensure API key is included in `X-API-Key` header for secure endpoints
   - Verify API key matches the configured value
   - Use public endpoints (`/ask-public`) for testing without authentication

3. **HTTPS Redirect Loops**
   - Ensure `HTTPSRedirectMiddleware` is not enabled (Azure handles HTTPS redirect)
   - Check that Azure Container Apps HTTPS is properly configured

### **Debug Commands**

```bash
# Check container logs
az containerapp logs show --name rg1 --resource-group rg1 --follow

# Test endpoints
curl https://rg1.bravesand-0daa5720.eastus.azurecontainerapps.io/health
curl https://rg1.bravesand-0daa5720.eastus.azurecontainerapps.io/security-test

# Check workflow status
gh run list --workflow="main.yml"
gh run view --log

# Test security headers
curl -I https://rg1.bravesand-0daa5720.eastus.azurecontainerapps.io/health
```

### **Security Testing**

Run the comprehensive security test:

```bash
python test_secure_webapp_complete.py
```

Expected output:

- ✅ Health: 200 | API Key: yes | Env: production
- ✅ Public API: 200
- ✅ No Auth: 401 (properly secured)
- ✅ With Auth: 200 (authentication working)
- ✅ Security Headers: implemented

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

**🍷🔒 Cheers to secure, intelligent wine recommendations! 🥂✨**
