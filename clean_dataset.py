import pandas as pd
import re

def clean_text(text):
    """Cleans raw text for the Machine Learning model."""
    if not isinstance(text, str):
        return ""
    
    # 1. Convert to lowercase
    text = text.lower()
    # 2. Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # 3. Remove user mentions (@username)
    text = re.sub(r'\@\w+', '', text)
    # 4. Remove special characters and punctuation, BUT keep letters, numbers, spaces, and 'ñ' for Tagalog
    text = re.sub(r'[^a-z0-9\sñ]', '', text)
    # 5. Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

print("Loading datasets...")
try:
    # Load the datasets
    df_fake = pd.read_csv('kasaysayan_api_dataset.csv')
    df_real = pd.read_csv('kasaysayan_control_dataset.csv')

    # Apply binary labels
    df_fake['Label'] = 1  # 1 = Suspicious / Fake Claim
    df_real['Label'] = 0  # 0 = Objective / Breaking News

    print("Merging and shuffling data...")
    # Combine the datasets
    master_df = pd.concat([df_fake, df_real], ignore_index=True)

    # Shuffle the dataset thoroughly
    master_df = master_df.sample(frac=1, random_state=42).reset_index(drop=True)

    print("Cleaning text (removing URLs, special characters, standardizing Taglish)...")
    # Apply the cleaning function to the 'Original_Claim' column
    master_df['Clean_Text'] = master_df['Original_Claim'].apply(clean_text)

    # Drop any rows where the text might have become empty after cleaning
    master_df = master_df[master_df['Clean_Text'] != ""]

    # Select only the columns we need for the ML model
    final_training_data = master_df[['Clean_Text', 'Label']]

    # Save the final pristine dataset
    final_training_data.to_csv('kasaysayan_clean_training_data.csv', index=False)
    
    print("\n✅ Success!")
    print(f"Total training samples: {len(final_training_data)}")
    print("Preview of your clean ML data:")
    print(final_training_data.head())

except FileNotFoundError as e:
    print(f"Error: Could not find one of the CSV files. {e}")