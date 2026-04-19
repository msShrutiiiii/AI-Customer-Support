# 💬 AI Customer Support Bot

A conversational AI customer support chatbot built with **Streamlit**, **Groq API**, and **LLaMA 3**.  
Features persistent multi-turn memory, quick-prompt buttons, and adjustable model settings.

---

## 🚀 Setup & Run in VS Code

### Step 1 — Open the project
```bash
# Open this folder in VS Code
code .
```

### Step 2 — Open the integrated terminal
Press **Ctrl + `** (backtick) to open the terminal inside VS Code.

### Step 3 — Create a virtual environment
```bash
python -m venv venv
```

### Step 4 — Activate the virtual environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac / Linux:**
```bash
source venv/bin/activate
```

> You should see `(venv)` appear at the start of your terminal line.

### Step 5 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 6 — Add your Groq API key

1. Open `.env` in VS Code
2. Replace `your_groq_api_key_here` with your actual key
3. Get a free key at: **https://console.groq.com**

### Step 7 — Run the app
```bash
streamlit run app.py
```

The app will open automatically at **http://localhost:8501** in your browser.

---

## 📁 Project Structure

```
ai_support_bot/
├── app.py              ← Main Streamlit application
├── requirements.txt    ← Python dependencies        
├── .env                ← Your actual API key (never share/commit this)
├── .gitignore          ← Prevents .env from being pushed to GitHub
└── README.md           ← This file
```

---

## ✨ Features

- 💬 Multi-turn conversation with persistent memory
- ⚡ Ultra-fast responses via Groq's LPU inference
- 🎛️ Adjustable model, temperature, and response length from sidebar
- 🖱️ Quick-prompt buttons for common support queries
- 🗑️ Clear chat button to reset conversation
- 🎨 Clean, professional UI with online status indicator

---

## 🔧 Customising the Bot

To change the bot's personality or domain, edit the `SYSTEM_PROMPT` in `app.py`:

```python
SYSTEM_PROMPT = """You are a helpful customer support agent for [YOUR COMPANY].
...
"""
```

---

## 📦 Deploy to Streamlit Cloud (free)

1. Push this project to a GitHub repository
2. Go to **https://streamlit.io/cloud**
3. Connect your GitHub repo
4. Add `GROQ_API_KEY` in the **Secrets** section
5. Click **Deploy** — your app goes live instantly!

---

Built by **Shruti Umakant Rede** , Pune
