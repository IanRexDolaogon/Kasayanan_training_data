import requests
import pandas as pd
import time

def fetch_verafiles_from_api(api_key, max_pages=5):
    all_claims = []
    base_url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
    
    # We filter specifically for Vera Files to adhere to your project scope
   # We filter specifically for Vera Files to adhere to your project scope
    params = {
        "key": api_key,
        "reviewPublisherSiteFilter": "verafiles.org", # The dot has been removed!
        "pageSize": 100 
    }
    
    next_page_token = None
    
    for page in range(1, max_pages + 1):
        print(f"Fetching API Page {page}...")
        if next_page_token:
            params["pageToken"] = next_page_token
            
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # If there are no claims, we've reached the end
            if "claims" not in data:
                print("No more claims found.")
                break
                
            for item in data['claims']:
                # Extract the specific text of the fake claim
                claim_text = item.get('text', 'No Claim Text')
                
                # Extract the fact-checker's verdict
                review = item.get('claimReview', [{}])[0]
                verdict = review.get('textualRating', 'No Verdict')
                url = review.get('url', 'No URL')
                title = review.get('title', 'No Title')
                
                all_claims.append({
                    "Original_Claim": claim_text,
                    "Verdict": verdict,
                    "Article_Title": title,
                    "Source_URL": url,
                    "Label": "Troll Discourse/Fake News" # Ready for your ML model
                })
            
            # Check if there is another page of results
            next_page_token = data.get('nextPageToken')
            if not next_page_token:
                print("Reached the final page of available API results.")
                break
                
            # A small delay is still good practice for APIs
            time.sleep(1)
            
        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}")
            break
            
    return pd.DataFrame(all_claims)

# --- RUN THE EXTRACTOR ---
# 1. PASTE YOUR API KEY HERE:
YOUR_API_KEY = "API_KEY_HERE"

# 2. Run the function (Let's grab up to 10 pages / 1000 claims)
df_dataset = fetch_verafiles_from_api(YOUR_API_KEY, max_pages=10)

if not df_dataset.empty:
    print(f"\nSuccessfully extracted {len(df_dataset)} claims!")
    print(df_dataset[['Original_Claim', 'Verdict']].head())
    
    df_dataset.to_csv('kasaysayan_api_dataset.csv', index=False)
    print("\nDataset perfectly formatted and saved to 'kasaysayan_api_dataset.csv'")