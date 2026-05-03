import feedparser
import pandas as pd
import time

def collect_google_news_control_data():
    real_news_data = []
    
    # We use specific search queries to trigger Google News to give us up to 100 articles per topic.
    # This guarantees a rich variety of 'breaking news' and 'political commentary' syntax.
    search_queries = [
        "philippines politics",
        "philippines economy breaking news",
        "philippines elections",
        "philippines senate update",
        "manila local news",
        "philippines business",
        "philippines infrastructure",
        "site:rappler.com breaking news", # Explicitly pulling from your approved source
        "site:verafiles.org news",        # Explicitly pulling from your approved source
        "philippines foreign policy",
        "philippines inflation rate"
    ]

    print("--- Booting up Google News RSS Aggregator ---")

    for query in search_queries:
        # Format the query for the URL
        formatted_query = query.replace(" ", "+")
        # Google News RSS URL localized for the Philippines
        rss_url = f"https://news.google.com/rss/search?q={formatted_query}&hl=en-PH&gl=PH&ceid=PH:en"
        
        print(f"Fetching articles for category: '{query}'...")
        feed = feedparser.parse(rss_url)
        
        for entry in feed.entries:
            title = entry.get('title', 'No Title')
            
            real_news_data.append({
                "Original_Claim": title, # Using the headline as the objective text baseline
                "Verdict": "Objective", 
                "Article_Title": title,
                "Source_URL": entry.get('link', ''),
                "Label": "0" # 0 = Real/Objective News
            })
            
        # Be polite to Google's servers
        time.sleep(2) 

    # Convert to DataFrame
    df = pd.DataFrame(real_news_data)
    
    # Drop any overlapping articles so we only train on unique text
    df = df.drop_duplicates(subset=['Original_Claim'])
    
    return df

# --- RUN THE EXTRACTOR ---
df_control = collect_google_news_control_data()

if not df_control.empty:
    print(f"\n✅ Success! Extracted {len(df_control)} unique objective news items.")
    df_control.to_csv('kasaysayan_control_dataset.csv', index=False)
    print("Bulk control dataset saved to 'kasaysayan_control_dataset.csv'")