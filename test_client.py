import os
import replicate
from pprint import pprint

# Get API token from environment
api_token = os.getenv("REPLICATE_API_TOKEN")
print(f"Using API token: {api_token}")

# Create client
client = replicate.Client(api_token=api_token)

# Search for models
print("\nSearching for flux models...")
page = client.models.search("flux")

# Print page attributes to understand pagination
print("\nPage attributes:")
pprint(vars(page))

# Print results
print("\nAll models:")
for model in page.results:
    print(f"Model: {model.owner}/{model.name}")
    print(f"Created: {getattr(model, 'created_at', 'N/A')}")
    print(f"Run count: {getattr(model, 'run_count', 'N/A')}")
    print("---") 