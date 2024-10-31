import json
import requests
from google.auth import default
from google.auth.transport.requests import Request

def get_access_token():
  credentials, _ = default()
  credentials.refresh(Request())
  return credentials.token

def predict(endpoint_id, project_id, data):
  url = f"https://us-central1-aiplatform.googleapis.com/v1/projects/{project_id}/locations/us-central1/endpoints/{endpoint_id}:predict"
  headers = {
    "Authorization": f"Bearer {get_access_token()}",
    "Content-Type": "application/json"
  }
  payload = {
    "instances": data,
  }
  response = requests.post(url, headers=headers, data=json.dumps(payload))
  return response

if __name__ == "__main__":
  ENDPOINT_ID = ""
  PROJECT_ID = ""
  data = {
    "max_tokens": 256,
    "prompt": "<start_of_turn>user You are a helpful AI assistant excellent in writing poetry. Please write a Haiku about the amazing DevFest Silicon Valley and Responsible AI <end_of_turn> <start_of_turn>model"
  }
  prediction = predict(ENDPOINT_ID, PROJECT_ID, data)
  print(prediction.__dict__)
