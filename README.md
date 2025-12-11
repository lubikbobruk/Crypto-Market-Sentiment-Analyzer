# 🧠 Crypto Market Sentiment Analyzer
A Python application that analyzes **social-media sentiment** of cryptocurrency markets and compares it with market indicators such as price movement and volatility. The goal is to explore how public sentiment correlates with short-term market behavior.  
This project is developed as part of the **BI-PYT.21** course at **FIT ČVUT**.

---

## 🚀 Project Overview
The application collects data from **Reddit** and **Telegram**, performs **text preprocessing**, applies **sentiment analysis** (VADER) and visualizes results using **CLI** and **Streamlit**.  
**Current status:** `Phase 6 — PEP8 Audit`  

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

**P.S. You must have internet connection for API calls to work, program can't be run offline.**

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
pip install -r requirements.txt
```
 - Run the Streamlit app

```bash
#Ensure you are on a right Path and conda is activated
conda activate crypto-sentiment
cd *root folder of the project*

#Run Streamlit
python -m streamlit run app\visualization\streamlit_app.py

#Run CLI
python -m app.cli.main
```

# 🚀 Project Roadmap

* Phase 0 — Setup: Initialize project structure, config files, and environment. ✅

* Phase 1 — Collectors: Implement Reddit/Telegram data collection modules. ✅

* Phase 2 — Text Preprocessing: Clean and normalize raw text into a unified format. ✅

* Phase 3 — Sentiment Analysis: Apply VADER scoring with interpretation logic. ✅

* Phase 4 — CLI: Enable preprocessing, sentiment scoring, and exporting via CLI. ✅

* Phase 5 — Streamlit UI: Interactive browsing, filters, visualization. ✅

* Phase 6 — PEP8 Audit: Ensure full compliance with codestyle. ✅

* Phase 7 — Docs: README, architecture notes, final cleanup.

**Optional for future development:**

* Phase 8 — Social-Reaction Scoring: Computing sentiment reactions on posts.
* Phase 9 — Market Data: Fetch crypto prices with yfinance and sync with sentiment.
* Phase 10 — Analytics: Compute correlations, sentiment metrics, and spike events.
* Phase 11 - Finalize again: Follow steps from phases 7-9 for updated version.
* Phase 12 - Adding News: Creating collector, preprocessing, sentiment, cli & 
streamlit
* Phase 13 - CLIP Embedding Similarity: validate if requested coin text is related to crypto/finance space.  
* Phase 14 - Multiple coins/sources: Implement system for handling multiple coin and source input.