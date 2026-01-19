from google import genai

# Use your new, working key here
API_KEY = "enter your api key"
client = genai.Client(api_key=API_KEY)

print("--- Listing available models ---")
try:
    # This fetches the list of all models your key can access
    for model in client.models.list():
        print(f"ID: {model.name} | Supported: {model.supported_actions}")
except Exception as e:
    print(f"Error fetching models: {e}")