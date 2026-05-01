# Kasaysayan-Check: Data Collection & Pre-processing Pipeline

This repository contains the data collection and cleaning architecture for **Kasaysayan-Check: A Neuro-Symbolic System for Historical and Electoral Fact-Verification in the Philippines**[cite: 1]. 

This specific pipeline focuses on building the training dataset for the Machine Learning layer, which serves as the system's linguistic sensor[cite: 1]. It securely extracts raw claims (misinformation) using the Google Fact Check Tools API and balances it with objective news via RSS feeds, entirely bypassing enterprise rate-limits (429 errors).

## Prerequisites
Before running the scripts, ensure you have:
* Python 3.8 or higher installed.
* A valid **Google Cloud API Key** check our GC send ko lng.

## Setup Instructions

### 1. Create a Virtual Environment
It is highly recommended to run these scripts inside a virtual environment to keep dependencies isolated. Open your terminal in the project directory and run:

**For Windows (PowerShell):**
python -m venv venv
.\venv\Scripts\Activate.ps1

### 2. Install Dependencies
Once your virtual environment is active `(venv)`, install the required Python libraries:

pip install requirements.txt

## Project Structure

* `api_extractor.py`: Queries the Google Fact Check API to collect verified fake claims from target publishers.
* `rss_extractor.py`: Parses official RSS feeds to collect objective, standard news text to serve as control data.
* `clean_dataset.py`: Cleans text (removes URLs, standardizes Taglish phrasing) and merges the datasets into a labeled format.

## Execution Guide

You must run the scripts in the following order to generate the final Machine Learning dataset.

### Step 1: Extract Misinformation Claims
Open `api_extractor.py` and paste your Google API Key into the `YOUR_API_KEY` variable. Then run the script:
```bash
python api_extractor.py
```
**Output:** Generates `kasaysayan_api_dataset.csv` containing the raw "troll" discourse and false claims.

### Step 2: Extract Objective Control Data
Run the RSS script to collect standard journalistic text from Rappler and Vera Files:
```bash
python rss_extractor.py
```
**Output:** Generates `kasaysayan_control_dataset.csv` containing standard news headlines and summaries.

### Step 3: Clean and Merge
Run the final cleaning script to process the raw text and apply the binary classification labels:
```bash
python clean_dataset.py
```
**Output:** Generates the pristine `kasaysayan_clean_training_data.csv`.

## Using the Training Data

The final output file, `kasaysayan_clean_training_data.csv`, is completely formatted and ready for the next phase of the project: training the **Multinomial Naive Bayes classifier with TF-IDF vectorization**[cite: 1].

The dataset contains two columns:
* **`Clean_Text`**: The normalized text (all lowercase, URLs/special characters removed, Taglish preserved).
* **`Label`**: 
  * `1` represents a Suspicious/Historical Fake Claim.
  * `0` represents Objective/Breaking News.

To load this into your `scikit-learn` pipeline:

```python
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the prepared data
df = pd.read_csv('kasaysayan_clean_training_data.csv')

# Separate features (X) and labels (y)
X = df['Clean_Text']
y = df['Label']

# Initialize the vectorizer
vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X)

# Proceed with training your Naive Bayes model...
```