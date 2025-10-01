import requests

# Test public health endpoint
health = requests.get("https://rg1.bravesand-0daa5720.eastus.azurecontainerapps.io/health")
print("🔒 Security Status:", health.json()["security_status"])
print("📋 SSL Info:", health.json()["ssl_info"])

# Test public endpoint (no API key needed)
public_response = requests.post(
    "https://rg1.bravesand-0daa5720.eastus.azurecontainerapps.io/ask-public",
    json={"message": "What is the best Cabernet Sauvignon?"}
)
print("✅ Public endpoint works:", public_response.status_code == 200)

# Test protected endpoint WITH API key
headers = {"X-API-Key": "wine-rag-secure-api-key-2024"}
secure_response = requests.post(
    "https://rg1.bravesand-0daa5720.eastus.azurecontainerapps.io/ask",
    json={"message": "What is the best Cabernet Sauvignon?"},
    headers=headers
)
print("🔐 Secure endpoint with API key:", secure_response.status_code == 200)

# Test protected endpoint WITHOUT API key (should fail)
no_key_response = requests.post(
    "https://rg1.bravesand-0daa5720.eastus.azurecontainerapps.io/ask",
    json={"message": "What is the best Cabernet Sauvignon?"}
)
print("❌ Without API key (should be 401):", no_key_response.status_code)

# Check security headers
print("🛡️ Security Headers:")
for header, value in secure_response.headers.items():
    if any(sec in header.lower() for sec in ['security', 'transport', 'content', 'frame', 'xss']):
        print(f"  {header}: {value}")