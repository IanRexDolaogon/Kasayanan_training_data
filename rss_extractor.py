import feedparser
import pandas as pd
from bs4 import BeautifulSoup # To clean any residual HTML in the RSS summary

def collect_control_data():
    real_news_data = []
    
    # The official RSS feeds for your approved sources
    rss_feeds = {
        "Vera Files": "https://verafiles.org/feed",
        "Rappler": "https://www.rappler.com/feed" 
    }

    for source, url in rss_feeds.items():
        print(f"Fetching RSS feed from {source}...")
        feed = feedparser.parse(url)
        
        for entry in feed.entries:
            title = entry.get('title', 'No Title')
            raw_summary = entry.get('summary', 'No Summary')
            
            # Sometimes RSS summaries contain basic HTML tags. We clean them out quickly:
            clean_summary = BeautifulSoup(raw_summary, "html.parser").text
            
            # Combine title and summary for a richer text block
            full_text = f"{title}. {clean_summary}"
            
            real_news_data.append({
                "Original_Claim": full_text, # Keeping column name consistent with our API dataset
                "Verdict": "Objective", 
                "Article_Title": title,
                "Source_URL": entry.get('link', ''),
                "Label": "0" # 0 represents "Real/Objective News"
            })
            
    return pd.DataFrame(real_news_data)

# --- RUN THE EXTRACTOR ---
df_control = collect_control_data()

if not df_control.empty:
    print(f"\nSuccessfully extracted {len(df_control)} objective news items!")
    print(df_control[['Original_Claim', 'Label']].head())
    
    df_control.to_csv('kasaysayan_control_dataset.csv', index=False)
    print("\nControl dataset saved to 'kasaysayan_control_dataset.csv'")