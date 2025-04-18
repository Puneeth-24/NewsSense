# 📰 NewsSense – "Why Is My Nifty Down?"

Have you ever checked your stocks or mutual funds and thought, “Why is this down today?”  
Most platforms just tell you the percentage drop, but not **why**.  
**NewsSense** bridges that gap using smart AI and real-world news analysis to give investors the **why behind the dip**.

---

## 🚀 Project Overview

**NewsSense** is an AI-powered explanation system that connects **stock performance** with **real-world news and events**.  
It helps users understand the **context** behind market movements using live data, news scraping, LLM-powered summarization, and a clean, interactive UI.

---

## 🔧 Tech Stack

### 📊 Stock Data
- **[yfinance](https://pypi.org/project/yfinance/)**: Fetches live and historical stock data (e.g., daily, weekly, 10-day trends).

### 🌐 Web Scraping
- **requests**: For sending HTTP requests to gather news data.
- **BeautifulSoup**: To parse and extract useful news content from web pages.

### 🧠 AI / NLP
- **Gemini-2.0-Flash LLM**: Used for high-quality summarization of extracted news articles.
  - Contextual understanding of economic and financial language
  - Handles large volumes of text efficiently
  - Generates concise, informative summaries explaining stock performance

### 🖥️ Frontend
- **Streamlit**: Used to build an intuitive, interactive web interface to:
  - Enter stock symbols
  - View performance charts
  - Read AI-generated news explanations

### 📈 Visualization
- Matplotlib / Plotly: Generate graphs showing stock trends over:
  - The current day
  - The last week
  - The last 10 days
  - Custom ranges (coming soon)

---

## 💡 Key Features

- 🔍 Scrapes latest financial news from multiple sources
- 🧠 Uses LLMs to generate human-like explanations of market movements
- 📉 Visualizes stock performance in clear, interactive graphs
- 🖥️ Clean and simple UI built with Streamlit
- 📚 Connects the **'what'** (drop in value) with the **'why'** (news events and trends)

---
