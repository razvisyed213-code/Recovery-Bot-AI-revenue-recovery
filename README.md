# RecoveryBot — AI Revenue Recovery Agent

An AI-powered agent built for the Razorpay AI Buildathon (Track 3: AI Revenue Recovery).

## What it does
RecoveryBot detects revenue at risk — failed payments, abandoned checkouts, and overdue B2B invoices — diagnoses the root cause using Google's Gemini LLM, and automatically decides the best recovery action: retry, send a message, or escalate to a human.

## Features
- AI-powered decision-making using Gemini API
- Recovery Rate Dashboard with live metrics
- Color-coded results table (green = recovered, red = escalated)
- Single-transaction detail view
- Bar chart visualizations of failure reasons

## Tech Stack
- Python
- Streamlit
- Google Gemini API (google-genai)
- Pandas

## Setup
```bash
python -m venv venv
venv\Scripts\activate
pip install streamlit google-genai pandas
setx GEMINI_API_KEY "your-key-here"
streamlit run app.py
```

## Files
- `app.py` — Streamlit dashboard
- `agent.py` — AI reasoning module (Gemini)
- `actions.py` — Recovery action executor
- `mock_data.py` — Sample transaction data
