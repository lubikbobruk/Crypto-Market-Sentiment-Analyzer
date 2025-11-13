# 🧠 Crypto Market Sentiment Analyzer
A Python application that analyzes **media and social-media sentiment** of cryptocurrency markets and compares it with market indicators such as price movement and volatility. The goal is to explore how public sentiment correlates with short-term market behavior.  
This project is developed as part of the **BI-PYT.21** course at **FIT ČVUT**.

---

## 🚀 Project Overview
The application collects data from **Reddit**, **Telegram**, and **NewsAPI**, performs **text preprocessing**, applies **sentiment analysis** (VADER), retrieves **market data** via `yfinance`, and visualizes results using **Streamlit**.  
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
pip install streamlit vaderSentiment yfinance snscrape praw flake8 black telethon
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

## 🔑 API Setup Guide

This project requires API credentials for Reddit and Telegram to collect data.

### 🟥 Reddit API
1. Visit [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps).  
2. Click **Create another app** and fill in:
   - **Name:** `CryptoSentimentAnalyzer`  
   - **Type:** `script`  
   - **Redirect URI:** `http://localhost:8080`  
3. After creation, copy:
   - `client_id` (shown under “personal use script”)  
   - `client_secret`  
   - `user_agent`
4. Add them to your config file:

   ```yaml
   reddit:
     client_id: *here*
     client_secret: *here*
     user_agent: *here*


### 🟦 Telegram API
1. Go to [https://my.telegram.org](https://my.telegram.org) and log in.  
2. Open **API Development Tools** → fill out the form (any app name and short name).  
3. Copy your generated:
   - `api_id`
   - `api_hash`
4. Add them to the same `config/secrets.yaml` file:

   ```yaml
   telegram:
     api_id: *here*
     api_hash: *here*