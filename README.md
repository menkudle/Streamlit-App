# 🚀 Streamlit Mastery App

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black?style=for-the-badge&logo=openai&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Built%20in-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

## 📖 Overview
This repository hosts a comprehensive **Multi-Page Streamlit Application** designed to demonstrate advanced Streamlit capabilities. It serves as a learning playground for building production-grade internal tools.

The app simulates a real-world business portal featuring **secure authentication**, **interactive data visualization**, **local AI integration**, and **persistent data management**.

---

## ✨ App Features

### 🔐 1. Secure Authentication Gatekeeper
* **Login System:** A main entry point (`app.py`) that protects all sub-pages.
* **Session Management:** Persists login state across page reloads using `st.session_state`.
* **Security Utils:** Reusable `require_auth()` decorator pattern to secure individual pages.

### 📊 2. Interactive Business Dashboard
* **Dynamic Filtering:** Sidebar controls to slice and dice datasets in real-time.
* **Visualizations:** Interactive charts (Line, Bar) powered by Streamlit's native charting and Pandas.
* **Raw Data View:** Toggleable dataframes for granular inspection.

### 🤖 3. Local AI Chat (Ollama Integration)
* **Privacy-First AI:** Chat interface connected to a **locally running LLM** (Nemotron-Mini via Ollama).
* **Context Awareness:** The bot remembers conversation history within the session.
* **Streaming UI:** Real-time feedback indicators ("Thinking...").

### ✅ 4. Persistent Task Manager
* **CRUD Operations:** Create, Read, and Delete tasks.
* **SQLite Backend:** A serverless database (`todo.db`) ensures tasks remain saved even if the app restarts.
* **Stateful Widgets:** Dynamic button generation for task management.

---

## 🛠️ Tech Stack
* **Frontend:** [Streamlit](https://streamlit.io/)
* **Data Processing:** Pandas, NumPy
* **Database:** SQLite3 (Native Python)
* **AI Engine:** [Ollama](https://ollama.com/) (running `nemotron-mini`)
* **Styling:** TOML Configuration (Custom Themes)

---

## 📂 Project Structure
```bash
stream-app-mastery/
├── .streamlit/             # App Configuration
│   └── config.toml         # Theme settings (colors, fonts)
├── data/                   # Data Storage
│   └── todo.db             # SQLite database (auto-generated)
├── pages/                  # Sub-pages
│   ├── 1_Dashboard.py      # Analytics View
│   ├── 2_AI_Chat.py        # LLM Interface
│   └── 3_Task_Manager.py   # Todo List
├── utils/                  # Helper Modules
│   ├── auth.py             # Authentication Logic
│   └── db_manager.py       # Database CRUD functions
├── app.py                  # Main Entry Point (Login)
└── README.md               # Documentation
```

## ⚙️ Commands to Setup

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
pip install streamlit pandas requests
```

### 4. Setup Local LLM
Pull the specific model used in the application code:
```bash
ollama pull nemotron-mini
```
Note: Keep the Ollama app running in the background.

### 5. Run the Application
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
* [ ] Implement user registration with password hashing.
* [ ] Add PDF RAG (Retrieval Augmented Generation) to the AI Chat.
* [ ] Deploy to Streamlit Community Cloud.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome!

## 📄 License
This project is licensed under the MIT License.