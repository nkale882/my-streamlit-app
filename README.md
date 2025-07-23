# 📈 TSLA Stock Analysis Dashboard with Gemini-Powered Chatbot

An interactive web app built with **Streamlit** that combines real-time candlestick charts and support/resistance analysis with a powerful AI chatbot powered by **Google Gemini**.

> 🟢 Live Demo: [my-app-tsla.streamlit.app](https://my-app-tsla.streamlit.app)  
> 🧠 Built for data-driven insights + conversational interaction using LLMs

---

## 🚀 Features

### 📊 Candlestick Chart Visualization
- Displays OHLC (Open, High, Low, Close) stock price data
- Annotates chart with **LONG/SHORT/NEUTRAL** markers
- Visual overlays of **Support** and **Resistance bands**
- Bonus feature: **chart animation** (playback of market movements)

### 🤖 Gemini-Powered AI Chatbot
- Ask natural language questions about TSLA data like:
  - “How many bullish days were there in 2023?”
  - “Which day had the highest trading volume?”
  - “Was TSLA generally above resistance in January?”
- Uses Google’s **Gemini 1.5 Flash** model via API

### 📈 Data Insights Engine
- Automatically computes:
  - Bullish/bearish days
  - Direction-based counts
  - Average volume
  - Time range, summaries

---

## 📦 Tech Stack

| Component            | Stack                                                |
|---------------------|------------------------------------------------------|
| Frontend/UI         | [Streamlit](https://streamlit.io)                   |
| Charting            | [streamlit-lightweight-charts](https://github.com/streamlit/lightweight-charts) |
| LLM Integration     | [Google Gemini API](https://ai.google.dev/)         |
| Backend Logic       | Python, Pandas, NumPy                                |
| Hosting             | [Streamlit Cloud](https://streamlit.io/cloud)       |

---

<img width="825" height="814" alt="image" src="https://github.com/user-attachments/assets/8d472362-fe52-425b-b715-7f12f6be96f0" />
<img width="825" height="814" alt="image" src="https://github.com/user-attachments/assets/c1f7a60e-3baa-4900-8119-10e30c801138" />


## 🧠 Sample Questions to Ask the Chatbot

- What was the highest price ever recorded?
- How many LONG days occurred in 2023?
- What is the correlation between volume and direction?
- Did the price ever close below the support band?

---

## 🛠️ Setup Instructions

### 1. Clone this repo
```bash
git clone https://github.com/nkale882/my-streamlit-app.git
cd my-streamlit-app
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your Gemini API key  
Create a file at `.streamlit/secrets.toml` and add:
```toml
GEMINI_API_KEY = "your-api-key-here"
```

### 4. Run the app
```bash
streamlit run app.py
```

---

## 📁 Project Structure
```
my-streamlit-app/
├── app.py                    # Main app logic
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── secrets.toml          # API key (excluded from repo)
└── ...
```

---

## 🤝 Contributions

Pull requests are welcome. For suggestions or improvements, feel free to open an issue or fork the repo.

---

## 🔍 Disclaimer

This project is for educational purposes only. Sample data is used and does not reflect real TSLA prices or financial advice.
