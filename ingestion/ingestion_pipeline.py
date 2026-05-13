import json
import requests
from pathlib import Path

url = "https://api.github.com"

response = requests.get(url)
response.raise_for_status()

data = response.json()

output_path = Path("data/raw/github_api_response.json")

with open(output_path, "w") as file:
	json.dump(data, file, indent=4)

print(f"Data saved to {output_path}")
