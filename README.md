# OuttaDoor 🌿

**An AI-powered outdoor quest planner using local AI.**

OuttaDoor helps users turn an outdoor outing into a fun, structured quest with activities and helpful tips. It uses a FastAPI backend and a locally running Gemma model through Ollama to generate quests.

## ✨ Features

* AI-generated outdoor quests
* Structured activities and practical tips
* Local AI inference using Gemma through Ollama
* Web interface built with HTML, CSS, and JavaScript
* FastAPI backend with an interactive API documentation page

## 🛠️ Tech Stack

* **Frontend:** HTML, CSS, JavaScript
* **Backend:** Python, FastAPI, Uvicorn
* **AI:** Gemma 3 1B through Ollama
* **HTTP requests:** Requests

## 📋 Prerequisites

Install the following before running the project:

* Python 3.10 or later
* [Ollama](https://ollama.com/)
* Git (optional, for cloning the repository)

## 🚀 Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/aditric7/OuttaDoor.git
cd OuttaDoor
```

### 2. Create and activate a virtual environment

On Windows:

```bat
python -m venv backend\venv
backend\venv\Scripts\activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Download the AI model

Make sure Ollama is installed and running, then execute:

```bash
ollama pull gemma3:1b
```

### 5. Start the backend

From the project root, run:

```bat
cd backend
uvicorn main:app --reload
```

The API should be available at:

* API base: http://127.0.0.1:8000
* Interactive API documentation: http://127.0.0.1:8000/docs

### 6. Open the frontend

Open `frontend/index.html` in your browser.

If the frontend cannot connect to the backend, check the API URL configured in `frontend/script.js` and ensure the backend is running.

## 📁 Project Structure

```text
OuttaDoor/
├── backend/
│   └── main.py
├── frontend/
│   ├── images/
│   │   ├── exercise.jpeg
│   │   └── park.jpeg
│   ├── index.html
│   ├── script.js
│   └── style.css
├── .gitignore
├── README.md
└── requirements.txt
```

## 🔒 Privacy

OuttaDoor uses a locally running AI model through Ollama. Do not commit environment files, API tokens, passwords, or other secrets to the repository.

## ⚠️ Disclaimer

AI-generated suggestions may be inaccurate. Verify locations, accessibility, weather, and safety conditions before following an outdoor quest.

## 📄 License

No license has been added yet. Please check the repository for licensing information before reusing or distributing this project.
