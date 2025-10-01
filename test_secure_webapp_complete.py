import requests

url = "https://rg1.bravesand-0daa5720.eastus.azurecontainerapps.io"

print("🔧 Testing Secure Wine RAG API")
print("=" * 50)

# Test 1: Health check
print("1. Health Check:")
health = requests.get(f"{url}/health")
print(f"   Status: {health.status_code}")
print(f"   Security: {health.json()['security_status']}")
print()

# Test 2: Security configuration test
print("2. Security Configuration:")
security_test = requests.get(f"{url}/security-test")
print(f"   Status: {security_test.status_code}")
if security_test.status_code == 200:
    config = security_test.json()
    print(f"   API Key in ENV: {config['api_key_in_env']}")
    print(f"   Environment: {config['environment']}")
print()

# Test 3: Public endpoint (should work)
print("3. Public Endpoint Test:")
public_response = requests.post(
    f"{url}/ask-public",
    json={"message": "What is the best Cabernet Sauvignon?"}
)
print(f"   Status: {public_response.status_code} ✅")
print()

# Test 4: Protected endpoint WITHOUT API key (should fail with 401)
print("4. Protected Endpoint WITHOUT API Key:")
no_key_response = requests.post(
    f"{url}/ask",
    json={"message": "What is the best Cabernet Sauvignon?"}
)
print(f"   Status: {no_key_response.status_code} {'✅' if no_key_response.status_code == 401 else '❌'}")
if no_key_response.status_code != 401:
    print(f"   Response: {no_key_response.json()}")
print()

# Test 5: Protected endpoint WITH API key (should work)
print("5. Protected Endpoint WITH API Key:")
headers = {"X-API-Key": "wine-rag-secure-api-key-2024"}
secure_response = requests.post(
    f"{url}/ask",
    json={"message": "What is the best Cabernet Sauvignon?"},
    headers=headers
)
print(f"   Status: {secure_response.status_code} {'✅' if secure_response.status_code == 200 else '❌'}")
print()

# Test 6: Security Headers Check
print("6. Security Headers:")
for header, value in secure_response.headers.items():
    if any(sec in header.lower() for sec in ['security', 'transport', 'content', 'frame', 'xss']):
        print(f"   {header}: {value}")

print("\n🎉 Security Testing Complete!")