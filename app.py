import streamlit as st
import pandas as pd
import ast
from datetime import datetime
from dotenv import load_dotenv
import os
import google.generativeai as genai
from streamlit_lightweight_charts import renderLightweightCharts

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("Gemini API key not found. Please set the GEMINI_API_KEY environment variable.")
    st.stop()

def ask_gemini(question, df):
    if not GEMINI_API_KEY:
        return "Gemini API key not configured"
    
    q = question.lower()
    
    # Custom logic for known queries
    if "bullish" in q and "2023" in q:
        try:
            df['year'] = df['timestamp'].dt.year
            bullish_2023 = df[(df['year'] == 2023) & (df['direction'] == 'LONG')].shape[0]
            return f"TSLA was bullish on {bullish_2023} days in 2023."
        except Exception as e:
            return f"Error calculating bullish days: {str(e)}"

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("models/gemini-1.5-flash")

        # Create a sample that fits within token limits
        sample_size = min(100, len(df))
        sample_df = df.sample(sample_size).copy()
        sample_df['timestamp'] = sample_df['timestamp'].astype(str)
        
        data_sample = sample_df[['timestamp', 'open', 'high', 'low', 'close', 'volume', 'direction']].to_csv(index=False)

        prompt = f"""You are a financial analyst. Analyze this TSLA stock data and answer the question.
        
        Data Sample (CSV format):
        {data_sample}
        
        Question: {question}
        
        Provide a concise answer with specific numbers/dates when available.
        If making calculations, show your work briefly."""
        
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Error getting answer: {str(e)}"


def load_data():
    df = pd.read_csv("data/tsla_data.csv")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['Support'] = df['Support'].apply(lambda x: ast.literal_eval(x) if pd.notna(x) and x.strip() else [])
    df['Resistance'] = df['Resistance'].apply(lambda x: ast.literal_eval(x) if pd.notna(x) and x.strip() else [])
    return df

def summarize_dataset(df):
    summary = f"Dataset has {len(df)} rows, date range: {df['timestamp'].min().date()} to {df['timestamp'].max().date()}. "
    summary += f"LONG days: {df[df['direction']=='LONG'].shape[0]}, SHORT days: {df[df['direction']=='SHORT'].shape[0]}.\n"
    summary += f"Sample row: {df.iloc[0].to_dict()}"
    return summary

def resample_data(df, timeframe):
    # if timeframe == 'Daily':
    #     return df.copy()
    # elif timeframe == 'Weekly':
    #     return df.resample('W', on='timestamp').agg({
    #         'open': 'first',
    #         'high': 'max',
    #         'low': 'min',
    #         'close': 'last',
    #         'volume': 'sum',
    #         'direction': lambda x: x.mode()[0] if len(x.mode()) > 0 else None,
    #         'Support': lambda x: list(set().union(*x)) if any(x) else [],
    #         'Resistance': lambda x: list(set().union(*x)) if any(x) else []
    #     }).reset_index()
    if timeframe == 'Monthly':
        return df.resample('ME', on='timestamp').agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum',
            'direction': lambda x: x.mode()[0] if len(x.mode()) > 0 else None,
            'Support': lambda x: list(set().union(*x)) if any(x) else [],
            'Resistance': lambda x: list(set().union(*x)) if any(x) else []
        }).reset_index()
    elif timeframe == 'Yearly':
        return df.resample('YE', on='timestamp').agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum',
            'direction': lambda x: x.mode()[0] if len(x.mode()) > 0 else None,
            'Support': lambda x: list(set().union(*x)) if any(x) else [],
            'Resistance': lambda x: list(set().union(*x)) if any(x) else []
        }).reset_index()

def format_ohlc(df):
    return [
        {
            "time": row['timestamp'].strftime('%Y-%m-%d'),
            "open": row['open'],
            "high": row['high'],
            "low": row['low'],
            "close": row['close']
        }
        for _, row in df.iterrows()
    ]

def format_markers(df):
    markers = []
    for _, row in df.iterrows():
        if pd.isna(row['direction']):
            continue
            
        time = row['timestamp'].strftime('%Y-%m-%d')
        if row['direction'] == "SHORT":
            markers.append({
                "time": time,
                "position": "aboveBar",
                "color": "#ef5350",
                "shape": "arrowDown",
                "text": "SHORT"
            })
        elif row['direction'] == "LONG":
            markers.append({
                "time": time,
                "position": "belowBar",
                "color": "#26a69a",
                "shape": "arrowUp",
                "text": "LONG"
            })
        else:
            markers.append({
                "time": time,
                "position": "inBar",
                "color": "#fdd835",
                "shape": "circle",
                "text": "NEUTRAL"
            })
    return markers

