# 🧠 Crypto Market Sentiment Analyzer
A Python application that analyzes **media and social-media sentiment** of cryptocurrency markets and compares it with market indicators such as price movement and volatility. The goal is to explore how public sentiment correlates with short-term market behavior.  
This project is developed as part of the **BI-PYT.21** course at **FIT ČVUT**.

---

## 🚀 Project Overview
The application collects data from **Reddit**, **X**, and **NewsAPI**, performs **text preprocessing**, applies **sentiment analysis** (VADER), retrieves **market data** via `yfinance`, and visualizes results using **Streamlit**.  
**Current status:** `Phase 1 – Data Collection `  

---

## 🛠️ Installation Guide

### Prerequisites
- [Anaconda](https://www.anaconda.com/download)
- Git
- Python 3.11 (compatible with 3.10-3.12)

### Setting Up
 - Clone the repository first
 - Create a Conda environment

```bash
conda create -n crypto-sentiment python=3.11 -y
conda activate crypto-sentiment
```
 - Install dependencies

```bash
conda install pandas numpy matplotlib pytest pyyaml -y
pip install streamlit vaderSentiment yfinance snscrape praw flake8 black
```
 - Run the Streamlit app

```bash
#Ensure you are on a right Path and conda is activated
conda activate crypto-sentiment
cd C:\Users\Lubomyr\Desktop\bobroliu

#Run
python -m streamlit run app\visualization\streamlit_app.py
```

---

## 🔑 Reddit API Setup (Required for Reddit Collector)

To use the Reddit collector, you must provide your own Reddit API credentials.

1. Log in to Reddit and open [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps).
2. Click **Create another app** and fill in:
   | Field | Value |
   |--------|--------|
   | **Name:** | `CryptoSentimentAnalyzer` |
   | **Type:** | `script` |
   | **Description:** | `Semestral project for BI-PYT` |
   | **Redirect URI:** | `http://localhost:8080` |
3. After creation, copy the **client ID** (under “personal use script”) and **secret**.
4. Create a file `config/secrets.yaml` (not committed to Git) and add:

   ```yaml
   reddit:
     client_id: "YOUR_CLIENT_ID"
     client_secret: "YOUR_CLIENT_SECRET"
     user_agent: "crypto-analyzer"


# Topic of your semestral work

Describe a function of developed application, necessary dependencies (e.g. utilize requirements.txt), how to start it, and last but not least how to run tests from CLI.
