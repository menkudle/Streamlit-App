# 🚀 Streamlit Agentic Dashboard

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-Fast%20Inference-orange?style=for-the-badge&logo=openai&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-Cloud%20DB-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local%20Fallback-black?style=for-the-badge&logo=linux&logoColor=white)

## 📖 Overview
This repository hosts a production-grade **Streamlit Application** that demonstrates a hybrid cloud/local architecture. It serves as a comprehensive example of building internal tools with **Agentic AI**, **Cloud Persistence**, and **Secure Authentication**.

The app is "Cloud Ready" — it runs seamlessly on **Streamlit Community Cloud** (using Groq + Supabase) while retaining the ability to run completely offline on a local machine (using Ollama + Supabase).

[![Live Demo](https://img.shields.io/badge/Live_Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://agentic-task-manager.streamlit.app/)



## ✨ Key Features

### 🔐 1. Secure Authentication
* **Gatekeeper Pattern:** Protecting multiple pages behind a login screen.
* **Session State:** Persists user authentication across page navigations.
* **Role-Based Access:** Simulates admin-level access control.

### 🤖 2. Agentic AI Assistant (Hybrid Engine)
* **Smart Agent:** The AI doesn't just chat; it executes **commands**. It can add tasks to your database or list your pending items (`COMMAND: ADD_TASK`).
* **Hybrid Intelligence:**
    * **Cloud Mode:** Uses **Groq API** (Llama 3.3 70B) for blazing-fast inference when deployed.
    * **Local Mode:** Automatically falls back to **Ollama** (Llama 3.2 / Qwen) when running locally without API keys.
* **Context Aware:** Remembers conversation history and previous tool outputs.

### ✅ 3. Cloud-Connected Task Manager
* **Single Source of Truth:** Uses **Supabase (PostgreSQL)** to store tasks.
* **Real-Time Sync:** Data persists across app restarts and is synchronized between your local development environment and the deployed cloud app.
* **CRUD Operations:** Create, Read, and Delete tasks with instant UI updates.

### 📊 4. Interactive Dashboards
* **Plotly Integration:** Advanced interactive charts (Scatter Maps, Line Charts).
* **Data Slicing:** Dynamic time-grain filtering (Daily/Weekly/Monthly) for trend analysis.
* **Cross-Filtering:** Drill down into sales performance by region and category.


## 🛠️ Tech Stack
* **Frontend:** [Streamlit](https://streamlit.io/)
* **Database:** [Supabase](https://supabase.com/) (PostgreSQL)
* **Cloud AI:** [Groq API](https://groq.com/) (Running Llama 3.3 70B)
* **Local AI:** [Ollama](https://ollama.com/) (Running Llama 3.2 / Qwen 2.5)
* **Visualization:** Plotly Express & Pandas


## 📂 Project Structure
```bash
stream-app-mastery/
├── .streamlit/             # App Configuration & Secrets
│   ├── config.toml         # Theme settings
│   └── secrets.toml        # API Keys (gitignored)
├── pages/                  # Application Pages
│   ├── basic_dashboard.py  # Pandas/Matplotlib Analytics
│   ├── plotly_dashboard.py # Advanced Plotly Analytics
│   ├── ai_chatbot.py       # Agentic AI Logic (Groq/Ollama)
│   └── task_manager.py     # Supabase CRUD Interface
├── utils/                  # Helper Modules
│   ├── auth.py             # Login/Logout Logic
│   ├── db_manager.py       # Supabase Connection Handler
│   └── data_generator.py   # Synthetic Business Data
├── app.py                  # Main Navigation & Entry Point
├── requirements.txt        # Dependency List
└── README.md               # Documentation
```


## ⚙ Setup

### 1. Prerequisites
Ensure you have Python installed. You also need **Ollama** installed for the AI features.
* [Download Python](https://www.python.org/downloads/)
* [Download Ollama](https://ollama.com/download)

### 2. Clone the Repository
```bash
git clone https://github.com/menkudle/Streamlit-App.git
cd streamlit-app
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Local LLM
Pull the specific model used in the application code:
```bash
ollama pull llama3.2
```
Run the Llama3.2 model locally:
```bash
ollama run llama3.2
```

Endpoint is available to access Local LLM:  ```http://localhost:11434/api/chat```

### 5. Configuration (Secrets)
Create a file named .streamlit/secrets.toml to store your API keys. (Note: Never commit this file to GitHub!)

```bash 
GROQ_API_KEY = "gsk_your_groq_api_key_here"

[supabase]
url = "[https://your-project.supabase.co](https://your-project.supabase.co)"
key = "your-public-anon-key-here"
```


### 6. Database Setup (Supabase)
* Create a free project at database.new.
* Create a table named tasks.
* Columns: id (int8, identity), task (text), status (text).
* Disable RLS (Row Level Security) for this demo project.

### 7. Run the Application
```bash
streamlit run app.py
```

## 🎨️ Customization
You can change the UI theme by editing ```.streamlit/config.toml```:
```bash
[theme]
base = "dark"
primaryColor = "#F63366"
backgroundColor = "#0E1117"
```

## 🔐 Default Credentials
(For testing purposes only)
* Username: ```admin```
* Password: ```password```


## 🚀 Future Roadmap
* [x] Implement user authentication.
* [x] Add Agentic capabilities (AI can manage tasks).
* [x] Add Groq API integration (Cloud AI).
* [x] Add Supabase Integration (Cloud DB).
* [x] Deploy to Streamlit Community Cloud.
* [ ] Add PDF RAG (Retrieval Augmented Generation).
* [ ] Multi-user support with Row Level Security.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome!


## 📄 License
This project is licensed under the MIT License.