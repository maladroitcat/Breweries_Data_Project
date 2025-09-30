import requests
import pandas as pd

BASE_URL = "https://api.openbrewerydb.org/v1/breweries"
COUNTRY = "united_states"
PER_PAGE = 200

all_breweries = []
page = 1

while True:
    response = requests.get(BASE_URL, params={
        "by_country": COUNTRY,
        "per_page": PER_PAGE,
        "page": page
    })
    data = response.json()
    
    if not data:  # stop if no more results
        break
    
    all_breweries.extend(data)
    page += 1

# Convert to DataFrame
df = pd.DataFrame(all_breweries)

# Save to CSV
df.to_csv("data/united_states_breweries.csv", index=False)

print(f"Saved {len(df)} breweries to united_states_breweries.csv")
