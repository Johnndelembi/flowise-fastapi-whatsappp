import requests

base_url = "http://localhost:8000"

# Test GET /
response = requests.get(f"{base_url}/")
print("GET /:", response.status_code, response.json())

# Test GET /webhook (successful)
params = {
    "hub.mode": "subscribe",
    "hub.challenge": "1998563788",
    "hub.verify_token": "JGfwMB03bb43zTd2t2pr"
}
response = requests.get(f"{base_url}/webhook", params=params)
print("GET /webhook (valid):", response.status_code, response.text)

# Test GET /webhook (with trailing slash)
response = requests.get(f"{base_url}/webhook/", params=params)
print("GET /webhook/ (valid):", response.status_code, response.text)

# Test GET /webhook (invalid token)
params["hub.verify_token"] = "wrong_token"
response = requests.get(f"{base_url}/webhook", params=params)
print("GET /webhook (invalid):", response.status_code, response.json())

# Test POST /webhook
payload = {"message": "test message"}
response = requests.post(f"{base_url}/webhook", json=payload)
print("POST /webhook:", response.status_code, response.json())