def format_bands(df):
    support_band = []
    resistance_band = []

    for _, row in df.iterrows():
        time_str = row['timestamp'].strftime('%Y-%m-%d')

        if row['Support']:
            support_band.append({
                "time": time_str,
                "value": min(row['Support']),
                "upper": max(row['Support']),
                "lower": min(row['Support'])
            })

        if row['Resistance']:
            resistance_band.append({
                "time": time_str,
                "value": max(row['Resistance']),
                "upper": max(row['Resistance']),
                "lower": min(row['Resistance'])
            })

    support_area = [{"time": row["time"], "value": row["lower"]} for row in support_band]
    resistance_area = [{"time": row["time"], "value": row["upper"]} for row in resistance_band]

    return support_area, resistance_area

def main():
    st.set_page_config(layout="wide", page_title="TSLA Stock Dashboard",page_icon="📊",initial_sidebar_state="expanded")
    st.title("TSLA Stock Dashboard")

    try:
        df = load_data()
    except FileNotFoundError:
        st.error("Data file not found. Please ensure 'data/tsla_data.csv' exists in the 'data/' folder.")
        st.stop()

    
    # Add timeframe selector
    timeframe = st.sidebar.selectbox(
        "Select Timeframe:",
        [ 'Monthly', 'Yearly'],
        index=0
    )
    
    # Resample data based on selected timeframe
    resampled_df = resample_data(df, timeframe)

    chart_tab, chatbot_tab = st.tabs([" Chart", " Ask the Chatbot"])

    with chart_tab:
        subtab1, subtab2 = st.tabs([" Support & Resistance", " Direction Markers"])
        
        ohlc_data = format_ohlc(resampled_df)
        markers = format_markers(resampled_df)
        support_area, resistance_area = format_bands(resampled_df)

        chart_config = {
            "width": 1200,
            "height": 600,
            "layout": {
                "background": {"type": "solid", "color": "#0f1419"},
                "textColor": "#d1d4dc"
            },
            "grid": {
                "vertLines": {"color": "rgba(197, 203, 206, 0.3)", "visible": True},
                "horzLines": {"color": "rgba(197, 203, 206, 0.3)", "visible": True}
            },
            "priceScale": {"borderVisible": False},
            "timeScale": {
                "borderVisible": False,
                "timeVisible": True,
                "secondsVisible": False
            }
        }

        with subtab1:
            st.subheader(f"🟩 Support & Resistance Bands ({timeframe})")
            renderLightweightCharts([{
                "chart": chart_config,
                "series": [
                    {
                        "type": "Candlestick",
                        "data": ohlc_data,
                        "options": {
                            "upColor": "#26a69a",
                            "downColor": "#ef5350",
                            "borderUpColor": "#26a69a",
                            "borderDownColor": "#ef5350",
                            "wickUpColor": "#26a69a",
                            "wickDownColor": "#ef5350"
                        }
                    },
                    {
                        "type": "Area",
                        "data": support_area,
                        "options": {
                            "lineColor": "rgba(38, 166, 154, 1)",
                            "topColor": "rgba(38, 166, 154, 0.3)",
                            "bottomColor": "rgba(38, 166, 154, 0.0)",
                            "lineWidth": 2
                        }
                    },
                    {
                        "type": "Area",
                        "data": resistance_area,
                        "options": {
                            "lineColor": "rgba(239, 83, 80, 1)",
                            "topColor": "rgba(239, 83, 80, 0.3)",
                            "bottomColor": "rgba(239, 83, 80, 0.0)",
                            "lineWidth": 2
                        }
                    }
                ]
            }], key="bands_chart")

        with subtab2:
            st.subheader(f"📍 Direction Markers ({timeframe})")
            renderLightweightCharts([{
                "chart": chart_config,
                "series": [
                    {
                        "type": "Candlestick",
                        "data": ohlc_data,
                        "options": {
                            "upColor": "#26a69a",
                            "downColor": "#ef5350",
                            "borderUpColor": "#26a69a",
                            "borderDownColor": "#ef5350",
                            "wickUpColor": "#26a69a",
                            "wickDownColor": "#ef5350"
                        },
                        "markers": markers
                    }
                ]
            }], key="markers_chart")

    with chatbot_tab:
        st.subheader("Ask questions about the TSLA dataset")
        user_q = st.text_input("Your question:")
        if user_q:
            with st.spinner("Thinking..."):
                response = ask_gemini(user_q, df)
                st.markdown(f"**Q:** {user_q}")
                st.markdown(f"**A:** {response}")

if __name__ == "__main__":
    main()